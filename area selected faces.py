import bpy
import math
import bmesh

#doplnit world matrix

def main():
    if bpy.context.active_object.mode == 'OBJECT':
        print('switch to edit mode')
        return
    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')
    
    meshObjektu = bpy.context.active_object.data
    
    bm = bmesh.new()   # create an empty BMesh
    bm.from_mesh(meshObjektu)   # fill it in from a Mesh
    
    newListOfFaces = []
    
    area = 0.0
    #area2 = 0.0
    for face in bm.faces:
        if face.select == True: 
            newListOfFaces.append(face)
            #area2 = area2 + face.calc_area()
    
    dict = bmesh.ops.triangulate(bm, faces = newListOfFaces)
    
    for faceT in dict['faces']:
        area = area + faceT.calc_area()
    
    print('new measure')
    bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text=str(area)),title="Delka",icon='INFO')
    print(area)
    #print(area2)
    
    bm.free()


main()