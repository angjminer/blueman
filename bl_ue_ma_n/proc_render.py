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
import bpy
import math
from bl_ue_ma_n import nodecopy
class Render_Proc(bpy.types.Operator):
    bl_label = "Render Proc Tex To File"
    bl_idname = "render.proc"
    #we will attempt to render procedural textures to an image :D
    def noise(self,context,vari_tup):
        n = vari_tup
        nn = 0
        n = (n >> 13) ^ n
        nn = (n * (n * n * 60493 + 19990303) + 1376312589) & 0x7fffffff
        return 0.5 * (nn / 1073741824.0)
    def modulo(self,context,vari_tup):
        a = vari_tup[0]
        b = vari_tup[1]
        mod_div = a/b
        mod_remainder = (mod_div - math.floor(mod_div))*b
        if mod_remainder > 0:
            return True
        else:
            return False
    def calc_brick(self,context,vari_tup):
        modulo = Render_Proc.modulo
        noise = Render_Proc.noise
        #vari_tup should only hold node and (x,y) when we are done..
        x = vari_tup[0][0]
        y = vari_tup[0][1]
        node = vari_tup[1]
        bricknum = 0 
        rownum = 0
        offset = 0
        ins_x = 0 
        ins_y = 0
        tint = 0
        mortar_size = node.inputs[5].default_value
        mortar_smooth = node.inputs[6].default_value
        bias = node.inputs[7].default_value
        brick_width = node.inputs[8].default_value
        row_height = node.inputs[9].default_value
        offset_amount = node.offset
        offset_frequency = node.offset_frequency
        squash = node.squash
        squash_frequency = node.squash_frequency
        
        rownum = math.floor(y / row_height)
        if squash_frequency > 0:
            if modulo(self,context,(rownum,squash_frequency)):
                brick_width *= squash
            else:
                brick_width *= 1
        if offset_frequency  > 0:
            if modulo(self,context,(rownum,offset_frequency)):
                offset = 0.0
            else:
                offset = (brick_width * offset_amount)
        bricknum = math.floor((x + offset) / brick_width);
        x = (x + offset) - brick_width * bricknum
        y = y - row_height * rownum
        tint = max(min((noise(self,context,((rownum << 16) + (bricknum & 0xFFFF))) + bias),1.0),0.0)
        min_dist = min(min(x, y), min(brick_width - x, row_height - y))
        if min_dist >= mortar_size:
            out = (tint, 0.0)
            return out
        elif mortar_smooth == 0.0:
            out = (tint, 1.0)
            return out
        else:
            min_dist = 1.0 - min_dist/mortar_size
            sub_smooth_step = max(min(((0.0 - mortar_smooth) / (min_dist - mortar_smooth)), 1.0), 0.0) 
            smooth_step = sub_smooth_step * sub_smooth_step *(3.0-2.0*sub_smooth_step)
            out = (tint, smooth_step)
            return out
    def tex_brick(self,context,vari_tup):
        bln_utils = nodecopy.BLUEMaN_Node_Utils
        x = vari_tup[0][0]
        y = vari_tup[0][1]
        node = vari_tup[1]
        res = vari_tup[2]
        color1 = node.inputs[1].default_value
        color2 = node.inputs[2].default_value
        mortar = node.inputs[3].default_value
        scale = node.inputs[4].default_value
        tx = x
        ty = y
        if x > 0:
            tx = (1/res)*x
        if y > 0:
            ty = (1/res)*y
        pos = (tx,ty)
        scaled_pos = (tx*scale,ty*scale)
        cb = Render_Proc.calc_brick(self,context,(scaled_pos,node))
        tint = cb[0]
        f = cb[1]
        col_1 = color1
        if f != 1.0:
            facm = 1.0 - tint
            col1r = facm * color1[0] + tint * color2[0]
            col1g = facm * color1[1] + tint * color2[1]
            col1b = facm * color1[2] + tint * color2[2]
            col1a = facm * color1[3] + tint * color2[3]
            col_1 = (col1r,col1g,col1b,col1a)
            
        return bln_utils.col_lerp(self,context,(col_1, mortar, f))
    def execute(self, context, vari_tup):
        res = vari_tup[0]
        path = vari_tup[1]
        node = vari_tup[2]
        name = node.name
        image = bpy.data.images.new(str(name), width=res, height=res)
        pixels = [None] * res * res
        for x in range(res):
            for y in range(res):
                pos =(x,y)
                color = Render_Proc.tex_brick(self,context,(pos,node,res))
                print(color)
                pixels[(y * res) + x] = [color[0], color[1], color[2], 1.0]
        pixels = [chan for px in pixels for chan in px]
        image.pixels = pixels
        nametup = name.split('.')
        newname = ""
        if len(nametup) > 1:
            for n in nametup:
                newname += n + '_'
        else:
            newname = name
        image.filepath_raw = str(path +'/'+ newname + ".png")
        image.file_format = 'PNG'
        image.save()
def render_proc(self, context, vari_tup):
    ctrlc = Render_Proc
    ctrlc.execute(self, context, vari_tup)
    return {'FINISHED'}
def register():
    bpy.utils.register_class(Render_Proc)

def unregister():
    bpy.utils.unregister_class(Render_Proc)

if __name__ == "__main__":
    register()
