import bpy
import numpy
import bmesh
import mathutils
import time
import math

#pridat kontrolu mesh, edit atd.
print('\nstart')
pocetKousku = 10

boolEditMode = False
if bpy.context.mode == 'EDIT_MESH':
    bpy.ops.object.mode_set(mode='OBJECT')
    boolEditMode = True

object = bpy.context.active_object

mesh = object.data

bm = bmesh.new()   # create an empty BMesh
bm.from_mesh(mesh)   # fill it in from a Mesh

bmS = bmesh.new()   # create an empty BMesh
bmS.from_mesh(mesh)   # fill it in from a Mesh

#print(mesh.vertices[0].co[0])

def vzdalenostDvouBodu(bod1, bod2):
    return math.sqrt((bod2[0] - bod1[0]) ** 2 + (bod2[1] - bod1[1]) ** 2 + (bod2[2] - bod1[2]) ** 2)

def volumeByTheorem(bm):
    bmesh.ops.triangulate(bm, faces=bm.faces)
    listFacesSelected = []
    listVertsSelected = []
    for vert in bm.verts:
        if vert.select == True:
            listVertsSelected.append(vert)
    for face in bm.faces: #pomoci tohoto vytahneme selected faces
        selected = True
        for vert in face.verts:
            if vert.select == False:
                selected = False
        if selected == True:
            listFacesSelected.append(face)
    #solid check - kdyz vypisu vsechny edge faces, tak kazdy musi existovat 2x
    sortedListOfEdges = []
    for face in listFacesSelected:
        for edge in face.edges:
            sortedListOfEdges.append(edge.index)
    sortedListOfEdges.sort()
    for i in range(len(sortedListOfEdges)):
        if i % 2 == 1:
            if sortedListOfEdges[i] != sortedListOfEdges[i-1]:
                print('sumtinkwonk')


    volume = 0
    for face in listFacesSelected:
        # Get the vertices of the triangle
        vert1 = numpy.array(face.verts[0].co)
        vert2 = numpy.array(face.verts[1].co)
        vert3 = numpy.array(face.verts[2].co)
        # print(vert1)
        # Compute the signed volume of the tetrahedron
        volume += numpy.dot(vert1, numpy.cross(vert2, vert3)) / 6.0
        #print(face.edges[0].index)
    print(volume)
    return

def calculate_mesh_volume(obj):
    # Zajištění, že objekt má triangulovanou mesh data
    depsgraph = bpy.context.evaluated_depsgraph_get()
    mesh = obj.evaluated_get(depsgraph).to_mesh()
    
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.transform(obj.matrix_world)  # Převod na světové souřadnice
    
    volume = sum(f.calc_area() * f.calc_center_median().dot(f.normal) / 3.0 for f in bm.faces)
    bm.free()
    
    print(abs(volume))
    return 

