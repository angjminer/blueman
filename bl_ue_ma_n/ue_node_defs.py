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
#this file holds all of the unreal material node definitions needed for conversion
import bpy

#number we will add to to get our unique 32 digit pin id
pid_base = 10000000000000000000000000000000
#we have to convert blender node names to ue names
blen_to_ue4 = {
    #MATH/MIX
    'ADD' : 'MaterialExpressionAdd',
    'SUBTRACT' : 'MaterialExpressionSubtract',
    'MULTIPLY' : 'MaterialExpressionMultiply',
    'DIVIDE' : 'MaterialExpressionDivide',
    #VECTOR MATH
    'NORMALIZE' : 'MaterialExpressionNormalize',
    'DOT_PRODUCT' : 'MaterialExpressionDotProduct',
    'CROSS_PRODUCT' : 'MaterialExpressionCrossProduct',
    #SPECIAL MATH
    'SINE' : 'MaterialExpressionSine',
    'ARCSINE' : 'MaterialExpressionArcsine',
    'COSINE' : 'MaterialExpressionCosine',
    'ARCCOSINE' : 'MaterialExpressionArccosine',
    'POWER' : 'MaterialExpressionPower',
    'MINIMUM' : 'MaterialExpressionMin',
    'MAXIMUM' : 'MaterialExpressionMax',
    'ROUND' : 'MaterialExpressionRound',
    'ABSOLUTE' : 'MaterialExpressionAbs',
    #MIX
    'MIX' : 'MaterialExpressionLinearInterpolate',
    'SCREEN' : 'MaterialExpressionMaterialFunctionCall',
    'DIFFERENCE' : 'MaterialExpressionMaterialFunctionCall',
    'DARKEN' : 'MaterialExpressionMaterialFunctionCall',
    'LIGHTEN' : 'MaterialExpressionMaterialFunctionCall',
    'OVERLAY' : 'MaterialExpressionMaterialFunctionCall',
    'DODGE' : 'MaterialExpressionMaterialFunctionCall',
    'BURN' : 'MaterialExpressionMaterialFunctionCall',
    'SOFT_LIGHT' : 'MaterialExpressionMaterialFunctionCall',
    'LINEAR_LIGHT' : 'MaterialExpressionMaterialFunctionCall',
    #PLACEHOLDER FOR MANUALLY BUILT NODES
    'ShaderNodeValToRGB' : 'WeManuallyBuildThisOne',
    #COMMON
    'ShaderNodeInvert' : 'MaterialExpressionOneMinus',
    'NodeReroute' : 'MaterialExpressionReroute',
    'ShaderNodeSeparateRGB' : 'MaterialExpressionMaterialFunctionCall',
    'ShaderNodeCombineRGB' : 'MaterialExpressionMaterialFunctionCall',
    'ShaderNodeSeparateXYZ' : 'MaterialExpressionMaterialFunctionCall',
    'ShaderNodeCombineXYZ' : 'MaterialExpressionMaterialFunctionCall',
    'ShaderNodeUVMap' : 'MaterialExpressionTextureCoordinate',
    'ShaderNodeValue' : 'MaterialExpressionConstant',
    'ShaderNodeRGB' : 'MaterialExpressionConstant3Vector',
    'ShaderNodeTexImage' : 'MaterialExpressionTextureSampleParameter2D',
    'ShaderNodeBsdfPrincipled' : 'MaterialExpressionSetMaterialAttributes',
    'ShaderNodeMixShader' : 'MaterialExpressionBlendMaterialAttributes',
    }
