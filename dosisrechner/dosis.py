"""Erkennt Dosisangaben pro kg (z. B. "12 - 15 mg/kg") in einem Text und rechnet sie
auf das Körpergewicht des Tieres um."""
from __future__ import annotations

import re

_NUM = r"\d+(?:[.,]\d+)?"
DOSIS_RE = re.compile(
    rf"(?P<a>{_NUM})(?:\s*[-–]\s*(?P<b>{_NUM}))?\s*"
    r"(?P<einheit>mg|µg|μg|mcg|ng|g|ml|mL|IE|I\.E\.|U|mmol)\s*/\s*kg\b"
)

# Umrechnung in die nächstgrössere/-kleinere Einheit für die Zusatzanzeige
_UMRECHNUNG = {"mg": ("µg", 1000, "g", 1 / 1000), "µg": ("ng", 1000, "mg", 1 / 1000)}


def _zahl(s: str) -> float:
    return float(s.replace(",", "."))


def format_zahl(x: float) -> str:
    """Rundet sinnvoll und formatiert mit Dezimalkomma."""
    if x == 0:
        return "0"
    if abs(x) >= 100:
        s = f"{x:.1f}"
    elif abs(x) >= 1:
        s = f"{x:.2f}"
    else:
        s = f"{x:.3g}"
        if "e" in s:
            s = f"{x:.6f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s.replace(".", ",")


def _ergebnis(werte: list[float], einheit: str) -> str:
    def fmt(vs, e):
        return " - ".join(format_zahl(v) for v in vs) + f" {e}"

    haupt = fmt(werte, einheit)
    if einheit in ("μg", "mcg"):
        einheit = "µg"
    if einheit in _UMRECHNUNG:
        klein, fk, gross, fg = _UMRECHNUNG[einheit]
        if max(werte) < 1:
            haupt += f" (= {fmt([v * fk for v in werte], klein)})"
        elif min(werte) >= 1000:
            haupt += f" (= {fmt([v * fg for v in werte], gross)})"
    return haupt


def berechne(text: str, gewicht_kg: float | None) -> list[dict]:
    """Zerlegt den Text in Segmente. Dosis-Segmente erhalten das berechnete Ergebnis.

    >>> [s.get("ergebnis") for s in berechne("3 × täglich 12 - 15 mg/kg alle 8 h", 10)]
    [None, '120 - 150 mg', None]
    """
    segmente: list[dict] = []
    pos = 0
    for m in DOSIS_RE.finditer(text):
        if m.start() > pos:
            segmente.append({"text": text[pos : m.start()]})
        werte = [_zahl(m.group("a"))]
        if m.group("b"):
            werte.append(_zahl(m.group("b")))
        seg = {"text": m.group(0), "dosis_pro_kg": werte, "einheit": m.group("einheit")}
        if gewicht_kg is not None and gewicht_kg > 0:
            seg["ergebnis"] = _ergebnis([w * gewicht_kg for w in werte], m.group("einheit"))
        else:
            seg["ergebnis"] = None
        segmente.append(seg)
        pos = m.end()
    if pos < len(text):
        segmente.append({"text": text[pos:]})
    return segmente
