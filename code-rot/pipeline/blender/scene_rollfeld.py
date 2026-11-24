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
ap.add_argument("--leiter", action="store_true")
ap.add_argument("--offen", action="store_true", help="Notausstiege offen (Licht)")
ap.add_argument("--rutsche", action="store_true")
ap.add_argument("--engine", default="cycles", help="cycles | eevee")
ap.add_argument("--pfad", default="", help="JSON-Datei mit Kamerapfad (Animation)")
ap.add_argument("--leer", action="store_true", help="ohne Zusatz-Requisiten (alte Szene)")
ap.add_argument("--zuendung", type=int, default=0, help="Frame, ab dem das Feuer brennt (Animation)")
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


class Masse:
    """Sammelt viele kleine Primitive in EINEM Mesh (schnell statt tausender Objekte)."""
    def __init__(self, name, material):
        self.bm = bmesh.new(); self.name = name; self.material = material
    def _add(self, fn, loc, rot=(0, 0, 0), scale=(1, 1, 1), **kw):
        import mathutils
        tmp = bmesh.new(); fn(tmp, **kw)
        M = mathutils.Matrix.LocRotScale(Vector(loc), mathutils.Euler(rot), Vector(scale))
        bmesh.ops.transform(tmp, matrix=M, verts=tmp.verts)
        me = bpy.data.meshes.new("tmp"); tmp.to_mesh(me); tmp.free(); self.bm.from_mesh(me); bpy.data.meshes.remove(me)
    def kegel(self, loc, r, h, rot=(0, 0, 0), verts=3):
        self._add(lambda b, **k: bmesh.ops.create_cone(b, cap_ends=True, segments=verts, radius1=r, radius2=0, depth=h),
                  Vector(loc) + Vector((0, 0, h / 2)), rot)
    def kugel(self, loc, r, scale=(1, 1, 1), sub=1):
        self._add(lambda b, **k: bmesh.ops.create_icosphere(b, subdivisions=sub, radius=r), loc, (0, 0, 0), scale)
    def quader(self, loc, scale, rot=(0, 0, 0)):
        self._add(lambda b, **k: bmesh.ops.create_cube(b, size=2.0), loc, rot, scale)
    def zylinder(self, loc, r, h, rot=(0, 0, 0), verts=6):
        self._add(lambda b, **k: bmesh.ops.create_cone(b, cap_ends=True, segments=verts, radius1=r, radius2=r, depth=h), loc, rot)
    def fertig(self):
        return obj_from_bm(self.name, self.bm, self.material)

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
M_FIRE = mat("feuer", (1, 0.2, 0.02), 0.5, emit=(1.0, 0.18, 0.01), strength=3.5)
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

# ---------- Leitern, offene Ausstiege, Rutschen ----------
M_LADDER = mat("leiter", (0.08, 0.08, 0.08), 0.8)
M_OPEN = mat("offen", (0.1, 0.07, 0.03), 0.5, emit=(1.0, 0.75, 0.45), strength=12.0)
M_SLIDE = mat("rutsche", (0.85, 0.65, 0.08), 0.5)
if args.leiter:
    for side in (-1, 1):
        for k, (x0, y0) in enumerate([(-1.2, side * 6.5)]):
            top = PLANE + Vector((-1.6, side * 3.2, 2.55)); bot = PLANE + Vector((x0, y0, 0.0))
            mid = (top + bot) / 2; d = top - bot
            for off in (-0.25, 0.25):
                bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.04, depth=d.length, location=mid + Vector((off, 0, 0)))
                o = bpy.context.object; o.rotation_euler = d.to_track_quat("Z", "Y").to_euler(); o.data.materials.append(M_LADDER)
            for r in range(9):
                pos = bot + d * (r + 0.5) / 9
                cube("sprosse", pos, (0.27, 0.025, 0.025), M_LADDER)
if args.offen:
    for side in (-1, 1):
        cube(f"offen{side}", PLANE + Vector((-1.2, side * (R + 0.01), 3.4)), (0.42, 0.02, 0.56), M_OPEN)
        cube(f"tuer_vorn{side}", PLANE + Vector((L / 2 - 1.0, side * (R + 0.01), 3.2)), (0.5, 0.02, 0.9), M_OPEN)
        cube(f"tuer_hinten{side}", PLANE + Vector((-L / 2 + 1.0, side * (R + 0.01), 3.2)), (0.5, 0.02, 0.9), M_OPEN)
    bpy.ops.object.light_add(type="POINT", location=PLANE + Vector((0, -4, 3.5)))
    ol = bpy.context.object; ol.data.energy = 3000; ol.data.color = (1, 0.75, 0.45)
