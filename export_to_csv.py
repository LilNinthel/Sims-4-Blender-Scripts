import bpy
from mathutils import Matrix, Vector
import os

name = bpy.context.object.name
filepath = bpy.data.filepath
directory = os.path.dirname(filepath)
csv_file = filepath + ".csv"

def is_keyframe(ob, frame, data_path, array_index=-1):
    if ob is not None and ob.animation_data is not None and ob.animation_data.action is not None:
        for fcu in ob.animation_data.action.fcurves:
            if fcu.data_path == data_path:
                if array_index == -1 or fcu.array_index == array_index:
                    return frame in (p.co.x for p in fcu.keyframe_points)
    return False

bpy.types.Object.is_keyframe = is_keyframe


f = open( csv_file, 'w' )


for currframe in range(0, bpy.context.scene.frame_end):
    bpy.context.scene.frame_set(currframe)
    obj = bpy.data.objects['rig']

    for key in obj.pose.bones.keys():
      # if key == "b__L_Toe__" or key == "b__R_Toe__"  or key == "b__ROOT_bind__":
#        print(abs(obj.pose.bones[key].head[0]))
        # print(f'{currframe}: {key} - {obj.pose.bones[key].head} - {obj.pose.bones[key].location}')
      f.write(f"{currframe},\"{key}\",\"{obj.pose.bones[key].head}\",\"{obj.pose.bones[key].location}\"\n")
f.close()

bpy.ops.wm.quit_blender()