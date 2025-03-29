import bpy #type: ignore
import numpy #type: ignore 
#numpy.float64()

#coords to substract are float - change to 64 bit only on some automatic coord alignment
diffX=782700.0
diffY=1197500.0
diffZ=720.0
decPlaces = 3
delimiter = ","
filePath = "body1.csv"
naming = "index"
#naming = "vertgroup"
format = "XYZ"
#format = "YXZ"
#format = "-XYZ"
#format = "-YXZ"

if bpy.context.active_object.mode == 'EDIT':
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')

meshObjektu = bpy.context.active_object.data
objekt = bpy.context.active_object

#chce to jump out and in object mode, jinak to nebere aktualni zmeny
#X = -715298.539     Y = -1152313.323
#X = -715029.336     Y = -1152358.855

#pridat if edit jump to object and back to edit!!!!!!!!!!!!!


with open(filePath, "w") as file:
    for vert in meshObjektu.vertices:
        if vert.select == True and vert.hide == False:
            if naming == "vertgroup":
                for group in objekt.vertex_groups:
                    try:
                        weight = group.weight(vert.index)
                        if weight > 0:
                            vertName = "\"" + group.name + "\""
                        break
                    except:
                        vertName = str(vert.index)
            else:
                vertName = str(vert.index)#pridat system pojmenovani
            file.write(vertName + delimiter)

            coordX = numpy.float64(vert.co[0])
            coordY = numpy.float64(vert.co[1])
            coordZ = numpy.float64(vert.co[2])

            diffZTmp = diffZ
            if coordZ == 0.0:
                diffZTmp = 0

            if format == "XYZ":
                file.write("{:.{}f}".format(round(coordX + diffX, decPlaces),decPlaces) + delimiter)
                file.write("{:.{}f}".format(round(coordY + diffY, decPlaces),decPlaces) + delimiter)
            if format == "YXZ":
                file.write("{:.{}f}".format(round(coordY + diffY, decPlaces),decPlaces) + delimiter)
                file.write("{:.{}f}".format(round(coordX + diffX, decPlaces),decPlaces) + delimiter)
            if format == "-XYZ":
                file.write("{:.{}f}".format(round(-coordX - diffX, decPlaces),decPlaces) + delimiter)
                file.write("{:.{}f}".format(round(-coordY - diffY, decPlaces),decPlaces) + delimiter)
            if format == "-YXZ":
                file.write("{:.{}f}".format(round(-coordY - diffY, decPlaces),decPlaces) + delimiter)
                file.write("{:.{}f}".format(round(-coordX - diffX, decPlaces),decPlaces) + delimiter)
            
            #textToPrint = str(vert.index) + "; " + str(round(vert.co[0]+715100,3)) + "; " + str(round(vert.co[1]+1152300,3)) + ";"
    
            file.write("{:.{}f}".format(round(coordZ + diffZTmp, decPlaces),decPlaces) + "\n")
                #textToPrint = textToPrint + str(round(vert.co[2]+470,3))
            #print(textToPrint + "\n")