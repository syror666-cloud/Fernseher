"""Low-Poly-Favela am Hang bei Nacht (CODE ROT Folge 3).

Gelände: Straße unten (y -18..-5), Hang steigt mit h(y)=0.38*(y+4) nach +y.
Hauptgasse mit Treppen bei x≈1, zweite Treppengasse bei x≈-6. Haus mit blauer Tür: Front bei y=37, x≈6.
blender -b -P scene_favela.py -- --pfad p.json --out f_#### [--zeit nacht|daemmerung|morgen]
       [--caveirao fahrt|steht|ab] [--junge ja|winkt] [--tuer zu|offen]
"""
import bpy, math, random, sys, argparse, os
from mathutils import Vector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import anim_common
from anim_common import Masse

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--out", default="/tmp/favela_####")
ap.add_argument("--res", default="540x960")
ap.add_argument("--samples", type=int, default=6)
ap.add_argument("--engine", default="eevee")
ap.add_argument("--pfad", default="")
ap.add_argument("--zeit", default="nacht")
ap.add_argument("--caveirao", default="")
ap.add_argument("--junge", default="")
ap.add_argument("--tuer", default="zu")
args = ap.parse_args(argv)
random.seed(19)
bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene
MORGEN = args.zeit == "morgen"; DAEMM = args.zeit == "daemmerung"
NACHT = not (MORGEN or DAEMM)


def H(y):
    return 0.38 * (y + 4) if y > -4 else 0.0


