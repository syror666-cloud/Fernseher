"""Low-Poly-Szene: Indischer Ozean bei Nacht – Zerstörer, Rettungsboot, Frachter (CODE ROT Folge 2).

blender -b -P scene_meer.py -- --pfad pfad.json --out f_#### [--zeit nacht|daemmerung|tag] [--rhib nah|fahrt] [--muendung 1] [--spritzer]
"""
import bpy, bmesh, math, random, sys, argparse, os
from mathutils import Vector, Matrix, Euler
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import anim_common

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--out", default="/tmp/meer_####")
ap.add_argument("--res", default="540x960")
ap.add_argument("--samples", type=int, default=6)
ap.add_argument("--engine", default="eevee")
ap.add_argument("--pfad", default="")
ap.add_argument("--zeit", default="nacht")
ap.add_argument("--rhib", default="")
ap.add_argument("--muendung", type=int, default=0)
ap.add_argument("--spritzer", action="store_true")
args = ap.parse_args(argv)
random.seed(4)
bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene
TAG = args.zeit == "tag"; DAEMM = args.zeit == "daemmerung"


def mat(name, color, rough=0.7, emit=None, strength=0.0, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = strength
    return m


def cube(loc, scale, m, rot=(0, 0, 0), parent=None):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object; o.scale = scale; o.data.materials.append(m)
    if parent: o.parent = parent
    return o


def cyl(loc, r, d, m, verts=12, rot=(0, 0, 0), r2=None, parent=None):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d, location=loc, rotation=rot)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r2, depth=d, location=loc, rotation=rot)
    o = bpy.context.object; o.data.materials.append(m)
    if parent: o.parent = parent
    return o


def rumpf(name, laenge, breite, hoehe, tiefgang, m, spitz=0.3):
    """Schiffsrumpf als Prisma mit spitzem Bug (+x)."""
    bm = bmesh.new()
    L, B = laenge, breite / 2
    pts = [(-L / 2, -B), (L / 2 - L * spitz, -B), (L / 2, 0), (L / 2 - L * spitz, B), (-L / 2, B)]
    unten = [bm.verts.new((x * 0.97, y * 0.7, -tiefgang)) for x, y in pts]
    oben = [bm.verts.new((x, y, hoehe)) for x, y in pts]
    bm.faces.new(oben); bm.faces.new(list(reversed(unten)))
    for i in range(len(pts)):
        j = (i + 1) % len(pts)
        bm.faces.new([unten[i], unten[j], oben[j], oben[i]])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); scn.collection.objects.link(o); o.data.materials.append(m)
    return o


# ---------- Materialien ----------
M_WASSER = mat("wasser", (0.01, 0.025, 0.05) if not TAG else (0.03, 0.12, 0.22), 0.08)
M_GRAU = mat("navygrau", (0.32, 0.34, 0.37), 0.55)
M_GRAU_D = mat("navygrau_d", (0.2, 0.21, 0.23), 0.6)
M_DECK = mat("deck", (0.12, 0.13, 0.14), 0.8)
M_SCHWARZ = mat("schwarz", (0.02, 0.02, 0.02), 0.6)
M_ORANGE = mat("rettungsboot", (0.95, 0.35, 0.05), 0.5, emit=(1.0, 0.35, 0.05), strength=0.12)
M_WEISS = mat("weiss", (0.85, 0.85, 0.82), 0.5)
M_FENSTER = mat("bullauge", (0.02, 0.02, 0.03), 0.1, emit=(0.9, 0.7, 0.4), strength=1.5)
M_LAMPE = mat("decklampe", (1, 1, 1), 0.3, emit=(1.0, 0.82, 0.55), strength=25)
M_ROT = mat("navi_rot", (1, 0, 0), 0.3, emit=(1, 0.02, 0.02), strength=30)
M_GRUEN = mat("navi_gruen", (0, 1, 0), 0.3, emit=(0.05, 1, 0.1), strength=30)
M_RHIB = mat("rhib", (0.08, 0.09, 0.08), 0.8)
M_CONT = [mat(f"container{i}", c, 0.7) for i, c in enumerate([(0.55, 0.12, 0.08), (0.08, 0.25, 0.45), (0.7, 0.55, 0.1),
                                                                (0.1, 0.35, 0.2), (0.6, 0.6, 0.62), (0.15, 0.3, 0.55)])]
