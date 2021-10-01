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
size = 640, 480

import bpy
mat = bpy.data.materials['Material']
nodes = mat.node_tree.nodes
brick = diffuse = nodes.get("Brick Texture")
# blank image
image = bpy.data.images.new("MyImage", width=size[0], height=size[1])

## For white image
# pixels = [1.0] * (4 * size[0] * size[1])

def noise(n):
    nn = 0
    n = (n >> 13) ^ n
    nn = (n * (n * n * 60493 + 19990303) + 1376312589) & 0x7fffffff
    return 0.5 * (nn / 1073741824.0)
    
pixels = [None] * size[0] * size[1]
for x in range(size[0]):
    for y in range(size[1]):
        # assign RGBA to something useful
        r = x / size[0]
        g = y / size[1]
        b = (1 - r) * g
        a = 1.0

        pixels[(y * size[0]) + x] = [r, g, b, a]

# flatten list
pixels = [chan for px in pixels for chan in px]

# assign pixels
image.pixels = pixels

# write image
image.filepath_raw = "/tmp/temp.png"
image.file_format = 'PNG'
image.save()
#nodes["Brick Texture"].outputs[0].default_value#color out
#nodes["Brick Texture"].inputs[0].default_value#vector in
#nodes["Brick Texture"].inputs[1].default_value#color1 in
#nodes["Brick Texture"].inputs[2].default_value#color2 in
#nodes["Brick Texture"].inputs[3].default_value#mortor color in
