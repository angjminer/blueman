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
import hashlib
from bl_ue_ma_n import pyperclip
from bl_ue_ma_n import ue_node_defs
from bl_ue_ma_n import proc_render    
#Class that holds all the utilities used to translate our nodes
class BLUEMaN_Node_Utils(bpy.types.Operator):
    bl_label = "BLUEMaN Node Utils"
    bl_idname = "blueman.nodeutils"
    #you will notice the name "vari_tup", it is a tuple i am using to ease passing variables around
    #eg: nodes = vari_tupe[0], list = vari_tupe[1].........
                 #group_nodes = node.node_tree.nodes
                #group_pidified[node.name] = bln_utils.assign_node_pin_ids(self,context,(group_nodes,True,node.name)) 
                  
    #in ue each node pin has a 32 digit unique id, here we will partially create those to add to pid_base later.
    #expected output:
    #'NODENAME': {
    #'group': {
    #'Group Input': {'inputs': {}, 'outputs': {0: 7584758157581304520, 1: 7584758157581304520, 2: 8939363086113385738, 3: 1271133332502060013}}, 
    #'Group Output': {'inputs': {0: 7485893833331065170, 1: 7065653424574185307}, 'outputs': {}}, 
    #'Mix.002': {'inputs': {0: 2368087132871844714, 1: 8488058183199353554, 2: 25347368053098471}, 'outputs': {0: 2363270044472599139}}, 
    #'Mix.004': {'inputs': {0: 8769018009162353871, 1: 6823539689759620905, 2: 576159276791133167}, 'outputs': {0: 6682489677078126270}}, 
    #'Mix.003': {'inputs': {0: 1784661991420971928, 1: 4816596428530329929, 2: 1510953725666668509}, 'outputs': {0: 6371308200607668616}}
    #}, 
    #'inputs': {0: 4369629311637653624, 1: 8836082557079069611, 2: 2428181517290877505}, 
    #'outputs': {0: 3226694844285547185}
    #'node_id' : numeric hashid
    #}
    def assign_node_pin_ids(self,context,vari_tup):
        bln_utils = BLUEMaN_Node_Utils
        nodes = vari_tup[0]
        if vari_tup[1]:
            parent_name = vari_tup[2]
        nodes_with_pid = {}
        for i, node in enumerate(nodes):
            name = node.name
            nodes_with_pid[name] = {}
            inputs = {}
            outputs = {}
            group = {}
            node_id = {}
            is_group = False
            if node.bl_idname == 'ShaderNodeGroup':
                is_group = True
                group_nodes = node.node_tree.nodes
                group = bln_utils.assign_node_pin_ids(self, context, (group_nodes, is_group, name)) 
            for j, input in enumerate(node.inputs):
                unique_pid= hash(name + str(i) + str(j) + input.name + 'input')
                #some hashes are negative numbers, we do not want that
                if unique_pid < 0:
                    unique_pid = unique_pid * -1
                inputs[j] = unique_pid
            for k, output in enumerate(node.outputs):
                unique_pid= hash(name + str(i) + str(k) + output.name + 'ouput')
                if unique_pid < 0:
                    unique_pid = unique_pid * -1
                outputs[k] = unique_pid  
            nodes_with_pid[name]['inputs'] = inputs
            nodes_with_pid[name]['outputs'] = outputs
            if vari_tup[1]:
                if node.bl_idname == 'NodeGroupInput':
                    for k, output in enumerate(node.outputs):
                        node_id[k] = hash(name + parent_name + str(i) +str(k))
                        if node_id[k] < 0:
                            node_id[k] = node_id[k] * -1
                elif node.bl_idname == 'NodeGroupOutput':
                    for j, input in enumerate(node.inputs):
                        node_id[j] = hash(name + parent_name + str(i) +str(j))
                        if node_id[j] < 0:
                            node_id[j] = node_id[j] * -1
                else:
                    node_id[0] = hash(name + parent_name + str(i))
                    if node_id[0] < 0:
                        node_id[0] = node_id[0] * -1
            else:
                node_id[0] = hash(name + str(i))
                if node_id[0] < 0:
                    node_id[0] = node_id[0] * -1
            nodes_with_pid[name]['node_id'] = node_id
            if is_group:
                nodes_with_pid[name]['group'] = group
        #print(nodes_with_pid)
        return nodes_with_pid    
    #if we only want selected    
    def get_selected(self, context, vari_tup):
        nodes = vari_tup[0]
        selected_only = vari_tup[1]
        selected = {}
        #create a list of selected nodes to export
        for i, node in enumerate(nodes):
            if selected_only:
                if node.select:
                    #add node to list,use enumeration as value
                    selected[node.name] = i
            else:
                selected[node.name] = i
        return selected
    #retrieve node links
    def get_links(self, context, vari_tup):
        pid_ified = vari_tup[0]
        nodes = vari_tup[1]
        links = vari_tup[2]
        from_to = vari_tup[3]
        pid_base = vari_tup[4]
        bln_utils = BLUEMaN_Node_Utils
        connections = {}
        group_connections = {}
        for i, node in enumerate(nodes):
            is_group = False
            if node.bl_idname == 'ShaderNodeGroup':
                is_group = True
                #print("into group")
                group_pid_ified = pid_ified[node.name]['group']
                group_nodes = node.node_tree.nodes
                group_links = node.node_tree.links
                group_connections = bln_utils.get_links(self, context, (group_pid_ified, group_nodes, group_links, from_to, pid_base)) 
            pins = {}
            names = {}
            if from_to:
                for p, output in enumerate(node.outputs):
                    outconnections = ""
                    for link in links:
                        outp = ""
                        if link.from_node.name == node.name:
                            #connections[node.name] = {}
                            names[node.name] = node.name
                            if output.identifier == link.from_socket.identifier:
                                for pn , input in enumerate(nodes[link.to_node.name].inputs):
                                    pident = ""
                                    input_num = 0
                                    if input.identifier == '__extend__':
                                        continue
                                    if input.identifier == link.to_socket.identifier:
                                        upn = pid_ified[link.to_node.name]['inputs'][pn]
                                        if link.to_node.bl_idname == 'ShaderNodeGroup':
                                            node_num = pid_ified[link.to_node.name]['group']['Group Input']['node_id'][pn]
                                        if link.to_node.bl_idname == 'NodeGroupOutput':
                                            node_num = pid_ified[link.to_node.name]['node_id'][pn]
                                        else:
                                            node_num = pid_ified[link.to_node.name]['node_id'][0]
                                        pident = 'MaterialGraphNode_'+ str(node_num) +' '+str(pid_base + upn) + ', '
                                    outp = outp + (pident)
                        outconnections = outconnections + outp
                    pins[p] = outconnections
                connections[node.name] = {}
                if node.name in names:
                    connections[node.name]['pins'] = pins
                if is_group:
                    connections[node.name]['group'] = group_connections
            else:
                for p, input in enumerate(node.inputs):
                    inconnections = ""
                    for link in links:
                        inp = ""
                        if link.to_node.name == node.name:
                            #connections[node.name] = {}
                            names[node.name] = node.name
                            if input.identifier == link.to_socket.identifier:
                                for pn , output in enumerate(nodes[link.from_node.name].outputs):
                                    pident = ""
                                    output_num = 0
                                    if output.identifier == '__extend__':
                                        continue
                                    if output.identifier == link.from_socket.identifier:
                                        upn = pid_ified[link.from_node.name]['outputs'][pn]
                                        if link.from_node.bl_idname == 'ShaderNodeGroup':
                                            node_num = pid_ified[link.from_node.name]['group']['Group Output']['node_id'][pn]
                                        if link.from_node.bl_idname == 'NodeGroupInput':
                                            node_num = pid_ified[link.from_node.name]['node_id'][pn]
                                        else:
                                            node_num = pid_ified[link.from_node.name]['node_id'][0]
                                        output_num = pn
                                        pident = 'MaterialGraphNode_'+ str(node_num) +' '+str(pid_base + upn) + ', '
                                    inp = (pident)
                        inconnections = inconnections + inp
                    pins[p] = inconnections
                connections[node.name] = {}
                if node.name in names:
                    connections[node.name]['pins'] = pins
                if is_group:
                    connections[node.name]['group'] = group_connections
        #print(str(from_to)+str(connections))
        return connections
    def make_node(self,context,vari_tup):
        node = vari_tup[0]
        name = node.name
        nodetype = vari_tup[1]
        selnum = vari_tup[2]
        from_node = vari_tup[3]
        to_node = vari_tup[4]
        pid_ified = vari_tup[5]
        node_location = vari_tup[6]
        bln_def = ue_node_defs
        pid_base = bln_def.pid_base
        blen_to_ue4 = bln_def.blen_to_ue4
        blen_const_to_ue4 = bln_def.blen_const_to_ue4
        blen_in_pin_to_ue4 = bln_def.blen_in_pin_to_ue4
        blen_out_pin_to_ue4 = bln_def.blen_out_pin_to_ue4
        skip_zero = False
        if node.bl_idname in bln_def.blen_skip_input_zero:
            skip_zero = True
        if nodetype in bln_def.blen_skip_input_zero:
            skip_zero = True
        clip_contents = ""
        MaterialExpression = ""
        MaterialExpression = blen_to_ue4[nodetype]
        node_num = pid_ified[name]['node_id'][0]
        #TODO: fix for if reroute_node "MaterialGraphNode" should be "MaterialGraphNode_Knot",,, maybe
        if node.bl_idname == 'NodeReroute':
            clip_contents += str('Begin Object Class=/Script/UnrealEd.MaterialGraphNode_Knot Name=\"MaterialGraphNode_Knot_'+ str(node_num) +'\"\n')
        else:
            clip_contents += str('Begin Object Class=/Script/UnrealEd.MaterialGraphNode Name=\"MaterialGraphNode_'+ str(node_num) +'\"\n')
        clip_contents += str('Begin Object Class=/Script/Engine.'+MaterialExpression+' Name=\"'+MaterialExpression+'_'+ str(node_num) +'\"\n')
        clip_contents += str('End Object\n')
        clip_contents += str('Begin Object Name=\"'+MaterialExpression+'_'+ str(node_num) +'\"\n')
        if node.bl_idname == 'ShaderNodeValue':
            for j, v in enumerate(node.outputs):
                clip_contents += str(blen_const_to_ue4[nodetype][j]+'='+str(node.outputs[j].default_value)+'\n')
        elif node.bl_idname == 'ShaderNodeTexImage': 
            imagepost = node.image.name
            print(str(imagepost))
            image = imagepost.split('.')
            print(str(image[0]))
            clip_contents += str(blen_const_to_ue4[nodetype] + str(image[0] + "." + image[0]) + '\"\'\n')
        elif nodetype == 'SINE': 
            val = 0
            clip_contents += str(blen_const_to_ue4[nodetype] + str(val) + '\"\'\n')
        elif nodetype == 'ARCSINE': 
            val = 0
        elif nodetype == 'COSINE': 
            val = 2
            clip_contents += str(blen_const_to_ue4[nodetype] + str(val) + '\"\'\n')
        elif nodetype == 'ARCCOSINE': 
            val = 0
        elif nodetype == 'ROUND': 
            val = 0
        elif nodetype == 'ABSOLUTE':
            val = 0
        elif nodetype == 'NORMALIZE': 
            val = 0
        elif nodetype == 'POWER': 
            val = node.inputs[1].default_value
            clip_contents += str(blen_const_to_ue4[nodetype] + str(val) + '\"\'\n')
        elif node.bl_idname == 'ShaderNodeBsdfPrincipled':
            for c in bln_def.principled_constants:
                clip_contents += str(c + '\n')
        elif node.bl_idname == 'ShaderNodeSeparateRGB':
            for c in bln_def.separatergb_constants:
                clip_contents += str(c + '\n')
        elif node.bl_idname == 'ShaderNodeCombineRGB':
            for c in bln_def.combinergb_constants:
                clip_contents += str(c + '\n')
        elif node.bl_idname == 'ShaderNodeSeparateXYZ':
            for c in bln_def.separatexyz_constants:
                clip_contents += str(c + '\n')
        elif node.bl_idname == 'ShaderNodeCombineXYZ':
            for c in bln_def.combinexyz_constants:
                clip_contents += str(c + '\n')
        elif nodetype == 'SCREEN':
            for c in bln_def.screen_constants:
                clip_contents += str(c + '\n')
        elif nodetype == 'DIFFERENCE':
            for c in bln_def.difference_constants:
                clip_contents += str(c + '\n')
        elif nodetype == 'DARKEN':
            for c in bln_def.darken_constants:
                clip_contents += str(c + '\n')
        elif nodetype == 'LIGHTEN':
            for c in bln_def.lighten_constants:
                clip_contents += str(c + '\n')
        elif nodetype == 'OVERLAY':
            for c in bln_def.overlay_constants:
                clip_contents += str(c + '\n')
        elif nodetype == 'DODGE':
            for c in bln_def.dodge_constants:
                clip_contents += str(c + '\n')
        elif nodetype == 'BURN':
            for c in bln_def.burn_constants:
                clip_contents += str(c + '\n')
        elif nodetype == 'SOFT_LIGHT':
            for c in bln_def.soft_light_constants:
                clip_contents += str(c + '\n')
        elif nodetype == 'LINEAR_LIGHT':
            for c in bln_def.linear_light_constants:
                clip_contents += str(c + '\n')
        elif node.bl_idname == 'ShaderNodeRGB':
            clip_contents += str('Constant=(R=' + str(node.outputs['Color'].default_value[0]) + ',G=' + str(node.outputs['Color'].default_value[1]) + ',B=' + str(node.outputs['Color'].default_value[2]) + ',A=' + str(node.outputs['Color'].default_value[3]) + ')\n')
        else:
            if node.inputs:	
                for j, v in enumerate(node.inputs):
                    if node.bl_idname == 'ShaderNodeMath':
                        if node.inputs[j].enabled == 'True':
                            clip_contents += str(blen_const_to_ue4[nodetype][j]+'='+str(node.inputs[j].default_value)+'\n')
                    elif node.bl_idname == 'ShaderNodeMixRGB':
                        if nodetype  in bln_def.blen_MIX_math:
                            mj=j+1
                            if mj>2:
                                continue
                            clip_contents += str(blen_const_to_ue4[nodetype][j]+'='+str(node.inputs[mj].default_value[0])+'\n')
        clip_contents += str('MaterialExpressionEditorX='+ str(node_location[0])+'\n')
        clip_contents += str('MaterialExpressionEditorY='+ str(node_location[1])+'\n')
        clip_contents += str('End Object\n')
        clip_contents += str('MaterialExpression='+MaterialExpression+'\'\"'+MaterialExpression+'_'+str(node_num)+'\"\'\n')
        clip_contents += str('NodePosX='+ str(node_location[0])+'\n')
        clip_contents += str('NodePosY='+ str(node_location[1]*-1)+'\n')
        if node.bl_idname == 'ShaderNodeBsdfPrincipled':
            #only place we do not rely on assign_node_pin_ids, this is an extra pin in ue
            upn = hash(name + str(selnum) + str('MaterialAttributes') + 'input')
            if upn < 0:
                upn = upn * -1
            clip_contents += str('CustomProperties Pin (PinId='+str(pid_base + upn)+',PinName="MaterialAttributes",LinkedTo=(),PersistentGuid=00000000000000000000000000000000,)\n')
        for pn , input in enumerate(node.inputs):
            if nodetype == 'NORMALIZE':
                if pn > 0:
                    continue
            #adjusting pin inputs to equal what we need
            npn = pn
            if node.bl_idname == 'ShaderNodeBsdfPrincipled':
                if pn == 1:
                    continue
                if pn == 2:
                    continue
                if pn == 3:
                    npn = pn-2
                if pn == 4:
                    npn = pn-2
                if pn == 5:
                    npn = pn-2				
                if pn == 6:
                    continue
                if pn == 7:
                    npn = pn-3
                if pn == 8:
                    continue
                if pn == 9:
                    continue
                if pn == 10:
                    continue
                if pn == 11:
                    continue
                if pn == 12:
                    npn = pn-7
                if pn == 13:
                    npn = pn-7
                if pn == 14:
                    npn = pn-7
                if pn == 15:
                    npn = pn-7
                if pn == 16:
                    continue
                if pn >= 17:
                    npn = pn-8		
            upn = pid_ified[name]['inputs'][pn]
            if upn < 0:
                upn = upn * -1
            if skip_zero:
                npn = pn-1
                if npn<0:
                    continue
            pname = blen_in_pin_to_ue4[nodetype][npn]
            incon = ''
            if name in to_node:
                if 'pins' in to_node[node.name]:
                    incon = to_node[name]['pins'][pn]
            clip_contents += str('CustomProperties Pin (PinId='+str(pid_base + upn)+',PinName="'+pname+'",LinkedTo=('+str(incon)+'),PersistentGuid=00000000000000000000000000000000,)\n')
        if nodetype in bln_def.blen_add_input_zero_back:#node.bl_idname == 'ShaderNodeMixRGB':
            upn = pid_ified[name]['inputs'][0]
            pname = blen_in_pin_to_ue4[nodetype][0]
            incon = ''
            if name in to_node:
                if 'pins' in to_node[node.name]:
                    incon = to_node[name]['pins'][0]
            clip_contents += str('CustomProperties Pin (PinId='+str(pid_base + upn)+',PinName="'+pname+'",LinkedTo=('+str(incon)+'),PersistentGuid=00000000000000000000000000000000,)\n')

        for pn , output in enumerate(node.outputs):
            if nodetype in bln_def.blen_drop_last_output:
                if pn > 0:
                    continue
            upn = pid_ified[name]['outputs'][pn]
            pname = str(blen_out_pin_to_ue4[nodetype][pn])
            outcon = ''
            if name in from_node:
                if 'pins' in from_node[node.name]:
                    outcon = from_node[name]['pins'][pn]
                #We have 2 outputs from the texture node, ue4 texture node has 5 last being alpha, so,,,,
                if node.bl_idname == 'ShaderNodeTexImage':
                    if pn > 0:
                        for i in range(1,4,1):
                            tpname = str(blen_out_pin_to_ue4[nodetype][i])
                            tupn = hash(str(upn)+tpname)
                            if tupn < 0:
                                tupn = tupn * -1
                            clip_contents += str('CustomProperties Pin (PinId='+str(pid_base + tupn)+',PinName="'+tpname+'",LinkedTo=(''),PersistentGuid=00000000000000000000000000000000,)\n')
                        tpname = str(blen_out_pin_to_ue4[nodetype][4])
                        tupn = hash(str(upn)+tpname)
                        if tupn < 0:
                            tupn = tupn * -1
                        clip_contents += str('CustomProperties Pin (PinId='+str(pid_base + tupn)+',PinName="'+tpname+'",LinkedTo=('+str(outcon)+'),PersistentGuid=00000000000000000000000000000000,)\n')
                    else:
                        clip_contents += str('CustomProperties Pin (PinId='+str(pid_base + upn)+',PinName="'+pname+'",LinkedTo=('+str(outcon)+'),PersistentGuid=00000000000000000000000000000000,)\n')
                else:
                    clip_contents += str('CustomProperties Pin (PinId='+str(pid_base + upn)+',PinName="'+pname+'",LinkedTo=('+str(outcon)+'),PersistentGuid=00000000000000000000000000000000,)\n')
        clip_contents += str('End Object\n')
        return clip_contents
    def create_new_reroute(self,context,vari_tup):
        in_pid = vari_tup[0]
        out_pid = vari_tup[1]
        in_node_pid = vari_tup[2]
        in_connections = vari_tup[3]
        out_connections = vari_tup[4]
        node_location = vari_tup[5]
        bln_def = ue_node_defs
        pid_base = bln_def.pid_base
        clip_contents = ""
        clip_contents += str('Begin Object Class=/Script/UnrealEd.MaterialGraphNode_Knot Name=\"MaterialGraphNode_Knot_'+ str(in_node_pid) +'\"\n')
        clip_contents += str('Begin Object Class=/Script/Engine.MaterialExpressionReroute Name=\"MaterialExpressionReroute_'+ str(in_node_pid) +'\"\n')
        clip_contents += str('End Object\n')
        clip_contents += str('Begin Object Name=\"MaterialExpressionReroute_'+ str(in_node_pid) +'\"\n')   
        clip_contents += str('MaterialExpressionEditorX='+ str(node_location[0])+'\n')
        clip_contents += str('MaterialExpressionEditorY='+ str(node_location[1])+'\n')
        clip_contents += str('End Object\n')
        clip_contents += str('MaterialExpression=MaterialExpressionReroute\'\"MaterialExpressionReroute_'+str(in_node_pid)+'\"\'\n')
        clip_contents += str('NodePosX='+ str(node_location[0])+'\n')
        clip_contents += str('NodePosY='+ str(node_location[1]*-1)+'\n')
        clip_contents += str('CustomProperties Pin (PinId='+str(pid_base + in_pid)+',PinName=\"InputPin\",PinType.PinCategory=\"wildcard\",LinkedTo=('+str(in_connections)+'),PersistentGuid=00000000000000000000000000000000,)\n')
        clip_contents += str('CustomProperties Pin (PinId='+str(pid_base + out_pid)+',PinName=\"OutputPin\",Direction=\"EGPD_Output\",PinType.PinCategory=\"wildcard\",LinkedTo=('+out_connections+'),PersistentGuid=00000000000000000000000000000000,)\n')
        clip_contents += str('End Object\n')
        return clip_contents
    def col_lerp(self,context,vari_tup):
        a = vari_tup[0]
        b = vari_tup[1]
        c = vari_tup[2]
        r = a[0] + (b[0] - a[0]) * c#a[0]*(1-c)+b[0]*c
        g = a[1] + (b[1] - a[1]) * c#a[1]*(1-c)+b[1]*c
        b = a[2] + (b[2] - a[2]) * c#a[2]*(1-c)+b[2]*c
        r = float("{0:.4f}".format(r))
        g = float("{0:.4f}".format(g))
        b = float("{0:.4f}".format(b))
        #alpha = a[3]*(1-c)+b[3]*c
        #(c * a) + ((1-c) * b)
        #a*(1-c)+b*c
        return (r,g,b)#a*(1-c)+b*c
    def create_custom_col_ramp_node(self,context,vari_tup):
        #create 1d lookup table from gradient
        #use input value to get output index value
        #will need to be a custom node in ue...
        lerp = BLUEMaN_Node_Utils.col_lerp
        node = vari_tup[0]
        to_node = vari_tup[1]
        from_node = vari_tup[2]
        pid_ified = vari_tup[3]
        col_ramp_res = vari_tup[4]
        bln_def = ue_node_defs
        pid_base = bln_def.pid_base
        name = node.name
        node_pid = pid_ified[name]['node_id'][0] 
        grad = {}
        ramp = []
        col_pos = []
        index = 0
        table_length = col_ramp_res
        clip_contents = ""
        zeronotatzero = False
        for i,col in enumerate(node.color_ramp.elements):
            if i == 0:
                if col.position > 0.0:
                    ramp.append(col.color)
                    col_pos.append(0.0)
                ramp.append(col.color)
                col_pos.append(col.position)
            elif i == (len(node.color_ramp.elements)-1):
                ramp.append(col.color)
                col_pos.append(col.position)
                if col.position < 1.0:
                    ramp.append(col.color)
                    col_pos.append(1.0)
            else:
                ramp.append(col.color)
                col_pos.append(col.position)
        for i in range(0,table_length,1):
            t = i/table_length
            #print(str(t))

            if (col_pos[index+1] < t):
                index += 1
                if(index>=(len(ramp)-1)):
                    index = index-1
            col1 = ramp[index]
            col2 = ramp[index+1]
            #print(str(col_pos[index+1] - t))
            t1 = (col_pos[index+1] - col_pos[index])
            t2 = (t - col_pos[index])
            t3 = (1/t1)*t2#(t1 / t2)*.1
            if (t3>1):
                t3 = 1 
            t = t3#((col_pos[index+1] - t)*10)
            #print(str(t3))
            grad[i] = lerp(self,context,(col1,col2,t))
            #print(str(index))
        if zeronotatzero:
            table_length = table_length-1
        col_ramp_code = ""
        col_ramp_code += str('Code="float3 gradient['+str(table_length)+'] = {\\'+'n')
        #print('float3 gradient[100] = {\\')
        for c in grad:
            col = grad[c]
            col_ramp_code += str('float3' + str(col) + ',\\'+'n')
        col_ramp_code += str('};\\'+'n')
        col_ramp_code += str('uint a = round(Alpha*'+str(table_length)+');\\'+'n')
        col_ramp_code += str('return float4(gradient[a-1],1);\"\\'+'n')
            
        clip_contents += str('Begin Object Class=/Script/UnrealEd.MaterialGraphNode Name=\"MaterialGraphNode_'+ str(node_pid) +'\"\n')
        clip_contents += str('Begin Object Class=/Script/Engine.MaterialExpressionCustom Name=\"MaterialExpressionCustom_'+ str(node_pid) +'\"\n')
        clip_contents += str('End Object\n')
        clip_contents += str('Begin Object Name=\"MaterialExpressionCustom_'+ str(node_pid) +'\"\n')
        clip_contents += str(col_ramp_code +'\n')
        clip_contents += str('Inputs(0)=(InputName=\"Alpha\")\n')
        clip_contents += str('MaterialExpressionEditorX='+ str(node.location[0])+'\n')
        clip_contents += str('MaterialExpressionEditorY='+ str(node.location[1])+'\n')
        clip_contents += str('End Object\n')
        clip_contents += str('MaterialExpression=MaterialExpressionCustom\'\"MaterialExpressionCustom_'+str(node_pid)+'\"\'\n')
        clip_contents += str('NodePosX='+ str(node.location[0])+'\n')
        clip_contents += str('NodePosY='+ str(node.location[1]*-1)+'\n')
        for pn , input in enumerate(node.inputs):
            upn = pid_ified[name]['inputs'][pn]
            incon = ''
            if name in to_node:
                if 'pins' in to_node[node.name]:
                    incon = to_node[name]['pins'][pn]
            clip_contents += str('CustomProperties Pin (PinId='+str(pid_base + upn)+',PinName=\"Alpha\",PinType.PinCategory=\"required\",LinkedTo=('+str(incon)+'),PersistentGuid=00000000000000000000000000000000,)\n')
        #for pn , output in enumerate(node.outputs):
        upn = pid_ified[name]['outputs'][0]
        outcon = ''
        if name in from_node:
            if 'pins' in from_node[node.name]:
                outcon = from_node[name]['pins'][pn]
        clip_contents += str('CustomProperties Pin (PinId='+str(pid_base + upn)+',PinName=\"OutputPin\",Direction=\"EGPD_Output\",PinType.PinCategory=\"\",LinkedTo=('+str(outcon)+'),PersistentGuid=00000000000000000000000000000000,)\n')
        clip_contents += str('End Object\n')
        #return grad
        return clip_contents
    def create_comment_box(self,context,vari_tup):
        node_pid = vari_tup[0]
        node_size = vari_tup[1]
        node_comment = vari_tup[2]
        node_location = vari_tup[3]
        clip_contents = ""
        clip_contents += str('Begin Object Class=/Script/UnrealEd.MaterialGraphNode_Comment Name=\"MaterialGraphNode_Comment_'+ str(node_pid) +'\"\n')
        clip_contents += str('Begin Object Class=/Script/Engine.MaterialExpressionComment Name=\"MaterialExpressionComment_'+ str(node_pid) +'\"\n')
        clip_contents += str('End Object\n')
        clip_contents += str('Begin Object Name=\"MaterialExpressionComment_'+ str(node_pid) +'\"\n')   
        clip_contents += str('SizeX='+ str(node_size[0])+'\n')
        clip_contents += str('SizeY='+ str(node_size[1])+'\n')
        clip_contents += str('Text=\"'+ str(node_comment)+'\"\n')
        clip_contents += str('End Object\n')
        clip_contents += str('MaterialExpressionComment=MaterialExpressionComment\'\"MaterialExpressionComment_'+str(node_pid)+'\"\'\n')
        clip_contents += str('NodePosX='+ str(node_location[0])+'\n')
        clip_contents += str('NodePosY='+ str((node_location[1]+(node_location[1]/2))*-1)+'\n')
        clip_contents += str('NodeWidth='+ str(node_size[0])+'\n')
        clip_contents += str('NodeHeight='+ str(node_size[1])+'\n')
        clip_contents += str('NodeComment=\"'+ str(node_comment)+'\"\n')
        clip_contents += str('End Object\n')
        return clip_contents
    def blueman_convert(self,context,vari_tup):
        bln_utils = BLUEMaN_Node_Utils
        bln_def = ue_node_defs
        blen_to_ue4 = bln_def.blen_to_ue4
        selected = vari_tup[0]
        nodes = vari_tup[1]
        from_node = vari_tup[2]
        to_node = vari_tup[3]
        pid_ified = vari_tup[4]
        col_ramp_res = vari_tup[7]
        clip_contents = ""
        for name in selected:
            node = nodes[name]
            nodetype = node.bl_idname
            #let the recursion begin... ugh
            #input/output should have been converted to reroute nodes by now so we skip them
            if nodetype == 'NodeGroupInput':
                continue
            if nodetype == 'NodeGroupOutput':
                continue
            if nodetype == 'ShaderNodeGroup':
                #turn group node inputs and outputs into reroute nodes
                #TODO:WORKING SANITYCHECK!!
                for i,input in enumerate(node.inputs):
                    print('inputreroute')
                    in_pid = pid_ified[node.name]['inputs'][i]
                    out_pid = pid_ified[node.name]['group']['Group Input']['outputs'][i]
                    in_node_pid = pid_ified[node.name]['group']['Group Input']['node_id'][i]
                    print(str(in_node_pid))
                    in_connections = ''
                    out_connections = ''
                    if node.name in to_node:
                        if 'pins' in to_node[node.name]:
                            in_connections = to_node[node.name]['pins'][i]
                    if node.name in from_node:
                        if 'pins' in from_node[node.name]['group']['Group Input']:
                            out_connections = from_node[node.name]['group']['Group Input']['pins'][i]
                    node_location = node.location#node.node_tree.nodes['Group Input'].location
                    clip_contents += bln_utils.create_new_reroute(self,context,(in_pid,out_pid,in_node_pid,in_connections,out_connections,node_location))
                for o,input in enumerate(node.outputs):
                    print('outputreroute')
                    in_pid = pid_ified[node.name]['group']['Group Output']['inputs'][o]
                    out_pid = pid_ified[node.name]['outputs'][o]
                    out_node_pid = pid_ified[node.name]['group']['Group Output']['node_id'][o]
                    print(str(out_node_pid))
                    in_connections = ''
                    out_connections = ''
                    if node.name in to_node:
                        if 'pins' in to_node[node.name]['group']['Group Output']:
                            in_connections = to_node[node.name]['group']['Group Output']['pins'][o]
                    if node.name in from_node:
                        if 'pins' in from_node[node.name]:
                            out_connections = from_node[node.name]['pins'][o]
                    node_location = node.location#node.node_tree.nodes['Group Output'].location
                    clip_contents += bln_utils.create_new_reroute(self,context,(in_pid,out_pid,out_node_pid,in_connections,out_connections,node_location))

                group_selected = bln_utils.get_selected(self, context, (node.node_tree.nodes, False))
                group_nodes = node.node_tree.nodes
                group_from_node = from_node[node.name]['group'] 
                group_to_node = to_node[node.name]['group']
                group_pidified = pid_ified[node.name]['group']
                group_node_location = node.location
                comment_node_num = pid_ified[name]['node_id'][0]
                comment_size = (200,200)
                clip_contents += bln_utils.create_comment_box(self,context,(comment_node_num,comment_size,node.label,node.location))
                clip_contents += bln_utils.blueman_convert(self,context,(group_selected,group_nodes,group_from_node,group_to_node,group_pidified,True,group_node_location,col_ramp_res))
                continue
            if nodetype == 'ShaderNodeValToRGB':
                clip_contents +=  bln_utils.create_custom_col_ramp_node(self,context,(node,to_node,from_node,pid_ified,col_ramp_res))
                continue
            if nodetype == 'NodeFrame':
                comment_node_num = pid_ified[name]['node_id'][0]
                comment_size = node.dimensions
                comment_text = node.label
                clip_contents += bln_utils.create_comment_box(self,context,(comment_node_num,comment_size,comment_text,node.location))
                continue
            if nodetype == 'ShaderNodeTexBrick':
                scene = context.scene
                blueman_props = scene.blueman_props
                if blueman_props.render_proc_tex:
                    res = blueman_props.proc_tex_res
                    path = blueman_props.proc_tex_path
                    proc_render.render_proc(self,context,(res,path,node))
                continue
            if nodetype == 'ShaderNodeMath':
                nodetype = node.operation
            if nodetype == 'ShaderNodeVectorMath':
                nodetype = node.operation
            if nodetype == 'ShaderNodeMixRGB':
                nodetype = node.blend_type						
            if nodetype in blen_to_ue4:
                print('cool')
            else:
                self.report({'ERROR'}, 'NODE ' + name + ' of TYPE: ' + nodetype + ' Not supported yet!!')
                print('not cool angelo')
                continue
            if vari_tup[5]:
                node_location = vari_tup[6]
            else:
                node_location = node.location
            clip_contents += bln_utils.make_node(self,context,(nodes[name],nodetype,selected[name],from_node,to_node,pid_ified,node_location))
        return clip_contents 
   
