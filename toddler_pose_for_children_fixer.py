import bpy

def is_keyframe(ob, frame, data_path, array_index=-1):
    if ob is not None and ob.animation_data is not None and ob.animation_data.action is not None:
        for fcu in ob.animation_data.action.fcurves:
            if fcu.data_path == data_path:
                if array_index == -1 or fcu.array_index == array_index:
                    return frame in (p.co.x for p in fcu.keyframe_points)
    return False

bpy.types.Object.is_keyframe = is_keyframe

for currframe in range(0, bpy.context.scene.frame_end):
    bpy.context.scene.frame_set(currframe)
    obj = bpy.data.objects['rig']
    for key in obj.pose.bones.keys():
      if obj.is_keyframe(currframe,obj.pose.bones[key].path_from_id("location")):
        if key == "b__ROOT_bind__":
          obj.pose.bones["b__ROOT_bind__"].location[0] = obj.pose.bones["b__ROOT_bind__"].location[0] + 0.27388
        else:
          obj.pose.bones[key].location = [0.0,0.0,0.0]
        obj.pose.bones[key].keyframe_insert(data_path="location", frame=currframe)
        
bpy.ops.wm.save_mainfile()
bpy.ops.wm.quit_blender()