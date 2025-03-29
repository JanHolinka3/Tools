import bpy #type: ignore
import math
import mathutils #type: ignore

def smerovyVektor(vektorBase: list[float], vektorSmer: list[float]) -> list[float]:
    sX = vektorSmer[0] - vektorBase[0]
    sY = vektorSmer[1] - vektorBase[1]
    sZ = vektorSmer[2] - vektorBase[2]
    vysledek = [sX, sY, sZ]
    return vysledek

def vektorSoucinNulaXY(vektorA: list[float]) -> list[float]:
    vektorB = [0.0,0.0,0.0]
    vektorB[0] = -vektorA[1]
    vektorB[1] = vektorA[0]
    #print(vektorB)
    sX = (vektorA[1] * vektorB[2]) - (vektorA[2] * vektorB[1])
    sY = (vektorA[2] * vektorB[0]) - (vektorA[0] * vektorB[2])
    sZ = (vektorA[0] * vektorB[1]) - (vektorA[1] * vektorB[0])
    vysledek = [sX, sY, sZ]
    return vysledek

def odsazeniRoviny(vektorPrimky, bod):
    vysledek = vektorPrimky[0] * bod[0] + vektorPrimky[1] * bod[1] + vektorPrimky[2] * bod[2]
    return -vysledek

def dopocitejZpodleRoviny(vektorRoviny, odsazeni, bod):
    vysledek = vektorRoviny[0] * bod[0] + vektorRoviny[1] * bod[1] + odsazeni
    vysledek = vysledek/vektorRoviny[2]
    return -vysledek

bpy.ops.object.mode_set(mode='OBJECT')

objectMesh = bpy.context.active_object.data
#pokud selectnu prave dve vetices - tvori vektor ale s nulovym [2], pokud selectnu jiny pocet tak se alignuje na ose [2]

counter = 0
predchozi = False
verticeJedna = mathutils.Vector((0.0, 0.0, 0.0))
verticeDva = mathutils.Vector((0.0, 0.0, 0.0))
verticeTri = mathutils.Vector((0.0, 0.0, 0.0))
for vert in objectMesh.vertices:
    if vert.select == True and vert.hide == False: #takove by mely byt jen 2
        if counter == 0:
            verticeJedna[0] = vert.co[0]
            verticeJedna[1] = vert.co[1]
            verticeJedna[2] = vert.co[2]
            counter = counter + 1
        elif counter == 1:
            verticeDva[0] = vert.co[0]
            verticeDva[1] = vert.co[1]
            verticeDva[2] = vert.co[2]
            counter = counter + 1
        elif counter == 2:
            verticeTri[0] = vert.co[0]
            verticeTri[1] = vert.co[1]
            verticeTri[2] = vert.co[2]
            counter = counter + 1
            
if counter == 3: #mame trojuhelnik
    direction = mathutils.Vector((0.0, 0.0, 1.0))
    #mathutils.geometry.intersect_ray_tri(v1, v2, v3, ray, orig, clip=True)
    for vert in objectMesh.vertices:
        if vert.hide:
            vert.hide = False
            intersectionPoint = mathutils.geometry.intersect_ray_tri(verticeJedna, verticeDva, verticeTri, direction, vert.co, False)
            if intersectionPoint != None:
                vert.co[2] = intersectionPoint[2]
    
else:
    vektorSmer = smerovyVektor(verticeJedna, verticeDva) 

    verticeTMP = [0.0,0.0,0.0]
    verticeNormal = [0.0,0.0,0.0]

    #print(vektorSmer)
    verticeNormal = vektorSoucinNulaXY(vektorSmer) #to uz je vlastne rovnice primky - dopocitame odsazeni
    odsazeni = odsazeniRoviny(verticeNormal, verticeJedna)
    #print(odsazeni)

    for vert in objectMesh.vertices:
        if vert.hide:
            vert.hide = False
            verticeTMP[0] = vert.co[0]
            verticeTMP[1] = vert.co[1]
            verticeTMP[2] = vert.co[2]
            #print('test')
            vert.co[2] = dopocitejZpodleRoviny(verticeNormal, odsazeni, verticeTMP)
        
for edg in objectMesh.edges:
    if edg.hide:
        edg.hide = False

for fac in objectMesh.polygons:
    if fac.hide:
        fac.hide = False

#print(verticeNormal)

bpy.ops.object.mode_set(mode='EDIT')