class BLUEMaN_Node_Copy(bpy.types.Operator):
    bl_label = "BLUEMaN Node Copy"
    bl_idname = "blueman.nodecopy"
    def execute(self, context, vari_tup):
        selected_only = vari_tup[0]
        print_to_console = vari_tup[1]
        matname = vari_tup[2]
        col_ramp_res = vari_tup[3]
        print_to_file = vari_tup[4]
        print_to_file_path = vari_tup[5]
        render_proc = vari_tup[6]
        render_proc_path = vari_tup[7]
        render_proc_file_res = vari_tup[8]
        bln_utils = BLUEMaN_Node_Utils
        bln_def = ue_node_defs
        pid_base = bln_def.pid_base
        blen_to_ue4 = bln_def.blen_to_ue4
        blen_const_to_ue4 = bln_def.blen_const_to_ue4
        blen_in_pin_to_ue4 = bln_def.blen_in_pin_to_ue4
        blen_out_pin_to_ue4 = bln_def.blen_out_pin_to_ue4
        principled_constants = bln_def.principled_constants
        mat = bpy.data.materials[matname]
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        selected = bln_utils.get_selected(self, context, (nodes, selected_only))
        pid_ified = bln_utils.assign_node_pin_ids(self,context,(nodes, False))
        from_node = bln_utils.get_links(self, context, (pid_ified, nodes, links, True, pid_base))
        to_node = bln_utils.get_links(self, context, (pid_ified, nodes, links, False, pid_base))

        clip_contents = bln_utils.blueman_convert(self,context,(selected,nodes,from_node,to_node,pid_ified,False,0,col_ramp_res))
        
        if print_to_console:
            print('##########################COPY FROM HERE##############################')
            print(str(clip_contents))
            print('########################TO HERE################################')
        elif print_to_file:
            f = open(print_to_file_path, 'w', encoding='utf-8')
            f.write(clip_contents)
            f.close()
        else:    
            #COPY TO CLIP BOARD
            pyperclip.copy(clip_contents)

            
def copy(self, context, vari_tup):
    ctrlc = BLUEMaN_Node_Copy
    ctrlc.execute(self, context, vari_tup)
    return {'FINISHED'}		

def menu_func(self, context):
    self.layout.operator(BLUEMaN_Node_Copy.bl_idname, text="Copy Nodes to Paste in UE")
    
def register():
    bpy.utils.register_class(BLUEMaN_Node_Utils)
    bpy.utils.register_class(BLUEMaN_Node_Copy)

def unregister():
    bpy.utils.unregister_class(BLUEMaN_Node_Utils)
    bpy.utils.unregister_class(BLUEMaN_Node_Copy)

if __name__ == "__main__":
	register()
