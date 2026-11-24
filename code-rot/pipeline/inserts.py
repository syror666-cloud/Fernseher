"""2D-Inserts im Serienstil (SVG, 1080x1920): POV-Hände, Silhouetten, Fernseher, Trage."""

HANDSCHUH, HANDSCHUH_S, AERMEL = "#1C1D1F", "#111214", "#3F4A2E"


def _svg(body, w=1080, h=1920):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{body}</svg>'


def hand_funk(led=True):
    """POV: behandschuhte Hand hält Funkgerät vor das Gesicht."""
    b = [
        f'<path d="M640,1920 L760,1380 Q790,1300 870,1320 L1080,1400 L1080,1920 Z" fill="{AERMEL}"/>',
        f'<path d="M700,1920 L790,1420 Q800,1360 860,1370 L1080,1440 L1080,1920 Z" fill="#000" opacity=".15"/>',
        '<rect x="420" y="760" width="300" height="640" rx="46" fill="#151618"/>',
        '<rect x="452" y="800" width="236" height="200" rx="22" fill="#26292C"/>',
        f'<rect x="478" y="830" width="184" height="120" rx="12" fill="{"#3C5A3A" if led else "#1E2A1E"}"/>',
        '<text x="570" y="908" font-family="monospace" font-size="56" fill="#9CE29A" text-anchor="middle">CH 2</text>' if led else "",
        '<rect x="600" y="520" width="44" height="260" rx="20" fill="#0F1011"/>',
        '<circle cx="490" cy="1060" r="20" fill="#C0392B"/>' if led else '<circle cx="490" cy="1060" r="20" fill="#5A1A14"/>',
        *[f'<rect x="470" y="{1110 + i*34}" width="200" height="12" rx="6" fill="#0C0D0E"/>' for i in range(7)],
        f'<path d="M700,1460 Q610,1430 560,1340 L540,1200 Q560,1150 620,1160 L700,1180 Q780,1150 800,1240 L820,1420 Z" fill="{HANDSCHUH}"/>',
        *[f'<rect x="{380 + i*6}" y="{980 + i*110}" width="140" height="92" rx="40" fill="{HANDSCHUH if i%2==0 else HANDSCHUH_S}"/>' for i in range(4)],
        '<rect x="660" y="930" width="110" height="250" rx="48" fill="#1C1D1F"/>',
    ]
    return _svg("".join(b))


def hand_leiter():
    """POV: zwei Hände greifen eine mit Gummi umwickelte Leiter, Blick nach oben."""
    b = ['<path d="M300,-40 L420,1960" stroke="#0E0E0E" stroke-width="54"/>',
         '<path d="M780,-40 L660,1960" stroke="#0E0E0E" stroke-width="54"/>']
    for i in range(8):
        y = 120 + i * 250
        x1 = 300 + (y + 40) / 2000 * 120 + 20
        x2 = 780 - (y + 40) / 2000 * 120 - 20
        b.append(f'<rect x="{x1}" y="{y}" width="{x2-x1}" height="44" rx="10" fill="#141414"/>')
        b.append(f'<rect x="{x1+40}" y="{y-6}" width="{x2-x1-80}" height="56" rx="14" fill="#2A2A2A"/>')
    for s, x in ((-1, 330), (1, 750)):
        b.append(f'<path d="M{x - s*260},1960 L{x - s*60},1240 L{x + s*70},1260 L{x + s*10},1960 Z" fill="{AERMEL}"/>')
        b.append(f'<ellipse cx="{x}" cy="1140" rx="120" ry="100" fill="{HANDSCHUH}"/>')
        for k in range(4):
            b.append(f'<rect x="{x - 110 + k*58}" y="1000" width="50" height="120" rx="24" fill="{HANDSCHUH if k%2 else HANDSCHUH_S}"/>')
    return _svg("".join(b))


