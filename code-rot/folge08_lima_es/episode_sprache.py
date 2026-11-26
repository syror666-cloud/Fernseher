"""Folge 8 Lima (Chavín de Huántar) (Spanisch, Lateinamerika) – nur Sprechtext für vo.py/stimmen.py (Bildteil liegt auf dem PC in episode.py)."""
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
    S("", titel="*CHAVÍN*", titel_sprich="[shouting] ¡Chavín!", pause=1.5),
    S("Eres comando en *Perú*.", regie="[excited]"),
    S("*14* rebeldes. *72* rehenes.", sprich="Catorce rebeldes. Setenta y dos rehenes."),
    S("Llevan cuatro meses en esta residencia."),
    S("Y cada tarde cometen *el mismo* error."),
    S("Recuérdalo.", regie="[whispers]"),
    S("Todo empezó en una *fiesta*."),
    S("En casa del embajador de Japón."),
    S("Llegaron en una *ambulancia*."),
    S("Y volaron el *muro*."),
    S("Ustedes no pueden entrar por la puerta."),
    S("Así que llaman a *mineros*."),
    S("Cavan *túneles* hasta debajo de la casa."),
    S("De día suenan *marchas militares*."),
    S("Para que nadie *sospeche*."),
    S("Construyen una *réplica* y ensayan."),
    S("*Micrófonos* ocultos escuchan todo."),
    S("Tu comandante solo dice:"),
    S("“Esperamos el *balón*.”", stimme="chef"),
    S("Tus órdenes:"),
    S("Ni un *ruido*."),
    S("*72* vidas.", sprich="Setenta y dos vidas."),
    S("Todos los túneles *a la vez*."),
    S("Y: espera la *señal*."),
    S("Día *126*.", sprich="Día ciento veintiséis."),
    S("*15:23*.", sprich="Las quince veintitrés."),
    S("Están en el *túnel*.", regie="[whispers]"),
    S("Arriba: *pasos*. Gritos.", regie="[whispers]"),
    S("“*¡Ahora!*”", stimme="funk"),
    S("El piso *explota*.", regie="[excited]"),
    S("Suben desde *abajo*."),
    S("*148* soldados.", sprich="Ciento cuarenta y ocho soldados."),
    S("Humo. *Disparos*."),
    S("Los rehenes salen a rastras."),
    S("Un oficial cubre a un *ministro* con su cuerpo."),
    S("El oficial *muere*."),
    S("*71* rehenes sobreviven.", sprich="Setenta y un rehenes sobreviven."),
    S("Lo lograste.", regie="[relieved]"),
    S("¿Y el *error*?", regie="[whispers]"),
    S("Cada tarde jugaban *fútbol* adentro."),
    S("Justo encima de su *túnel*."),
    S("Solo esperaban el *pitazo inicial*."),
    S("Hasta hoy se discute"),
    S("si *algunos* ya se habían rendido."),
    S("El nombre de la operación: un templo lleno de *túneles*."),
    S("*Chavín de Huántar*.", sprich="Chavín de Huántar."),
    S("¿Y mañana?"),
    S("Vendrá *otra*."),
]
