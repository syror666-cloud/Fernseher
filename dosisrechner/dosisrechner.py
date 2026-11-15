#!/usr/bin/env python3
"""Dosisrechner – lokales Programm zur Berechnung von Tierarzneimittel-Dosierungen.

Starten:            python3 dosisrechner.py
Wirkstoff import:   python3 dosisrechner.py import <vetpharm-URL der Dosierungsseite>
Wirkstoffe listen:  python3 dosisrechner.py liste

Benötigt nur Python 3.8+ (keine Zusatzpakete).
"""
from __future__ import annotations

import json
import sqlite3
import sys
import threading
import unicodedata
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import dosis

BASIS = Path(__file__).resolve().parent
DB_PFAD = BASIS / "data" / "dosierungen.db"
STARTDATEN = BASIS / "data" / "startdaten.json"
INDEX_HTML = BASIS / "static" / "index.html"
HOST, PORT = "127.0.0.1", 8765

SCHEMA = """
CREATE TABLE IF NOT EXISTS wirkstoff (
    id      INTEGER PRIMARY KEY,
    name    TEXT NOT NULL UNIQUE,
    quelle  TEXT
);
CREATE TABLE IF NOT EXISTS hinweis (
    id          INTEGER PRIMARY KEY,
    wirkstoff_id INTEGER NOT NULL REFERENCES wirkstoff(id) ON DELETE CASCADE,
    tierart     TEXT NOT NULL,
    text        TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS dosierung (
    id          INTEGER PRIMARY KEY,
    wirkstoff_id INTEGER NOT NULL REFERENCES wirkstoff(id) ON DELETE CASCADE,
    tierart     TEXT NOT NULL,
    alter_      TEXT,
    applikation TEXT,
    indikation  TEXT,
    text        TEXT NOT NULL,
    literatur   TEXT
);
"""

WARNWOERTER = ("abgeraten", "toxisch", "kontraindiziert", "nicht verabreich", "tödlich", "vorsicht")


# ---------------------------------------------------------------- Datenbank
def verbinde(pfad: Path = DB_PFAD) -> sqlite3.Connection:
    neu = not pfad.exists()
    pfad.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(pfad, check_same_thread=False)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript(SCHEMA)
    if neu and STARTDATEN.exists():
        for w in json.loads(STARTDATEN.read_text(encoding="utf-8")):
            speichere_wirkstoff(con, w)
    return con


def speichere_wirkstoff(con: sqlite3.Connection, w: dict) -> int:
    """Legt einen Wirkstoff an bzw. ersetzt ihn vollständig (gleicher Name)."""
    with con:
        con.execute("DELETE FROM wirkstoff WHERE name = ?", (w["name"],))
        wid = con.execute(
            "INSERT INTO wirkstoff (name, quelle) VALUES (?, ?)", (w["name"], w.get("quelle", ""))
        ).lastrowid
        con.executemany(
            "INSERT INTO hinweis (wirkstoff_id, tierart, text) VALUES (?, ?, ?)",
            [(wid, h["tierart"], h["text"]) for h in w.get("hinweise", [])],
        )
        con.executemany(
            "INSERT INTO dosierung (wirkstoff_id, tierart, alter_, applikation, indikation, text, literatur)"
            " VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                (wid, d["tierart"], d.get("alter", ""), d.get("applikation", ""),
                 d.get("indikation", ""), d["text"], d.get("literatur", ""))
                for d in w["dosierungen"]
            ],
        )
    return wid


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.casefold())
    return "".join(c for c in s if not unicodedata.combining(c))


def suche(con: sqlite3.Connection, q: str) -> list[dict]:
    q = _norm(q.strip())
    rows = con.execute(
        "SELECT w.id, w.name, COUNT(d.id) AS anzahl FROM wirkstoff w"
        " LEFT JOIN dosierung d ON d.wirkstoff_id = w.id GROUP BY w.id ORDER BY w.name"
    ).fetchall()
    treffer = [dict(r) for r in rows if q in _norm(r["name"])]
    treffer.sort(key=lambda r: (not _norm(r["name"]).startswith(q), r["name"]))
    return treffer


def _passt(hinweis_tierart: str, tierart: str) -> bool:
    worte = {_norm(t.strip()) for t in tierart.replace("&", ",").split(",")}
    return _norm(hinweis_tierart) in worte


