import bpy
import mathutils
import bmesh
import numpy
import math

def createArc(bm, center, radius, start_angle, end_angle, segments):
    if end_angle < start_angle:
        tmp = start_angle
        start_angle = end_angle + 360
        end_angle = tmp 

    start_rad = math.radians(start_angle - 180)
    end_rad = math.radians(end_angle - 180)
    # Vytvoření vrcholů
    vertices = []
    for i in range(segments + 1):
        t = i / segments
        angle = start_rad + (end_rad - start_rad) * t
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        vert = bm.verts.new((x, y, center[2]))
        vertices.append(vert)
    # Propojení hranami
    for i in range(len(vertices) - 1):
        bm.edges.new((vertices[i], vertices[i + 1]))
    return

#doplnit textovy popis - nazvy bodu - vlastni collection
def main():
    print('spoustim dxf import')

    arrayX = []
    arrayY = []
    arrayZ = []
    slova = []
    arrayCircle = []
    arrayPolyline = []
    arrayPolylineClosed = [] # 1 closed, ostatni neresime
    arrayLine = []

    odecetX=00.0 #prohozene XY - X je vzdy to mensi cislo
    odecetY=00.0 #prohozene XY - X je vzdy to mensi cislo
    odecetZ=0.0

    rozsahS = 10000.0 #do vsech smeru
    rozsahV = 500.0 #nahoru i dolu

    segmentovani = 1 #tzn ze kruh bude cca po metru edges...

    #with open("RD Hluboká projekt.dxf", "r", encoding="windows-1252") as file:
    with open("RD Hluboká projekt.dxf", "r") as file:
        pointActive = False
        circleActive = False
        arcActive = False
        #AcDbPolyline
        polylineActive = False
        lineActive = False
        arcCountHelp = False
        polylineHeightHelp = False #resi optional vyskyt vysky s kodem 38
        polylineEndHelp = False #resi ukonceni sekvence x,y polyline
        next10 = False
        next20 = False
        next30 = False
        next40 = False
        next50 = False
        next51 = False
        next38 = False
        next70 = False
        next11 = False
        next21 = False
        next31 = False
        for line in file:
            #print(line)
            if line == "AcDbPoint\n":
                pointActive = True
            if line == "AcDbCircle\n":
                circleActive = True
            if line == "AcDbArc\n":
                arcActive = True
            if line == "AcDbPolyline\n":
                polylineActive = True
                polylineHeightHelp = False #jsme na zacatku Polyline
                polylineEndHelp = False
            if line == '  3\n' and polylineActive == True:
                polylineActive = False
            if line == "AcDbLine\n":
                lineActive = True

            #AcDbPoint
            if next10 == True and pointActive == True:
                slova.append(line.replace("\n", ""))
                next10 = False
            if next20 == True and pointActive == True:
                slova.append(line.replace("\n", ""))
                next20 = False
            if next30 == True and pointActive == True:
                slova.append(line.replace("\n", ""))
                next30 = False
                pointActive = False
                #mame slova najebana ve slova[]
                arrayX.append(numpy.float64(slova[0]))
                arrayY.append(numpy.float64(slova[1]))
                arrayZ.append(numpy.float64(slova[2]))
                #print(numpy.float64(slova[0]))
                #print(slova)
                slova.clear()
            
            #pridavek pro AcDbArc
            if arcCountHelp == True: #znamena ze jsme v predchozim radku dokoncily circle - tedy testneme jestli tento radek nema marker a pokud ne, tak pridame prazdne 2 elemnty do arrayCircle, v opacnem pripade se provede AcDbArc
                if line != '100\n':
                    arrayCircle.append(numpy.float64(0))
                    arrayCircle.append(numpy.float64(0))
                # a jeste vypneme marker
                arcCountHelp = False

            #AcDbCircle
            if next10 == True and circleActive == True:
                slova.append(line.replace("\n", ""))
                next10 = False
            if next20 == True and circleActive == True:
                slova.append(line.replace("\n", ""))
                next20 = False
            if next30 == True and circleActive == True:
                slova.append(line.replace("\n", ""))
                next30 = False
            if next40 == True and circleActive == True:
                slova.append(line.replace("\n", ""))
                next40 = False    
                circleActive = False
                arcCountHelp = True #prave jsme dokoncily Circle
                #mame slova najebana ve slova[]
                arrayCircle.append(numpy.float64(slova[0]))
                arrayCircle.append(numpy.float64(slova[1]))
                arrayCircle.append(numpy.float64(slova[2]))
                arrayCircle.append(numpy.float64(slova[3]))
                slova.clear()
            
            #AcDbArc - patri pod AcDbCircle, tedy se prida do arrayCircle
            if next50 == True and arcActive == True:
                slova.append(line.replace("\n", ""))
                next50 = False
            if next51 == True and arcActive == True:
                slova.append(line.replace("\n", ""))
                next51 = False 
                arcActive = False
                #mame slova najebana ve slova[]
                arrayCircle.append(numpy.float64(slova[0]))
                arrayCircle.append(numpy.float64(slova[1]))
                slova.clear()
            
            #AcDbPolyline
            if next38 == True and polylineActive == True: #to je vyska
                slova.append(line.replace("\n", ""))
                next38 = False
                polylineHeightHelp = True #pridali jsme vysku a nemusime pridavat vysku 0
            if next10 == True and polylineActive == True:
                #nejdriv kontrolujeme jestli byla zadana vyska a pokud ne, tak dame prvni 0
                if polylineHeightHelp == False:
                    slova.append("0")
                    polylineHeightHelp = True #nastavime na true, aby se pri dalsi next10 uz nula nepridavala
                slova.append(line.replace("\n", ""))
                next10 = False
            if next20 == True and polylineActive == True:
                slova.append(line.replace("\n", ""))
                next20 = False
                polylineEndHelp = True #potencionalne muze polyline v nasledujici line koncit - "  0"
            if polylineActive == True and polylineEndHelp == True and line == "  0\n": #aktualni polyline konci
                polylineActive = False
                polylineEndHelp = False
                slova.append('98989898989898')#znak pro polyline end
                #mame slova najebana ve slova[]
                for slovo in slova:
                    arrayPolyline.append(numpy.float64(slovo))
                slova.clear()
            if next70 == True and polylineActive == True:
                arrayPolylineClosed.append(line.replace("\n", ""))
            
            #AcDbLine
            if next10 == True and lineActive == True: #x y z x y z
                slova.append(line.replace("\n", ""))
                next10 = False
            if next20 == True and lineActive == True:
                slova.append(line.replace("\n", ""))
                next20 = False
            if next30 == True and lineActive == True:
                slova.append(line.replace("\n", ""))
                next30 = False
            if next11 == True and lineActive == True:
                slova.append(line.replace("\n", ""))
                next11 = False
            if next21 == True and lineActive == True:
                slova.append(line.replace("\n", ""))
                next21 = False
            if next31 == True and lineActive == True:
                slova.append(line.replace("\n", ""))
                next31 = False
                for slovo in slova:
                    arrayLine.append(numpy.float64(slovo))
                slova.clear()
                lineActive = False
            
            #tohle aktivuje sber podle kodu - vzdy jenom jeden radek pod kodem
            if next10 == True:
                next10 = False
            if next20 == True:
                next20 = False
            if next30 == True:
                next30 = False
            if next40 == True:
                next40 = False
            if next50 == True:
                next50 = False
            if next51 == True:
                next51 = False
            if next38 == True:
                next38 = False
            if next70 == True:
                next70 = False
            if next11 == True:
                next11 = False
            if next21 == True:
                next21 = False
            if next31 == True:
                next31 = False

            if line == " 10\n":
                next10 = True
            if line == " 20\n":
                next20 = True
            if line == " 30\n":
                next30 = True
            if line == " 40\n":
                next40 = True
            if line == " 50\n":
                next50 = True
            if line == " 51\n":
                next51 = True
            if line == " 38\n":
                next38 = True
            if line == " 70\n":
                next70 = True
            if line == " 11\n":
                next11 = True
            if line == " 21\n":
                next21 = True
            if line == " 31\n":
                next31 = True

            if line == "100\n":
                pointActive = False
                circleActive = False
                arcActive = False
                polylineActive = False
                lineActive = False

    #print(arrayX)
    #print(arrayY)      
    #print(arrayZ)

    #print(arrayLine)

    #print(arrayPolyline)
    #AcDbPoint
    bpy.ops.mesh.primitive_plane_add()
    objectMesh = bpy.context.active_object.data
    bpy.context.active_object.name = 'Points'
    bFA=bmesh.new() 
    indA = 0
    for xVal in arrayX: #spravne osetrene rozsahy jsou nyni v polyline - prevzit odtam
        x = abs(xVal) - odecetX
        y = abs(arrayY[indA]) - odecetY
        z = abs(arrayZ[indA]) - odecetZ
        if z < (- rozsahV) or z > (rozsahV):
            z = abs(arrayZ[indA])
        vector = (x, y, z)
        bFA.verts.new(vector)
        indA = indA + 1
    bFA.to_mesh(objectMesh) 
    bFA.free()

    #print(arrayCircle)
    #AcDbCircle - tohle ma kreslit jenom vysece podle dalsich kodu - to chce dat do jednoho kodu - pocet segmentu nejak podle velikosti
    bpy.ops.mesh.primitive_plane_add()
    objectMesh = bpy.context.active_object.data
    bpy.context.active_object.name = 'Circles'
    bFA=bmesh.new() 
    counterCircle = 0
    for element in arrayCircle:
        if counterCircle % 6 == 5:
            xCircle = abs(arrayCircle[counterCircle - 5]) - odecetX
            if xCircle < (- rozsahS) or xCircle > (rozsahS):
                xCircle = abs(arrayCircle[counterCircle - 5])
            yCircle = abs(arrayCircle[counterCircle - 4]) - odecetY
            if yCircle < (- rozsahS) or yCircle > (rozsahS):
                yCircle = abs(arrayCircle[counterCircle - 4])
            zCircle = abs(arrayCircle[counterCircle - 3]) - odecetZ
            if zCircle < (- rozsahV) or zCircle > (rozsahV):
                zCircle = abs(arrayCircle[counterCircle - 3])
            polomerCircle = arrayCircle[counterCircle - 2]
            segmentsF = int((polomerCircle*2*3.14)/segmentovani)
            if segmentsF < 12:
                segmentsF = 12
            if arrayCircle[counterCircle - 1] != '0':
                segmentsF = int((abs(arrayCircle[counterCircle] - arrayCircle[counterCircle - 1])/360)*segmentsF)
                if segmentsF < 2:
                    segmentsF = 2
                createArc(bFA, [xCircle, yCircle, zCircle], polomerCircle, arrayCircle[counterCircle - 1], arrayCircle[counterCircle], segmentsF)
            else:
                kruh = bmesh.ops.create_circle(bFA, segments = segmentsF, radius = polomerCircle) #obvod je radius*2*3.14
                #print(kruh.get(1))
                bmesh.ops.translate(bFA, verts = kruh["verts"], vec = (xCircle, yCircle, zCircle))
        counterCircle = counterCircle + 1

    bFA.to_mesh(objectMesh)
    bFA.free()

    #AcDbPolyline
    bpy.ops.mesh.primitive_plane_add()
    objectMesh = bpy.context.active_object.data
    bpy.context.active_object.name = 'Polylines'
    bFA=bmesh.new() 
    konecBool = True
    suda = False
    x = numpy.float64(0)
    y = numpy.float64(0)
    z = numpy.float64(0)
    body = []
    linesCounter = 0
    for value in arrayPolyline:
        if konecBool == True:
            z = abs(value)  #470 - 420 az 520
            if z > (odecetZ - rozsahV) and z < (odecetZ + rozsahV):
                z = abs(value) - odecetZ
            konecBool = False
            continue
        if value != 98989898989898:
            if suda == True:
                y = abs(value) 
                if y > (odecetY - rozsahS) and y < (odecetY + rozsahS):
                    y = abs(value) - odecetY
                suda = False
                bodicek = bFA.verts.new((x,y,z))
                body.append(bodicek)
            else: 
                x = abs(value) 
                if x > (odecetX - rozsahS) and x < (odecetX + rozsahS):
                    x = abs(value) - odecetX
                suda = True
        if value == 98989898989898:
            for i in range(len(body) - 1):
                bFA.edges.new((body[i], body[i + 1]))
                if len(body) - 1 == i + 2: #kdyz jsme na konci
                    if arrayPolylineClosed[linesCounter] != '     0':
                        bFA.edges.new((body[i + 2], body[0]))

            body.clear()
            konecBool = True
            linesCounter = linesCounter + 1

    bFA.to_mesh(objectMesh) 
    bFA.free()

    #AcDbLine
    bpy.ops.mesh.primitive_plane_add()
    objectMesh = bpy.context.active_object.data
    bpy.context.active_object.name = 'Lines'
    bFA=bmesh.new() 
    x = numpy.float64(0)
    y = numpy.float64(0)
    z = numpy.float64(0)
    x2 = numpy.float64(0)
    y2 = numpy.float64(0)
    z2 = numpy.float64(0)
    #body = []
    linesCounter = 0
    for value in arrayLine:
        if linesCounter % 6 == 5:
            x = abs(arrayLine[linesCounter - 5])
            if x > (odecetX - rozsahS) and x < (odecetX + rozsahS):
                x = x - odecetX
            y = abs(arrayLine[linesCounter - 4])
            if y > (odecetY - rozsahS) and y < (odecetY + rozsahS):
                y = y - odecetY
            z = abs(arrayLine[linesCounter - 3])
            if z > (odecetZ - rozsahV) and z < (odecetZ + rozsahV):
                z = z - odecetZ
            x2 = abs(arrayLine[linesCounter - 2])
            if x2 > (odecetX - rozsahS) and x2 < (odecetX + rozsahS):
                x2 = x2 - odecetX
            y2 = abs(arrayLine[linesCounter - 1])
            if y2 > (odecetY - rozsahS) and y2 < (odecetY + rozsahS):
                y2 = y2 - odecetY
            z2 = abs(arrayLine[linesCounter])
            if z2 > (odecetZ - rozsahV) and z2 < (odecetZ + rozsahV):
                z2 = z2 - odecetZ
            bodicek1 = bFA.verts.new((x,y,z))
            bodicek2 = bFA.verts.new((x2,y2,z2))
            bFA.edges.new((bodicek1, bodicek2))
        linesCounter = linesCounter + 1
    bFA.to_mesh(objectMesh) 
    bFA.free()


    return

main()
'''
bpy.ops.mesh.primitive_plane_add()
objectMesh = bpy.context.active_object.data
bFA=bmesh.new()
createArc(bFA, [0.0,0.0,0.0], 2, 23, 359, 12)
bFA.to_mesh(objectMesh) 
bFA.free()
'''