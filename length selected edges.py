import bpy
import math

#doplnit world matrix

def main():
    if bpy.context.active_object.mode == 'OBJECT':
        print('switch to edit mode')
        return
    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')
    
    meshObjektu = bpy.context.active_object.data
    
    delka = 0.0
    
    for edge in meshObjektu.edges:
        if edge.select == True:
            delka = delka + vzdalenostMeziDvemaBody(meshObjektu.vertices[edge.vertices[0]].co, meshObjektu.vertices[edge.vertices[1]].co)
    print(delka)
    bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text=str(delka)),title="Delka",icon='INFO')
            
    
def vzdalenostMeziDvemaBody(bod1: list[float], bod2: list[float]) -> float:
    del1 = bod1[0] - bod2[0]
    del2 = bod1[1] - bod2[1]
    del3 = bod1[2] - bod2[2]
    vysledekSq = (del1*del1) + (del2*del2) + (del3*del3)
    vysledek = math.sqrt(vysledekSq)

    return vysledek


main()