blen_const_to_ue4 = {
    #MATH/MIX
    'ADD' : ('ConstA' , 'ConstB'),
    'SUBTRACT' : ('ConstA' , 'ConstB'),
    'MULTIPLY' : ('ConstA' , 'ConstB'),
    'DIVIDE' : ('ConstA' , 'ConstB'),
    #VECTOR MATH
    'NORMALIZE' : (''),
    'DOT_PRODUCT' : (''),
    'CROSS_PRODUCT' : (''),
    #SPECIAL MATH
    'SINE' : ('Period='),
    'ARCSINE' : (''),
    'COSINE' : ('Period='),
    'ARCCOSINE' : (''),
    'POWER' : ('ConstExponent='),
    'MINIMUM' : ('ConstA' , 'ConstB'),
    'MAXIMUM' : ('ConstA' , 'ConstB'),
    'ROUND' : (''),
    'ABSOLUTE' : (''),
    #MIX
    'MIX' : ('A' , 'B' , 'Alpha'),
    'SCREEN' : (''),
    'DIFFERENCE' : (''),
    'DARKEN' : (''),
    'LIGHTEN' : (''),
    'OVERLAY' : (''),
    'DODGE' : (''),
    'BURN' : (''),
    'SOFT_LIGHT' : (''),
    'LINEAR_LIGHT' : (''),
    #COMMON
    'ShaderNodeInvert' : ('',''),
    'NodeReroute' : (''),
    'ShaderNodeSeparateRGB' : (''),
    'ShaderNodeCombineRGB' : (''),
    'ShaderNodeSeparateXYZ' : (''),
    'ShaderNodeCombineXYZ' : (''),
    'ShaderNodeUVMap' : ('CoordinateIndex'),
    'ShaderNodeValue' : ('R'),
    'ShaderNodeRGB' : ('R' , 'G' , 'B' , 'A'),
    'ShaderNodeTexImage' : ('Texture=Texture2D\'\"'),
    'ShaderNodeBsdfPrincipled' :(''),
    'ShaderNodeMixShader' : ('A' , 'B' , 'Alpha'),
    }
blen_in_pin_to_ue4 = {
    #MATH/MIX
    'ADD' : ('A' , 'B'),
    'SUBTRACT' : ('A' , 'B'),
    'MULTIPLY' : ('A' , 'B'),
    'DIVIDE' : ('A' , 'B'),
    #VECTOR MATH
    'NORMALIZE' : ('VectorInput',),
    'DOT_PRODUCT' : ('A' , 'B'),
    'CROSS_PRODUCT' : ('A' , 'B'),
    #SPECIAL MATH
    'SINE' : ('Input',),
    'ARCSINE' : ('Input',),
    'COSINE' : ('Input',),
    'ARCCOSINE' : ('Input'),
    'POWER' : ('Base",PinType.PinCategory="required' , 'Exp'),
    'MINIMUM' : ('A' , 'B'),
    'MAXIMUM' : ('A' , 'B'),
    'ROUND' : ('Input',),
    'ABSOLUTE' : ('Input',),
    #MIX
    'MIX' : ('A' , 'B' , 'Alpha'),
    'SCREEN' : ('Blend (V3)' , 'Base (V3)'),
    'DIFFERENCE' : ('Blend (V3)' , 'Base (V3)'),
    'DARKEN' : ('Blend (V3)' , 'Base (V3)'),
    'LIGHTEN' : ('Blend (V3)' , 'Base (V3)'),
    'OVERLAY' : ('Base (V3)' , 'Blend (V3)'),
    'DODGE' : ('Base (V3)' , 'Blend (V3)'),
    'BURN' : ('Base (V3)' , 'Blend (V3)'),
    'SOFT_LIGHT' : ('Base (V3)' , 'Blend (V3)'),
    'LINEAR_LIGHT' : ('Base (V3)' , 'Blend (V3)'),
    #COMMON
    'ShaderNodeInvert' : ('Input',),
    'NodeReroute' : ('InputPin",PinType.PinCategory="wildcard'),
    'ShaderNodeSeparateRGB' : ('Float3 (V3)'),
    'ShaderNodeCombineRGB' : ('X (S)','Y (S)','Z (S)'),
    'ShaderNodeSeparateXYZ' : ('Float3 (V3)'),
    'ShaderNodeCombineXYZ' : ('X (S)','Y (S)','Z (S)'),
    'ShaderNodeUVMap' : ('CoordinateIndex'),#just for looks
    'ShaderNodeValue' : ('R'),#just for looks
    'ShaderNodeRGB' : ('R' , 'G' , 'B' , 'A'),#just for looks
    'ShaderNodeTexImage' : ('UVs'),
    'ShaderNodeBsdfPrincipled' :('BaseColor' , 'SubsurfaceColor' , 'Metallic' , 'Specular' , 'Roughness' , 'ClearCoat' , 'ClearCoatRoughness' , 'Refraction' , 'Opacity' , 'Normal' , 'ClearCoatBottomNormal' , 'CustomEyeTangent'),
    'ShaderNodeMixShader' : ('A' , 'B' , 'Alpha'),
    }
