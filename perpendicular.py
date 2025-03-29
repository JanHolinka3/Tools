import bpy
import bmesh
from mathutils import Vector
from bpy.props import FloatProperty

class MESH_OT_copy_vert_perpendicular(bpy.types.Operator):
    """Creates new vert perpendicular to edge"""
    bl_idname = "mesh.perpendicular_vert"
    bl_label = "Perpendicular vert"
    bl_options = {'REGISTER', 'UNDO'}
    
    distance: FloatProperty(
        name="Distance",
        description="Distance to move the copied vertex",
        default=1.0,
        precision=3
    )
    
    def execute(self, context):
        obj = context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        selected_verts = [v for v in bm.verts if v.select]
        if len(selected_verts) != 1:
            self.report({'ERROR'}, "Select exactly one vertex")
            return {'CANCELLED'}
        
        v = selected_verts[0]
        edges = v.link_edges
        if not edges:
            self.report({'ERROR'}, "Selected vertex is not connected to an edge")
            return {'CANCELLED'}
        
        edge = edges[0]  # První spojená hrana
        v1, v2 = edge.verts
        dir_vector = (v2.co - v1.co).normalized()
        
        # Najdeme kolmý vektor v XY rovině
        perp_vector = Vector((-dir_vector.y, dir_vector.x, 0)).normalized()
        if self.distance < 0:
            perp_vector = Vector((dir_vector.y, -dir_vector.x, 0)).normalized()
        
        # Vytvoříme kopii vrcholu a posuneme ji
        new_vert = bm.verts.new(v.co + perp_vector * abs(self.distance))
        bm.verts.index_update()
        bmesh.update_edit_mesh(me)
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

# Registrace operátoru
def menu_func(self, context):
    self.layout.operator(MESH_OT_copy_vert_perpendicular.bl_idname)

def register():
    bpy.utils.register_class(MESH_OT_copy_vert_perpendicular)
    bpy.types.VIEW3D_MT_edit_mesh.append(menu_func)

def unregister():
    bpy.utils.unregister_class(MESH_OT_copy_vert_perpendicular)
    bpy.types.VIEW3D_MT_edit_mesh.remove(menu_func)

if __name__ == "__main__":
    register()