if args.rutsche:
    for side in (-1, 1):
        for xd in (L / 2 - 1.0, -L / 2 + 1.0):
            top = PLANE + Vector((xd, side * (R + 0.1), 2.4)); bot = PLANE + Vector((xd, side * (R + 5.8), 0.15))
            mid = (top + bot) / 2; d = bot - top
            bpy.ops.mesh.primitive_cube_add(location=mid)
            o = bpy.context.object; o.scale = (0.75, d.length / 2, 0.12)
            o.rotation_euler = (math.atan2(d.z, abs(d.y)) * (-side), 0, 0)
            o.data.materials.append(M_SLIDE)

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


# ---------- Requisiten: Rollfeld füllen ----------
anim_objs = {}
if not args.leer:
    import json as _json
    M_ARMY = mat("armee", (0.16, 0.17, 0.1), 0.85)
    M_ARMY_D = mat("armee_dunkel", (0.08, 0.085, 0.05), 0.9)
    M_CANVAS = mat("plane_stoff", (0.22, 0.2, 0.12), 1.0)
    M_TIRE = mat("reifen", (0.02, 0.02, 0.02), 0.9)
    M_HEAD = mat("scheinwerfer", (1, 1, 0.9), 0.3, emit=(1.0, 0.92, 0.7), strength=30.0)
    M_TAIL_L = mat("ruecklicht", (0.5, 0.0, 0.0), 0.3, emit=(1.0, 0.05, 0.02), strength=12.0)
    M_SANDBAG = mat("sandsack", (0.38, 0.32, 0.22), 1.0)
    M_METAL = mat("metall", (0.3, 0.3, 0.32), 0.4)
    M_FUEL = mat("tankwagen", (0.75, 0.74, 0.7), 0.5)
    M_STAIRS = mat("treppe", (0.85, 0.78, 0.2), 0.6)
    M_SOLDIER = mat("soldat", (0.12, 0.13, 0.08), 0.9)
    M_SKIN_D = mat("haut_d", (0.18, 0.11, 0.07), 0.9)
    M_FLOOD = mat("flutlicht", (1, 1, 1), 0.3, emit=(1.0, 0.95, 0.8), strength=40.0)
    M_GRASS = mat("gras", (0.32, 0.3, 0.14), 1.0)
    M_HILL = mat("huegel", (0.03, 0.035, 0.05), 1.0)
    M_CITY = mat("stadtlicht", (1, 0.7, 0.4), 0.5, emit=(1.0, 0.7, 0.35), strength=20.0)
    M_BEACON = mat("leuchtfeuer", (1, 0, 0), 0.3, emit=(1.0, 0.03, 0.02), strength=60.0)
    M_HANGAR = mat("hangar", (0.17, 0.17, 0.18), 0.7)
    M_STONE = mat("stein", (0.25, 0.22, 0.18), 1.0)

    def truck(pos, rotz, licht=True, plane=True):
        import mathutils
        R = mathutils.Matrix.Rotation(rotz, 4, "Z")
        def P(v): return Vector(pos) + (R @ Vector(v))
        cube("lkw_kabine", P((2.6, 0, 1.5)), (0.9, 1.15, 0.9), M_ARMY, rot=(0, 0, rotz))
        cube("lkw_haube", P((3.7, 0, 1.0)), (0.5, 1.0, 0.45), M_ARMY, rot=(0, 0, rotz))
        cube("lkw_rahmen", P((0, 0, 0.75)), (3.6, 1.15, 0.12), M_ARMY_D, rot=(0, 0, rotz))
        cube("lkw_ladeflaeche", P((-0.8, 0, 1.2)), (2.4, 1.2, 0.4), M_ARMY, rot=(0, 0, rotz))
        if plane:
            cube("lkw_plane", P((-0.8, 0, 2.15)), (2.4, 1.2, 0.6), M_CANVAS, rot=(0, 0, rotz))
        for dx in (2.8, -0.5, -2.2):
            for dy in (-1.1, 1.1):
                cyl("rad", P((dx, dy, 0.5)), 0.5, 0.35, M_TIRE, verts=10, rot=(math.pi / 2, 0, rotz))
        if licht:
            for dy in (-0.7, 0.7):
                cube("lkw_licht", P((4.21, dy, 1.1)), (0.03, 0.15, 0.12), M_HEAD, rot=(0, 0, rotz))
                bpy.ops.object.light_add(type="SPOT", location=P((4.3, dy, 1.1)))
                sp = bpy.context.object; sp.data.energy = 1800; sp.data.spot_size = 0.75; sp.data.spot_blend = 0.4
                sp.data.color = (1.0, 0.9, 0.7)
                d = (R @ Vector((1, 0, -0.06)))
                sp.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
            for dy in (-1.0, 1.0):
                cube("lkw_rueck", P((-3.22, dy, 1.0)), (0.03, 0.1, 0.08), M_TAIL_L, rot=(0, 0, rotz))

    def jeep(pos, rotz, licht=True):
        import mathutils
        R = mathutils.Matrix.Rotation(rotz, 4, "Z")
        def P(v): return Vector(pos) + (R @ Vector(v))
        cube("jeep", P((0, 0, 0.85)), (1.7, 0.85, 0.35), M_ARMY, rot=(0, 0, rotz))
        cube("jeep_scheibe", P((0.5, 0, 1.4)), (0.05, 0.8, 0.25), M_METAL, rot=(0, 0, rotz))
        for dx in (1.1, -1.1):
            for dy in (-0.85, 0.85):
                cyl("rad", P((dx, dy, 0.42)), 0.42, 0.3, M_TIRE, verts=10, rot=(math.pi / 2, 0, rotz))
        if licht:
            for dy in (-0.55, 0.55):
                cube("jeep_licht", P((1.71, dy, 0.95)), (0.03, 0.12, 0.1), M_HEAD, rot=(0, 0, rotz))
            bpy.ops.object.light_add(type="SPOT", location=P((1.9, 0, 1.0)))
            sp = bpy.context.object; sp.data.energy = 2200; sp.data.spot_size = 0.8; sp.data.spot_blend = 0.5
            sp.data.color = (1.0, 0.9, 0.7)
            sp.rotation_euler = (R @ Vector((1, 0, -0.05))).to_track_quat("-Z", "Y").to_euler()

    def soldat(pos, rotz=0):
        cyl("soldat_bein", Vector(pos) + Vector((0, 0, 0.45)), 0.18, 0.9, M_SOLDIER, verts=8)
        cyl("soldat_koerper", Vector(pos) + Vector((0, 0, 1.25)), 0.24, 0.75, M_SOLDIER, verts=8)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=6, radius=0.16, location=Vector(pos) + Vector((0, 0, 1.8)))
        bpy.context.object.data.materials.append(M_SKIN_D)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=6, radius=0.18, location=Vector(pos) + Vector((0, 0, 1.88)))
        o = bpy.context.object; o.scale = (1, 1, 0.55); o.data.materials.append(M_SOLDIER)
        cyl("gewehr", Vector(pos) + Vector((0.15, 0.2, 1.35)), 0.03, 1.0, M_TIRE, verts=6, rot=(0.4, 0, rotz))

    def flutlicht(pos, ziel):
        cyl("mast", Vector(pos) + Vector((0, 0, 9)), 0.18, 18, M_METAL, verts=6)
        cube("lampenkopf", Vector(pos) + Vector((0, 0, 18.3)), (1.4, 0.3, 0.6), M_METAL)
        for k in range(4):
            cube("lampe", Vector(pos) + Vector((-1.05 + k * 0.7, -0.32, 18.3)), (0.28, 0.03, 0.4), M_FLOOD)
        bpy.ops.object.light_add(type="SPOT", location=Vector(pos) + Vector((0, -0.5, 18.2)))
        sp = bpy.context.object; sp.data.energy = 90000; sp.data.spot_size = 0.55; sp.data.spot_blend = 0.6
        sp.data.color = (1.0, 0.93, 0.8)
        sp.rotation_euler = (Vector(ziel) - sp.location).to_track_quat("-Z", "Y").to_euler()

    SACK = Masse("sandsaecke", M_SANDBAG)
    def sandsaecke(x0, x1, y, rotz=0, reihen=3):
        n = int((x1 - x0) / 0.85)
        for r in range(reihen):
            for i in range(n):
                SACK.quader((x0 + i * 0.85 + (r % 2) * 0.42, y, 0.22 + r * 0.38), (0.4, 0.3, 0.18), (0, 0, random.uniform(-0.08, 0.08)))

    # Fahrzeuge der somalischen Armee (Absperrung, Scheinwerfer auf das Flugzeug)
    truck((-34, 24, 0), math.radians(-35))
    truck((30, 27, 0), math.radians(215))
    truck((-58, 40, 0), math.radians(-10), licht=False)
    truck((-30, -14, 0), math.radians(20))            # links vor dem Flugzeug, Scheinwerfer aufs Heck
    truck((-46, -6, 0), math.radians(5), licht=False)
    jeep((26, -16, 0), math.radians(165))              # rechts vorne, Licht auf den Bug
    jeep((-14, -19, 0), math.radians(40), licht=False)
    # Absperrring der Armee rund um das Flugzeug (aus jedem Winkel sichtbar)
    for k in range(16):
        ang = k / 16 * math.tau
        if abs(((ang - math.radians(-110)) + math.pi) % math.tau - math.pi) < math.radians(18):
            continue  # Sichtachse der Hauptkamera frei lassen
        r = random.uniform(34, 40)
        px, py = math.cos(ang) * r * 1.25, math.sin(ang) * r
        rot = math.atan2(-py, -px) + random.uniform(-0.3, 0.3)
        if k % 3 == 0:
            truck((px, py, 0), rot, licht=(k % 2 == 0))
        else:
            jeep((px, py, 0), rot, licht=(k % 2 == 1))
        for m in range(random.randint(1, 3)):
            soldat((px + random.uniform(-3, 3), py + random.uniform(-3, 3), 0))
    # Treppenwagen und Tankwagen
    cube("treppenwagen", (11, -11, 0.7), (2.2, 1.0, 0.5), M_STAIRS)
    for k in range(10):
        cube("stufe", (11 - 1.5 + k * 0.25, -8.0, 0.9 + k * 0.22), (0.15, 0.7, 0.04), M_STAIRS)
    cube("treppe_seite", (11.0, -8.6, 2.0), (1.6, 0.03, 0.9), M_STAIRS, rot=(0, -0.65, 0))
    cube("tankwagen_tank", (-30, 12, 2.0), (3.5, 1.2, 1.1), M_FUEL)
    cube("tankwagen_kabine", (-25.6, 12, 1.6), (0.9, 1.1, 1.0), M_FUEL)
    for dx in (-32, -28.5, -25.8):
        for dy in (10.9, 13.1):
            cyl("rad", (dx, dy, 0.5), 0.5, 0.35, M_TIRE, verts=10, rot=(math.pi / 2, 0, 0))
    # Soldaten an der Absperrung
    for x, y in [(-31, 21), (-29, 22.5), (-36.5, 20), (27, 23), (25, 24.5), (33, 23.5), (-40, 26),
                 (-24, -16), (-22.5, -17.5), (-26, -11), (22, -18), (23.5, -19.5), (-12, -21), (-16, -22)]:
        soldat((x, y, 0))
    # Flutlichtmasten
    flutlicht((-48, 34, 0), (0, 0, 0))
    flutlicht((52, 36, 0), (5, 0, 0))
    flutlicht((-40, -20, 0), (-5, 0, 0))
    # Sandsäcke, Fässer, Kisten
    sandsaecke(-45, -36, 17)
    sandsaecke(34, 42, 19)
    sandsaecke(-27, -19, -21, reihen=2)
    sandsaecke(14, 21, -22, reihen=2)
    for i in range(7):
        cyl("fass", (-39 + random.uniform(-2, 2), 15 + random.uniform(-1.5, 1.5), 0.45), 0.3, 0.9,
            random.choice([M_ARMY, M_METAL, M_STAIRS]), verts=10)
    for i in range(4):
        cube("kiste", (44 + i * 1.3, 15 + random.uniform(-0.5, 0.5), 0.4), (0.6, 0.5, 0.4), M_CANVAS)
    # Zaun entlang des Vorfelds
    ZAUN = Masse("zaun", M_METAL)
    for i in range(-40, 41):
        ZAUN.zylinder((i * 3.5, 46, 1.2), 0.05, 2.4, verts=5)
    ZAUN.fertig()
    for zh in (0.6, 1.3, 2.0):
        cube("zaundraht", (0, 46, zh), (140, 0.01, 0.01), M_METAL)
    # Hangar
    cube("hangar", (-90, 62, 7), (16, 10, 7), M_HANGAR)
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=10.5, depth=32, location=(-90, 62, 13.5), rotation=(0, math.pi / 2, 0))
    o = bpy.context.object; o.scale = (1, 1, 1); o.data.materials.append(M_HANGAR)
    cube("hangartor", (-90, 51.9, 5), (10, 0.1, 5), M_WIN)
    bpy.ops.object.light_add(type="AREA", location=(-90, 50, 6), rotation=(math.pi / 2, 0, 0))
    hl = bpy.context.object; hl.data.energy = 6000; hl.data.size = 18; hl.data.color = (1, 0.8, 0.55)
    # Windsack
    cyl("windsack_mast", (70, -20, 3), 0.08, 6, M_METAL, verts=6)
    cyl("windsack", (71.2, -20, 5.8), 0.35, 2.2, mat("windsack_stoff", (0.9, 0.35, 0.05), 0.8), verts=8,
        rot=(0, math.pi / 2, 0), r2=0.15)
    # Tower: Leuchtfeuer (blinkt) + Radar (dreht sich)
    cube("leuchtfeuer", (40, 80, 23.2), (0.4, 0.4, 0.4), M_BEACON)
    bpy.ops.object.light_add(type="POINT", location=(40, 80, 24))
    bl = bpy.context.object; bl.data.energy = 8000; bl.data.color = (1, 0.05, 0.03)
    anim_objs["leuchtfeuer"] = bl
    bpy.ops.object.empty_add(location=(40, 84, 23))
    radar = bpy.context.object
    cyl("radarmast", (40, 84, 22.5), 0.15, 1.5, M_METAL, verts=6)
    bpy.ops.mesh.primitive_cube_add(location=(40, 84, 23.6)); rd = bpy.context.object
    rd.scale = (2.2, 0.15, 0.5); rd.data.materials.append(M_METAL); rd.parent = radar
    rd.location = (0, 0, 0.6)
    anim_objs["radar"] = radar
    # Hügel am Horizont mit Lichtern der Stadt
    HUEGEL = Masse("huegel", M_HILL)
    for i in range(70):
        a = i / 70 * math.tau
        r = random.uniform(230, 280)
        HUEGEL.kugel((math.cos(a) * r, math.sin(a) * r, 0), 1, (random.uniform(25, 45), random.uniform(25, 45), random.uniform(8, 26)))
    HUEGEL.fertig()
    STADT = Masse("stadtlichter", M_CITY)
    for i in range(160):
        a = random.uniform(math.radians(40), math.radians(140))
        r = random.uniform(190, 225)
        STADT.quader((math.cos(a) * r, math.sin(a) * r, random.uniform(0.5, 4)), (0.35, 0.35, 0.35))
    STADT.fertig()
    # Dünen, Grasbüschel, Steine im Vordergrund (für Bodenperspektiven)
    DUENE = Masse("duenen", M_SAND)
    for i in range(26):
        dx = random.choice([random.uniform(-45, -18), random.uniform(8, 45)])
        DUENE.kugel((dx, random.uniform(-55, -17), -0.2), 1,
                    (random.uniform(3, 7), random.uniform(1.5, 3), random.uniform(0.4, 1.0)), sub=2)
    DUENE.fertig()
    GRAS = Masse("gras", M_GRASS)
    for i in range(420):
        x = random.uniform(-45, 45); y = random.uniform(-50, -16)
        for k in range(random.randint(3, 6)):
            GRAS.kegel((x + random.uniform(-0.15, 0.15), y + random.uniform(-0.15, 0.15), 0.0), 0.025, random.uniform(0.12, 0.35),
                       (random.uniform(-0.4, 0.4), random.uniform(-0.4, 0.4), 0))
    GRAS.fertig()
    STEIN = Masse("steine", M_STONE)
    for i in range(140):
        STEIN.kugel((random.uniform(-45, 45), random.uniform(-50, -16), 0.0), random.uniform(0.05, 0.2), (1, 1, 0.6))
    STEIN.fertig()
    SACK.fertig()
    # zusätzliche Palmen nahe an den Bildrändern
    for x, y in [(-38, -20), (36, -24), (-55, -8), (60, -12), (-20, -46), (24, -48)]:
        palm(Vector((x, y, 0)), random.uniform(8, 12))

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
    cam.location = (-10, -15, 1.0); look_at(cam, (-1.5, -3.0, 2.6)); cam.data.lens = 22
