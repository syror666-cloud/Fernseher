"""Serien-Intro CODE ROT: Waffenkammer mit Spind-Zellen aller Einheiten.

Rendert einen breiten Streifen (orthografisch), der im Schnitt horizontal
abgefahren wird (Roulette). Aufruf:
  blender -b -P scene_spinde.py -- --out streifen.png [--hoehe 1920] [--samples 32] [--fokus GSG 9]
"""
import bpy, math, sys, argparse, random, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--out", default="/tmp/spinde.png")
ap.add_argument("--hoehe", type=int, default=1920)
ap.add_argument("--samples", type=int, default=32)
ap.add_argument("--fokus", default="GSG 9")
ap.add_argument("--font", default="")
ap.add_argument("--figuren", default=".")
ap.add_argument("--engine", default="cycles")
ap.add_argument("--pfad", default="", help="Animation: JSON mit Kamerapfad (Perspektive)")
ap.add_argument("--res", default="720x1280")
args = ap.parse_args(argv)
random.seed(3)

EINHEITEN = [
    ("NAVY SEALS", "USA", "helm"), ("SAS", "UK", "barett"), ("GIGN", "FRANKREICH", "helm"),
    ("BOPE", "BRASILIEN", "barett"), ("KSK", "DEUTSCHLAND", "helm"), ("SAYERET MATKAL", "ISRAEL", "kappe"),
    ("GSG 9", "DEUTSCHLAND", "helm"), ("DELTA FORCE", "USA", "kappe"), ("GROM", "POLEN", "helm"),
    ("SEK", "DEUTSCHLAND", "helm"), ("PARARESCUE", "USA", "helm"), ("EKO COBRA", "ÖSTERREICH", "helm"),
    ("JTF2", "KANADA", "kappe"), ("SAT", "JAPAN", "helm"),
]

KUERZEL = {"NAVY SEALS": "seals", "SAS": "sas", "GIGN": "gign", "BOPE": "bope", "KSK": "ksk", "SAYERET MATKAL": "matkal",
           "GSG 9": "gsg9", "DELTA FORCE": "delta", "GROM": "grom", "SEK": "sek", "PARARESCUE": "pj", "EKO COBRA": "cobra",
           "JTF2": "jtf2", "SAT": "sat"}

bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene
font = bpy.data.fonts.load(args.font) if args.font else None


