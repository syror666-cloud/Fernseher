"""Low-Poly-Szene: Rollfeld Mogadischu bei Nacht (CODE ROT Folge 1).

Aufruf:
  blender -b -P scene_rollfeld.py -- --shot boden --out out.png [--res 540x960] [--samples 32]
Shots: boden (Bodenperspektive aus dem Sand), drohne (Vogelperspektive), tragflaeche (unter dem Flügel)
"""
import bpy, bmesh, math, random, sys, argparse
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--shot", default="boden")
ap.add_argument("--out", default="/tmp/rollfeld.png")
ap.add_argument("--res", default="540x960")
ap.add_argument("--samples", type=int, default=32)
ap.add_argument("--fire", type=float, default=1.0, help="0 = kein Feuer")
args = ap.parse_args(argv)

random.seed(7)
bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene

# ---------- Hilfsfunktionen ----------
def mat(name, color, rough=0.8, emit=None, strength=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = strength
    return m

def obj_from_bm(name, bm, material):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me)
    scn.collection.objects.link(o)
    o.data.materials.append(material)
    for p in o.data.polygons:
        p.use_smooth = False
    return o

def cube(name, loc, scale, material, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    o.scale = scale
    o.data.materials.append(material)
    return o

def cyl(name, loc, r, depth, material, verts=12, rot=(0, 0, 0), r2=None):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r2, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    o.data.materials.append(material)
    return o

# ---------- Materialien ----------
M_SAND = mat("sand", (0.42, 0.36, 0.27), 1.0)
M_RUNWAY = mat("runway", (0.06, 0.06, 0.065), 0.9)
M_LINE = mat("line", (0.8, 0.8, 0.75), 0.6)
M_WHITE = mat("rumpf", (0.85, 0.86, 0.88), 0.45)
M_BLUE = mat("streifen", (0.05, 0.09, 0.22), 0.5)
M_TAIL = mat("leitwerk", (0.04, 0.07, 0.18), 0.5)
M_GREY = mat("grau", (0.35, 0.36, 0.38), 0.6)
M_WIN = mat("fenster", (0.1, 0.07, 0.03), 0.3, emit=(1.0, 0.72, 0.38), strength=6.0)
M_COCKPIT = mat("cockpit", (0.02, 0.02, 0.03), 0.2, emit=(0.4, 0.5, 0.7), strength=0.6)
M_PALM = mat("palme", (0.03, 0.05, 0.035), 0.9)
M_TRUNK = mat("stamm", (0.06, 0.045, 0.03), 0.9)
M_FIRE = mat("feuer", (1, 0.4, 0.1), 0.5, emit=(1.0, 0.35, 0.05), strength=6.0)
M_BLDG = mat("gebaeude", (0.12, 0.12, 0.13), 0.9)
M_LAMP = mat("lampe", (0.1, 0.1, 0.1), 0.5, emit=(1.0, 0.8, 0.5), strength=25.0)

# ---------- Boden ----------
bpy.ops.mesh.primitive_plane_add(size=600, location=(0, 0, 0))
ground = bpy.context.object; ground.name = "sand"
bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.subdivide(number_cuts=60); bpy.ops.object.mode_set(mode="OBJECT")
for v in ground.data.vertices:
    d = Vector((v.co.x, v.co.y)).length
    if d > 25:
        v.co.z = random.uniform(-0.15, 0.35) * min(1, (d - 25) / 40)
ground.data.materials.append(M_SAND)

cube("rollbahn", (0, 0, 0.02), (300, 14, 0.02), M_RUNWAY)
for i in range(-20, 21):
    cube(f"mittellinie{i}", (i * 14, 0, 0.045), (3, 0.25, 0.005), M_LINE)
for s in (-1, 1):
    cube(f"rand{s}", (0, s * 13.2, 0.045), (300, 0.15, 0.005), M_LINE)
    for i in range(-15, 16):
        cyl(f"befeuerung{s}{i}", (i * 18, s * 15.5, 0.25), 0.12, 0.5, M_LAMP, verts=6)

# ---------- Flugzeug (generischer Zweistrahler, ohne Logos) ----------
PLANE = Vector((0, 0, 0))
L, R = 30.0, 1.9  # Rumpflänge, -radius
fus = cyl("rumpf", PLANE + Vector((0, 0, 3.0)), R, L, M_WHITE, verts=16, rot=(0, math.pi / 2, 0))
nose = cyl("nase", PLANE + Vector((L / 2 + 2.0, 0, 2.85)), R, 4.0, M_WHITE, verts=16, rot=(0, math.pi / 2, 0), r2=0.35)
tailc = cyl("heck", PLANE + Vector((-L / 2 - 2.5, 0, 3.35)), R, 5.0, M_WHITE, verts=16, rot=(0, -math.pi / 2, 0), r2=0.35)
cube("zierstreifen_l", PLANE + Vector((1, -R + 0.02, 3.0)), (L / 2 + 1.5, 0.03, 0.28), M_BLUE)
cube("zierstreifen_r", PLANE + Vector((1, R - 0.02, 3.0)), (L / 2 + 1.5, 0.03, 0.28), M_BLUE)
for side in (-1, 1):
    for i in range(22):
        x = -L / 2 + 2.5 + i * 1.15
        if random.random() < 0.82:
            cube(f"fenster{side}_{i}", PLANE + Vector((x, side * (R - 0.01), 3.55)), (0.18, 0.03, 0.22), M_WIN)
    cube(f"cockpitscheibe{side}", PLANE + Vector((L / 2 + 1.4, side * 1.45, 3.9)), (0.7, 0.35, 0.25), M_COCKPIT,
         rot=(0, 0, side * 0.5))
    # Flügel (gepfeilt)
    bm = bmesh.new()
    pts = [(3, side * R * 0.8, 2.3), (-3.5, side * R * 0.8, 2.3), (-8.5, side * 14.5, 2.9), (-6.8, side * 14.5, 2.9)]
    vs_top = [bm.verts.new(Vector(p) + PLANE + Vector((0, 0, 0.18))) for p in pts]
    vs_bot = [bm.verts.new(Vector(p) + PLANE) for p in pts]
    bm.faces.new(vs_top); bm.faces.new(list(reversed(vs_bot)))
    for a in range(4):
        b = (a + 1) % 4
        bm.faces.new([vs_bot[a], vs_bot[b], vs_top[b], vs_top[a]])
    obj_from_bm(f"fluegel{side}", bm, M_GREY)
    # Triebwerk unter dem Flügel
    cyl(f"triebwerk{side}", PLANE + Vector((0.5, side * 5.2, 1.6)), 0.85, 3.4, M_GREY, verts=14, rot=(0, math.pi / 2, 0))
    cyl(f"triebwerk_einlass{side}", PLANE + Vector((2.25, side * 5.2, 1.6)), 0.7, 0.1, M_RUNWAY, verts=14, rot=(0, math.pi / 2, 0))
    # Höhenleitwerk
    bm = bmesh.new()
    pts = [(-L / 2 - 2.0, side * 0.5, 3.8), (-L / 2 - 4.6, side * 0.5, 3.8), (-L / 2 - 6.4, side * 6.0, 4.2), (-L / 2 - 5.2, side * 6.0, 4.2)]
    vs_top = [bm.verts.new(Vector(p) + PLANE + Vector((0, 0, 0.12))) for p in pts]
    vs_bot = [bm.verts.new(Vector(p) + PLANE) for p in pts]
    bm.faces.new(vs_top); bm.faces.new(list(reversed(vs_bot)))
    for a in range(4):
        b = (a + 1) % 4
        bm.faces.new([vs_bot[a], vs_bot[b], vs_top[b], vs_top[a]])
    obj_from_bm(f"hoehenleitwerk{side}", bm, M_GREY)
    # Fahrwerk
    cyl(f"rad{side}", PLANE + Vector((-1.5, side * 2.6, 0.55)), 0.55, 0.4, M_RUNWAY, verts=10, rot=(math.pi / 2, 0, 0))
    cube(f"bein{side}", PLANE + Vector((-1.5, side * 2.6, 1.3)), (0.12, 0.12, 0.75), M_GREY)
cyl("bugrad", PLANE + Vector((L / 2, 0, 0.45)), 0.45, 0.3, M_RUNWAY, verts=10, rot=(math.pi / 2, 0, 0))
cube("bugbein", PLANE + Vector((L / 2, 0, 1.2)), (0.1, 0.1, 0.8), M_GREY)
# Seitenleitwerk
bm = bmesh.new()
pts = [(-L / 2 + 1.0, 4.4), (-L / 2 - 4.5, 4.4), (-L / 2 - 6.8, 11.2), (-L / 2 - 4.4, 11.2)]
vs_a = [bm.verts.new(Vector((x, -0.12, z)) + PLANE) for x, z in pts]
vs_b = [bm.verts.new(Vector((x, 0.12, z)) + PLANE) for x, z in pts]
bm.faces.new(vs_a); bm.faces.new(list(reversed(vs_b)))
for a in range(4):
    b = (a + 1) % 4
    bm.faces.new([vs_a[a], vs_a[b], vs_b[b], vs_b[a]])
obj_from_bm("seitenleitwerk", bm, M_TAIL)
# Notausstieg-Markierung über der Tragfläche
for side in (-1, 1):
    cube(f"notausstieg{side}", PLANE + Vector((-1.2, side * (R - 0.005), 3.4)), (0.45, 0.02, 0.6), M_GREY)

# ---------- Feuer vor dem Cockpit (Ablenkung) ----------
if args.fire > 0:
    FIRE = PLANE + Vector((L / 2 + 12, -3, 0))
    for i in range(9):
        h = random.uniform(1.0, 2.6) * args.fire
        cyl(f"flamme{i}", FIRE + Vector((random.uniform(-1.2, 1.2), random.uniform(-1.2, 1.2), h / 2)),
            random.uniform(0.3, 0.6), h, M_FIRE, verts=5, r2=0.0)
    bpy.ops.object.light_add(type="POINT", location=FIRE + Vector((0, 0, 1.5)))
    fl = bpy.context.object; fl.data.energy = 20000 * args.fire; fl.data.color = (1.0, 0.45, 0.15); fl.data.shadow_soft_size = 1.5

# ---------- Umgebung: Palmen, Terminal, Masten ----------
def palm(pos, h):
    cyl("stamm", pos + Vector((0, 0, h / 2)), 0.25, h, M_TRUNK, verts=6, r2=0.18)
    for k in range(7):
        a = k / 7 * math.tau + random.uniform(-0.2, 0.2)
        leaf = cube("blatt", pos + Vector((math.cos(a) * 1.6, math.sin(a) * 1.6, h - 0.3)), (1.8, 0.35, 0.04), M_PALM,
                    rot=(0, 0.45, a))
for i in range(40):
    x = random.uniform(-150, 150)
    y = random.choice([-1, 1]) * random.uniform(45, 120)
    palm(Vector((x, y, 0)), random.uniform(6, 11))
for i in range(6):
    cube(f"terminal{i}", (-60 + i * 22, 75, 4), (9, 6, 4 + random.uniform(0, 3)), M_BLDG)
    for j in range(4):
        if random.random() < 0.6:
            cube("terminalfenster", (-66 + i * 22 + j * 3.5, 68.9, 5), (0.8, 0.05, 0.6), M_WIN)
cube("tower", (40, 80, 10), (2.5, 2.5, 10), M_BLDG)
cube("tower_kanzel", (40, 80, 21), (3.5, 3.5, 1.4), M_WIN)

# ---------- Licht & Welt ----------
world = bpy.data.worlds.new("nacht"); scn.world = world; world.use_nodes = True
wn = world.node_tree.nodes; wl = world.node_tree.links
bg = wn["Background"]
grad = wn.new("ShaderNodeTexGradient"); grad.gradient_type = "LINEAR"
mapn = wn.new("ShaderNodeMapping"); tc = wn.new("ShaderNodeTexCoord")
ramp = wn.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color = (0.05, 0.085, 0.2, 1)
ramp.color_ramp.elements[1].color = (0.008, 0.012, 0.04, 1)
mapn.inputs["Rotation"].default_value = (0, -math.pi / 2, 0)
sep = wn.new("ShaderNodeSeparateXYZ")
wl.new(tc.outputs["Normal"], sep.inputs["Vector"])
wl.new(sep.outputs["Z"], ramp.inputs["Fac"])
ramp.color_ramp.elements[1].position = 0.45
wl.new(ramp.outputs["Color"], bg.inputs["Color"])
bg.inputs["Strength"].default_value = 4.0
# Nebel
vol = wn.new("ShaderNodeVolumePrincipled")
vol.inputs["Density"].default_value = 0.0012
vol.inputs["Color"].default_value = (0.5, 0.6, 0.8, 1)
wl.new(vol.outputs["Volume"], wn["World Output"].inputs["Volume"])

bpy.ops.object.light_add(type="SUN", rotation=(math.radians(55), 0, math.radians(-30)))
moon = bpy.context.object; moon.data.energy = 1.4; moon.data.color = (0.55, 0.65, 1.0); moon.data.angle = 0.02
bpy.ops.object.light_add(type="AREA", location=(0, 0, 20))
fill = bpy.context.object; fill.data.energy = 9000; fill.data.size = 60; fill.data.color = (0.4, 0.5, 0.9)

M_STAR = mat("stern", (1, 1, 1), 1, emit=(0.9, 0.95, 1.0), strength=30.0)
for i in range(260):
    a = random.uniform(0, math.tau); el = random.uniform(0.08, 1.2)
    p = Vector((math.cos(a) * math.cos(el), math.sin(a) * math.cos(el), math.sin(el))) * 400
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=random.uniform(0.25, 0.6), location=p)
    bpy.context.object.data.materials.append(M_STAR)
