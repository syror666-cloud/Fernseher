"""Eigene 2D-Cutout-Figuren für CODE ROT (SVG).

Stil: runder Kopf, Kreisaugen mit Pupillen, flache Farben ohne Outlines,
leichte Schattierung. Körper als abgerundeter Torso mit Ausrüstung.
Alle Maße in einem 600x1000-Koordinatensystem (Halbnah-Ansicht).
"""
from dataclasses import dataclass, field

HAUT = {"hell": ("#EBC09A", "#D7A67F"), "mittel": ("#D39B6E", "#BC855A"), "dunkel": ("#8E5B3A", "#774A2E")}


@dataclass
class Figur:
    name: str
    haut: str = "hell"
    haar: str = "#5A3A22"
    frisur: str = "kurz"          # kurz | seitenscheitel | glatze
    bart: str = ""                # "" | schnurrbart | stoppeln
    sommersprossen: bool = False
    jacke: str = "#3F4A2E"        # Oliv
    jacke_schatten: str = "#333C25"
    weste: str = "#1E2226"
    helm: bool = False
    helm_farbe: str = "#2A2E24"
    funk: bool = True
    kopf: str = ""                # "" | barett | kappe | nachtsicht | sturmhaube | gasmaske | visier
    kopf_farbe: str = "#1A1A1A"
    hose: str = ""                # leer = wie Jacke
    zivil: bool = False           # Hemd statt Weste


def _augen(expr, cx, cy, haut="#EBC09A"):
    """Augenpaar je nach Ausdruck. Pupillen und Lider als animierbare Gruppen (rig-pupillen, rig-lider)."""
    weiss, pup, lid, deckel = [], [], [], []
    for dx in (-48, 48):
        x = cx + dx
        if expr in ("erleichtert", "zu"):
            weiss.append(f'<path d="M{x-24},{cy+4} Q{x},{cy-16} {x+24},{cy+4}" stroke="#2B1B14" stroke-width="7" fill="none" stroke-linecap="round"/>')
            continue
        r = 36 if expr in ("angst", "schock") else 32
        px, py = (x + 4, cy + 4)
        if expr == "seitenblick":
            px = x + 12
        if expr == "entschlossen":
            py = cy + 6
        pr = 10 if expr == "schock" else 14
        weiss.append(f'<circle cx="{x}" cy="{cy}" r="{r}" fill="#FFFFFF"/>')
        pup.append(f'<circle cx="{px}" cy="{py}" r="{pr}" fill="#1A1210"/><circle cx="{px+4}" cy="{py-4}" r="3.5" fill="#FFFFFF"/>')
        if expr == "entschlossen":
            deckel.append(f'<path d="M{x-38},{cy-6} L{x+38},{cy-6} L{x+38},{cy-44} L{x-38},{cy-44} Z" fill="{haut}"/>')
        lid.append(f'<ellipse cx="{x}" cy="{cy}" rx="{r+3}" ry="{r+3}" fill="{haut}"/>'
                   f'<path d="M{x-r},{cy} Q{x},{cy+10} {x+r},{cy}" stroke="#2B1B14" stroke-width="6" fill="none"/>')
    out = "".join(weiss)
    if pup:
        out += f'<g class="rig-pupillen">{"".join(pup)}</g>'
    out += "".join(deckel)
    if lid:
        out += f'<g class="rig-lider" data-o="{cx},{cy}" transform="scale(1,0)" style="transform-origin:{cx}px {cy}px">{"".join(lid)}</g>'
    return out


def _brauen(expr, cx, cy):
    out = []
    for s, dx in ((-1, -48), (1, 48)):
        x = cx + dx
        if expr == "angst":
            a, b = (cy - 52 + (s * 6), cy - 44 - (s * 6))
        elif expr == "entschlossen":
            a, b = (cy - 52 - s * 10, cy - 52 + s * 10) if s < 0 else (cy - 42, cy - 62)
            a, b = (cy - 62, cy - 44) if s < 0 else (cy - 44, cy - 62)
        elif expr == "schock":
            a, b = cy - 64, cy - 64
        else:
            a, b = cy - 50, cy - 50
        out.append(f'<line x1="{x-22}" y1="{a}" x2="{x+22}" y2="{b}" stroke="#3B2618" stroke-width="9" stroke-linecap="round"/>')
    return "".join(out)


