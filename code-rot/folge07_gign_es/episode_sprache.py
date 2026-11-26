"""Folge 7 GIGN (Spanisch, Lateinamerika) – nur Sprechtext für vo.py/stimmen.py (Bildteil liegt auf dem PC in episode.py)."""
SPRACHE = "es"
STIMME = "w7IU2bIH6xHcyfkUUWi3"  # Santiago – neutral lateinamerikanisch, natürlich
MODELL = "eleven_v3"  # lebendiger, mit Regieanweisungen (regie="[whispers]" …), Tags nicht im Timing
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
    S("", titel="*GIGN*", titel_sprich="[shouting] ¡G-I-G-N!", pause=1.5),
    S("Eres del *GIGN*.", sprich="Eres del G. I. G. N.", regie="[excited]"),
    S("Cuatro secuestradores. Un *Airbus* lleno de gente."),
    S("Quieren ir a *París*."),
    S("Y exigen *27 toneladas* de combustible.", sprich="Y exigen veintisiete toneladas de combustible."),
    S("Recuerda ese número.", regie="[whispers]"),
    S("La toman en *Argel*, en Nochebuena."),
    S("Disfrazados de *policías*."),
    S("Ya mataron a *tres* rehenes."),
    S("A bordo: *dinamita*."),
    S("Ustedes entrenan en un avión *gemelo*."),
    S("Luego aterriza en *Marsella*."),
    S("El tanque está casi vacío."),
    S("Y *nadie* les trae combustible."),
    S("Tu comandante solo dice:"),
    S("“Ese avión *no* vuelve a despegar.”", stimme="chef"),
    S("Tus órdenes:"),
    S("*Tres* escaleras."),
    S("Tres puertas *a la vez*."),
    S("Cuidado, *dinamita*."),
    S("Y: *pasajeros* afuera."),
    S("*17:12*.", sprich="Las diecisiete doce.", regie="[tense]"),
    S("Las escaleras arrancan."),
    S("La tuya queda *muy alta*."),
    S("La puerta *no* abre."),
    S("Atrás. Y otra vez."),
    S("Por fin, *adentro*."),
    S("Disparos desde la *cabina de mando*.", regie="[excited]"),
    S("Más de *mil* disparos."),
    S("Vuela una *granada*."),
    S("El copiloto salta por la *ventana*."),
    S("Atrás, los rehenes bajan por los toboganes."),
    S("Cae el último secuestrador."),
    S("*Ningún* pasajero muere en el asalto."),
    S("Lo lograste.", regie="[relieved]"),
    S("¿Pero recuerdas las *27 toneladas*?", sprich="¿Pero recuerdas las veintisiete toneladas?", regie="[whispers]"),
    S("Hasta París bastaban unas *ocho*."),
    S("¿Para qué el *resto*?"),
    S("Los investigadores *sospechaban* algo."),
    S("El avión mismo sería la *bomba*.", regie="[tense]"),
    S("Sobre París. Quizá en la *Torre Eiffel*."),
    S("Casi *siete* años antes del 11 de septiembre.", sprich="Casi siete años antes del once de septiembre."),
    S("¿Y mañana?"),
    S("Vendrá *otra*."),
]
