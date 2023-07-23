bl_info = {
    "name": "Shape Outline Length",
    "author": "Cube Creative Agency",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Shape Outline Length",
    "description": "Calculates the length of a shape outline for meshes and curves in millimeters",
    "warning": "",
    "wiki_url": "",
    "category": "Object"
}

import bpy
from mathutils import Vector

class ShapeOutlineLengthOperator(bpy.types.Operator):
    bl_idname = "object.shape_outline_length"
    bl_label = "Calculate Shape Outline Length"
    bl_description = "Calculates the length of a shape outline for meshes and curves in millimeters"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        unit_scale = context.scene.unit_settings.scale_length
        if obj.type == 'MESH':
            length = 0.0
            for edge in obj.data.edges:
                length += (obj.matrix_world @ edge.vertices[1].co - obj.matrix_world @ edge.vertices[0].co).length * unit_scale * 1000
            self.report({'INFO'}, f"Mesh shape outline length: {length:.2f} mm")
        elif obj.type == 'CURVE':
            length = 0.0
            for spline in obj.data.splines:
                for i in range(len(spline.bezier_points)-1):
                    length += (obj.matrix_world @ spline.bezier_points[i+1].co - obj.matrix_world @ spline.bezier_points[i].co).length * unit_scale * 1000
            self.report({'INFO'}, f"Curve shape outline length: {length:.2f} mm")
        else:
            self.report({'ERROR'}, "Active object is not a mesh or curve")
        return {'FINISHED'}

class ShapeOutlineLengthPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_shape_outline_length"
    bl_label = "Shape Outline Length"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Shape Outline Length"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.shape_outline_length", text="Calculate Length")

def register():
    bpy.utils.register_class(ShapeOutlineLengthOperator)
    bpy.utils.register_class(ShapeOutlineLengthPanel)

def unregister():
    bpy.utils.unregister_class(ShapeOutlineLengthOperator)
    bpy.utils.unregister_class(ShapeOutlineLengthPanel)

if __name__ == "__main__":
    register()