"""Folge 11 Moskau 2002 (Nord-Ost) – Spanisch (Lateinamerika) – nur Sprechtext für vo.py/stimmen.py (Bildteil liegt auf dem PC in episode.py)."""
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
    S("", titel="*ALPHA*", titel_sprich="[shouting] ¡Alfa!", pause=1.5),
    S("Eres del grupo *Alfa*."),
    S("Moscú, octubre de 2002.", sprich="Moscú, octubre de dos mil dos."),
    S("Un *teatro* lleno. Un musical."),
    S("De pronto, hombres armados toman el *escenario*."),
    S("Más de *850* rehenes.", sprich="Más de ochocientos cincuenta rehenes."),
    S("Unos *40* atacantes. Explosivos en el *cuerpo*.", sprich="Unos cuarenta atacantes. Explosivos en el cuerpo."),
    S("Si entran, lo vuelan *todo*."),
    S("¿Cómo salvas a *850* personas a la vez?", sprich="¿Cómo salvas a ochocientas cincuenta personas a la vez?"),
    S("Recuerda la pregunta.", regie="[whispers]"),
    S("Casi tres días de negociación."),
    S("La exigencia: que Rusia salga de *Chechenia*."),
    S("Entonces llega la *orden*."),
    S("No por la puerta. Por la *ventilación*."),
    S("Tu comandante dice:"),
    S("“Primero el gas. Luego *ustedes*.”", stimme="chef"),
    S("Tus órdenes:"),
    S("Máscara de gas *puesta*."),
    S("Que nadie *detone* nada."),
    S("Entra cuando haya *silencio*."),
    S("Y: sácalos a *todos*."),
    S("26 de octubre. De madrugada.", sprich="Veintiséis de octubre. De madrugada."),
    S("Un gas entra en la *sala*.", regie="[whispers]"),
    S("La gente se *duerme*."),
    S("También los atacantes."),
    S("Entran.", regie="[tense]"),
    S("Todos los atacantes mueren."),
    S("Al principio dicen: *ningún* rehén muerto."),
    S("Lo lograste."),
    S("Pero afuera…"),
    S("Hay personas en filas sobre la *acera*."),
    S("Los médicos esperan víctimas de balas y *bombas*."),
    S("No de un *gas* secreto."),
    S("Un antídoto podría haber ayudado. Si se daba *enseguida*."),
    S("*73* rehenes no reciben ninguna ayuda.", sprich="Setenta y tres rehenes no reciben ninguna ayuda.", regie="[somber]"),
    S("Al final mueren unos *130* rehenes.", sprich="Al final mueren unos ciento treinta rehenes.", regie="[somber]"),
    S("Casi ninguno por una *bala*."),
    S("Sino por el *gas*."),
    S("¿Qué gas exactamente? Rusia nunca lo ha *revelado* del todo."),
    S("Un tribunal en Estrasburgo dictó: el rescate fue mal *planificado*."),
    S("Más de *700* salvados. Unos *130* muertos.", sprich="Más de setecientos salvados. Unos ciento treinta muertos.", regie="[somber]"),
    S("¿Rescate o *catástrofe*?", regie="[serious]"),
    S("¿Qué habrías hecho *tú*? Escríbelo en los *comentarios*."),
    S("¿Y mañana?"),
    S("Vendrá *otra*."),
]