def fenster_silhouette(anzahl=1, licht="#F2B26B"):
    """Nahaufnahme Flugzeugfenster von außen, dahinter Schatten."""
    b = ['<rect width="1080" height="1920" fill="#C9CCD2"/>',
         '<rect y="0" width="1080" height="1920" fill="url(#rumpf)"/>',
         '<defs><linearGradient id="rumpf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B0E16" stop-opacity=".85"/>'
         '<stop offset=".5" stop-color="#2A3040" stop-opacity=".35"/><stop offset="1" stop-color="#05070C" stop-opacity=".9"/></linearGradient>'
         f'<radialGradient id="glow"><stop offset="0" stop-color="{licht}"/><stop offset="1" stop-color="#7A3A10"/></radialGradient></defs>',
         '<rect y="1240" width="1080" height="90" fill="#0B1A3A"/>']
    xs = [540] if anzahl == 1 else [260, 820]
    for k, x in enumerate(xs):
        b.append(f'<clipPath id="fc{k}"><rect x="{x-160}" y="590" width="320" height="460" rx="130"/></clipPath>')
        b.append(f'<rect x="{x-190}" y="560" width="380" height="520" rx="150" fill="#9AA0AA"/>')
        b.append(f'<rect x="{x-160}" y="590" width="320" height="460" rx="130" fill="url(#glow)"/>')
        b.append(f'<g clip-path="url(#fc{k})">')
        # Kopf + Schultern im Gegenlicht
        b.append(f'<g class="rig-silhouette"><path d="M{x-150},1050 Q{x-140},900 {x-60},880 Q{x-110},800 {x-70},730 Q{x},670 {x+70},730 '
                 f'Q{x+110},800 {x+60},880 Q{x+140},900 {x+150},1050 Z" fill="#0A0806"/></g></g>')
    b.append('<rect width="1080" height="1920" fill="#0A1230" opacity=".25"/>')
    return _svg("".join(b))


def tv(text_oben="SONDERSENDUNG", text_unten="MÜNCHEN · 1972", rauschen=True):
    """Alter Röhrenfernseher mit Rauschen und Laufschrift."""
    b = ['<defs><filter id="n"><feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="2" seed="4"/>'
         '<feColorMatrix type="saturate" values="0"/></filter>'
         '<clipPath id="bild"><rect x="190" y="700" width="700" height="540" rx="70"/></clipPath></defs>',
         '<rect width="1080" height="1920" fill="#141310"/>',
         '<rect x="120" y="620" width="840" height="700" rx="60" fill="#5B4632"/>',
         '<rect x="150" y="650" width="780" height="640" rx="50" fill="#3E2F22"/>',
         '<rect x="190" y="700" width="700" height="540" rx="70" fill="#7C8078"/>']
    if rauschen:
        b.append('<g clip-path="url(#bild)"><g class="rig-tvbild"><rect x="190" y="660" width="700" height="620" filter="url(#n)" opacity=".75"/></g></g>')
    b += ['<rect x="190" y="700" width="700" height="540" rx="70" fill="#C8CFC0" opacity=".18"/>',
          f'<rect x="240" y="1110" width="600" height="90" fill="#101010" opacity=".85" clip-path="url(#bild)"/>',
          f'<text x="540" y="1172" font-family="MB" font-size="54" fill="#F2F2F2" text-anchor="middle">{text_unten}</text>',
          f'<text x="540" y="790" font-family="MB" font-size="40" fill="#F2F2F2" text-anchor="middle" opacity=".9">{text_oben}</text>',
          '<rect x="300" y="1320" width="60" height="120" fill="#2B2118"/><rect x="720" y="1320" width="60" height="120" fill="#2B2118"/>',
          '<line x1="430" y1="620" x2="300" y2="380" stroke="#222" stroke-width="10"/><line x1="650" y1="620" x2="800" y2="400" stroke="#222" stroke-width="10"/>']
    return _svg("".join(b))


def trage():
    """Zwei Helfer tragen eine Trage (Silhouetten, Person unter Decke)."""
    b = ['<g fill="#07080B">']
    for x in (210, 870):
        b.append(f'<circle cx="{x}" cy="980" r="62"/><path d="M{x-80},1060 Q{x},1030 {x+80},1060 L{x+70},1400 L{x-70},1400 Z"/>'
                 f'<rect x="{x-60}" y="1390" width="50" height="260" rx="20"/><rect x="{x+10}" y="1390" width="50" height="260" rx="20"/>')
    b.append('<rect x="200" y="1180" width="680" height="26" rx="10"/>')
    b.append('</g>')
    b.append('<path d="M290,1180 Q300,1080 420,1090 Q560,1060 700,1100 Q800,1110 800,1180 Z" fill="#C9C9C2"/>')
    b.append('<circle cx="740" cy="1110" r="50" fill="#0E0D0C"/>')
    return _svg("".join(b))


