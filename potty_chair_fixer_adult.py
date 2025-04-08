#This script can be used as a template for adjusting bone rotation throughout a clip.
#More complex animations could use conditionals or functions to modify the amount of rotation depending on the frame
import bpy

def is_keyframe(ob, frame, data_path, array_index=-1):
    if ob is not None and ob.animation_data is not None and ob.animation_data.action is not None:
        for fcu in ob.animation_data.action.fcurves:
            if fcu.data_path == data_path:
                if array_index == -1 or fcu.array_index == array_index:
                    return frame in (p.co.x for p in fcu.keyframe_points)
    return False

bpy.types.Object.is_keyframe = is_keyframe

kneeBones = ["b__L_Calf__","b__R_Calf__"]
hipBones = ["b__L_Thigh__","b__R_Thigh__"]

for currframe in range(0, bpy.context.scene.frame_end):
    bpy.context.scene.frame_set(currframe)
    obj = bpy.data.objects['rig']
    for key in obj.pose.bones.keys():
      obj.pose.bones[key].bone.select = False
      if obj.is_keyframe(currframe,obj.pose.bones[key].path_from_id("location")):
        if key == "b__ROOT_bind__":
          obj.pose.bones["b__ROOT_bind__"].location[0] = obj.pose.bones["b__ROOT_bind__"].location[0]
        else:
          obj.pose.bones[key].location = [0.0,0.0,0.0]
        obj.pose.bones[key].keyframe_insert(data_path="location", frame=currframe)
      if obj.is_keyframe(currframe,obj.pose.bones[key].path_from_id("rotation_quaternion")):
        if key in hipBones:
          obj.pose.bones[key].bone.select = True
          bpy.ops.transform.rotate(value=-0.700, orient_axis='Z', orient_type = 'LOCAL')
          obj.pose.bones[key].keyframe_insert(data_path="rotation_quaternion", frame=currframe)
          obj.pose.bones[key].bone.select = False
        if key in kneeBones:
          obj.pose.bones[key].bone.select = True
          bpy.ops.transform.rotate(value=0.700, orient_axis='Z', orient_type = 'LOCAL')
          obj.pose.bones[key].keyframe_insert(data_path="rotation_quaternion", frame=currframe)
          obj.pose.bones[key].bone.select = False

        
bpy.ops.wm.save_mainfile()
bpy.ops.wm.quit_blender()