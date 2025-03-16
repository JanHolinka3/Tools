import bpy
import math
import bmesh

#procenta = -0.03
#procenta = 0.6667 #to je 1:1.5
#procenta = 0.08
#procenta = 0.60
#procenta = 0.02
procenta = -1.00

def getLastSelectedVert(mesh):
    bm = bmesh.from_edit_mesh(mesh)

    for elem in reversed(bm.select_history):
        if isinstance(elem, bmesh.types.BMVert):
            #print("Active vertex:", elem.index)
            vysledek = elem.index
            bm.free()
            return vysledek
    bm.free()
    return -1

def main():
    #add object and edit mode switch
    modeB = bpy.context.mode

    if modeB == 'EDIT_MESH':
        bpy.ops.object.mode_set(mode='OBJECT')
        #bpy.ops.object.mode_set(mode='EDIT')

    mesh = bpy.context.active_object.data
    
    bpy.ops.object.mode_set(mode='EDIT')
    lastSelectedVert = getLastSelectedVert(mesh)
    bpy.ops.object.mode_set(mode='OBJECT')

    listVertices = []

    for vert in mesh.vertices:
        if vert.select == True: #takove by mely byt jen 2
            listVertices.append(vert)
    if len(listVertices) != 2:
        if modeB == 'EDIT_MESH':
            #bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.mode_set(mode='EDIT')
        print('prilis mnoho vertices')
        return

    bod1X = listVertices[0].co[0]
    bod1Y = listVertices[0].co[1]
    bod2X = listVertices[1].co[0]
    bod2Y = listVertices[1].co[1]
    discr = ((bod2X - bod1X) * (bod2X - bod1X)) + ((bod2Y - bod1Y) * (bod2Y - bod1Y))
    delka = math.sqrt(discr)
    odecet = procenta * delka
    if lastSelectedVert == listVertices[0].index:
        listVertices[0].co[2] = listVertices[1].co[2] - odecet
    if lastSelectedVert == listVertices[1].index:
        listVertices[1].co[2] = listVertices[0].co[2] - odecet      
                
    if modeB == 'EDIT_MESH':
        #bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')
        pass

    #print(listVertices)
    #print(listEdges)
    #print(delka)
    return

main()