def gericht():
    """Gerichtssaal-Andeutung: Richterpult mit Hammer, Gegenlicht."""
    b = ['<rect width="1080" height="1920" fill="#2A2018"/>',
         '<rect y="0" width="1080" height="900" fill="#3A2C20"/>',
         *[f'<rect x="{80 + i*190}" y="80" width="120" height="700" fill="#4A3828"/>' for i in range(5)],
         '<rect x="100" y="900" width="880" height="520" fill="#5B4430"/>',
         '<rect x="100" y="900" width="880" height="60" fill="#6E5440"/>',
         '<rect x="560" y="820" width="220" height="60" rx="20" fill="#2A1C12" transform="rotate(-18 670 850)"/>',
         '<rect x="640" y="760" width="40" height="200" rx="12" fill="#2A1C12" transform="rotate(-18 670 850)"/>',
         '<rect x="380" y="860" width="220" height="40" rx="12" fill="#2A1C12"/>',
         '<rect width="1080" height="1920" fill="#000" opacity=".25"/>']
    return _svg("".join(b))


def zielfernrohr():
    """Blick durch das Zielfernrohr: schwarze Maske mit rundem Ausschnitt, Fadenkreuz, Mil-Dots."""
    r = 470
    b = ['<defs><mask id="loch"><rect width="1080" height="1920" fill="white"/>'
         f'<circle cx="540" cy="900" r="{r}" fill="black"/></mask>'
         '<radialGradient id="rand"><stop offset=".78" stop-color="#000" stop-opacity="0"/>'
         '<stop offset="1" stop-color="#000" stop-opacity=".85"/></radialGradient></defs>',
         '<rect width="1080" height="1920" fill="#030303" mask="url(#loch)"/>',
         f'<circle cx="540" cy="900" r="{r}" fill="url(#rand)"/>',
         f'<circle cx="540" cy="900" r="{r}" fill="none" stroke="#111" stroke-width="18"/>',
         '<g class="rig-fadenkreuz">',
         f'<line x1="{540-r}" y1="900" x2="{540+r}" y2="900" stroke="#0a0a0a" stroke-width="3"/>',
         f'<line x1="540" y1="{900-r}" x2="540" y2="{900+r}" stroke="#0a0a0a" stroke-width="3"/>',
         f'<line x1="{540-r}" y1="900" x2="440" y2="900" stroke="#0a0a0a" stroke-width="12"/>',
         f'<line x1="640" y1="900" x2="{540+r}" y2="900" stroke="#0a0a0a" stroke-width="12"/>',
         f'<line x1="540" y1="1000" x2="540" y2="{900+r}" stroke="#0a0a0a" stroke-width="12"/>',
         *[f'<circle cx="{540 + d*38}" cy="900" r="5" fill="#0a0a0a"/>' for d in (-4, -3, -2, -1, 1, 2, 3, 4)],
         *[f'<circle cx="540" cy="{900 + d*38}" r="5" fill="#0a0a0a"/>' for d in (-4, -3, -2, -1, 1, 2, 3, 4)],
         '<circle cx="540" cy="900" r="4" fill="#E02020"/>',
         '</g>',
         '<text x="540" y="1460" font-family="MB" font-size="34" fill="#9a9a9a" text-anchor="middle" letter-spacing="6">DIST 0032 M</text>']
    return _svg("".join(b))


def pirat_silhouette():
    """Sitzende Silhouette in einem Schiffsraum, Kopf gesenkt, Gegenlicht (keine Gesichtszüge)."""
    b = ['<defs><radialGradient id="lampe" cx=".5" cy=".25" r=".7"><stop offset="0" stop-color="#E8D9B0" stop-opacity=".55"/>'
         '<stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>',
         '<rect width="1080" height="1920" fill="url(#lampe)"/>',
         '<g class="rig-silhouette" fill="#050506">',
         '<circle cx="540" cy="980" r="95"/>',
         '<path d="M400,1110 Q540,1050 680,1110 L720,1420 L360,1420 Z"/>',
         '<rect x="330" y="1400" width="420" height="60" rx="20"/>',
         '<rect x="380" y="1440" width="70" height="330" rx="25"/><rect x="630" y="1440" width="70" height="330" rx="25"/>',
         '</g>',
         '<rect x="250" y="1780" width="580" height="30" fill="#0a0a0a"/>']
    return _svg("".join(b))


ALLE = {"hand_funk": hand_funk, "hand_leiter": hand_leiter, "fenster1": lambda: fenster_silhouette(1),
        "fenster2": lambda: fenster_silhouette(2), "tv_1972": tv, "tv_rauschen": lambda: tv("", "", True),
        "trage": trage, "gericht": gericht, "zielfernrohr": zielfernrohr, "pirat_silhouette": pirat_silhouette}

if __name__ == "__main__":
    import sys, pathlib
    out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    for k, fn in ALLE.items():
        (out / f"{k}.svg").write_text(fn())
    print("ok", len(ALLE))