def _mund(expr, cx, cy):
    if expr in ("angst", "schock"):
        return f'<ellipse cx="{cx}" cy="{cy}" rx="{12 if expr=="angst" else 16}" ry="{16 if expr=="angst" else 22}" fill="#5A1F1A"/><ellipse cx="{cx}" cy="{cy+8}" rx="8" ry="6" fill="#C9605A"/>'
    if expr == "entschlossen":
        return f'<line x1="{cx-22}" y1="{cy}" x2="{cx+22}" y2="{cy}" stroke="#4A2318" stroke-width="7" stroke-linecap="round"/>'
    if expr == "erleichtert":
        return f'<path d="M{cx-26},{cy-4} Q{cx},{cy+22} {cx+26},{cy-4} Z" fill="#5A1F1A"/>'
    if expr == "schreien":
        return f'<path d="M{cx-30},{cy-12} Q{cx},{cy-18} {cx+30},{cy-12} Q{cx+22},{cy+34} {cx},{cy+36} Q{cx-22},{cy+34} {cx-30},{cy-12} Z" fill="#4A1612"/><rect x="{cx-22}" y="{cy-12}" width="44" height="9" rx="3" fill="#F4F0E8"/>'
    return f'<path d="M{cx-18},{cy} Q{cx},{cy+8} {cx+18},{cy}" stroke="#4A2318" stroke-width="6" fill="none" stroke-linecap="round"/>'


def _kopfbedeckung(f, cx, ky, kr):
    k, c = f.kopf, f.kopf_farbe
    if k == "barett":
        return (f'<path d="M{cx-170},{ky-70} Q{cx-150},{ky-200} {cx+20},{ky-190} Q{cx+200},{ky-180} {cx+190},{ky-110} '
                f'Q{cx+120},{ky-60} {cx-170},{ky-70} Z" fill="{c}"/>'
                f'<rect x="{cx-160}" y="{ky-92}" width="300" height="26" rx="12" fill="#151515"/>'
                f'<circle cx="{cx-80}" cy="{ky-118}" r="20" fill="#B8B8B0"/>')
    if k == "kappe":
        return (f'<path d="M{cx-158},{ky-40} Q{cx-160},{ky-190} {cx},{ky-190} Q{cx+160},{ky-190} {cx+158},{ky-40} Z" fill="{c}"/>'
                f'<path d="M{cx-150},{ky-48} Q{cx},{ky-80} {cx+230},{ky-40} L{cx+220},{ky-20} Q{cx},{ky-50} {cx-150},{ky-30} Z" fill="{c}" opacity="0.85"/>')
    if k in ("nachtsicht", "visier"):
        out = (f'<path d="M{cx-172},{ky-10} Q{cx-176},{ky-200} {cx},{ky-206} Q{cx+176},{ky-200} {cx+172},{ky-10} '
               f'L{cx+156},{ky-44} Q{cx},{ky-84} {cx-156},{ky-44} Z" fill="{c}"/>'
               f'<path d="M{cx-156},{ky-44} Q{cx},{ky-84} {cx+156},{ky-44}" stroke="#111" stroke-width="10" fill="none"/>')
        if k == "nachtsicht":
            out += (f'<rect x="{cx-16}" y="{ky-160}" width="32" height="60" rx="6" fill="#111"/>'
                    f'<rect x="{cx-70}" y="{ky-110}" width="140" height="44" rx="14" fill="#1B1E1B"/>'
                    f'<circle cx="{cx-36}" cy="{ky-88}" r="16" fill="#0E3B1C"/><circle cx="{cx+36}" cy="{ky-88}" r="16" fill="#0E3B1C"/>'
                    f'<circle cx="{cx-36}" cy="{ky-88}" r="7" fill="#4CFF7A"/><circle cx="{cx+36}" cy="{ky-88}" r="7" fill="#4CFF7A"/>')
        else:
            out += f'<path d="M{cx-150},{ky-40} Q{cx},{ky-70} {cx+150},{ky-40} L{cx+140},{ky+30} Q{cx},{ky+10} {cx-140},{ky+30} Z" fill="#7FA6C4" opacity="0.35"/>'
        return out
    if k == "sturmhaube":
        return (f'<path fill-rule="evenodd" d="M{cx-kr-6},{ky} A{kr+6},{kr+6} 0 1 1 {cx+kr+6},{ky} L{cx+kr-10},{ky+170} L{cx-kr+10},{ky+170} Z '
                f'M{cx-96},{ky-34} Q{cx},{ky-52} {cx+96},{ky-34} L{cx+96},{ky+30} Q{cx},{ky+44} {cx-96},{ky+30} Z" fill="{c}"/>')
    if k == "gasmaske":
        return (f'<path d="M{cx-kr-6},{ky} A{kr+6},{kr+6} 0 1 1 {cx+kr+6},{ky} L{cx+kr-10},{ky+170} L{cx-kr+10},{ky+170} Z" fill="{c}"/>'
                f'<circle cx="{cx-50}" cy="{ky}" r="40" fill="#6E7C84"/><circle cx="{cx+50}" cy="{ky}" r="40" fill="#6E7C84"/>'
                f'<circle cx="{cx-50}" cy="{ky}" r="30" fill="#25343C"/><circle cx="{cx+50}" cy="{ky}" r="30" fill="#25343C"/>'
                f'<circle cx="{cx-40}" cy="{ky-10}" r="8" fill="#B9D2DE"/><circle cx="{cx+60}" cy="{ky-10}" r="8" fill="#B9D2DE"/>'
                f'<circle cx="{cx}" cy="{ky+84}" r="44" fill="#2C2C2C"/><circle cx="{cx}" cy="{ky+84}" r="30" fill="#1A1A1A"/>')
    return ""