blen_out_pin_to_ue4 = {
    #MATH/MIX 
    'ADD' : ('Output",Direction="EGPD_Output',),
    'SUBTRACT' : ('Output",Direction="EGPD_Output',),
    'MULTIPLY' : ('Output",Direction="EGPD_Output',),
    'DIVIDE' : ('Output",Direction="EGPD_Output',),
    #VECTOR MATH
    'NORMALIZE' : ('Output",Direction="EGPD_Output',),
    'DOT_PRODUCT' : ('Output",Direction="EGPD_Output',),
    'CROSS_PRODUCT' : ('Output",Direction="EGPD_Output',),
    #SPECIAL MATH
    'SINE' : ('Output",Direction="EGPD_Output',),
    'ARCSINE' : ('Output",Direction="EGPD_Output',),
    'COSINE' : ('Output",Direction="EGPD_Output',),
    'ARCCOSINE' : ('Output",Direction="EGPD_Output',),
    'POWER' : ('Output",Direction="EGPD_Output',),
    'MINIMUM' : ('Output",Direction="EGPD_Output',),
    'MAXIMUM' : ('Output",Direction="EGPD_Output',),
    'ROUND' : ('Output",Direction="EGPD_Output',),
    'ABSOLUTE' : ('Output",Direction="EGPD_Output',),
    #MIX
    'MIX' : ('Output",Direction="EGPD_Output',),
    'SCREEN' : ('Result",Direction="EGPD_Output',),
    'DIFFERENCE' : ('Result",Direction="EGPD_Output',),
    'DARKEN' : ('Result",Direction="EGPD_Output',),
    'LIGHTEN' : ('Result",Direction="EGPD_Output',),
    'OVERLAY' : ('Result",Direction="EGPD_Output',),
    'DODGE' : ('Result",Direction="EGPD_Output',),
    'BURN' : ('Result",Direction="EGPD_Output',),
    'SOFT_LIGHT' : ('Result",Direction="EGPD_Output',),
    'LINEAR_LIGHT' : ('Result",Direction="EGPD_Output',),
    #COMMON
    'ShaderNodeInvert' : ('Output",Direction="EGPD_Output',),
    'NodeReroute' : ('OutputPin",Direction="EGPD_Output",PinType.PinCategory="wildcard',),
    'ShaderNodeSeparateRGB' : ('R",Direction="EGPD_Output','G",Direction="EGPD_Output','B",Direction="EGPD_Output',),
    'ShaderNodeCombineRGB' : ('Result",Direction="EGPD_Output',),
    'ShaderNodeSeparateXYZ' : ('R",Direction="EGPD_Output','G",Direction="EGPD_Output','B",Direction="EGPD_Output',),
    'ShaderNodeCombineXYZ' : ('Result",Direction="EGPD_Output',),
    'ShaderNodeUVMap' : ('Output",Direction="EGPD_Output',),
    'ShaderNodeValue' : ('Output",Direction="EGPD_Output',),
    'ShaderNodeRGB' : ('Output",Direction="EGPD_Output',),
    'ShaderNodeTexImage' : ('Output",Direction="EGPD_Output','Output2",Direction="EGPD_Output','Output3",Direction="EGPD_Output','Output4",Direction="EGPD_Output','Output5",Direction="EGPD_Output',),
    'ShaderNodeBsdfPrincipled' :('Output",Direction="EGPD_Output',),
    'ShaderNodeMixShader' : ('Output",Direction="EGPD_Output',),
    }