def volumeByShoot(bm):
    boundingBox_Xbig = mesh.vertices[0].co[0]
    boundingBox_Xsmall = mesh.vertices[0].co[0]
    boundingBox_Ybig = mesh.vertices[0].co[1]
    boundingBox_Ysmall = mesh.vertices[0].co[1]
    boundingBox_Zbig = mesh.vertices[0].co[2]
    boundingBox_Zsmall = mesh.vertices[0].co[2]

    for vert in mesh.vertices:
        #print(vert)
        if vert.co[0] > boundingBox_Xbig:
            boundingBox_Xbig = vert.co[0]
        if vert.co[0] < boundingBox_Xsmall:
            boundingBox_Xsmall = vert.co[0]
        if vert.co[1] > boundingBox_Ybig:
            boundingBox_Ybig = vert.co[1]
        if vert.co[1] < boundingBox_Ysmall:
            boundingBox_Ysmall = vert.co[1]
        if vert.co[2] > boundingBox_Zbig:
            boundingBox_Zbig = vert.co[2]
        if vert.co[2] < boundingBox_Zsmall:
            boundingBox_Zsmall = vert.co[2]

    #prostrelujeme zepredu
    vodorovnaVzdalenost = boundingBox_Xbig - boundingBox_Xsmall
    svislaVzdalenost = boundingBox_Zbig - boundingBox_Zsmall
    dilekVod = vodorovnaVzdalenost / pocetKousku
    dilekSvis = svislaVzdalenost / pocetKousku
    plocha = dilekVod * dilekSvis

    pocetLoops = range(pocetKousku)

    #ray zatim zepredu
    smer = mathutils.Vector((0.0, 1.0, 0.0))

    print("START VOLUME BY SHOOT")

    bmTri = bmesh.new()
    bmTri.from_mesh(mesh) 
    bmesh.ops.triangulate(bmTri, faces=bmTri.faces)
    bmTri.verts.ensure_lookup_table()

    bpy.ops.object.mode_set(mode='EDIT')

    vertListDouble = []

    dotazNaDouble = False

    delka = 0.0

    for i in pocetLoops:
        #print(i)
        for j in pocetLoops:
            #print('loop round')
            #tvorba originu - asi vzdy prictu (odectu) 1 pro kolme steny?
            x = boundingBox_Xsmall + (i * dilekVod) + (dilekVod/2)
            y = boundingBox_Ysmall - 1 
            z = boundingBox_Zsmall + (j * dilekSvis) + (dilekSvis/2)
            bodVystelu = mathutils.Vector((x, y, z))
            #print(bodVystelu)
            #print(bodVystelu)
            #nyni loop skrz vsechny faces
            vertList = []
            vertList.clear()
            for face in bmTri.faces:
                #print(face.index)

                #bmViz = bmTri.copy() 

                #bpy.ops.object.mode_set(mode='OBJECT')
                face.verts[0].select = True
                face.verts[1].select = True
                face.verts[2].select = True
                #bpy.ops.object.mode_set(mode='EDIT')

                #print(face.verts[0].co, face.verts[1].co, face.verts[2].co)
                kolize = mathutils.geometry.intersect_ray_tri(face.verts[0].co, face.verts[1].co, face.verts[2].co, smer, bodVystelu, True)
                #print(kolize)
                #print('vystrel')
                if kolize != None:
                    #print(kolize)
                    #nez tady pridam vert, musim loopnout vsechny pridane, jestli uz tam nejaka neni prilis blizko

                    for vertT in vertListDouble:
                        if abs(vertT[0]-kolize[0])<0.0001 and abs(vertT[1]-kolize[1])<0.0001 and abs(vertT[2]-kolize[2])<0.0001:
                            dotazNaDouble = True
                            break
                    if dotazNaDouble == False:
                        #bm.verts.new(kolize)
                        #bmTri.verts.new(kolize)
                        vertList.append(kolize)
                        vertListDouble.append(kolize)
                    else:
                        dotazNaDouble = False
                
                #bpy.ops.object.mode_set(mode='OBJECT')
                #bmTri.to_mesh(mesh)
                #bpy.ops.object.mode_set(mode='EDIT')


                #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

                #time.sleep(0.1)

                #bpy.ops.object.mode_set(mode='OBJECT')
                face.verts[0].select = False
                face.verts[1].select = False
                face.verts[2].select = False
                #bpy.ops.object.mode_set(mode='EDIT')
            #mam vertList - pro pary spocitam delku
            counter = 0
            for vert in vertList:
                if counter == 0:
                    counter = counter + 1
                    continue
                if counter % 2 == 1: #mame sude
                    delka = delka + vzdalenostDvouBodu(vertList[counter], vertList[counter -1])
                counter = counter + 1


            #vymazat doubles ve vertListu  

    print(delka * plocha)               
                    
    bpy.ops.object.mode_set(mode='OBJECT')
                    
    bm.to_mesh(mesh)
    bm.free()    

    print("HOTOVO")    
    return    

volumeByTheorem(bm)

#volumeByShoot(bmS)

if boolEditMode == True:
    bpy.ops.object.mode_set(mode ='EDIT')
#calculate_mesh_volume(object)