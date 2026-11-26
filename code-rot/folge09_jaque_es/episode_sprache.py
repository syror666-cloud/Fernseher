"""Folge 9 Operation Jaque (Kolumbien 2008) – Spanisch (Lateinamerika) – nur Sprechtext für vo.py/stimmen.py (Bildteil liegt auf dem PC in episode.py)."""
SPRACHE = "es"
STIMME = "w7IU2bIH6xHcyfkUUWi3"
MODELL = "eleven_v3"  # lebendig, mit Regieanweisungen (regie="[whispers]" …), Tags nicht im Timing
STIMM_EINSTELLUNG = {"stability": 0.5, "similarity_boost": 0.8, "style": 0.45, "use_speaker_boost": True, "speed": 1.0}
# Titelkarte: Einheitenname laut, fast gerufen (eigene Aufnahme)
TITEL_MODELL = "eleven_v3"
TITEL_EINSTELLUNG = {"stability": 0.0, "similarity_boost": 0.8, "style": 0.8, "use_speaker_boost": True, "speed": 1.0}
TITEL_PEGEL = 3.0  # dB über der normalen Erzählerlautstärke


def S(text, **extra):
    return dict(text=text, **extra)


SHOTS = [
    S("Una de estas *unidades*"),
    S("viene por ti esta noche."),
    S("Veamos"),
    S("si *regresas*."),
    S("", titel="*JAQUE*", titel_sprich="[shouting] ¡JAQUE!", pause=1.5),
    S("Eres soldado en *Colombia*.", regie="[excited]"),
    S("*15* rehenes en la selva.", sprich="Quince rehenes en la selva."),
    S("Una de ellas, desde hace más de *seis* años."),
    S("Custodiados por unos *60* guerrilleros.", sprich="Custodiados por unos sesenta guerrilleros."),
    S("¿Cómo sacarlos sin *un solo* disparo?"),
    S("Recuerda la pregunta.", regie="[whispers]"),
    S("Ustedes interceptan su *radio*."),
    S("Conocen sus *códigos*."),
    S("Entonces les envían una *orden*."),
    S("Supuestamente de su propio *jefe*."),
    S("“Lleven a los rehenes a una *misión humanitaria*.”", stimme="funk"),
    S("La misión humanitaria son *ustedes*."),
    S("Pintan dos helicópteros de *blanco*."),
    S("Hasta toman *clases de actuación*."),
    S("Tu comandante solo dice:"),
    S("“Una palabra equivocada y *todos* mueren.”", stimme="chef"),
    S("Tus órdenes:"),
    S("Ni un *disparo*."),
    S("No salgas del *papel*."),
    S("No muestres el *arma*."),
    S("Y: los *15* a bordo.", sprich="Y: los quince a bordo."),
    S("2 de julio de 2008.", sprich="Dos de julio de dos mil ocho."),
    S("Dos helicópteros blancos sobre la *selva*."),
    S("Aterrizan en un *claro*.", regie="[tense]"),
    S("A su alrededor: guerrilleros *armados*."),
    S("Llegan los rehenes."),
    S("Ustedes mismos les ponen *esposas*."),
    S("Para que nadie *sospeche*."),
    S("El jefe también *sube*."),
    S("Se cierra la puerta. Despegan."),
    S("Y entonces, en el aire:", regie="[tense]"),
    S("Dos guerrilleros caen *al suelo*.", regie="[excited]"),
    S("“Somos el Ejército Nacional. ¡Ustedes están en *libertad*!”", stimme="jubel"),
    S("Los rehenes *gritan*. De alegría."),
    S("*Ni un* disparo. *15* libres.", sprich="Ni un disparo. Quince libres."),
    S("Lo lograste.", regie="[relieved]"),
    S("Pero uno de ustedes llevaba un emblema que *jamás* debió usar."),
    S("La *Cruz Roja*."),
    S("En la guerra protege a los *socorristas*."),
    S("Quien lo usa mal pone en riesgo a *todos* ellos."),
    S("El gobierno tuvo que *disculparse*."),
    S("¿Y el nombre *Jaque*?", sprich="¿Y el nombre Jaque?", regie="[whispers]"),
    S("Como en el *ajedrez*."),
    S("Ganaron sin capturar una sola *pieza*."),
    S("¿Y mañana?"),
    S("Vendrá *otra*."),
]