M_SCHAUM = mat("gischt", (0.9, 0.95, 1.0), 0.4, emit=(0.6, 0.7, 0.8), strength=0.3)
M_MUZ = mat("muendung", (1, 0.8, 0.4), 0.3, emit=(1.0, 0.75, 0.35), strength=80)

# ---------- Meer mit animierten Wellen ----------
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
meer = bpy.context.object; meer.scale = (1600, 1600, 1); meer.data.materials.append(M_WASSER)
bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.subdivide(number_cuts=160); bpy.ops.object.mode_set(mode="OBJECT")
tex = bpy.data.textures.new("wellen", type="CLOUDS"); tex.noise_scale = 0.012; tex.noise_depth = 1
wellen_empty = bpy.data.objects.new("wellen_bewegung", None); scn.collection.objects.link(wellen_empty)
wellen_empty.scale = (0.03, 0.03, 0.03)
dm = meer.modifiers.new("wellen", "DISPLACE"); dm.texture = tex; dm.strength = 1.4; dm.mid_level = 0.5
dm.texture_coords = "OBJECT"; dm.texture_coords_object = wellen_empty
for p in meer.data.polygons:
    p.use_smooth = False

# ---------- Zerstörer (Heck bei x=0, Bug bei +x) ----------
schiff = rumpf("zerstoerer", 154, 20, 6, 6, M_GRAU, spitz=0.22); schiff.location = (77, 0, 0)
cube((77, 0, 6.05), (75, 9.6, 0.05), M_DECK)
cube((65, 0, 11), (22, 7, 5), M_GRAU)            # Aufbau achtern
cube((95, 0, 13), (15, 7.5, 7), M_GRAU)          # Brückenaufbau
cube((100, 0, 21), (5, 6, 1.5), M_GRAU_D)        # Brücke
for i in range(8):
    cube((95.2 + i * 1.2 - 4.2, -7.55, 20.8), (0.45, 0.05, 0.6), M_FENSTER)
cyl((90, 0, 30), 0.5, 18, M_GRAU_D, verts=8)     # Mast
cube((90, 0, 36), (0.3, 4, 0.2), M_GRAU_D)
cyl((80, 0, 18), 2.6, 8, M_GRAU_D, verts=10)     # Schornstein
cube((14, 0, 7.5), (2.6, 3.2, 1.5), M_GRAU)      # Hubschrauberhangar-Rand am Heck
for side in (-1, 1):                             # Reling am Heck
    for i in range(14):
        cyl((1 + i * 1.6, side * 9.4, 6.6), 0.04, 1.1, M_GRAU_D, verts=5)
    cube((12, side * 9.4, 7.1), (11, 0.03, 0.03), M_GRAU_D)
for i in range(7):
    cyl((0.2, -9 + i * 3, 6.6), 0.04, 1.1, M_GRAU_D, verts=5)
cube((0.2, 0, 7.1), (0.03, 9.4, 0.03), M_GRAU_D)
for x in (4, 22, 40):                            # Decklampen
    cube((x, 0, 10.2), (0.4, 0.4, 0.15), M_LAMPE)
    bpy.ops.object.light_add(type="POINT", location=(x, 0, 9.8))
    l = bpy.context.object; l.data.energy = 700; l.data.color = (1.0, 0.8, 0.55)
