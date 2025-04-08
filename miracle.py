import bpy
from mathutils import Matrix, Vector

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
    anchor =  obj.pose.bones["b__L_Toe__"]
    midpoint = (obj.pose.bones["b__L_Toe__"].head[0] - obj.pose.bones["b__R_Toe__"].head[0]) / 2
    print(midpoint)
    
    desiredLoc = Vector(( midpoint,-0.08,0.0))
    actualLoc = obj.pose.bones["b__L_Toe__"].head
    
    
    diff = actualLoc-desiredLoc
    
    print(f'diff: {diff}')

    xDiff = actualLoc[0]-desiredLoc[0]
    yDiff = actualLoc[1]-desiredLoc[1]
    zDiff = actualLoc[2]-desiredLoc[2]
    
    rtest = obj.pose.bones["b__ROOT_bind__"].head - diff
    
    print(f'rtest: {rtest}')
    print(obj.pose.bones["b__ROOT_bind__"].head[0])
    print(obj.pose.bones["b__ROOT_bind__"].head.x)
    
    
    rootDesiredLoc = Vector((obj.pose.bones["b__ROOT_bind__"].head[0]-xDiff, obj.pose.bones["b__ROOT_bind__"].head[1] + yDiff, obj.pose.bones["b__ROOT_bind__"].head[2] - zDiff))
    
    globTgt = Vector((xDiff,yDiff,zDiff))
    
    print(obj.pose.bones["b__ROOT_bind__"].matrix.inverted() @ rtest)
    
#    pbone_global_loc = (obj.matrix_world @ obj.pose.bones["b__ROOT_bind__"].matrix).inverted() 
    
    
    rootDesiredLocLocal = obj.pose.bones["b__ROOT_bind__"].matrix.inverted() @ rtest

    print(f'desiredLoc: {desiredLoc}')
    print(f'actualLoc: {actualLoc}')
    print(f'{xDiff},{yDiff},{zDiff}')
    print(f'{currframe}: b__ROOT_bind__ - {obj.pose.bones["b__ROOT_bind__"].head} - {obj.pose.bones["b__ROOT_bind__"].location}')
    print(f'globTgt: {globTgt}')
    print(f'rootDesiredLoc: {rootDesiredLoc}')
#    print(f'pbone_global_loc: {pbone_global_loc}')
    print(f'rootDesiredLocLocal: {rootDesiredLocLocal}')
#    print(pbone_global_loc)
    

    for key in obj.pose.bones.keys():
      if key == "b__L_Toe__" or key == "b__R_Toe__":
#        print(abs(obj.pose.bones[key].head[0]))
        print(f'{currframe}: {key} - {obj.pose.bones[key].head} - {obj.pose.bones[key].location}')
      if obj.is_keyframe(currframe,obj.pose.bones[key].path_from_id("location")):
        if key == "b__ROOT_bind__":
#         bpy.ops.object.mode_set(mode='EDIT', toggle=False)
#          obj.pose.bones["b__ROOT_bind__"].translate(pbone_global_loc)
#          bpy.ops.object.mode_set(mode='POSE', toggle=False)
#           obj.pose.bones["b__ROOT_bind__"].location = obj.pose.bones["b__ROOT_bind__"].location - diff
#           actualLoc = (obj.matrix_world @ obj.pose.bones["b__L_Toe__"].matrix).inverted() 
          # actualLoc = obj.pose.bones["b__L_Toe__"].head
          # print(f'actualLoc: {actualLoc}')
          obj.pose.bones["b__ROOT_bind__"].location[0] = obj.pose.bones["b__ROOT_bind__"].location[0] - diff[2]
          obj.pose.bones["b__ROOT_bind__"].location[1] = obj.pose.bones["b__ROOT_bind__"].location[1] + diff[1]
          obj.pose.bones["b__ROOT_bind__"].location[2] = obj.pose.bones["b__ROOT_bind__"].location[2] - diff[0]
        else:
          obj.pose.bones[key].location = [0.0,0.0,0.0]
          obj.pose.bones[key].keyframe_insert(data_path="location", frame=currframe)
