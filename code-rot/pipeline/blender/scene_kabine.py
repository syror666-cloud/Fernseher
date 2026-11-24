"""Low-Poly-Kabine eines Verkehrsflugzeugs bei Nacht (CODE ROT Folge 1).

Aufruf: blender -b -P scene_kabine.py -- --shot gang --out out.png [--res 864x1536] [--samples 24] [--licht dunkel|zugriff]
Shots: gang (POV im Gang nach vorne), reihe (seitlich auf Sitzreihe), notausstieg (Blick zum offenen Ausstieg)
"""
import bpy, math, random, sys, argparse
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--shot", default="gang")
ap.add_argument("--out", default="/tmp/kabine.png")
ap.add_argument("--res", default="540x960")
ap.add_argument("--samples", type=int, default=24)
ap.add_argument("--licht", default="dunkel")
ap.add_argument("--engine", default="cycles")
ap.add_argument("--pfad", default="")
ap.add_argument("--schuesse", default="", help="Frames mit Mündungsfeuer, z. B. 3,4,9,10")
args = ap.parse_args(argv)
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import anim_common
random.seed(11)
bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene


def mat(name, color, rough=0.8, emit=None, strength=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = strength
    return m


def cube(loc, scale, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object; o.scale = scale; o.data.materials.append(m); return o


M_WALL = mat("wand", (0.55, 0.53, 0.5), 0.7)
M_FLOOR = mat("teppich", (0.08, 0.09, 0.14), 1.0)
M_SEAT = mat("sitz", (0.07, 0.12, 0.28), 0.9)
M_SEATTOP = mat("kopfteil", (0.75, 0.75, 0.72), 0.9)
M_BIN = mat("gepaeck", (0.6, 0.58, 0.55), 0.6)
M_WIN = mat("fenster", (0.01, 0.015, 0.03), 0.2, emit=(0.15, 0.2, 0.4), strength=0.8)
M_EXIT = mat("exitschild", (0.1, 0.4, 0.1), 0.5, emit=(0.2, 1.0, 0.3), strength=6.0)
M_STRIP = mat("bodenlicht", (1, 0.5, 0.2), 0.5, emit=(1.0, 0.45, 0.15), strength=5.0)
SKIN = [mat(f"haut{i}", c, 0.9) for i, c in enumerate([(0.85, 0.62, 0.45), (0.65, 0.42, 0.28), (0.4, 0.25, 0.16)])]
HAIR = [mat(f"haar{i}", c, 0.9) for i, c in enumerate([(0.05, 0.035, 0.025), (0.25, 0.15, 0.07), (0.5, 0.4, 0.25), (0.02, 0.02, 0.02)])]

R, L = 1.9, 26.0
# Rumpf-Innenraum: Boden, Wände, Decke als Polygon-Ring
seg = 14
for i in range(seg):
    a0 = math.pi * 0.12 + i / seg * math.pi * 1.76
    a1 = math.pi * 0.12 + (i + 1) / seg * math.pi * 1.76
    am = (a0 + a1) / 2
    w = 2 * R * math.sin((a1 - a0) / 2)
    pos = Vector((0, math.cos(am) * R, 1.6 + math.sin(am) * R))
    o = cube(pos, (L / 2, w / 2 + 0.02, 0.04), M_WALL, rot=(am + math.pi / 2, 0, 0))
cube((0, 0, 0.0), (L / 2, R, 0.05), M_FLOOR)
# Fenster
for side in (-1, 1):
    for i in range(20):
        x = -L / 2 + 1.5 + i * 1.2
        cube((x, side * (R - 0.25), 2.0), (0.16, 0.03, 0.22), M_WIN, rot=(0, 0, 0))
# Gepäckfächer
for side in (-1, 1):
    cube((0, side * 1.3, 2.75), (L / 2, 0.45, 0.25), M_BIN)
# Sitzreihen 3-3
rows = 20
for r in range(rows):
    x = -L / 2 + 1.5 + r * 1.2
    for side in (-1, 1):
        for k in range(3):
            y = side * (0.55 + k * 0.48)
            cube((x, y, 0.45), (0.25, 0.22, 0.08), M_SEAT)
            cube((x - 0.25, y, 0.85), (0.06, 0.22, 0.42), M_SEAT)
            cube((x - 0.25, y, 1.22), (0.065, 0.2, 0.08), M_SEATTOP)
            if random.random() < 0.8:  # Passagier (geduckt)
                hgt = random.uniform(0.95, 1.12)
                bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.14, location=(x - 0.05, y, hgt))
                h = bpy.context.object; h.data.materials.append(random.choice(SKIN))
                bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.145, location=(x - 0.08, y, hgt + 0.04))
                hh = bpy.context.object; hh.scale = (1, 1, 0.75); hh.data.materials.append(random.choice(HAIR))
                cube((x - 0.05, y, hgt - 0.3), (0.12, 0.17, 0.2), mat(f"kleid{r}{k}{side}", (random.random() * 0.5 + 0.1, random.random() * 0.4 + 0.1, random.random() * 0.4 + 0.1), 0.9))
    cube((x, 0, 0.055), (0.05, 0.03, 0.005), M_STRIP)