KURZ = 0.7  # Beinlänge im Comic-Look (große Köpfe, kurze Beine)


def _beine_kurz(f):
    return f'<g transform="translate(0,1000) scale(1,{KURZ}) translate(0,-1000)">{_beine(f)}</g>'


def svg_ganz(f: Figur, expr: str = "neutral", width: int = 600, height: int = 1600, arm: str = "unten", kurz: bool = False) -> str:
    """Ganzkörper: Halbnah-Figur plus Gürtel, Beine, Stiefel (viewBox 600x1600)."""
    oben = svg(f, expr, arm=arm).split(">", 1)[1].rsplit("</svg>", 1)[0]
    oben = oben.replace('Q150,820 168,690 Z" fill="' + f.jacke + '"/></g>', 'Q150,820 168,690 Z" fill="' + f.jacke + '"/><circle cx="132" cy="1000" r="34" fill="#141414"/></g>', 1)
    oben = oben.replace('Q450,820 432,690 Z" fill="' + f.jacke + '"/></g>', 'Q450,820 432,690 Z" fill="' + f.jacke + '"/><circle cx="468" cy="1000" r="34" fill="#141414"/></g>', 1)
    # Beine hinter den Oberkörper legen
    if kurz:
        hh = int(1000 + 600 * KURZ)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 {hh}" width="{width}" height="{int(width * hh / 600)}">'
                f'<g class="rig-ganz">{_beine_kurz(f)}{oben}</g></svg>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 1600" width="{width}" height="{height}">'
            f'<g class="rig-ganz">{_beine(f)}{oben}</g></svg>')