def wirkstoff_details(con, wid: int, gewicht_kg: float | None, tierart: str = "") -> dict | None:
    w = con.execute("SELECT * FROM wirkstoff WHERE id = ?", (wid,)).fetchone()
    if not w:
        return None
    hinweise = [dict(h) for h in con.execute(
        "SELECT tierart, text FROM hinweis WHERE wirkstoff_id = ? ORDER BY id", (wid,))]
    for h in hinweise:
        h["warnung"] = any(x in _norm(h["text"]) for x in WARNWOERTER)
    alle = con.execute("SELECT * FROM dosierung WHERE wirkstoff_id = ? ORDER BY id", (wid,)).fetchall()
    tierarten = list(dict.fromkeys(d["tierart"] for d in alle))

    gruppen: dict[tuple, dict] = {}
    for d in alle:
        if tierart and d["tierart"] != tierart:
            continue
        key = (d["tierart"], d["alter_"])
        g = gruppen.setdefault(key, {
            "tierart": d["tierart"], "alter": d["alter_"], "dosierungen": [],
            "hinweise": [h for h in hinweise if _passt(h["tierart"], d["tierart"])],
        })
        g["dosierungen"].append({
            "applikation": d["applikation"], "indikation": d["indikation"],
            "literatur": d["literatur"], "text": d["text"],
            "segmente": dosis.berechne(d["text"], gewicht_kg),
        })
    # Hinweise, die keiner Tierart mit Dosierung zugeordnet werden können, separat zeigen
    allgemein = [] if tierart else [
        h for h in hinweise if not any(_passt(h["tierart"], t) for t in tierarten)]
    return {
        "id": w["id"], "name": w["name"], "quelle": w["quelle"], "tierarten": tierarten,
        "gewicht_kg": gewicht_kg, "hinweise_allgemein": allgemein,
        "gruppen": list(gruppen.values()),
    }


# ---------------------------------------------------------------- Webserver
class Handler(BaseHTTPRequestHandler):
    con: sqlite3.Connection

    def log_message(self, *args):  # ruhige Konsole
        pass

    def _send(self, code: int, body: bytes, typ: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", typ)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code: int = 200) -> None:
        self._send(code, json.dumps(obj, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def do_GET(self):
        url = urllib.parse.urlsplit(self.path)
        qs = dict(urllib.parse.parse_qsl(url.query))
        teile = [t for t in url.path.split("/") if t]
        if not teile or teile == ["index.html"]:
            self._send(200, INDEX_HTML.read_bytes(), "text/html; charset=utf-8")
        elif teile == ["api", "wirkstoffe"]:
            self._json(suche(self.con, qs.get("q", "")))
        elif len(teile) == 3 and teile[:2] == ["api", "wirkstoff"] and teile[2].isdigit():
            try:
                g = float(qs["gewicht"].replace(",", ".")) if qs.get("gewicht") else None
            except ValueError:
                g = None
            det = wirkstoff_details(self.con, int(teile[2]), g, qs.get("tierart", ""))
            self._json(det) if det else self._json({"fehler": "nicht gefunden"}, 404)
        else:
            self._json({"fehler": "nicht gefunden"}, 404)


def starte_server(con, oeffnen: bool = True, port: int = PORT) -> None:
    Handler.con = con
    srv = None
    for p in range(port, port + 20):
        try:
            srv = ThreadingHTTPServer((HOST, p), Handler)
            break
        except OSError:
            continue
    if srv is None:
        sys.exit("Kein freier Port gefunden.")
    adresse = f"http://{HOST}:{srv.server_address[1]}/"
    print(f"Dosisrechner läuft auf {adresse}  (Beenden mit Strg+C)")
    if oeffnen:
        threading.Timer(0.5, lambda: webbrowser.open(adresse)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nBeendet.")


def main(argv: list[str]) -> None:
    con = verbinde()
    if len(argv) >= 2 and argv[0] == "import":
        import vetpharm_import
        for url in argv[1:]:
            w = vetpharm_import.fetch(url)
            speichere_wirkstoff(con, w)
            print(f"Importiert: {w['name']} ({len(w['dosierungen'])} Dosierungen)")
    elif argv and argv[0] == "liste":
        for r in suche(con, ""):
            print(f"{r['name']}: {r['anzahl']} Dosierungen")
    elif not argv or argv[0] in ("start", "--kein-browser"):
        starte_server(con, oeffnen="--kein-browser" not in argv)
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