cube((100, -7.6, 22.5), (0.3, 0.1, 0.3), M_ROT); cube((100, 7.6, 22.5), (0.3, 0.1, 0.3), M_GRUEN)
# Scharfschützen-Silhouetten auf dem Heck (liegend)
M_SNIPER = mat("sniper", (0.04, 0.045, 0.04), 0.9)
for y in (-4.5, 0.5, 5):
    cube((3.5, y, 6.3), (1.0, 0.35, 0.22), M_SNIPER)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=6, radius=0.24, location=(2.4, y, 6.45))
    bpy.context.object.data.materials.append(M_SNIPER)
    cyl((1.3, y, 6.45), 0.04, 1.6, M_SCHWARZ, verts=6, rot=(0, math.pi / 2, 0))
# Suchscheinwerfer vom Heck auf das Rettungsboot
bpy.ops.object.light_add(type="SPOT", location=(2, 0, 12))
sl = bpy.context.object; sl.data.energy = 30000 if not TAG else 0; sl.data.spot_size = 0.22; sl.data.spot_blend = 0.5
sl.data.color = (0.85, 0.9, 1.0); sl.rotation_euler = (Vector((-32, 0, 1)) - sl.location).to_track_quat("-Z", "Y").to_euler()

# ---------- Rettungsboot (geschlossen, orange) bei (-32, 0) ----------
boot = bpy.data.objects.new("boot_pivot", None); scn.collection.objects.link(boot); boot.location = (-32, 0, 0)
br = rumpf("boot_rumpf", 8.5, 3.0, 0.9, 0.7, M_ORANGE, spitz=0.25); br.parent = boot
bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=1.45, depth=6.6, location=(-0.2, 0, 0.9), rotation=(0, math.pi / 2, 0))
dach = bpy.context.object; dach.scale = (0.65, 1, 1); dach.data.materials.append(M_ORANGE); dach.parent = boot
for side in (-1, 1):
    for i in range(5):
        cube((-2.6 + i * 1.2, side * 1.38, 1.35), (0.25, 0.05, 0.16), M_FENSTER, parent=boot)
cube((2.2, 0, 2.0), (0.45, 0.45, 0.18), M_ORANGE, parent=boot)   # Luke vorne
cube((-2.8, 0, 2.0), (0.45, 0.45, 0.18), M_ORANGE, parent=boot)  # Luke hinten
cube((0, 0, 0.92), (4.2, 1.5, 0.05), M_WEISS, parent=boot)
bpy.ops.object.light_add(type="POINT", location=(4, -7, 7)); al = bpy.context.object; al.data.energy = 2500 if not TAG else 0
al.data.color = (0.75, 0.85, 1.0)
bpy.ops.object.light_add(type="POINT", location=(0, 0, 1.2)); il = bpy.context.object; il.data.energy = 60
il.data.color = (1.0, 0.75, 0.4); il.parent = boot
# Gischt am Boot
for i in range(14):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=random.uniform(0.2, 0.5),
                                          location=(random.uniform(-4.5, 4.5), random.choice([-1.6, 1.6]) + random.uniform(-0.3, 0.3), 0.05))
    o = bpy.context.object; o.scale = (2, 1, 0.3); o.data.materials.append(M_SCHAUM); o.parent = boot

# ---------- Schlauchboot (RHIB) ----------
rhib = None
if args.rhib:
    rhib = bpy.data.objects.new("rhib_pivot", None); scn.collection.objects.link(rhib)
    rhib.location = (-29, -4.5, 0) if args.rhib == "nah" else (-6, -14, 0)
    rr = rumpf("rhib", 9, 3.2, 0.6, 0.3, M_RHIB, spitz=0.3); rr.parent = rhib
    for side in (-1, 1):
        cyl((0, side * 1.45, 0.45), 0.45, 8.5, M_SCHWARZ, verts=10, rot=(0, math.pi / 2, 0), parent=rhib)
    for i in range(4):
        cube((-2 + i * 1.3, 0, 1.2), (0.3, 0.3, 0.6), M_SNIPER, parent=rhib)
    if args.rhib == "fahrt":
        rhib.rotation_euler = (0, 0, math.radians(160))

