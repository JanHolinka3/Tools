import bpy #type: ignore

odecetZ=720.0

def main():

    bpy.ops.object.mode_set(mode='OBJECT')

    ObjectworldMatrix = bpy.context.active_object.matrix_world

    meshObjektu = bpy.context.active_object.data

    for vert in meshObjektu.vertices:
        if vert.select == True:
            bpy.ops.object.text_add()
            textObjekt = bpy.context.active_object
            textObjekt.location = ObjectworldMatrix @ vert.co
            #textObjekt.data.body = str(vert.index)
            textObjekt.data.body = str("{:.3f}".format(round(vert.co[2]+odecetZ,3)))
            #textObjekt.data.body = str(vert.index)
            textObjekt.data.size = 0.6
            textObjekt.data.offset_x = 0.05
            textObjekt.data.offset_y = 0.05
            #material = bpy.data.materials['ColorBaseMat']
            textObjekt.data.materials.append(bpy.data.materials['ColorBaseMat'])
            #return
    return

main()