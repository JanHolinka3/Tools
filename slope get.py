import bpy
import math
import bmesh

def calculate_slope_percentage(edge):
    # Získání dvou vrcholů hrany
    vert1, vert2 = edge.verts
    
    # Souřadnice vrcholů
    co1 = vert1.co
    co2 = vert2.co
    
    # Výpočet horizontální vzdálenosti (X-Y rovina)
    horizontal_distance = math.sqrt((co2.x - co1.x)**2 + (co2.y - co1.y)**2)
    
    # Výpočet změny výšky (Z osa)
    height_difference = co2.z - co1.z
    
    # Výpočet spádu v procentech
    if horizontal_distance == 0:
        return None  # Hrana je svislá, spád nelze spočítat
    slope_percentage = (height_difference / horizontal_distance) * 100
    return slope_percentage

def calculate_jednaKu(edge):
    # Získání dvou vrcholů hrany
    vert1, vert2 = edge.verts
    
    # Souřadnice vrcholů
    co1 = vert1.co
    co2 = vert2.co
    
    # Výpočet horizontální vzdálenosti (X-Y rovina)
    horizontal_distance = math.sqrt((co2.x - co1.x)**2 + (co2.y - co1.y)**2)
    
    # Výpočet změny výšky (Z osa)
    height_difference = co2.z - co1.z
    
    # Výpočet spádu v procentech
    if horizontal_distance == 0:
        return None  # Hrana je svislá, spád nelze spočítat
    #svisla je 1
    slope_percentage = abs(( horizontal_distance / height_difference))
    return slope_percentage

# Hlavní logika
def main():
    obj = bpy.context.object
    if obj is None or obj.type != 'MESH':
        print("Vyberte objekt typu Mesh.")
        return
    
    bm = bmesh.from_edit_mesh(obj.data)
    
    # Filtrování vybraných hran
    selected_edges = [edge for edge in bm.edges if edge.select]
    
    if len(selected_edges) != 1:
        print("Vyberte přesně jednu hranu.")
        return
    
    edge = selected_edges[0]
    slope = calculate_slope_percentage(edge)
    jednaKu = calculate_jednaKu(edge)
    
    if slope is None:
        print("Hrana je svislá, nelze spočítat spád.")
    else:
        print(f"Spád hrany je {slope:.2f} % a 1 : {jednaKu:.2f}")
        bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text=f"Spád hrany je {slope:.2f} % a 1 : {jednaKu:.2f}"),title="Delka",icon='INFO')

# Volání hlavní funkce
main()