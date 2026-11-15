"""Liest die Dosierungsseite eines Wirkstoffs von vetpharm.uzh.ch (CliniPharm) ein.

Ergebnis ist ein Dict:
{
  "name": "Ibuprofen",
  "quelle": "<URL>",
  "hinweise": [{"tierart": "Hund", "text": "..."}],
  "dosierungen": [{"tierart": "Hund", "alter": "adultes Tier",
                   "applikation": "oral", "indikation": "", "text": "...",
                   "literatur": "Scherkl 1987a"}]
}
"""
from __future__ import annotations

import json
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser

SUBMIT = "Hier KLICKEN zum Weiterlesen - sponsored by Laboklin"


def _clean(text: str) -> str:
    text = text.replace("﻿", "").replace(" ", " ").replace("​", "")
    return re.sub(r"\s+", " ", text).strip()


class _Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in_title = False
        self._h2 = None  # Text des aktuellen h2
        self.section = None  # "allgemein" | "speziell"
        # allgemein
        self._h3 = None
        self._cur_species = None
        self._buf: list[str] = []
        self.hinweise: list[dict] = []
        # speziell
        self._in_th = False
        self._th_buf: list[str] = []
        self.group = None  # (tierart, alter)
        self._outer_td = 0  # Zähler der äusseren Zellen in einer Zeile
        self._in_outer_td = False
        self._app_buf: list[str] = []
        self.applikation = ""
        self._in_h4 = False
        self._h4_buf: list[str] = []
        self.indikation = ""
        self._inner_tds: list[str] = []
        self._inner_td_buf = None
        self.dosierungen: list[dict] = []
        self._done = False

    # ---------- Hilfen ----------
    def _flush_hinweis(self) -> None:
        if self._cur_species is not None:
            text = _clean("".join(self._buf))
            if text:
                if text.count("(") > text.count(")"):
                    text += ")"
                self.hinweise.append({"tierart": self._cur_species, "text": text})
        self._buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "h2":
            if self.section == "allgemein":
                self._flush_hinweis()
                self._cur_species = None
            self._h2 = []
        elif self.section == "allgemein" and tag == "h3":
            self._flush_hinweis()
            self._h3 = []
        elif self.section == "speziell" and not self._done:
            if tag == "th":
                self._in_th, self._th_buf = True, []
            elif tag == "tr" and not self._in_outer_td:
                self._outer_td = 0
            elif tag == "td" and "pt-2" in (a.get("class") or ""):
                self._outer_td += 1
                self._in_outer_td = True
                if self._outer_td == 1:
                    self._app_buf = []
                else:
                    self.indikation = ""
            elif tag == "h4" and self._in_outer_td:
                self._in_h4, self._h4_buf = True, []
            elif tag == "tr" and self._in_outer_td:
                self._inner_tds = []
            elif tag == "td" and self._in_outer_td:
                self._inner_td_buf = []

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "h2" and self._h2 is not None:
            h = _clean("".join(self._h2))
            self._h2 = None
            if "allgemein" in h:
                self.section = "allgemein"
            elif "speziell" in h:
                self.section = "speziell"
            else:
                self.section = None
        elif self.section == "allgemein" and tag == "h3" and self._h3 is not None:
            self._cur_species = _clean("".join(self._h3))
            self._h3 = None
        elif self.section == "allgemein" and tag == "v-col":
            self._flush_hinweis()
            self._cur_species = None
        elif self.section == "speziell" and not self._done:
            if tag == "th" and self._in_th:
                self._in_th = False
                head = _clean("".join(self._th_buf))
                m = re.match(r"(.+?)\s*\(([^)]*)\)\s*-\s*.+$", head)
                if m:
                    self.group = (m.group(1).strip(), m.group(2).strip())
                else:
                    self.group = (head.rsplit(" - ", 1)[0], "")
            elif tag == "h4" and self._in_h4:
                self._in_h4 = False
                self.indikation = _clean("".join(self._h4_buf))
            elif tag == "td" and self._inner_td_buf is not None:
                self._inner_tds.append(_clean("".join(self._inner_td_buf)))
                self._inner_td_buf = None
            elif tag == "td" and self._in_outer_td:
                self._in_outer_td = False
                if self._outer_td == 1:
                    self.applikation = _clean("".join(self._app_buf))
            elif tag == "tr" and self._in_outer_td:
                self._add_entry(self._inner_tds)
                self._inner_tds = []
            elif tag == "template":
                self._done = True

    def _add_entry(self, cells: list[str]) -> None:
        cells = [c for c in cells if c]
        if len(cells) < 2 or self.group is None:
            return
        text = cells[-1]
        literatur = ""
        m = re.search(r"\(([^()]*\d{4}[a-z]?[^()]*)\)\s*$", text)
        if m:
            literatur = m.group(1).strip()
            text = text[: m.start()].strip()
        self.dosierungen.append(
            {
                "tierart": self.group[0],
                "alter": self.group[1],
                "applikation": self.applikation,
                "indikation": self.indikation,
                "text": text,
                "literatur": literatur,
            }
        )

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._h2 is not None:
            self._h2.append(data)
        if self.section == "allgemein":
            if self._h3 is not None:
                self._h3.append(data)
            elif self._cur_species is not None:
                self._buf.append(data)
        if self.section == "speziell":
            if self._in_th:
                self._th_buf.append(data)
            if self._in_h4:
                self._h4_buf.append(data)
            if self._inner_td_buf is not None:
                self._inner_td_buf.append(data)
            elif self._in_outer_td and self._outer_td == 1:
                self._app_buf.append(data)


def parse_html(html: str, quelle: str = "") -> dict:
    p = _Parser()
    p.feed(html)
    p.close()
    title = _clean(p.title)
    m = re.match(r"Wirkstoff:\s*(.+?)\s*-\s*Dosierung", title)
    name = m.group(1) if m else title
    if not p.dosierungen:
        raise ValueError("Keine Dosierungen auf der Seite gefunden.")
    return {"name": name, "quelle": quelle, "hinweise": p.hinweise, "dosierungen": p.dosierungen}


def _full_url(url: str) -> str:
    parts = urllib.parse.urlsplit(url)
    q = dict(urllib.parse.parse_qsl(parts.query))
    q.setdefault("Submit", SUBMIT)  # ohne diesen Parameter zeigt die Seite nur einen Teaser
    return urllib.parse.urlunsplit(parts._replace(query=urllib.parse.urlencode(q)))


def fetch(url: str) -> dict:
    url = _full_url(url)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Dosisrechner)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        html = r.read().decode("utf-8-sig", errors="replace")
    return parse_html(html, url)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Aufruf: python vetpharm_import.py <URL oder HTML-Datei>")
        sys.exit(1)
    src = sys.argv[1]
    if src.startswith("http"):
        data = fetch(src)
    else:
        with open(src, encoding="utf-8-sig") as f:
            data = parse_html(f.read(), src)
    print(json.dumps(data, ensure_ascii=False, indent=2))
