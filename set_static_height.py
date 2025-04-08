import bpy

def is_keyframe(ob, frame, data_path, array_index=-1):
    if ob is not None and ob.animation_data is not None and ob.animation_data.action is not None:
        for fcu in ob.animation_data.action.fcurves:
            if fcu.data_path == data_path:
                if array_index == -1 or fcu.array_index == array_index:
                    return frame in (p.co.x for p in fcu.keyframe_points)
    return False

bpy.types.Object.is_keyframe = is_keyframe

bpy.context.scene.frame_set(0)
staticloc = bpy.data.objects['rig'].pose.bones["b__ROOT_bind__"].location

for currframe in range(1, bpy.context.scene.frame_end):
    obj = bpy.data.objects['rig']
    bpy.context.scene.frame_set(currframe)
    if bpy.context.object.is_keyframe(currframe, obj.pose.bones["b__ROOT_bind__"].path_from_id("location")):
        obj.pose.bones["b__ROOT_bind__"].location = staticloc
        obj.pose.bones["b__ROOT_bind__"].keyframe_insert(data_path="location", frame=currframe)