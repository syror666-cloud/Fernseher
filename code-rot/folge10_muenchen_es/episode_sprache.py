"""Folge 10 München 1972 – Spanisch (Lateinamerika) – nur Sprechtext für vo.py/stimmen.py (Bildteil liegt auf dem PC in episode.py)."""
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
    S("", titel="*POLIZEI*", titel_sprich="[shouting] ¡POLICÍA!", pause=1.5),
    S("Eres policía en *Múnich*."),
    S("Juegos Olímpicos, *1972*.", sprich="Juegos Olímpicos de mil novecientos setenta y dos."),
    S("Ocho terroristas asaltan el edificio de los *israelíes*."),
    S("Dos miembros del equipo son *asesinados*.", regie="[somber]"),
    S("*Nueve* son tomados como rehenes."),
    S("Y Alemania no tiene *ninguna* unidad especial."),
    S("¿Cómo salvas a nueve personas sin *entrenamiento*?"),
    S("Recuerda la pregunta.", regie="[whispers]"),
    S("Suben a los *tejados*."),
    S("Disfrazados con *chándales*."),
    S("Pero la televisión lo transmite *en directo*."),
    S("Y los terroristas lo están *viendo*."),
    S("La operación se *suspende*."),
    S("Nuevo plan: un *aeródromo*."),
    S("Dos helicópteros los llevan a todos a *Fürstenfeldbruck*."),
    S("Allí espera un avión."),
    S("Dentro: policías disfrazados de *tripulación*."),
    S("Tu jefe dice:"),
    S("“En cuanto suban al avión, *atacamos*.”", stimme="chef"),
    S("Tus órdenes:"),
    S("Espera la *señal*."),
    S("Dispara solo a los *terroristas*."),
    S("No hieras a ningún *rehén*."),
    S("Y: los *nueve* con vida."),
    S("Pero en el avión, los policías *votan*."),
    S("Se *van*. Sin más."),
    S("El avión está *vacío*."),
    S("Ahora solo quedan ustedes. *Cinco* tiradores."),
    S("Sin mira telescópica. Sin *visión nocturna*."),
    S("Creen que son cinco terroristas. Son *ocho*."),
    S("Aterrizan los helicópteros.", regie="[tense]"),
    S("Dos terroristas revisan el avión."),
    S("*Vacío*. Corren de vuelta."),
    S("Entonces suenan los primeros *disparos*.", regie="[tense]"),
    S("¿Los blindados? Atascados en el *tráfico*."),
    S("Poco antes de medianoche, el gobierno anuncia: *éxito*."),
    S("Pero *ningún* rehén sobrevive.", regie="[somber]"),
    S("Y aún hay más."),
    S("Tres terroristas sobreviven."),
    S("Menos de dos meses después, secuestran un *avión*."),
    S("La exigencia: liberar a los *tres*."),
    S("Y Alemania los deja *ir*."),
    S("Después, Alemania crea el *GSG 9*.", sprich="Después, Alemania crea el Ge Ese Ge Nueve."),
    S("¿Pero se pudo *evitar*?", regie="[serious]"),
    S("¿Fracaso o mala suerte? Escríbelo en los *comentarios*."),
    S("¿Y mañana?"),
    S("Vendrá *otra*."),
]