elif args.shot == "nase":
    cam.location = (40, -16, 1.2); look_at(cam, (17, 0, 3.0)); cam.data.lens = 26
elif args.shot == "fenster":
    cam.location = (6, -8.5, 3.0); look_at(cam, (0, -1.9, 3.5)); cam.data.lens = 30
elif args.shot == "rutsche":
    cam.location = (-30, -26, 1.6); look_at(cam, (2, 0, 2.5)); cam.data.lens = 26
elif args.shot == "boden_tief":
    cam.location = (-4, -24, 0.35); look_at(cam, (4, 0, 3.8)); cam.data.lens = 32
else:
    raise SystemExit(f"unbekannter shot {args.shot}")

# ---------- Render ----------
w, h = map(int, args.res.split("x"))
scn.render.resolution_x, scn.render.resolution_y = w, h
scn.view_settings.view_transform = "AgX"
scn.view_settings.look = "AgX - Punchy"
if args.engine == "eevee":
    import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import anim_common
    anim_common.engine(scn, "eevee", args.samples, bloom=False)
    bg.inputs["Strength"].default_value = 1.1
    scn.render.engine = "BLENDER_EEVEE_NEXT"
    scn.eevee.taa_render_samples = args.samples
    scn.eevee.use_shadows = True
    scn.eevee.use_raytracing = False
    fill.data.energy = 2500
    moon.data.energy = 0.9
    M_SAND.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.26, 0.21, 0.15, 1)
    scn.eevee.volumetric_end = 260
    scn.eevee.volumetric_tile_size = "8"
    # Glühen (Bloom) über den Compositor
    scn.use_nodes = True
    nt = scn.node_tree; rl = nt.nodes["Render Layers"]; comp = nt.nodes["Composite"]
    gl = nt.nodes.new("CompositorNodeGlare"); gl.glare_type = "FOG_GLOW"; gl.quality = "MEDIUM"; gl.threshold = 1.2; gl.size = 8
    nt.links.new(rl.outputs["Image"], gl.inputs["Image"]); nt.links.new(gl.outputs["Image"], comp.inputs["Image"])