def mat(name, color, rough=0.6, emit=None, strength=0.0, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = strength
    return m


def cube(loc, scale, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object; o.scale = scale; o.data.materials.append(m); return o


def cyl(loc, r, d, m, verts=16, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d, location=loc, rotation=rot)
    o = bpy.context.object; o.data.materials.append(m); return o


def sphere(loc, r, m, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=10, radius=r, location=loc)
    o = bpy.context.object; o.scale = scale; o.data.materials.append(m)
    bpy.ops.object.shade_smooth(); return o


def text(body, loc, size, m, align="CENTER"):
    bpy.ops.object.text_add(location=loc, rotation=(math.pi / 2, 0, 0))
    t = bpy.context.object; t.data.body = body; t.data.size = size
    t.data.align_x = align; t.data.align_y = "CENTER"
    if font:
        t.data.font = font
    t.data.extrude = 0.004
    t.data.materials.append(m); return t


M_WALL = mat("wand", (0.035, 0.037, 0.045), 0.8)
M_FLOOR = mat("boden", (0.03, 0.03, 0.035), 0.35, metal=0.3)
M_STEEL = mat("stahl", (0.25, 0.27, 0.3), 0.35, metal=0.9)
M_BACK = mat("rueckwand", (0.07, 0.08, 0.1), 0.7)
M_SIGN = mat("schild", (0.015, 0.015, 0.02), 0.5)
M_SIGNTXT = mat("schildtext", (1, 1, 1), 0.5, emit=(0.95, 0.95, 1.0), strength=3.0)
M_LAND = mat("landtext", (1, 1, 1), 0.5, emit=(0.75, 0.78, 0.85), strength=1.5)
M_LIGHT = mat("deckenlicht", (1, 1, 1), 0.5, emit=(0.85, 0.9, 1.0), strength=25.0)
M_RED = mat("alarm", (1, 0.05, 0.05), 0.5, emit=(1.0, 0.05, 0.03), strength=30.0)
M_SUIT = mat("anzug", (0.06, 0.065, 0.07), 0.8)
M_VEST = mat("weste", (0.1, 0.11, 0.1), 0.8)
M_HELM = mat("helm", (0.09, 0.1, 0.08), 0.5)
M_FACE = mat("maske", (0.03, 0.03, 0.035), 0.7)
M_GOGGLE = mat("brille", (0.05, 0.3, 0.15), 0.2, emit=(0.1, 1.0, 0.35), strength=4.0)
M_BERET = {"SAS": mat("barett_sas", (0.6, 0.55, 0.4), 0.9), "BOPE": mat("barett_bope", (0.03, 0.03, 0.03), 0.9)}
M_CONE = bpy.data.materials.new("kegel"); M_CONE.use_nodes = True
_n = M_CONE.node_tree.nodes; _l = M_CONE.node_tree.links
_n.remove(_n["Principled BSDF"])
_em = _n.new("ShaderNodeEmission"); _em.inputs["Color"].default_value = (0.8, 0.85, 1.0, 1); _em.inputs["Strength"].default_value = 0.018
_tr = _n.new("ShaderNodeBsdfTransparent"); _add = _n.new("ShaderNodeAddShader")
_l.new(_em.outputs[0], _add.inputs[0]); _l.new(_tr.outputs[0], _add.inputs[1])
_l.new(_add.outputs[0], _n["Material Output"].inputs["Surface"])
M_SCRATCH = mat("zellennr", (0.6, 0.62, 0.66), 0.6, emit=(0.5, 0.52, 0.56), strength=0.6)

W = 2.0  # Zellenbreite
ALARM = []
SPOTS = []
N = len(EINHEITEN)
x0 = -(N - 1) * W / 2

cube((0, 0.9, 2.2), (N * W / 2 + 2, 0.05, 2.4), M_WALL)
cube((0, -2, -0.02), (N * W / 2 + 2, 3.5, 0.02), M_FLOOR)

for i, (name, land, kopf) in enumerate(EINHEITEN):
    x = x0 + i * W
    fokus = name == args.fokus
    cube((x, 0.8, 1.6), (W / 2 - 0.08, 0.04, 1.6), M_BACK)
    # Gitterrahmen
    for s in (-1, 1):
        cube((x + s * (W / 2 - 0.05), 0.0, 1.6), (0.05, 0.85, 1.6), M_STEEL)
    cube((x, 0.0, 3.25), (W / 2, 0.85, 0.05), M_STEEL)
    cube((x, 0.0, 0.03), (W / 2, 0.85, 0.03), M_STEEL)
    for k in range(7):  # Gitterstäbe vorne
        cyl((x - W / 2 + 0.2 + k * (W - 0.4) / 6, -0.82, 1.6), 0.018, 3.2, M_STEEL, verts=8)
    # Deckenlicht
    cube((x, 0.0, 3.17), (0.45, 0.06, 0.02), M_LIGHT)
    bpy.ops.object.light_add(type="SPOT", location=(x, -0.2, 3.1), rotation=(0.12, 0, 0))
    sp = bpy.context.object; sp.data.energy = 260; sp.data.spot_size = 0.9; sp.data.spot_blend = 0.6
    sp.data.color = (0.85, 0.9, 1.0)
    SPOTS.append(sp)
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.95, radius2=0.12, depth=3.0, location=(x, -0.1, 1.6))
    kegel = bpy.context.object; kegel.data.materials.append(M_CONE)
    # Namensschild + Land
    cube((x, -0.9, 3.55), (W / 2 - 0.15, 0.02, 0.2), M_SIGN)
    text(name, (x, -0.93, 3.6), 0.17, M_SIGNTXT)
    text(land, (x, -0.93, 3.43), 0.085, M_LAND)
    text(f"ZELLE {201 + i}", (x, 0.74, 2.6), 0.09, M_SCRATCH)
    # Figur: eigene 2D-Figur der Einheit als Bild-Ebene
    png = f"{args.figuren}/einheit_{KUERZEL[name]}.png"
    img = bpy.data.images.load(png)
    m = bpy.data.materials.new("fig_" + name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    tex = nt.nodes.new("ShaderNodeTexImage"); tex.image = img
    nt.links.new(tex.outputs["Color"], b.inputs["Base Color"])
    nt.links.new(tex.outputs["Alpha"], b.inputs["Alpha"])
    nt.links.new(tex.outputs["Color"], b.inputs["Emission Color"])
    b.inputs["Emission Strength"].default_value = 0.08
    b.inputs["Roughness"].default_value = 0.9
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, 0.3, 1.45), rotation=(math.pi / 2, 0, 0))
    pl = bpy.context.object; pl.scale = (1.06, 2.83, 1); pl.data.materials.append(m)
    if random.random() < 0.35 or fokus:  # rote Alarmleuchte
        cube((x + W / 2 - 0.25, -0.85, 3.0), (0.06, 0.02, 0.06), M_RED)
        bpy.ops.object.light_add(type="POINT", location=(x + W / 2 - 0.25, -1.0, 3.0))
        r = bpy.context.object; r.data.energy = 120; r.data.color = (1, 0.05, 0.03)
        ALARM.append(r)