def svg_ruecken(f: Figur, width: int = 600, height: int = 1600, waffe: bool = True) -> str:
    """Rückansicht in ganzer Größe (Figur läuft vom Zuschauer weg, wie im Referenz-Stil). viewBox 600x1600."""
    haut, haut_s = HAUT[f.haut]
    cx, ky, kr = 300, 330, 160
    hh = int(1000 + 600 * KURZ)
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 {hh}" width="{width}" height="{int(width * hh / 600)}">',
         '<g class="rig-ganz">', _beine_kurz(f), '<g class="rig-figur"><g class="rig-koerper" data-o="300,1000">',
         f'<path d="M110,1000 L118,640 Q124,560 210,540 L390,540 Q476,560 482,640 L490,1000 Z" fill="{f.jacke}"/>',
         f'<path d="M420,1000 L428,620 Q470,600 482,640 L490,1000 Z" fill="{f.jacke_schatten}"/>']
    if not f.zivil:  # Westen-Rückenplatte mit Rucksack/Funk
        p.append(f'<path d="M150,1000 L156,640 Q170,590 236,580 L364,580 Q430,590 444,640 L450,1000 Z" fill="{f.weste}"/>')
        p.append('<rect x="200" y="640" width="200" height="230" rx="26" fill="#22281E"/><rect x="200" y="640" width="200" height="60" rx="22" fill="#2C3326"/>'
                 '<rect x="232" y="720" width="136" height="16" rx="6" fill="#1A1F17"/>')
        if f.funk:
            p.append('<rect x="372" y="600" width="44" height="110" rx="8" fill="#121416"/><rect x="398" y="470" width="8" height="140" rx="3" fill="#121416"/>')
    if waffe:
        p.append('<path d="M120,600 L470,960 L452,980 L104,622 Z" fill="#1B1D1F"/>')  # Gewehr am Riemen über dem Rücken
    p.append('</g>')
    p.append(f'<g class="rig-arm-l" data-o="140,650"><path d="M118,640 Q90,800 104,1000 L160,1000 Q150,820 168,690 Z" fill="{f.jacke}"/></g>')
    p.append(f'<g class="rig-arm-r" data-o="460,650"><path d="M482,640 Q510,800 496,1000 L440,1000 Q450,820 432,690 Z" fill="{f.jacke_schatten}"/></g>')
    p.append(f'<rect x="262" y="470" width="76" height="80" rx="20" fill="{haut_s}"/>')
    p.append(f'<g class="rig-kopf" data-o="{cx},{ky+170}"><circle cx="{cx}" cy="{ky}" r="{kr}" fill="{haut}"/>')
    for s_ in (-1, 1):
        p.append(f'<ellipse cx="{cx + s_*150}" cy="{ky+20}" rx="22" ry="34" fill="{haut_s}"/>')
    p.append(f'<path d="M{cx-160},{ky+20} Q{cx-172},{ky-172} {cx},{ky-168} Q{cx+172},{ky-172} {cx+160},{ky+20} '
             f'Q{cx+150},{ky+120} {cx+90},{ky+140} Q{cx},{ky+120} {cx-90},{ky+140} Q{cx-150},{ky+120} {cx-160},{ky+20} Z" fill="{f.haar}"/>'
             f'<path d="M{cx-100},{ky+60} Q{cx},{ky+90} {cx+100},{ky+60}" stroke="#000" stroke-opacity=".18" stroke-width="10" fill="none"/>')
    if f.kopf == "kappe":
        p.append(f'<path d="M{cx-162},{ky-30} Q{cx-164},{ky-196} {cx},{ky-196} Q{cx+164},{ky-196} {cx+162},{ky-30} Q{cx},{ky-60} {cx-162},{ky-30} Z" fill="{f.kopf_farbe}"/>'
                 f'<rect x="{cx-40}" y="{ky-50}" width="80" height="22" rx="8" fill="#1A1C16"/>')
    elif f.helm or f.kopf in ("nachtsicht", "visier"):
        c = f.helm_farbe if f.helm else f.kopf_farbe
        p.append(f'<path d="M{cx-172},{ky+10} Q{cx-176},{ky-206} {cx},{ky-210} Q{cx+176},{ky-206} {cx+172},{ky+10} Q{cx},{ky-20} {cx-172},{ky+10} Z" fill="{c}"/>')
    elif f.kopf in ("sturmhaube", "gasmaske"):
        p.append(f'<circle cx="{cx}" cy="{ky}" r="{kr+6}" fill="{f.kopf_farbe}"/>')
    p.append('</g></g></g></svg>')
    return "".join(p)


def _beine(f):
    hose = f.hose or f.jacke
    unten = (f'<rect x="150" y="960" width="300" height="50" rx="10" fill="#151719"/>'
             f'<rect x="282" y="966" width="36" height="38" rx="6" fill="#5C5E60"/>'
             f'<g class="rig-bein-l" data-o="225,1000"><path d="M160,1000 L290,1000 L282,1500 L176,1500 Z" fill="{hose}"/>'
             f'<path d="M160,1000 L200,1000 L196,1500 L176,1500 Z" fill="#000" opacity="0.15"/>'
             f'<rect x="168" y="1180" width="110" height="80" rx="12" fill="#000" opacity="0.18"/>'
             f'<path d="M168,1490 L288,1490 L300,1590 L140,1590 Q140,1540 168,1490 Z" fill="#111214"/></g>'
             f'<g class="rig-bein-r" data-o="375,1000"><path d="M310,1000 L440,1000 L424,1500 L318,1500 Z" fill="{hose}"/>'
             f'<rect x="322" y="1180" width="110" height="80" rx="12" fill="#000" opacity="0.18"/>'
             f'<path d="M312,1490 L432,1490 L460,1590 L300,1590 Z" fill="#111214"/></g>')
    return unten