else:
    scn.render.engine = "CYCLES"
    scn.cycles.device = "CPU"
    scn.cycles.samples = args.samples
    scn.cycles.use_denoising = True
    scn.cycles.max_bounces = 4

if args.pfad:
    import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import anim_common, json
    P = json.load(open(args.pfad))
    anim_common.kamerapfad(scn, cam, args.pfad)
    n = P["frames"]; off = P.get("offset", 0)
    scn.frame_start = 1 + off; scn.frame_end = n + off
    # Animation: Feuer flackert, Leuchtfeuer blinkt, Radar dreht sich
    rnd = random.Random(5)
    for f in range(1, n + off + 2):
        t = (f - 1) / 30.0
        if args.fire > 0:
            fl.data.energy = 20000 * args.fire * (0.75 + 0.5 * rnd.random()); fl.data.keyframe_insert("energy", frame=f)
            an = 1.0 if f >= args.zuendung else 0.0
            if args.zuendung and f < args.zuendung + 8:
                an = max(0.0, min(1.0, (f - args.zuendung) / 8))
            fl.data.energy *= an; fl.data.keyframe_insert("energy", frame=f)
            for ob in bpy.data.objects:
                if ob.name.startswith("flamme") and (f % 2 == 1 or an < 1):
                    ob.scale = (an, an, max(0.001, an * (0.7 + 0.6 * rnd.random()))); ob.keyframe_insert("scale", frame=f)
        if "leuchtfeuer" in anim_objs:
            anim_objs["leuchtfeuer"].data.energy = 8000 if (t % 1.2) < 0.25 else 0
            anim_objs["leuchtfeuer"].data.keyframe_insert("energy", frame=f)
    if "radar" in anim_objs:
        r_ = anim_objs["radar"]; r_.rotation_euler = (0, 0, 0); r_.keyframe_insert("rotation_euler", frame=1)
        r_.rotation_euler = (0, 0, math.tau * (n + off) / 30 / 4); r_.keyframe_insert("rotation_euler", frame=n + off + 1)
        for fc in r_.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"
    scn.render.fps = 30
    scn.render.filepath = args.out  # z. B. /pfad/shot_####.png
    scn.render.image_settings.file_format = "PNG"
    bpy.ops.render.render(animation=True)
    print("FERTIG_ANIM", args.out, n)
else:
    scn.render.filepath = args.out
    bpy.ops.render.render(write_still=True)
    print("FERTIG", args.out)
