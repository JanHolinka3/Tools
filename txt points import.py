import bpy
import mathutils
import bmesh
import numpy

#doplnit textovy popis - nazvy bodu - vlastni collection

arrayX = []
arrayY = []
arrayZ = []
slova = []

with open("trubky - Copy.txt", "r") as file:
    lineIndex = 0
    for line in file:
        indexSlova = 0
        slovo = ''
        posledniPismeno = False
        for char in line:
            if char != ' ':
                slovo = slovo + char
                posledniPismeno = True
            if char == ' ' and posledniPismeno == True:
                posledniPismeno = False
                slova.append(slovo)
                slovo = ''
                indexSlova = indexSlova + 1
        if posledniPismeno == True:
            posledniPismeno = False
            slova.append(slovo)
            slovo = ''
            indexSlova = indexSlova + 1
        #mame slova najebana ve slova[]
        slova[1]=slova[1].replace(",", ".")
        slova[2]=slova[2].replace(",", ".")
        arrayX.append(abs(numpy.float64(slova[1])))
        arrayY.append(abs(numpy.float64(slova[2])))
        try:
            arrayZ.append(abs(numpy.float64(slova[3])))
        except:
            arrayZ.append(numpy.float64(0.0))
        slova.clear()
        lineIndex = lineIndex +1
    #print(arrayZ)
    
bpy.ops.mesh.primitive_plane_add()
objectMesh = bpy.context.active_object.data
bFA=bmesh.new() 
odecetX=782700.0
odecetY=1197500.0
odecetZ=720.0

indA = 0
for xVal in arrayX:
    #print(xVal)
    #vector = (xVal-odecetX, arrayY[indA]-odecetY, arrayZ[indA]-odecetZ) #pro Z
    vector = (xVal-odecetX, arrayY[indA]-odecetY, arrayZ[indA] - odecetZ) #bez Z
    #vector = (arrayY[indA]-odecetX, xVal-odecetY, arrayZ[indA]) #bez Z prvni Y
    bFA.verts.new(vector)
    indA = indA + 1


bFA.to_mesh(objectMesh)
bFA.free()