blen_MIX_blend_types = {
    'MIX' : '',
    'SCREEN' : '',
    'DIFFERENCE' : '',
    'DARKEN' : '',
    'LIGHTEN' : '',
    'OVERLAY' : '',
    'DODGE' : '',
    'BURN' : '',
    'SOFT_LIGHT' : '',
    'LINEAR_LIGHT' : ''
    }
blen_MIX_math = {
    'ADD' : '',
    'SUBTRACT' : '',
    'MULTIPLY' : '',
    'DIVIDE' : '',
    'MINIMUM' : '',
    'MAXIMUM' : ''
    }
blen_skip_input_zero = {
    'ShaderNodeMixRGB':'',
    'ShaderNodeInvert':'',
    'SINE' : '',
    'COSINE' : '',
    'ARCSINE' : '',
    'ARCCOSINE' : '',
    'ROUND' : '',
    'ABSOLUTE' : '',
    'ShaderNodeMixShader' : ''
    }
blen_add_input_zero_back = {
    'MIX':'',
    'ShaderNodeMixShader' : ''
    }
blen_drop_last_output = {
    'NORMALIZE':'',
    'ADD':'',
    'SUBTRACT':'',
    'DOT_PRODUCT':'',
    'CROSS_PRODUCT':''
    }
#####################################################
#NEEDED AND 'SHOULD' NOT CHANGE
#IF SO REBUILD A 'MaterialExpressionSetMaterialAttributes' IN UNREAL MAT EDITOR TO RETRIEVE THE  'AttributeSetTypes()'
#      Inputs(1)=()
#      Inputs(2)=()
#      Inputs(3)=()
#      Inputs(4)=()
#      Inputs(5)=()
#      Inputs(6)=()
#      Inputs(7)=()
#      Inputs(8)=()
#      Inputs(9)=()
#      Inputs(10)=()
#      Inputs(11)=()
#      Inputs(12)=()
#      AttributeSetTypes(0)=69B8D33616ED4D499AA497292F050F7A == BaseColor
#      AttributeSetTypes(1)=5B8FC67951CE40829D777BEEF4F72C44 == SubsurfaceColor
#      AttributeSetTypes(2)=57C3A1617F064296B00B24A5A496F34C == Metallic
#      AttributeSetTypes(3)=9FDAB39925564CC98CD2D572C12C8FED == Specular
#      AttributeSetTypes(4)=D1DD967C4CAD47D39E6346FB08ECF210 == Roughness
#      AttributeSetTypes(5)=9E502E693C8F48FA94645CFD28E5428D == ClearCoat
#      AttributeSetTypes(6)=BE4F2FFD12FC4296B0124EEA12C28D92 == ClearCoatRoughness
#      AttributeSetTypes(7)=D0B0FA0314D74455A851BAC581A0788B == Refraction
#      AttributeSetTypes(8)=B8F50FBA2A754EC19EF672CFEB27BF51 == Opacity
#      AttributeSetTypes(9)=0FA2821A200F4A4AB719B789C1259C64 == Normal
#      AttributeSetTypes(10)=AA3D5C0416294716BBDEC8696A27DD72 == ClearCoatBottomNormal
#      AttributeSetTypes(11)=8EAB2CB273634A248CD14F473F9C8E55 == CustomEyeTangent
#####################################################################
principled_constants = ('Inputs(1)=()','Inputs(2)=()','Inputs(3)=()','Inputs(4)=()','Inputs(5)=()','Inputs(6)=()','Inputs(7)=()','Inputs(8)=()','Inputs(9)=()','Inputs(10)=()','Inputs(11)=()','Inputs(12)=()','AttributeSetTypes(0)=69B8D33616ED4D499AA497292F050F7A','AttributeSetTypes(1)=5B8FC67951CE40829D777BEEF4F72C44','AttributeSetTypes(2)=57C3A1617F064296B00B24A5A496F34C','AttributeSetTypes(3)=9FDAB39925564CC98CD2D572C12C8FED','AttributeSetTypes(4)=D1DD967C4CAD47D39E6346FB08ECF210','AttributeSetTypes(5)=9E502E693C8F48FA94645CFD28E5428D','AttributeSetTypes(6)=BE4F2FFD12FC4296B0124EEA12C28D92','AttributeSetTypes(7)=D0B0FA0314D74455A851BAC581A0788B','AttributeSetTypes(8)=B8F50FBA2A754EC19EF672CFEB27BF51','AttributeSetTypes(9)=0FA2821A200F4A4AB719B789C1259C64','AttributeSetTypes(10)=AA3D5C0416294716BBDEC8696A27DD72','AttributeSetTypes(11)=8EAB2CB273634A248CD14F473F9C8E55')
separatergb_constants = ('MaterialFunction=MaterialFunction\'\"/Engine/Functions/Engine_MaterialFunctions02/Utility/BreakOutFloat3Components.BreakOutFloat3Components\"\'','FunctionInputs(0)=(ExpressionInputId=0FC5C56B4335798F20CB928CF1C87421,Input=(OutputIndex=-1,InputName="Float3"))','FunctionOutputs(0)=(ExpressionOutputId=6BC893C247FCFC567178CE944E213385,Output=(OutputName="R"))','FunctionOutputs(1)=(ExpressionOutputId=9720C81E449DF8E5514FCB8A80FD5FA3,Output=(OutputName="G"))','FunctionOutputs(2)=(ExpressionOutputId=17CE6E2C4E70841B48F3D1B73828AA03,Output=(OutputName="B"))','Outputs(0)=(OutputName="R")','Outputs(1)=(OutputName="G")','Outputs(2)=(OutputName="B")',)
combinergb_constants = ('MaterialFunction=MaterialFunction\'\"/Engine/Functions/Engine_MaterialFunctions02/Utility/MakeFloat3.MakeFloat3\"\'','FunctionInputs(0)=(ExpressionInputId=529C1D96441E07EB03A9E59B8A7F67B6,Input=(OutputIndex=-1,InputName="X"))','FunctionInputs(1)=(ExpressionInputId=B5BD7D1B494F6928732CCDA1C63D8E15,Input=(OutputIndex=-1,InputName="Y"))','FunctionInputs(2)=(ExpressionInputId=050F17B8471570B47A802CB7CAA5A201,Input=(OutputIndex=-1,InputName="Z"))','FunctionOutputs(0)=(ExpressionOutputId=0DD6F9954C067C3E5DDBBBA0D6910DD2,Output=(OutputName="Result"))','Outputs(0)=(OutputName="Result")',)
separatexyz_constants = ('MaterialFunction=MaterialFunction\'\"/Engine/Functions/Engine_MaterialFunctions02/Utility/BreakOutFloat3Components.BreakOutFloat3Components\"\'','FunctionInputs(0)=(ExpressionInputId=0FC5C56B4335798F20CB928CF1C87421,Input=(OutputIndex=-1,InputName="Float3"))','FunctionOutputs(0)=(ExpressionOutputId=6BC893C247FCFC567178CE944E213385,Output=(OutputName="R"))','FunctionOutputs(1)=(ExpressionOutputId=9720C81E449DF8E5514FCB8A80FD5FA3,Output=(OutputName="G"))','FunctionOutputs(2)=(ExpressionOutputId=17CE6E2C4E70841B48F3D1B73828AA03,Output=(OutputName="B"))','Outputs(0)=(OutputName="R")','Outputs(1)=(OutputName="G")','Outputs(2)=(OutputName="B")',)
combinexyz_constants = ('MaterialFunction=MaterialFunction\'\"/Engine/Functions/Engine_MaterialFunctions02/Utility/MakeFloat3.MakeFloat3\"\'','FunctionInputs(0)=(ExpressionInputId=529C1D96441E07EB03A9E59B8A7F67B6,Input=(OutputIndex=-1,InputName="X"))','FunctionInputs(1)=(ExpressionInputId=B5BD7D1B494F6928732CCDA1C63D8E15,Input=(OutputIndex=-1,InputName="Y"))','FunctionInputs(2)=(ExpressionInputId=050F17B8471570B47A802CB7CAA5A201,Input=(OutputIndex=-1,InputName="Z"))','FunctionOutputs(0)=(ExpressionOutputId=0DD6F9954C067C3E5DDBBBA0D6910DD2,Output=(OutputName="Result"))','Outputs(0)=(OutputName="Result")',)
screen_constants = ('MaterialFunction=MaterialFunction\'\"/Engine/Functions/Engine_MaterialFunctions03/Blends/Blend_Screen.Blend_Screen\"\'','FunctionInputs(0)=(ExpressionInputId=A591DEF24B8DE9173A27AE80DCEF3259,Input=(OutputIndex=-1,InputName=\"Blend\"))','FunctionInputs(1)=(ExpressionInputId=A2AC794848506B955B2643B4D7D5E64E,Input=(OutputIndex=-1,InputName=\"Base\"))','FunctionOutputs(0)=(ExpressionOutputId=085286B14E9452E3918853BB8CB1AB7D,Output=(OutputName=\"Result\"))','Outputs(0)=(OutputName=\"Result\")')
difference_constants = ('MaterialFunction=MaterialFunction\'\"/Engine/Functions/Engine_MaterialFunctions03/Blends/Blend_Difference.Blend_Difference\"\'','FunctionInputs(0)=(ExpressionInputId=A591DEF24B8DE9173A27AE80DCEF3259,Input=(OutputIndex=-1,InputName=\"Blend\"))','FunctionInputs(1)=(ExpressionInputId=A2AC794848506B955B2643B4D7D5E64E,Input=(OutputIndex=-1,InputName=\"Base\"))','FunctionOutputs(0)=(ExpressionOutputId=085286B14E9452E3918853BB8CB1AB7D,Output=(OutputName=\"Result\"))','Outputs(0)=(OutputName=\"Result\")')
darken_constants = ('MaterialFunction=MaterialFunction\'\"/Engine/Functions/Engine_MaterialFunctions03/Blends/Blend_Darken.Blend_Darken\"\'','FunctionInputs(0)=(ExpressionInputId=A591DEF24B8DE9173A27AE80DCEF3259,Input=(OutputIndex=-1,InputName=\"Blend\"))','FunctionInputs(1)=(ExpressionInputId=A2AC794848506B955B2643B4D7D5E64E,Input=(OutputIndex=-1,InputName=\"Base\"))','FunctionOutputs(0)=(ExpressionOutputId=085286B14E9452E3918853BB8CB1AB7D,Output=(OutputName=\"Result\"))','Outputs(0)=(OutputName=\"Result\")')
lighten_constants = ('MaterialFunction=MaterialFunction\'\"/Engine/Functions/Engine_MaterialFunctions03/Blends/Blend_Lighten.Blend_Lighten\"\'','FunctionInputs(0)=(ExpressionInputId=A591DEF24B8DE9173A27AE80DCEF3259,Input=(OutputIndex=-1,InputName=\"Blend\"))','FunctionInputs(1)=(ExpressionInputId=A2AC794848506B955B2643B4D7D5E64E,Input=(OutputIndex=-1,InputName=\"Base\"))','FunctionOutputs(0)=(ExpressionOutputId=085286B14E9452E3918853BB8CB1AB7D,Output=(OutputName=\"Result\"))','Outputs(0)=(OutputName=\"Result\")')
overlay_constants = ('MaterialFunction=MaterialFunction\'\"/Engine/Functions/Engine_MaterialFunctions03/Blends/Blend_Overlay.Blend_Overlay\"\'','FunctionInputs(0)=(ExpressionInputId=88817477432D9FAD10A549A321ACA1A3,Input=(OutputIndex=-1,InputName=\"Base\"))','FunctionInputs(1)=(ExpressionInputId=199F573E4F017F639BE3529FE8C8D580,Input=(OutputIndex=-1,InputName=\"Blend\"))','FunctionOutputs(0)=(ExpressionOutputId=C17FADFB4135A52E64E751901D7BE521,Output=(OutputName=\"Result\"))','Outputs(0)=(OutputName=\"Result\")')
dodge_constants = ('MaterialFunction=MaterialFunction\'\"/Engine/Functions/Engine_MaterialFunctions03/Blends/Blend_ColorDodge.Blend_ColorDodge\"\'','FunctionInputs(0)=(ExpressionInputId=A591DEF24B8DE9173A27AE80DCEF3259,Input=(OutputIndex=-1,InputName=\"Blend\"))','FunctionInputs(1)=(ExpressionInputId=A2AC794848506B955B2643B4D7D5E64E,Input=(OutputIndex=-1,InputName=\"Base\"))','FunctionOutputs(0)=(ExpressionOutputId=085286B14E9452E3918853BB8CB1AB7D,Output=(OutputName=\"Result\"))','Outputs(0)=(OutputName=\"Result\")')
burn_constants = ('MaterialFunction=MaterialFunction\'\"/Engine/Functions/Engine_MaterialFunctions03/Blends/Blend_ColorBurn.Blend_ColorBurn\"\'','FunctionInputs(0)=(ExpressionInputId=A2AC794848506B955B2643B4D7D5E64E,Input=(OutputIndex=-1,InputName=\"Base\"))','FunctionInputs(1)=(ExpressionInputId=A591DEF24B8DE9173A27AE80DCEF3259,Input=(OutputIndex=-1,InputName=\"Blend\"))','FunctionOutputs(0)=(ExpressionOutputId=085286B14E9452E3918853BB8CB1AB7D,Output=(OutputName=\"Result\"))','Outputs(0)=(OutputName=\"Result\")')
soft_light_constants = ('MaterialFunction=MaterialFunction\'\"/Engine/Functions/Engine_MaterialFunctions03/Blends/Blend_SoftLight.Blend_SoftLight\"\'','FunctionInputs(0)=(ExpressionInputId=88817477432D9FAD10A549A321ACA1A3,Input=(OutputIndex=-1,InputName=\"Base\"))','FunctionInputs(1)=(ExpressionInputId=199F573E4F017F639BE3529FE8C8D580,Input=(OutputIndex=-1,InputName=\"Blend\"))','FunctionOutputs(0)=(ExpressionOutputId=C17FADFB4135A52E64E751901D7BE521,Output=(OutputName=\"Result\"))','Outputs(0)=(OutputName=\"Result\")')
linear_light_constants = ('MaterialFunction=MaterialFunction\'\"/Engine/Functions/Engine_MaterialFunctions03/Blends/Blend_LinearLight.Blend_LinearLight\"\'','FunctionInputs(0)=(ExpressionInputId=88817477432D9FAD10A549A321ACA1A3,Input=(OutputIndex=-1,InputName=\"Base\"))','FunctionInputs(1)=(ExpressionInputId=199F573E4F017F639BE3529FE8C8D580,Input=(OutputIndex=-1,InputName=\"Blend\"))','FunctionOutputs(0)=(ExpressionOutputId=C17FADFB4135A52E64E751901D7BE521,Output=(OutputName=\"Result\"))','Outputs(0)=(OutputName=\"Result\")')


   
if __name__ == "__main__":
	register()