M_MOON = mat("mond", (1, 1, 1), 1, emit=(0.85, 0.9, 1.0), strength=8.0)
bpy.ops.mesh.primitive_uv_sphere_add(radius=9, location=(120, 260, 190))
bpy.context.object.data.materials.append(M_MOON)

# ---------- Kamera ----------
bpy.ops.object.camera_add()
cam = bpy.context.object; scn.camera = cam
def look_at(o, target):
    d = Vector(target) - o.location
    o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
if args.shot == "boden":
    cam.location = (-10, -30, 1.1); look_at(cam, (9, 0, 5.5)); cam.data.lens = 24
elif args.shot == "drohne":
    cam.location = (-45, -55, 55); look_at(cam, (8, 0, 0)); cam.data.lens = 28
elif args.shot == "tragflaeche":
    cam.location = (-6, -9.5, 0.9); look_at(cam, (-1.2, -1.9, 3.6)); cam.data.lens = 18
else:
    raise SystemExit(f"unbekannter shot {args.shot}")

# ---------- Render ----------
w, h = map(int, args.res.split("x"))
scn.render.resolution_x, scn.render.resolution_y = w, h
scn.render.engine = "CYCLES"
scn.cycles.device = "CPU"
scn.cycles.samples = args.samples
scn.cycles.use_denoising = True
scn.cycles.max_bounces = 4
scn.view_settings.view_transform = "AgX"
scn.view_settings.look = "AgX - Punchy"
scn.render.filepath = args.out
bpy.ops.render.render(write_still=True)
print("FERTIG", args.out)
