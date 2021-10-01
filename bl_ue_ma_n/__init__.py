# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
#linux users
#in kde manually start Klipper
#optionally remove /usr/share/plasma/plasmoids/org.kde.plasma.clipboard folder
bl_info = {
  "name": "Blender to UE4 Material node Copier",
  "author": "Angelo Miner (angjminer@gmail.com)",
  "version": (0, 0, 1),
  "blender": (2, 80, 0),
  "location": "Properties > Material",
  "description": "Copy Node-Tree from blender to unreal 4 material editor",
  "warning": "",
  "wiki_url": "",
  "tracker_url": "",
  "category": "Material"}

import bpy
import os
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )
import hashlib
from bpy_extras.io_utils import ExportHelper
from bl_ue_ma_n import nodecopy
#from bl_ue_ma_n import ue_node_defs

class BLUEMaN_Settings(PropertyGroup):

    only_selected: BoolProperty(
            name="Only Selected",
            description="Only copy Selected",
            default=False,
            )
    print_to_console: BoolProperty(
            name="Print To Console",
            description="Print output to console",
            default=False,
            )
    print_to_file: BoolProperty(
            name="Print To File",
            description="Print output to file",
            default=False,
            )
    render_proc_tex: BoolProperty(
            name="Render Procedural Textures",
            description="Render Procedural Textures to file",
            default=False,
            )

    proc_tex_res: IntProperty(
        name = "Procedural Texture Resolution",
        description="The Resolution of your Procedural Textures when rendered to file",
        default = 64,
        min = 64,
        max = 1024
        )

    col_ramp_res: IntProperty(
        name = "Color Ramp Resolution",
        description="The Resolution of your Color Ramp Gradient in UE",
        default = 64,
        min = 64,
        max = 1024
        )
    nodecopy_path: StringProperty(
            default="*.nodecopy",
            options={'HIDDEN'},
            maxlen=255,  # Max internal buffer length, longer would be clamped.
            )
    proc_tex_path: StringProperty(
            default="*.png",
            options={'HIDDEN'},
            maxlen=255,  # Max internal buffer length, longer would be clamped.
            )
    my_float: FloatProperty(
        name = "Set a value",
        description = "A float property",
        default = 23.7,
        min = 0.01,
        max = 30.0
        )
class Open_txt_Path(bpy.types.Operator, ExportHelper):
    bl_label = "OK"
    bl_idname = "find_txt.path"
    filename_ext = ".nodecopy"
    def execute(self, context):
        context.scene.blueman_props['nodecopy_path'] = "%s" % (self.filepath)
        return {'FINISHED'}
class Open_tex_Path(bpy.types.Operator, ExportHelper):
    bl_label = "OK"
    bl_idname = "find_tex.path"
    filename_ext = ".filename_will_change_to_node_name_dot_png"
    def execute(self, context):
        path_for_images = os.path.dirname(bpy.path.abspath("%s" % (self.filepath)))
        context.scene.blueman_props['proc_tex_path'] = path_for_images#"%s" % (self.filepath)
        return {'FINISHED'}
class BLUEMaN_Copy(bpy.types.Operator):
    bl_label = "BLUEMaN Copy"
    bl_idname = "blueman.copy"
    def execute(self,context):
        selected_only = context.scene.blueman_props['only_selected']
        print_to_console = context.scene.blueman_props['print_to_console']
        col_ramp_res = context.scene.blueman_props['col_ramp_res']
        
        print_node_to_file = context.scene.blueman_props['print_to_file']
        print_node_to_file_path = context.scene.blueman_props['nodecopy_path']
        render_proc = context.scene.blueman_props['render_proc_tex']
        render_proc_file_path = context.scene.blueman_props['proc_tex_path']
        render_proc_file_res = context.scene.blueman_props['proc_tex_res']
        
        mat = context.material
        return nodecopy.copy(self,context,(selected_only,print_to_console,mat.name,col_ramp_res,print_node_to_file,print_node_to_file_path,render_proc,render_proc_file_path,render_proc_file_res))
class BLUEMaN_Mat_Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "BLUEMaN Node Copy Panel"
    bl_idname = "OBJECT_PT_BLUEMaN_Mat"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
    #have to trigger this somehow :/
    #bpy.context.scene.blueman_props['only_selected'] = False

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        blueman_props = scene.blueman_props
        mat = context.material


        row = layout.row()
        row.label(text="Active Material is: " + mat.name)
        #row = layout.row()
        split = layout.split()
        col = split.column()
        col.prop(blueman_props, "only_selected", text="Only Copy Selected")
        #row = layout.row()
        sub = col.column()
        sub.prop(blueman_props, "print_to_console", text="Print Output to Console")
        col = split.column()
        col.prop(blueman_props, "print_to_file", text="Print Output to File")
        sub = col.column()
        sub.prop(blueman_props, "render_proc_tex", text="Render Procedural Textures to file")
        if blueman_props.only_selected:
            row = layout.row()
            row.label(text="Select Nodes to Copy in Node Editor!", icon='NODETREE')
        if blueman_props.print_to_file:
            box = layout.box()
            row = box.row()
            row.label(text="Node Copy Path: " +blueman_props.nodecopy_path)
            row = box.row()
            row.operator("find_txt.path", text="File to save Nodes to", icon='FILEBROWSER')
        if blueman_props.render_proc_tex:
            box = layout.box()
            row = box.row()
            row.prop(blueman_props, "proc_tex_res", text="The Resolution of your Procedural Textures when rendered to file")
            row = box.row()
            row.label(text="Node Copy Path: " +blueman_props.proc_tex_path)
            row = box.row()
            row.operator("find_tex.path", text="Find Path To Save Proc Textures", icon='FILEBROWSER')
        row = layout.row()
        #col_ramp_res
        row.prop(blueman_props, "col_ramp_res", text="The Resolution of your Color Ramp Gradient in UE")
        row = layout.row()
        row.operator("blueman.copy", text="Copy Material Nodes to paste in UE", icon='COPYDOWN')

def register():
    bpy.utils.register_class(Open_txt_Path)
    bpy.utils.register_class(Open_tex_Path)
    bpy.utils.register_class(BLUEMaN_Settings)
    bpy.utils.register_class(BLUEMaN_Copy)
    bpy.utils.register_class(BLUEMaN_Mat_Panel)
    bpy.types.Scene.blueman_props = PointerProperty(type=BLUEMaN_Settings)

def unregister():
    bpy.utils.unregister_class(Open_txt_Path)
    bpy.utils.unregister_class(Open_tex_Path)
    bpy.utils.unregister_class(BLUEMaN_Settings)
    bpy.utils.unregister_class(BLUEMaN_Copy)
    bpy.utils.unregister_class(BLUEMaN_Mat_Panel)
    del bpy.types.Scene.blueman_props


if __name__ == "__main__":
    register()