# ---------- Frachter (Maersk Alabama, ohne Logos) weit weg ----------
fr = rumpf("frachter", 155, 24, 10, 7, mat("frachter_rumpf", (0.15, 0.32, 0.55), 0.6), spitz=0.18)
fr.location = (-420, 260, 0); fr.rotation_euler = (0, 0, math.radians(-30))
for i in range(9):
    for j in range(4):
        for k in range(random.randint(1, 3)):
            cube((0, 0, 0), (2.9, 1.25, 1.25), random.choice(M_CONT)).parent = fr
            o = bpy.context.object; o.location = (-55 + i * 12, -7.5 + j * 5, 11.3 + k * 2.6)
cube((0, 0, 0), (6, 11, 7), M_WEISS).parent = fr; bpy.context.object.location = (-66, 0, 17)
for i in range(10):
    cube((0, 0, 0), (0.6, 0.05, 0.5), M_FENSTER).parent = fr; bpy.context.object.location = (-61, -11.1, 21 - (i // 5) * 3)

# ---------- Fregatte in der Ferne ----------
fg = rumpf("fregatte", 135, 14, 5, 5, M_GRAU_D, spitz=0.22); fg.location = (180, 420, 0); fg.rotation_euler = (0, 0, 0.4)
cube((0, 0, 0), (25, 5, 6), M_GRAU_D).parent = fg; bpy.context.object.location = (10, 0, 10)

# ---------- Mündungsfeuer ----------
muz = []
if args.muendung:
    for y in (-4.5, 0.5, 5):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.35, location=(0.4, y, 6.45))
        o = bpy.context.object; o.scale = (2.0, 1, 1); o.data.materials.append(M_MUZ); muz.append(o)
    bpy.ops.object.light_add(type="POINT", location=(0.0, 0, 7)); ml = bpy.context.object; ml.data.color = (1, 0.75, 0.4)

# ---------- Spritzer (Kapitän springt) ----------
if args.spritzer:
    for i in range(26):
        h = random.uniform(0.5, 2.6)
        bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=random.uniform(0.15, 0.4), radius2=0, depth=h,
                                        location=(-32 + random.uniform(-1.2, 1.2), -2.8 + random.uniform(-1.2, 1.2), h / 2))
        bpy.context.object.data.materials.append(M_SCHAUM)

# ---------- Himmel, Licht ----------
world = bpy.data.worlds.new("w"); scn.world = world; world.use_nodes = True
wn = world.node_tree.nodes; wl = world.node_tree.links; bg = wn["Background"]
tc = wn.new("ShaderNodeTexCoord"); sep = wn.new("ShaderNodeSeparateXYZ"); ramp = wn.new("ShaderNodeValToRGB")
wl.new(tc.outputs["Normal"], sep.inputs["Vector"]); wl.new(sep.outputs["Z"], ramp.inputs["Fac"]); wl.new(ramp.outputs["Color"], bg.inputs["Color"])
if TAG:
    ramp.color_ramp.elements[0].color = (0.75, 0.82, 0.9, 1); ramp.color_ramp.elements[1].color = (0.2, 0.42, 0.8, 1)
    bg.inputs["Strength"].default_value = 1.0
    bpy.ops.object.light_add(type="SUN", rotation=(math.radians(40), 0, math.radians(30))); s = bpy.context.object
    s.data.energy = 4.0; s.data.color = (1, 0.96, 0.88)
elif DAEMM:
    ramp.color_ramp.elements[0].color = (0.85, 0.35, 0.18, 1); ramp.color_ramp.elements[1].color = (0.06, 0.07, 0.2, 1)
    ramp.color_ramp.elements[1].position = 0.35; bg.inputs["Strength"].default_value = 1.2
    bpy.ops.object.light_add(type="SUN", rotation=(math.radians(86), 0, math.radians(-100))); s = bpy.context.object
    s.data.energy = 1.2; s.data.color = (1, 0.55, 0.3)
