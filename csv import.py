import bpy #type: ignore
import bmesh #type: ignore
import numpy #type: ignore

diffX=782700.0
diffY=1197500.0
diffZ=720.0
decPlaces = 3
delimiter = ","
filePath = "body1.csv"
#naming = "index"
format = "XYZ"
#format = "YXZ"

#doplnit textovy popis - nazvy bodu - vlastni collection

arrayX = []
arrayY = []
arrayZ = []
slova = []

with open(filePath, "r") as file:
    lineIndex = 0
    for line in file:
        if lineIndex == 0:
            lineIndex = lineIndex + 1
            continue
        indexSlova = 0
        slovo = ''
        posledniPismeno = False
        for char in line:
            if char != delimiter:
                slovo = slovo + char
                posledniPismeno = True
            if char == delimiter and posledniPismeno == True:
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
        #slova[1]=slova[1].replace(",", ".")
        #slova[2]=slova[2].replace(",", ".")
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

indA = 0
for xVal in arrayX:
    if format == "XYZ":
        vector = (xVal-diffX, arrayY[indA]-diffY, arrayZ[indA] - diffZ) 
    if format == "YXZ":
        vector = (arrayY[indA]-diffY, xVal-diffX, arrayZ[indA] - diffZ) 
    bFA.verts.new(vector)
    indA = indA + 1


bFA.to_mesh(objectMesh)
bFA.free()