def svg(f: Figur, expr: str = "neutral", arm: str = "unten", width: int = 600, height: int = 1000) -> str:
    haut, haut_s = HAUT[f.haut]
    cx, kopf_y, kopf_r = 300, 330, 160
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 1000" width="{width}" height="{height}" style="--hautfarbe:{haut}">']
    # --- Torso ---
    p.append('<g class="rig-figur">')
    p.append('<g class="rig-koerper" data-o="300,1000">')
    p.append(f'<path d="M110,1000 L118,640 Q124,560 210,540 L390,540 Q476,560 482,640 L490,1000 Z" fill="{f.jacke}"/>')
    p.append(f'<path d="M110,1000 L118,640 Q124,575 180,552 L170,1000 Z" fill="{f.jacke_schatten}"/>')
    # Kragen
    p.append(f'<path d="M230,540 L300,610 L370,540 L350,532 L300,580 L250,532 Z" fill="{f.jacke_schatten}"/>')
    if f.zivil:
        p.append(f'<path d="M262,540 L300,640 L338,540 Z" fill="#F2EEE6"/>')
        p.append(f'<path d="M240,536 L300,600 L280,640 L222,560 Z M360,536 L300,600 L320,640 L378,560 Z" fill="{f.jacke_schatten}"/>')
        for yy in (700, 780, 860, 940):
            p.append(f'<circle cx="300" cy="{yy}" r="7" fill="{f.jacke_schatten}"/>')
    # Weste mit Taschen
    if not f.zivil:
        p.append(f'<path d="M160,1000 L168,660 Q172,600 236,585 L300,640 L364,585 Q428,600 432,660 L440,1000 Z" fill="{f.weste}"/>')
        for i, x in enumerate((190, 252, 318, 380)):
            p.append(f'<rect x="{x}" y="760" width="52" height="74" rx="8" fill="#2B3036"/><rect x="{x}" y="760" width="52" height="18" rx="6" fill="#353B42"/>')
        if f.funk:
            p.append('<rect x="372" y="640" width="34" height="70" rx="6" fill="#121416"/><rect x="384" y="596" width="7" height="48" rx="3" fill="#121416"/><circle cx="389" cy="660" r="5" fill="#C0392B"/>')
    p.append('</g>')  # Ende Körper
    # Arme
    ARM_L = f'<g class="rig-arm-l" data-o="140,650"><path d="M118,640 Q90,800 104,1000 L160,1000 Q150,820 168,690 Z" fill="{f.jacke}"/>{{hand_l}}</g>'
    if arm == "unten":
        p.append(ARM_L.replace("{hand_l}", ""))
        p.append(f'<g class="rig-arm-r" data-o="460,650"><path d="M482,640 Q510,800 496,1000 L440,1000 Q450,820 432,690 Z" fill="{f.jacke}"/></g>')
    elif arm == "funk":  # rechte Hand am Funkgerät
        p.append(ARM_L.replace("{hand_l}", ""))
        p.append(f'<g class="rig-arm-r" data-o="460,650"><path d="M482,640 Q540,760 470,820 L420,760 Q470,720 432,690 Z" fill="{f.jacke}"/>'
                 '<circle cx="412" cy="728" r="30" fill="#1B1D1F"/></g>')
    elif arm == "zeigen":  # Handzeichen nach vorne
        p.append(ARM_L.replace("{hand_l}", ""))
        p.append(f'<g class="rig-arm-r" data-o="480,640"><path d="M470,620 L590,500 L612,540 L500,690 Z" fill="{f.jacke}"/>'
                 '<circle cx="600" cy="510" r="30" fill="#1B1D1F"/></g>')
    elif arm == "waffe":  # Gewehr schräg vor der Brust, beide Hände dran
        p.append(f'<g class="rig-arm-l" data-o="140,650"><path d="M118,640 Q80,760 150,860 L300,800 L280,760 L196,790 Q170,720 168,690 Z" fill="{f.jacke}"/></g>')
        p.append('<g class="rig-waffe" data-o="300,800"><path d="M70,930 L520,640 L548,668 L120,960 Z" fill="#1B1D1F"/>'
                 '<rect x="250" y="760" width="40" height="90" rx="8" fill="#141516" transform="rotate(-33 270 805)"/>'
                 '<path d="M120,960 L60,1010 L40,980 L70,930 Z" fill="#3A2A1E"/>'
                 '<g class="rig-muendung" opacity="0"><polygon points="560,628 640,560 600,630 690,620 604,654 650,720 572,664" fill="#FFD23A"/>'
                 '<circle cx="574" cy="640" r="26" fill="#FFF4C0"/></g></g>')
        p.append('<circle cx="290" cy="790" r="30" fill="#1B1D1F"/>')
        p.append(f'<g class="rig-arm-r" data-o="460,650"><path d="M482,640 Q520,720 470,720 L430,700 Q440,690 432,690 Z" fill="{f.jacke}"/>'
                 '<circle cx="452" cy="706" r="28" fill="#1B1D1F"/></g>')
    elif arm == "fernglas":  # Fernglas vor den Augen (nach dem Kopf gezeichnet, siehe unten)
        p.append(f'<g class="rig-arm-l" data-o="140,650"><path d="M118,640 Q60,560 170,400 L220,430 Q150,560 168,690 Z" fill="{f.jacke}"/></g>')
        p.append(f'<g class="rig-arm-r" data-o="460,650"><path d="M482,640 Q540,560 430,400 L380,430 Q450,560 432,690 Z" fill="{f.jacke}"/></g>')
    # --- Hals & Kopf ---
    p.append(f'<rect x="262" y="470" width="76" height="80" rx="20" fill="{haut_s}"/>')
    p.append(f'<g class="rig-kopf" data-o="{cx},{kopf_y+170}">')
    p.append(f'<circle cx="{cx}" cy="{kopf_y}" r="{kopf_r}" fill="{haut}"/>')
    p.append(f'<path d="M{cx-kopf_r},{kopf_y} A{kopf_r},{kopf_r} 0 0 0 {cx+kopf_r*0.2},{kopf_y+kopf_r*0.99} A{kopf_r*1.1},{kopf_r*1.1} 0 0 1 {cx-kopf_r},{kopf_y} Z" fill="{haut_s}" opacity="0.55"/>')
    # Ohren
    for s in (-1, 1):
        p.append(f'<ellipse cx="{cx + s*146}" cy="{kopf_y+20}" rx="22" ry="34" fill="{haut_s}"/>')
    # Haare / Helm
    if f.helm:
        p.append(f'<path d="M{cx-168},{kopf_y-10} Q{cx-170},{kopf_y-190} {cx},{kopf_y-196} Q{cx+170},{kopf_y-190} {cx+168},{kopf_y-10} L{cx+150},{kopf_y-40} Q{cx},{kopf_y-80} {cx-150},{kopf_y-40} Z" fill="{f.helm_farbe}"/>')
        p.append(f'<path d="M{cx-150},{kopf_y-40} Q{cx},{kopf_y-80} {cx+150},{kopf_y-40}" stroke="#1A1C16" stroke-width="10" fill="none"/>')
        p.append(f'<rect x="{cx-14}" y="{kopf_y-150}" width="28" height="44" rx="6" fill="#1A1C16"/>')  # Halterung
        for s in (-1, 1):
            p.append(f'<path d="M{cx+s*150},{kopf_y-30} L{cx+s*120},{kopf_y+120}" stroke="#1A1C16" stroke-width="8"/>')
    elif f.kopf in ("sturmhaube", "gasmaske", "nachtsicht", "visier"):
        pass
    elif f.frisur == "kurz":
        p.append(f'<path d="M{cx-148},{kopf_y-20} Q{cx-150},{kopf_y-160} {cx},{kopf_y-158} Q{cx+150},{kopf_y-160} {cx+148},{kopf_y-20} Q{cx+120},{kopf_y-90} {cx+40},{kopf_y-96} Q{cx-60},{kopf_y-70} {cx-148},{kopf_y-20} Z" fill="{f.haar}"/>')
    elif f.frisur == "lang":
        p.append(f'<path d="M{cx-165},{kopf_y+170} L{cx-162},{kopf_y-30} Q{cx-160},{kopf_y-175} {cx},{kopf_y-172} Q{cx+160},{kopf_y-175} {cx+162},{kopf_y-30} '
                 f'L{cx+165},{kopf_y+170} L{cx+120},{kopf_y+170} L{cx+118},{kopf_y-40} Q{cx+60},{kopf_y-110} {cx},{kopf_y-100} Q{cx-60},{kopf_y-110} {cx-118},{kopf_y-40} L{cx-120},{kopf_y+170} Z" fill="{f.haar}"/>')
    elif f.frisur == "seitenscheitel":
        p.append(f'<path d="M{cx-150},{kopf_y+10} Q{cx-160},{kopf_y-170} {cx+10},{kopf_y-160} Q{cx+160},{kopf_y-150} {cx+150},{kopf_y-10} Q{cx+130},{kopf_y-70} {cx+60},{kopf_y-100} Q{cx-20},{kopf_y-40} {cx-120},{kopf_y-60} Q{cx-140},{kopf_y-20} {cx-150},{kopf_y+10} Z" fill="{f.haar}"/>')
    # Gesicht
    p.append(f'<g class="rig-brauen">{_brauen(expr, cx, kopf_y)}</g>')
    p.append(_augen(expr, cx, kopf_y, haut))
    p.append(f'<ellipse cx="{cx}" cy="{kopf_y+42}" rx="14" ry="10" fill="{haut_s}"/>')
    if f.bart == "schnurrbart":
        p.append(f'<path d="M{cx-46},{kopf_y+74} Q{cx},{kopf_y+50} {cx+46},{kopf_y+74} Q{cx+20},{kopf_y+66} {cx},{kopf_y+68} Q{cx-20},{kopf_y+66} {cx-46},{kopf_y+74} Z" fill="{f.haar}"/>')
    if f.bart == "stoppeln" or f.sommersprossen:
        import random
        rnd = random.Random(f.name)
        for _ in range(22 if f.bart == "stoppeln" else 10):
            x = cx + rnd.uniform(-90, 90)
            y = kopf_y + (rnd.uniform(70, 125) if f.bart == "stoppeln" else rnd.uniform(25, 55))
            p.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3.2" fill="{"#7A4A30" if f.bart=="stoppeln" else "#B5704A"}"/>')
    p.append(f'<g class="rig-mund" data-o="{cx},{kopf_y+92}">{_mund(expr, cx, kopf_y + 92)}</g>')
    # offener Mund für Lippenbewegung beim Sprechen (Laufzeit blendet zwischen rig-mund und rig-mund-offen um)
    p.append(f'<g class="rig-mund-offen" opacity="0"><ellipse cx="{cx}" cy="{kopf_y+96}" rx="24" ry="20" fill="#4A1612"/>'
             f'<ellipse cx="{cx}" cy="{kopf_y+106}" rx="14" ry="8" fill="#C9605A"/></g>')
    p.append(_kopfbedeckung(f, cx, kopf_y, kopf_r))
    if expr in ("angst", "schock"):
        p.append(f'<g class="rig-schweiss"><path d="M{cx+128},{kopf_y-90} Q{cx+142},{kopf_y-60} {cx+128},{kopf_y-52} Q{cx+114},{kopf_y-60} {cx+128},{kopf_y-90} Z" fill="#9FD3F0"/></g>')
    if arm == "fernglas":
        p.append(f'<g class="rig-fernglas"><rect x="{cx-120}" y="{kopf_y-40}" width="100" height="80" rx="20" fill="#16181A"/>'
                 f'<rect x="{cx+20}" y="{kopf_y-40}" width="100" height="80" rx="20" fill="#16181A"/>'
                 f'<rect x="{cx-30}" y="{kopf_y-20}" width="60" height="34" fill="#16181A"/>'
                 f'<circle cx="{cx-70}" cy="{kopf_y}" r="26" fill="#2E4A5E"/><circle cx="{cx+70}" cy="{kopf_y}" r="26" fill="#2E4A5E"/>'
                 f'<circle cx="{cx-78}" cy="{kopf_y-8}" r="7" fill="#9CC4DC"/><circle cx="{cx+62}" cy="{kopf_y-8}" r="7" fill="#9CC4DC"/>'
                 f'<circle cx="{cx-150}" cy="{kopf_y+20}" r="30" fill="#1B1D1F"/><circle cx="{cx+150}" cy="{kopf_y+20}" r="30" fill="#1B1D1F"/></g>')
    p.append("</g>")  # Ende Kopf
    p.append("</g>")  # Ende Figur
    p.append("</svg>")
    return "".join(p).replace("var(--hautfarbe)", haut)