def mat(name, color, rough=0.85, emit=None, strength=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = strength
    return m


def cube(loc, scale, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object; o.scale = scale; o.data.materials.append(m); return o


WAND_FARBEN = [(0.55, 0.24, 0.12), (0.5, 0.22, 0.11), (0.6, 0.3, 0.16), (0.62, 0.6, 0.55), (0.75, 0.62, 0.35),
               (0.35, 0.55, 0.6), (0.7, 0.4, 0.45), (0.45, 0.58, 0.35), (0.8, 0.78, 0.7), (0.55, 0.24, 0.12)]
WAENDE = [Masse(f"waende{i}", mat(f"wand{i}", c)) for i, c in enumerate(WAND_FARBEN)]
DACH = Masse("daecher", mat("dach", (0.3, 0.3, 0.31), 0.9))
TANK = Masse("wassertanks", mat("tank", (0.08, 0.22, 0.55), 0.5))
FENSTER_AN = Masse("fenster_an", mat("fenster_an", (0.1, 0.08, 0.05), 0.4, emit=(1.0, 0.7, 0.35), strength=4.0 if NACHT else 1.0))
FENSTER_AUS = Masse("fenster_aus", mat("fenster_aus", (0.02, 0.02, 0.025), 0.3))
TREPPE = Masse("treppen", mat("beton", (0.42, 0.41, 0.4), 0.9))
EISEN = Masse("eisen", mat("eisen", (0.12, 0.1, 0.09), 0.7))
WAESCHE = [Masse(f"waesche{i}", mat(f"waesche{i}", c, 0.9)) for i, c in
           enumerate([(0.8, 0.1, 0.1), (0.95, 0.85, 0.2), (0.1, 0.4, 0.8), (0.9, 0.9, 0.9), (0.2, 0.6, 0.3)])]
M_BODEN = mat("hang", (0.25, 0.18, 0.12), 1.0)
M_STRASSE = mat("asphalt", (0.07, 0.07, 0.075), 0.9)

# ---------- Gelände ----------
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
hang = bpy.context.object; hang.scale = (400, 400, 1); hang.data.materials.append(M_BODEN)
bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.subdivide(number_cuts=100); bpy.ops.object.mode_set(mode="OBJECT")
for v in hang.data.vertices:
    wy = v.co.y * 400
    v.co.z = H(wy) / 1.0 if wy < 120 else H(120) + (wy - 120) * 0.1
cube((0, -11.5, 0.02), (200, 6.5, 0.02), M_STRASSE)

# ---------- Häuser ----------
GASSEN = [(-1.2, 3.2), (-8.0, -4.2)]
PLATZ = (3.4, 9.0, 29.0, 37.0)  # x0,x1,y0,y1 frei vor dem Haus mit blauer Tür


def frei(x0, x1, y0, y1):
    for a, b in GASSEN:
        if x1 > a and x0 < b:
            return False
    if x1 > PLATZ[0] and x0 < PLATZ[1] and y1 > PLATZ[2] and y0 < PLATZ[3]:
        return False
    if x1 > 3.4 and x0 < 9.0 and y1 > 36.8 and y0 < 42.5:  # das Türhaus selbst
        return False
    return True


fenster_liste = []
y = -3.5
while y < 115:
    x = -70
    tiefe = random.uniform(4.5, 6.5)
    while x < 70:
        breite = random.uniform(3.6, 6.5)
        if frei(x, x + breite, y, y + tiefe) and random.random() < 0.93:
            stock = random.choice([1, 2, 2, 2, 3, 3, 4])
            hoehe = stock * 2.9
            g = H(y + tiefe / 2) - 1.2
            cx, cy, cz = x + breite / 2, y + tiefe / 2, g + hoehe / 2 + 0.6
            random.choice(WAENDE).quader((cx, cy, cz), (breite / 2 - 0.05, tiefe / 2 - 0.05, hoehe / 2 + 0.6))
            DACH.quader((cx, cy, g + hoehe + 1.25), (breite / 2, tiefe / 2, 0.08))
            if random.random() < 0.45:
                TANK.zylinder((cx + random.uniform(-1, 1), cy + random.uniform(-1, 1), g + hoehe + 1.85), 0.55, 1.1, verts=10)
            if random.random() < 0.4:
                for k in range(4):
                    EISEN.zylinder((x + 0.3 + k * (breite - 0.6) / 3, y + 0.3, g + hoehe + 1.8), 0.03, 1.2, verts=4)
            for s_ in range(stock):  # Fenster auf der Vorderseite (-y) und zur Gasse
                for fx in range(max(1, int(breite // 2.2))):
                    px = x + 1.1 + fx * 2.2
                    pz = g + 1.9 + s_ * 2.9
                    (FENSTER_AN if random.random() < (0.35 if NACHT else 0.08) else FENSTER_AUS).quader((px, y - 0.02, pz), (0.45, 0.04, 0.55))
                    if random.random() < 0.08 and NACHT:
                        fenster_liste.append((px, y - 0.6, pz))
            # Fenster zur Gasse
            for a, b in GASSEN:
                if abs(x - b) < 0.5 or abs(x + breite - a) < 0.5:
                    sx = x + 0.02 if abs(x - b) < 0.5 else x + breite - 0.02
                    for s_ in range(stock):
                        (FENSTER_AN if random.random() < 0.4 else FENSTER_AUS).quader((sx, cy, g + 1.9 + s_ * 2.9), (0.04, 0.45, 0.55))
        x += breite + random.uniform(0.0, 0.5)
    y += tiefe + random.uniform(0.2, 1.2)

# Treppen in den Gassen
for a, b in GASSEN:
    yy = -4.0
    while yy < 112:
        TREPPE.quader(((a + b) / 2, yy, H(yy) - 0.15), ((b - a) / 2, 0.16, 0.18))
        yy += 0.42
# Wäscheleinen über der Hauptgasse
for i in range(9):
    yy = 4 + i * 7.5
    z = H(yy) + random.uniform(3.2, 4.2)
    for k in range(5):
        random.choice(WAESCHE).quader((-0.8 + k * 0.8, yy, z - 0.35), (0.25, 0.02, 0.33))
for m in WAENDE + [DACH, TANK, FENSTER_AN, FENSTER_AUS, TREPPE, EISEN] + WAESCHE:
    m.fertig()

# Stromkabel (Kettenlinien) über den Gassen
M_KABEL = mat("kabel", (0.01, 0.01, 0.01), 0.6)
for i in range(70):
    yy = random.uniform(-2, 70)
    x0 = random.choice([-1.4, -8.2, 3.4]); x1 = x0 + random.uniform(3.5, 6) * random.choice([-1, 1])
    z0 = H(yy) + random.uniform(3.5, 6.5)
    cd = bpy.data.curves.new("kabel", "CURVE"); cd.dimensions = "3D"; cd.bevel_depth = 0.025
    sp = cd.splines.new("POLY"); n = 8; sp.points.add(n - 1)
    dy = random.uniform(-3, 3)
    for k in range(n):
        u = k / (n - 1)
        sp.points[k].co = (x0 + (x1 - x0) * u, yy + dy * u, z0 - 0.9 * math.sin(math.pi * u), 1)
    o = bpy.data.objects.new("kabel", cd); scn.collection.objects.link(o); o.data.materials.append(M_KABEL)

# Straßenlaternen (Natriumdampf)
M_BIRNE = mat("birne", (1, 0.6, 0.2), 0.3, emit=(1.0, 0.55, 0.15), strength=40)
for a, b in GASSEN:
    for yy in range(-2, 90, 9):
        cube(((a + b) / 2 + 1.6, yy, H(yy) + 4.2), (0.15, 0.15, 0.1), M_BIRNE)
        bpy.ops.object.light_add(type="POINT", location=((a + b) / 2 + 1.2, yy, H(yy) + 3.9))
        l = bpy.context.object; l.data.energy = 260 if not MORGEN else 40; l.data.color = (1.0, 0.55, 0.2)
for xx in range(-60, 61, 15):
    cube((xx, -5.6, 5.5), (0.12, 0.12, 5.5), mat("mast", (0.1, 0.1, 0.1)))
    cube((xx, -6.6, 10.8), (0.3, 1.0, 0.12), M_BIRNE)
    bpy.ops.object.light_add(type="SPOT", location=(xx, -7.4, 10.6)); l = bpy.context.object
    l.data.energy = 3000 if not MORGEN else 300; l.data.color = (1.0, 0.55, 0.2); l.data.spot_size = 1.3

# ---------- Haus mit blauer Tür (Front bei y=37) ----------
g0 = H(39.5) - 1.2 + 0.0
fl = H(42.5) + 0.05  # Fußboden (über dem Gelände)
M_WANDT = mat("wand_tuerhaus", (0.45, 0.62, 0.52), 0.9)
M_BLAU = mat("blaue_tuer", (0.05, 0.25, 0.75), 0.6)
cube((4.0, 39.5, fl + 1.5), (0.6, 2.6, 2.1), M_WANDT)      # links
cube((8.6, 39.5, fl + 1.5), (0.4, 2.6, 2.1), M_WANDT)      # rechts
cube((6.3, 42.2, fl + 1.5), (2.7, 0.1, 2.1), M_WANDT)      # hinten
cube((4.95, 37.0, fl + 1.5), (0.55, 0.1, 2.1), M_WANDT)    # Front links der Tür
cube((7.75, 37.0, fl + 1.5), (1.25, 0.1, 2.1), M_WANDT)    # Front rechts
cube((6.0, 37.0, fl + 3.25), (0.6, 0.1, 0.35), M_WANDT)    # Sturz
cube((6.3, 39.5, fl + 3.65), (2.8, 2.8, 0.08), mat("dach2", (0.3, 0.3, 0.31)))
cube((6.3, 39.5, fl - 0.02), (2.7, 2.6, 0.04), mat("fliesen", (0.55, 0.5, 0.45), 0.6))
if args.tuer == "offen":
    cube((5.45, 36.5, fl + 1.1), (0.05, 0.55, 1.05), M_BLAU, rot=(0, 0, 0.3))
else:
    cube((6.0, 37.0, fl + 1.1), (0.55, 0.05, 1.05), M_BLAU)
for k in range(6):  # Stufen zur Tür
    cube((6.0, 36.2 - k * 0.45, fl - 0.2 - k * 0.38), (0.9, 0.25, 0.2), mat("stufe", (0.42, 0.41, 0.4)))
M_HOLZ = mat("holz", (0.35, 0.2, 0.1), 0.8)
cube((7.0, 40.6, fl + 0.75), (0.8, 0.5, 0.04), M_HOLZ)         # Tisch
for dx in (-0.7, 0.7):
    for dy in (-0.4, 0.4):
        cube((7.0 + dx, 40.6 + dy, fl + 0.37), (0.04, 0.04, 0.37), M_HOLZ)
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.06, depth=0.11, location=(6.8, 40.4, fl + 0.85))
bpy.context.object.data.materials.append(mat("tasse", (0.9, 0.9, 0.88), 0.4))
bpy.ops.object.light_add(type="POINT", location=(6.5, 40, fl + 3.0)); l = bpy.context.object
l.data.energy = 90; l.data.color = (1, 0.8, 0.55)
cube((5.0, 41.6, fl + 1.2), (0.8, 0.4, 0.5), mat("fernsehschrank", (0.2, 0.15, 0.1)))
cube((5.0, 41.6, fl + 1.95), (0.45, 0.25, 0.3), mat("tv_an", (0.1, 0.12, 0.15), 0.3, emit=(0.5, 0.6, 0.8), strength=3))

# ---------- Junge auf dem Dach ----------
if args.junge:
    M_KIND = mat("kind_shirt", (0.9, 0.3, 0.1)); M_HAUT = mat("kind_haut", (0.45, 0.28, 0.18))
    jx, jy = 4.6, 22.0; jz = H(jy) + 8.0
    cube((jx, jy, jz + 0.55), (0.18, 0.12, 0.3), M_KIND)
    cube((jx - 0.08, jy, jz + 0.12), (0.06, 0.08, 0.22), mat("hose", (0.1, 0.1, 0.25)))
    cube((jx + 0.08, jy, jz + 0.12), (0.06, 0.08, 0.22), mat("hose2", (0.1, 0.1, 0.25)))
    bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=6, radius=0.15, location=(jx, jy, jz + 1.0))
    bpy.context.object.data.materials.append(M_HAUT)
    arm = cube((jx + 0.24, jy, jz + 0.9 if args.junge == "winkt" else jz + 0.55), (0.05, 0.05, 0.25), M_KIND)
    if args.junge == "winkt":
        arm.rotation_euler = (0, 0.3, 0); anim_arm = arm
    # Dachfläche darunter sicherstellen
    cube((jx, jy, jz - 0.06), (2.5, 2.5, 0.08), mat("dachjunge", (0.3, 0.3, 0.31)))

# ---------- Caveirão (schwarzer Panzerwagen, ohne Emblem) ----------
cav = None
if args.caveirao:
    M_CAV = mat("caveirao", (0.03, 0.03, 0.035), 0.5)
    cav = bpy.data.objects.new("caveirao", None); scn.collection.objects.link(cav)
    teile = [((0, 0, 1.6), (3.4, 1.3, 1.0)), ((2.9, 0, 1.0), (0.8, 1.25, 0.55)), ((0, 0, 2.7), (3.2, 1.2, 0.12))]
    for loc, sc in teile:
        o = cube(loc, sc, M_CAV); o.parent = cav
    o = cube((3.7, 0, 1.7), (0.05, 1.1, 0.5), M_CAV, rot=(0, -0.6, 0)); o.parent = cav
    for side in (-1, 1):
        for i in range(4):
            o = cube((-2.2 + i * 1.3, side * 1.31, 2.0), (0.25, 0.02, 0.05), mat("schlitz", (0.0, 0.0, 0.0), 0.2)); o.parent = cav
        for dx in (2.4, 0.4, -2.2):
            bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.6, depth=0.4, location=(dx, side * 1.25, 0.6), rotation=(math.pi / 2, 0, 0))
            w_ = bpy.context.object; w_.data.materials.append(mat("reifen", (0.02, 0.02, 0.02))); w_.parent = cav
    for dy in (-0.8, 0.8):
        o = cube((3.72, dy, 1.1), (0.03, 0.15, 0.1), mat("cav_licht", (1, 1, 0.9), 0.3, emit=(1, 0.92, 0.75), strength=30)); o.parent = cav
    bpy.ops.object.light_add(type="SPOT", location=(4.0, 0, 1.2)); hl = bpy.context.object
    hl.data.energy = 6000; hl.data.spot_size = 0.9; hl.rotation_euler = (0, math.radians(95), 0); hl.parent = cav
    cav.location = (0, -10, 0)
    bpy.ops.object.light_add(type="POINT", location=(2.5, -15, 5)); kl = bpy.context.object
    kl.data.energy = 900; kl.data.color = (1.0, 0.6, 0.3)

# ---------- Himmel, Licht ----------
world = bpy.data.worlds.new("w"); scn.world = world; world.use_nodes = True
wn = world.node_tree.nodes; wl = world.node_tree.links; bg = wn["Background"]
tc = wn.new("ShaderNodeTexCoord"); sep = wn.new("ShaderNodeSeparateXYZ"); ramp = wn.new("ShaderNodeValToRGB")
wl.new(tc.outputs["Normal"], sep.inputs["Vector"]); wl.new(sep.outputs["Z"], ramp.inputs["Fac"]); wl.new(ramp.outputs["Color"], bg.inputs["Color"])
if MORGEN:
    ramp.color_ramp.elements[0].color = (0.95, 0.6, 0.4, 1); ramp.color_ramp.elements[1].color = (0.35, 0.45, 0.7, 1)
    ramp.color_ramp.elements[1].position = 0.5; bg.inputs["Strength"].default_value = 1.1
    bpy.ops.object.light_add(type="SUN", rotation=(math.radians(78), 0, math.radians(-150))); s = bpy.context.object
    s.data.energy = 2.2; s.data.color = (1, 0.75, 0.55)
elif DAEMM:
    ramp.color_ramp.elements[0].color = (0.5, 0.35, 0.45, 1); ramp.color_ramp.elements[1].color = (0.06, 0.07, 0.18, 1)
    ramp.color_ramp.elements[1].position = 0.4; bg.inputs["Strength"].default_value = 1.0
    bpy.ops.object.light_add(type="SUN", rotation=(math.radians(84), 0, math.radians(-150))); s = bpy.context.object
    s.data.energy = 0.6; s.data.color = (0.9, 0.6, 0.7)
else:
    ramp.color_ramp.elements[0].color = (0.05, 0.06, 0.14, 1); ramp.color_ramp.elements[1].color = (0.005, 0.007, 0.025, 1)
    ramp.color_ramp.elements[1].position = 0.45; bg.inputs["Strength"].default_value = 1.1
    bpy.ops.object.light_add(type="SUN", rotation=(math.radians(55), 0, math.radians(160))); s = bpy.context.object
    s.data.energy = 0.25; s.data.color = (0.6, 0.7, 1.0)
    M_STERN = mat("stern", (1, 1, 1), 1, emit=(0.9, 0.95, 1), strength=20)
    for i in range(150):
        a = random.uniform(0, math.tau); el = random.uniform(0.15, 1.2)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=random.uniform(0.5, 1.2),
                                              location=Vector((math.cos(a) * math.cos(el), math.sin(a) * math.cos(el), math.sin(el))) * 700)
        bpy.context.object.data.materials.append(M_STERN)
bpy.ops.object.light_add(type="AREA", location=(0, 20, 60)); fill = bpy.context.object
fill.data.energy = 6000 if NACHT else 2000; fill.data.size = 120; fill.data.color = (0.45, 0.5, 0.8) if NACHT else (1, 0.85, 0.75)

# ---------- Kamera + Animation ----------
bpy.ops.object.camera_add(); cam = bpy.context.object; scn.camera = cam; cam.data.clip_end = 2000
w, h = map(int, args.res.split("x")); scn.render.resolution_x, scn.render.resolution_y = w, h
anim_common.engine(scn, args.engine, args.samples)
n, off = anim_common.kamerapfad(scn, cam, args.pfad)
N = n + off + 1
if cav is not None:
    if args.caveirao == "fahrt":
        cav.location = (-24, -10, 0); cav.keyframe_insert("location", frame=1)
        cav.location = (-2, -10, 0); cav.keyframe_insert("location", frame=N)
    elif args.caveirao == "ab":
        cav.location = (0, -10, 0); cav.keyframe_insert("location", frame=1)
        cav.location = (-40, -10, 0); cav.keyframe_insert("location", frame=N)
        cav.rotation_euler = (0, 0, math.pi)
    for f in range(1, N + 1, 3):  # Motor-Vibration
        cav.rotation_euler.x = 0.004 * math.sin(f * 2.1); cav.keyframe_insert("rotation_euler", frame=f)
if args.junge == "winkt":
    for f in range(1, N + 1, 2):
        anim_arm.rotation_euler = (0, 0.3 + 0.5 * math.sin(f / 30 * 9), 0); anim_arm.keyframe_insert("rotation_euler", frame=f)
scn.render.filepath = args.out
bpy.ops.render.render(animation=True)
print("FERTIG_ANIM", args.out, n)