# Weltlicht + Kamera
world = bpy.data.worlds.new("w"); scn.world = world; world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.005, 0.005, 0.008, 1)
vol = world.node_tree.nodes.new("ShaderNodeVolumePrincipled")
vol.inputs["Density"].default_value = 0.0
world.node_tree.links.new(vol.outputs["Volume"], world.node_tree.nodes["World Output"].inputs["Volume"])

if args.pfad:
    import anim_common
    w, h = map(int, args.res.split("x"))
    scn.render.resolution_x, scn.render.resolution_y = w, h
    bpy.ops.object.camera_add(location=(0, -8, 1.9)); cam = bpy.context.object; scn.camera = cam
    anim_common.engine(scn, args.engine, args.samples)
    if args.engine == "eevee":
        scn.render.use_motion_blur = True; scn.render.motion_blur_shutter = 0.6
    n, off = anim_common.kamerapfad(scn, cam, args.pfad)
    # Rotes Alarm-Strobo + flackernde Deckenspots
    for k, r in enumerate(ALARM):
        frames = [f for f in range(1, n + off + 2) if ((f + k * 4) // 6) % 3 == 0]
        anim_common.blitze(r, 260, frames)
    for k, sp in enumerate(SPOTS):
        anim_common.flackern(sp, 260, 1, n + off + 1, 0.25, seed=k, takt=3)
    # zusätzliches rotes Rundumlicht im Gang
    bpy.ops.object.light_add(type="AREA", location=(0, -3, 4.5), rotation=(0.3, 0, 0))
    gl = bpy.context.object; gl.data.color = (1, 0.08, 0.05); gl.data.size = 30
    anim_common.blitze(gl, 900, [f for f in range(1, n + off + 2) if (f // 8) % 2 == 0])
    scn.render.filepath = args.out
    bpy.ops.render.render(animation=True)
    print("FERTIG_ANIM", args.out, n)
    raise SystemExit(0)

bpy.ops.object.camera_add(location=(0, -12, 1.95), rotation=(math.pi / 2, 0, 0))
cam = bpy.context.object; scn.camera = cam
cam.data.type = "ORTHO"
breite = N * W + 0.4
cam.data.ortho_scale = breite
h = args.hoehe
# Höhe entspricht 4.6 Einheiten Bildhöhe
px_pro_einheit = h / 4.6
scn.render.resolution_x = int(breite * px_pro_einheit)
scn.render.resolution_y = h
cam.location.z = 1.95
scn.render.engine = "CYCLES"; scn.cycles.device = "CPU"
scn.cycles.samples = args.samples; scn.cycles.use_denoising = True; scn.cycles.max_bounces = 4
scn.view_settings.view_transform = "AgX"; scn.view_settings.look = "AgX - Punchy"
scn.render.filepath = args.out
bpy.ops.render.render(write_still=True)
print("FERTIG", args.out, scn.render.resolution_x, "x", h, "zellen_px", W * px_pro_einheit,
      "fokus_index", [e[0] for e in EINHEITEN].index(args.fokus))
