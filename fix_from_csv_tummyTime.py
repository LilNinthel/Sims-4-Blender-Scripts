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
        
dict = {}

boneRotateDict = {
'b__L_Thigh__': [{'axis':'Z', 'rotation': 0.3}],
'b__R_Thigh__': [{'axis':'Z', 'rotation': 0.3}],

'b__L_Calf__': [{'axis':'Y', 'rotation': -0.3}],
'b__R_Calf__': [{'axis':'Y', 'rotation': 0.3}],

'b__L_UpperArm__': [{'axis':'Y', 'rotation': -0.570}],
'b__R_UpperArm__': [{'axis':'Y', 'rotation': 0.570}],

'b__L_Forearm__': [{'axis':'Z', 'rotation': -0.300}],
'b__R_Forearm__': [{'axis':'Z', 'rotation': -0.300}],
}


#The bones in this array will be prevented from falling below 0 height by adjusting the position of the root bone. Use with caution, can cause jerkiness.
# anchors = ["b__R_Toe__","b__L_Toe__","b__R_Foot__","b__L_Foot__","b__R_Hand__","b__L_Hand__","b__R_Calf__","b__L_Calf__","b__R_Elbow__","b__L_Elbow__"]
anchors = ["b__R_Toe__","b__L_Toe__","b__R_Foot__","b__L_Foot__","b__R_Calf__","b__L_Calf__"]

for currframe in targetData:
    if currframe.frame not in dict:
        dict[currframe.frame] = {}
    dict[currframe.frame][currframe.bone] = currframe

for currframe in range(0, bpy.context.scene.frame_end):
    bpy.context.scene.frame_set(currframe)
    obj = bpy.data.objects['rig']
    
    desiredLoc = dict[currframe]["b__ROOT_bind__"].globalLoc
    
    actualLoc = obj.pose.bones["b__ROOT_bind__"].head
    
    diff = actualLoc-desiredLoc
    
    obj.pose.bones["b__ROOT_bind__"].location[0] = obj.pose.bones["b__ROOT_bind__"].location[0] - diff[2]
    obj.pose.bones["b__ROOT_bind__"].location[1] = obj.pose.bones["b__ROOT_bind__"].location[1] + diff[1]
    obj.pose.bones["b__ROOT_bind__"].location[2] = obj.pose.bones["b__ROOT_bind__"].location[2] - diff[0] + 0.0
    
#    obj.pose.bones["b__ROOT_bind__"].location = dict[currframe]["b__ROOT_bind__"].globalLoc
    obj.pose.bones["b__ROOT_bind__"].keyframe_insert(data_path="location", frame=currframe)
    
    for key in obj.pose.bones.keys():
        obj.pose.bones[key].bone.select = False
    
        if obj.is_keyframe(currframe,obj.pose.bones[key].path_from_id("rotation_quaternion")):
            if key in boneRotateDict.keys():
                obj.pose.bones[key].bone.select = True
                for rotation in boneRotateDict[key]:
                    bpy.ops.transform.rotate(value=rotation['rotation'], orient_axis=rotation['axis'], orient_type = 'LOCAL')
                    obj.pose.bones[key].keyframe_insert(data_path="rotation_quaternion", frame=currframe)
                    obj.pose.bones[key].bone.select = False
    
    for key in anchors:
        bpy.context.scene.frame_set(currframe)
        obj = bpy.data.objects['rig']
    
        if obj.pose.bones[key].head.z < 0.0:
  #            if currframe >= 78 and currframe < 133 and key in ["b__R_Toe__","b__L_Toe__"]:
  #                continue
            desiredLoc = Vector((obj.pose.bones[key].head.x,obj.pose.bones[key].head.y,0.0))
            actualLoc = obj.pose.bones[key].head

            diff = actualLoc-desiredLoc
            obj.pose.bones["b__ROOT_bind__"].location.x = obj.pose.bones["b__ROOT_bind__"].location.x - diff.z
            obj.pose.bones["b__ROOT_bind__"].keyframe_insert(data_path="location", frame=currframe)

bpy.ops.wm.save_mainfile()
bpy.ops.wm.quit_blender()