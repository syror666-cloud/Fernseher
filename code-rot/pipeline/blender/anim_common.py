"""Gemeinsame Helfer für animierte Blender-Szenen (EEVEE, Kamerapfade, Lichtflackern)."""
import bpy, json, math, random


def engine(scn, name="eevee", samples=8, bloom=True):
    scn.view_settings.view_transform = "AgX"
    scn.view_settings.look = "AgX - Punchy"
    if name == "eevee":
        scn.render.engine = "BLENDER_EEVEE_NEXT"
        scn.eevee.taa_render_samples = samples
        scn.eevee.use_shadows = True
        scn.eevee.use_raytracing = False
        # Performance (CPU-Rendering): kein Volumen, Schatten nur für Hauptlichter
        if scn.world and scn.world.node_tree:
            wo = scn.world.node_tree.nodes["World Output"]
            for l in list(scn.world.node_tree.links):
                if l.to_socket == wo.inputs["Volume"]:
                    scn.world.node_tree.links.remove(l)
        for ob in scn.objects:
            if ob.type == "LIGHT" and ob.data.type in ("SPOT", "POINT", "AREA") and ob.data.energy < 5000:
                ob.data.use_shadow = False
        scn.eevee.shadow_ray_count = 1; scn.eevee.shadow_step_count = 2
        if bloom:
            scn.use_nodes = True
            nt = scn.node_tree
            rl = nt.nodes["Render Layers"]; comp = nt.nodes["Composite"]
            gl = nt.nodes.new("CompositorNodeGlare"); gl.glare_type = "FOG_GLOW"; gl.quality = "MEDIUM"
            gl.threshold = 1.2; gl.size = 8
            nt.links.new(rl.outputs["Image"], gl.inputs["Image"]); nt.links.new(gl.outputs["Image"], comp.inputs["Image"])
    else:
        scn.render.engine = "CYCLES"; scn.cycles.device = "CPU"; scn.cycles.samples = samples
        scn.cycles.use_denoising = True; scn.cycles.max_bounces = 4


def kamerapfad(scn, cam, pfad_datei):
    """Keyframes für Kamera + Zielpunkt. Datei: {"frames": N, "offset": 0, "keys": [{"f","loc","ziel","lens","shake"}]}"""
    P = json.load(open(pfad_datei))
    ziel = bpy.data.objects.new("kameraziel", None); scn.collection.objects.link(ziel)
    cam.constraints.clear()
    tc = cam.constraints.new("TRACK_TO"); tc.target = ziel; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"
    for k in P["keys"]:
        f = k["f"] + 1
        cam.location = k["loc"]; cam.keyframe_insert("location", frame=f)
        ziel.location = k["ziel"]; ziel.keyframe_insert("location", frame=f)
        cam.data.lens = k.get("lens", 24); cam.data.keyframe_insert("lens", frame=f)
    for o in (cam, ziel):
        for fc in o.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = "BEZIER"; kp.easing = "AUTO"
                kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"
    # Handkamera-Wackeln (Noise-Modifier) wenn gewünscht
    shake = P.get("shake", 0)
    if shake:
        for fc in ziel.animation_data.action.fcurves:
            m = fc.modifiers.new("NOISE"); m.strength = shake; m.scale = 6; m.phase = random.uniform(0, 100)
    n = P["frames"]; off = P.get("offset", 0)
    scn.frame_start = 1 + off; scn.frame_end = P.get("bis", n) + off
    scn.render.fps = 30
    return n, off


def flackern(licht, basis, von, bis, staerke=0.5, seed=1, takt=1):
    rnd = random.Random(seed)
    for f in range(von, bis + 1, takt):
        licht.data.energy = basis * (1 - staerke / 2 + staerke * rnd.random())
        licht.data.keyframe_insert("energy", frame=f)


def blitze(licht, energie, frames):
    """Mündungsfeuer / Strobo: Licht nur in den angegebenen Frames an."""
    alle = set(frames)
    lo, hi = min(alle) - 1, max(alle) + 1
    for f in range(max(1, lo), hi + 1):
        licht.data.energy = energie if f in alle else 0
        licht.data.keyframe_insert("energy", frame=f)
        for fc in licht.data.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"


class Masse:
    """Sammelt viele Primitive in EINEM Mesh-Objekt (schnell statt tausender Einzelobjekte)."""
    def __init__(self, name, material):
        import bmesh
        self.bm = bmesh.new(); self.name = name; self.material = material

    def _add(self, fn, loc, rot=(0, 0, 0), scale=(1, 1, 1)):
        import bmesh, mathutils
        tmp = bmesh.new(); fn(tmp)
        M = mathutils.Matrix.LocRotScale(mathutils.Vector(loc), mathutils.Euler(rot), mathutils.Vector(scale))
        bmesh.ops.transform(tmp, matrix=M, verts=tmp.verts)
        me = bpy.data.meshes.new("tmp"); tmp.to_mesh(me); tmp.free(); self.bm.from_mesh(me); bpy.data.meshes.remove(me)

    def quader(self, loc, scale, rot=(0, 0, 0)):
        import bmesh
        self._add(lambda b: bmesh.ops.create_cube(b, size=2.0), loc, rot, scale)

    def zylinder(self, loc, r, h, rot=(0, 0, 0), verts=8):
        import bmesh
        self._add(lambda b: bmesh.ops.create_cone(b, cap_ends=True, segments=verts, radius1=r, radius2=r, depth=h), loc, rot)

    def kugel(self, loc, r, scale=(1, 1, 1), sub=1):
        import bmesh
        self._add(lambda b: bmesh.ops.create_icosphere(b, subdivisions=sub, radius=r), loc, (0, 0, 0), scale)

    def fertig(self):
        me = bpy.data.meshes.new(self.name); self.bm.to_mesh(me); self.bm.free()
        o = bpy.data.objects.new(self.name, me); bpy.context.scene.collection.objects.link(o)
        o.data.materials.append(self.material)
        return o