else:
    ramp.color_ramp.elements[0].color = (0.03, 0.05, 0.12, 1); ramp.color_ramp.elements[1].color = (0.004, 0.006, 0.02, 1)
    ramp.color_ramp.elements[1].position = 0.45; bg.inputs["Strength"].default_value = 1.1
    bpy.ops.object.light_add(type="SUN", rotation=(math.radians(60), 0, math.radians(140))); s = bpy.context.object
    s.data.energy = 0.5; s.data.color = (0.6, 0.7, 1.0)
    M_STERN = mat("stern", (1, 1, 1), 1, emit=(0.9, 0.95, 1), strength=25)
    for i in range(220):
        a = random.uniform(0, math.tau); el = random.uniform(0.05, 1.2)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=random.uniform(0.6, 1.4),
                                              location=Vector((math.cos(a) * math.cos(el), math.sin(a) * math.cos(el), math.sin(el))) * 900)
        bpy.context.object.data.materials.append(M_STERN)
    M_MOND = mat("mond", (1, 1, 1), 1, emit=(0.9, 0.92, 1), strength=6)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=22, location=(-700, 300, 380)); bpy.context.object.data.materials.append(M_MOND)

# ---------- Kamera + Animation ----------
bpy.ops.object.camera_add(); cam = bpy.context.object; scn.camera = cam
w, h = map(int, args.res.split("x")); scn.render.resolution_x, scn.render.resolution_y = w, h
anim_common.engine(scn, args.engine, args.samples)
cam.data.clip_end = 3000
n, off = anim_common.kamerapfad(scn, cam, args.pfad)
N = n + off + 1
# Wellen laufen, Boote schaukeln
wellen_empty.location = (0, 0, 0); wellen_empty.keyframe_insert("location", frame=1)
wellen_empty.location = (N * 0.35, N * 0.12, N * 0.02); wellen_empty.keyframe_insert("location", frame=N)
for fc in wellen_empty.animation_data.action.fcurves:
    for kp in fc.keyframe_points: kp.interpolation = "LINEAR"
for f in range(1, N + 1, 2):
    t = f / 30
    boot.location = (-32, 0, 0.25 * math.sin(t * 1.7) + 0.1 * math.sin(t * 3.1))
    boot.rotation_euler = (0.09 * math.sin(t * 1.3), 0.05 * math.sin(t * 1.9 + 1), 1.25 + 0.03 * math.sin(t * 0.7))
    boot.keyframe_insert("location", frame=f); boot.keyframe_insert("rotation_euler", frame=f)
    schiff.location = (77, 0, 0.12 * math.sin(t * 0.6)); schiff.keyframe_insert("location", frame=f)
    if rhib:
        base = rhib.location.copy() if f == 1 else base
        mv = Vector((-t * 2.5, t * 0.8, 0)) if args.rhib == "fahrt" else Vector((0, 0, 0))
        rhib.location = base + mv + Vector((0, 0, 0.2 * math.sin(t * 2.1)))
        rhib.rotation_euler.x = 0.06 * math.sin(t * 1.6); rhib.keyframe_insert("location", frame=f); rhib.keyframe_insert("rotation_euler", frame=f)
if muz:
    for o in muz:
        o.hide_render = True; o.keyframe_insert("hide_render", frame=1)
        o.hide_render = False; o.keyframe_insert("hide_render", frame=args.muendung + 1)
        o.hide_render = True; o.keyframe_insert("hide_render", frame=args.muendung + 3)
    anim_common.blitze(ml, 9000, [args.muendung + 1, args.muendung + 2])
scn.render.filepath = args.out
bpy.ops.render.render(animation=True)
print("FERTIG_ANIM", args.out, n)
