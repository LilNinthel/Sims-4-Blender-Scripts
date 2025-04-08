import bpy
from mathutils import Matrix, Vector
import os
import csv

class Expando(object):
    pass

name = bpy.context.object.name
filepath = bpy.data.filepath
directory = os.path.dirname(filepath)

sourceCsv = os.path.join( directory , filepath+".csv")

targetData = []

with open(sourceCsv, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        rowData = Expando()
        
        rowData.frame = int(row[0])
        rowData.bone = row[1]
        glbTmp = row[2].split("(")[1].split(")")[0].split(", ")
        rowData.globalLoc = Vector((float(glbTmp[0]),float(glbTmp[1]),float(glbTmp[2])))
        glbTmp = row[3].split("(")[1].split(")")[0].split(", ")
        rowData.localLoc = Vector((float(glbTmp[0]),float(glbTmp[1]),float(glbTmp[2])))
        
        targetData.append(rowData)
#        print(rowData)
        

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
          obj.pose.bones["b__ROOT_bind__"].location[0] = obj.pose.bones["b__ROOT_bind__"].location[0]
        else:
          obj.pose.bones[key].location = [0.0,0.0,0.0]
        obj.pose.bones[key].keyframe_insert(data_path="location", frame=currframe)

#The root bone's location will be adjusted so that the anchorBone's absolute position is exactly the same as in the original clip the .csv was exported from.
#This is useful when another animation contains a prop that is meant to align with a body part in this animation, such as bottle feeding
#It can also be used to keep a Sim's leg planted on the ground instead of them slightly wobbling due to rig differences. It's useful to adjust the offsets when doing this to keep the Sim centered
anchorBone = "b__L_Toe__"

for currframe in targetData:
    key = currframe.bone
    
    if key == anchorBone:
        bpy.context.scene.frame_set(currframe.frame)
        
        obj = bpy.data.objects['rig']
        desiredLoc = currframe.globalLoc
        actualLoc = obj.pose.bones[key].head
    
        diff = actualLoc-desiredLoc
        
        
#        obj.pose.bones[key].location = desiredLoc
        obj.pose.bones["b__ROOT_bind__"].location[0] = obj.pose.bones["b__ROOT_bind__"].location[0] - diff[2] + 0.00 #You can adjust the added/subtracted values to make adjustments in positioning to the entire animation
        obj.pose.bones["b__ROOT_bind__"].location[1] = obj.pose.bones["b__ROOT_bind__"].location[1] + diff[1] + 0.00 #You can adjust the added/subtracted values to make adjustments in positioning to the entire animation
        obj.pose.bones["b__ROOT_bind__"].location[2] = obj.pose.bones["b__ROOT_bind__"].location[2] - diff[0] + 0.02605 #You can adjust the added/subtracted values to make adjustments in positioning to the entire animation
        obj.pose.bones["b__ROOT_bind__"].keyframe_insert(data_path="location", frame=currframe.frame)
        
        bpy.context.scene.frame_set(currframe.frame)
        obj = bpy.data.objects['rig']
        
        if obj.pose.bones["b__ROOT_bind__"].head.z < 0.0:
            desiredLoc = Vector((obj.pose.bones["b__ROOT_bind__"].head.x,obj.pose.bones["b__ROOT_bind__"].head.y,0.0))
            actualLoc = obj.pose.bones["b__ROOT_bind__"].head
    
            diff = actualLoc-desiredLoc
#            obj.pose.bones["b__ROOT_bind__"].location = desiredLoc
            obj.pose.bones["b__ROOT_bind__"].location.x = obj.pose.bones["b__ROOT_bind__"].location.x - diff.z
#            obj.pose.bones["b__ROOT_bind__"].location[1] = obj.pose.bones["b__ROOT_bind__"].location[1] - diff[1]
#            obj.pose.bones["b__ROOT_bind__"].location[2] = obj.pose.bones["b__ROOT_bind__"].location[2] - diff[0] + 0.0
        
            obj.pose.bones["b__ROOT_bind__"].keyframe_insert(data_path="location", frame=currframe.frame)
#        obj.pose.bones[key].keyframe_insert(data_path="location", frame=currframe.frame)

bpy.ops.wm.save_mainfile()
bpy.ops.wm.quit_blender()