import bpy
import numpy

odecetX=782700.0
odecetY=1197500.0
odecetZ=720.0


if bpy.context.active_object.mode == 'EDIT':
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')

meshObjektu = bpy.context.active_object.data

#chce to jump out and in object mode, jinak to nebere aktualni zmeny
#X = -715298.539     Y = -1152313.323
#X = -715029.336     Y = -1152358.855

#pridat if edit jump to object and back to edit!!!!!!!!!!!!!


with open("exportovaneBody.txt", "w") as file:
    for vert in meshObjektu.vertices:
        if vert.select == True and vert.hide == False:
            #textToPrint = ''
            #file.write(str(vert.index) + ";")
            file.write(str(vert.index) + ";")
            file.write(str("{:.3f}".format(round(vert.co[0]+odecetX,3)) + ";"))
            file.write(str("{:.3f}".format(round(vert.co[1]+odecetY,3)) + ";"))
            
            #textToPrint = str(vert.index) + "; " + str(round(vert.co[0]+715100,3)) + "; " + str(round(vert.co[1]+1152300,3)) + ";"
            
            if vert.co[2] == 0:
                file.write("000.000" + "\n")
                #textToPrint = textToPrint + "000.00"
            else:
                file.write(str("{:.3f}".format(round(vert.co[2]+odecetZ,3)) + "\n"))
                #textToPrint = textToPrint + str(round(vert.co[2]+470,3))
            #print(textToPrint + "\n")