cube((L / 2 - 0.5, 0, 2.6), (0.05, 0.3, 0.1), M_EXIT)

# Licht
world = bpy.data.worlds.new("w"); scn.world = world; world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.002, 0.003, 0.008, 1)
if args.licht == "zugriff":
    for x in (-1.2,):
        for side in (-1, 1):
            bpy.ops.object.light_add(type="AREA", location=(x, side * (R - 0.3), 2.0), rotation=(side * math.pi / 2, 0, 0))
            l = bpy.context.object; l.data.energy = 400 if args.engine != "eevee" else 22; l.data.size = 0.8; l.data.color = (0.6, 0.7, 1.0)
    bpy.ops.object.light_add(type="POINT", location=(L / 2 + 1.5, -1.5, 1.5))
    f = bpy.context.object; f.data.energy = 900 if args.engine != "eevee" else 250; f.data.color = (1.0, 0.45, 0.15)
    for i in range(4):
        bpy.ops.object.light_add(type="SPOT", location=(-9 + i * 0.4, 0.3 * (i % 2), 1.9), rotation=(0, -math.pi / 2 + 0.1, 0))
        sp = bpy.context.object; sp.data.energy = 300 if args.engine != "eevee" else 40; sp.data.spot_size = 0.35; sp.data.color = (1, 1, 0.95)
else:
    bpy.ops.object.light_add(type="POINT", location=(L / 2 + 1.5, -1.5, 1.5))
    f = bpy.context.object; f.data.energy = 200; f.data.color = (1.0, 0.6, 0.3)
for i in range(6):
    bpy.ops.object.light_add(type="POINT", location=(-L / 2 + 2 + i * 4.5, 0, 2.95))
    p = bpy.context.object; p.data.energy = 25; p.data.color = (1.0, 0.8, 0.55)

bpy.ops.object.camera_add(); cam = bpy.context.object; scn.camera = cam
def look_at(o, t):
    o.rotation_euler = (Vector(t) - o.location).to_track_quat("-Z", "Y").to_euler()
if args.shot == "gang":
    cam.location = (-10.5, 0, 1.55); look_at(cam, (5, 0, 1.25)); cam.data.lens = 22
elif args.shot == "reihe":
    cam.location = (-2.5, 0.05, 1.3); look_at(cam, (-1.8, -1.3, 1.0)); cam.data.lens = 20
elif args.shot == "notausstieg":
    cam.location = (-3.5, 0.6, 1.5); look_at(cam, (-1.2, -1.9, 1.9)); cam.data.lens = 22
else:
    raise SystemExit("unbekannter shot")

w, h = map(int, args.res.split("x"))
scn.render.resolution_x, scn.render.resolution_y = w, h
anim_common.engine(scn, args.engine, args.samples)
if args.pfad:
    n, off = anim_common.kamerapfad(scn, cam, args.pfad)
    # Kabinenlicht flackert leicht, Feuerschein von vorne pulsiert
    anim_common.flackern(f, f.data.energy, 1, n + off + 1, 0.6, seed=3, takt=2)
    if args.schuesse:
        bpy.ops.object.light_add(type="POINT", location=(3.0, 0.2, 1.6))
        mz = bpy.context.object; mz.data.color = (1.0, 0.8, 0.4)
        anim_common.blitze(mz, 6000, [int(x) for x in args.schuesse.split(",")])
    scn.render.filepath = args.out
    bpy.ops.render.render(animation=True)
    print("FERTIG_ANIM", args.out, n)
else:
    scn.render.filepath = args.out
    bpy.ops.render.render(write_still=True)
    print("FERTIG", args.out)