# ---------- Serien-Besetzung: ein Vertreter pro Einheit (für das Intro) ----------
EINHEITEN_FIGUREN = {
    "NAVY SEALS": Figur("seals", haut="mittel", jacke="#7A6A4F", jacke_schatten="#665840", weste="#5E5442", kopf="nachtsicht", kopf_farbe="#6E6250", bart="stoppeln"),
    "SAS": Figur("sas", jacke="#1B1B1D", jacke_schatten="#121214", weste="#2A2A2C", kopf="gasmaske", kopf_farbe="#1A1A1A"),
    "GIGN": Figur("gign", jacke="#1D2434", jacke_schatten="#151B28", weste="#262E40", kopf="visier", kopf_farbe="#20283A"),
    "BOPE": Figur("bope", haut="dunkel", haar="#140E0B", jacke="#151515", jacke_schatten="#0D0D0D", weste="#222", kopf="barett", kopf_farbe="#0B0B0B"),
    "KSK": Figur("ksk", jacke="#4B5536", jacke_schatten="#3C452B", weste="#55603F", kopf="nachtsicht", kopf_farbe="#4A5238"),
    "SAYERET MATKAL": Figur("matkal", haut="mittel", haar="#1E1410", jacke="#56583E", jacke_schatten="#47492F", weste="#3B3D2B", kopf="kappe", kopf_farbe="#45472F", bart="stoppeln"),
    "GSG 9": Figur("gsg9", jacke="#3F4A2E", jacke_schatten="#333C25", weste="#1E2226", kopf="visier", kopf_farbe="#2A2E24"),
    "DELTA FORCE": Figur("delta", haar="#3A2A1C", jacke="#7B6E57", jacke_schatten="#665B47", weste="#4E4636", kopf="kappe", kopf_farbe="#3E3A30", bart="stoppeln"),
    "GROM": Figur("grom", jacke="#202226", jacke_schatten="#16181B", weste="#2C2F34", kopf="sturmhaube", kopf_farbe="#141414"),
    "SEK": Figur("sek", jacke="#1E2A3C", jacke_schatten="#16202E", weste="#283548", kopf="sturmhaube", kopf_farbe="#121821"),
    "PARARESCUE": Figur("pj", haut="dunkel", haar="#140E0B", jacke="#5A6046", jacke_schatten="#4A503A", weste="#3E4332", kopf="barett", kopf_farbe="#6B1E24"),
    "EKO COBRA": Figur("cobra", jacke="#17191C", jacke_schatten="#101214", weste="#25282C", kopf="visier", kopf_farbe="#1C1F23"),
    "JTF2": Figur("jtf2", jacke="#D8DCE0", jacke_schatten="#BFC4C9", weste="#9AA1A8", kopf="sturmhaube", kopf_farbe="#E6E8EA"),
    "SAT": Figur("sat", haar="#0E0E10", jacke="#1A2233", jacke_schatten="#121828", weste="#232C40", kopf="visier", kopf_farbe="#1A2233"),
}

ZIVIL_M = Figur("zivil_m", haut="hell", haar="#4A3420", frisur="seitenscheitel", bart="", jacke="#A86A3A", jacke_schatten="#8A552D", zivil=True, funk=False, hose="#3B3328")
ZIVIL_F = Figur("zivil_f", haut="hell", haar="#B8862E", frisur="lang", jacke="#5C7FA8", jacke_schatten="#4A6A90", zivil=True, funk=False, hose="#2E3A4A")
ZIVIL_K = Figur("zivil_k", haut="mittel", haar="#1C1410", frisur="kurz", jacke="#B9463A", jacke_schatten="#9A3A30", zivil=True, funk=False, hose="#2A2A30")

# ---------- Besetzung Folge 1 ----------
DU = Figur("du", haut="hell", haar="#6B4429", frisur="kurz", sommersprossen=True, helm=False)
TRUPPFUEHRER = Figur("truppfuehrer", haut="hell", haar="#2E2018", frisur="seitenscheitel", bart="schnurrbart",
                     jacke="#39432A", jacke_schatten="#2E3622")
KOLLEGE = Figur("kollege", haut="mittel", haar="#1E1612", frisur="kurz", bart="stoppeln")

if __name__ == "__main__":
    import sys, pathlib
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    out.mkdir(parents=True, exist_ok=True)
    for name, fig in EINHEITEN_FIGUREN.items():
        (out / f"einheit_{fig.name}.svg").write_text(svg_ganz(fig, "entschlossen"))
    for fig in (ZIVIL_M, ZIVIL_F, ZIVIL_K):
        for e in ("angst", "erleichtert", "schock"):
            (out / f"{fig.name}_{e}_ganz.svg").write_text(svg_ganz(fig, e))
    (out / "truppfuehrer_erleichtert_funk.svg").write_text(svg(TRUPPFUEHRER, "erleichtert", arm="funk"))
    (out / "truppfuehrer_entschlossen_zeigen.svg").write_text(svg(TRUPPFUEHRER, "entschlossen", arm="zeigen"))
    for fig in (DU, TRUPPFUEHRER, KOLLEGE):
        for e in ("neutral", "angst", "entschlossen", "erleichtert", "schreien", "seitenblick"):
            (out / f"{fig.name}_{e}.svg").write_text(svg(fig, e, arm="funk" if fig is TRUPPFUEHRER and e == "entschlossen" else "unten"))
    print("ok")
