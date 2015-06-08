#////////////////////////////////////////////////////////////////////////////
#/////////////////////////////Simple tail animation assist tool//////////////
#////////////////////////////ALEC FARAI'S SCRIPT :)//////////////////////////
#############################################################################
# This is not going to animate all tail action corectecly. //////////////////
# You will have to animate the bones after baking them.//////////////////////
# Its based on the principles of animation///////////////////////////////////
#..//////////////IT is open to Development ///////////////////////////////////
#############################################################################
import numpy as np
import bpy
import math
from bpy.props import *
TIP = False
STEP = 1

def Add_driver():
    root_bone = bpy.context.scene['MySpeedFloat']
    # Add driver for Tip's Z rotation
    # Tip.rotz = 1.0 - 1.0*x, where x = Driver.locx
    fcurve = bpy.data.objects['tail'].pose.bones["Bone"].driver_add('location', 2)
    
    drv = fcurve.driver
    drv.type = 'SCRIPTED'
    drv.expression = 'Up_axis_var/2'
    drv.show_debug_info = True
     
    var = drv.variables.new()
    var.name = 'Up_axis_var'
    var.type = 'TRANSFORMS'
     
    targ = var.targets[0]
    targ.id = bpy.data.objects['ty']
    targ.transform_type = 'LOC_Y'
    targ.bone_target = 'Bone'
    targ.transform_space = 'LOCAL_SPACE'


     
    fmod = fcurve.modifiers[0]
    fmod.mode = 'POLYNOMIAL'
    fmod.poly_order = 1
    fmod.coefficients = (1.0, -1.0)
    
def initSceneProperties(scn):
    bpy.types.Scene.MySpeedFloat = FloatProperty(
        name = "Smooth value", 
        description = "Controlls how fast it reacts to the movement",
        default = 2.0,
        min = -10,
        max = 10)   
        
    bpy.types.Scene.MyString = StringProperty(
        name = "MainBone", 
        description = "Add the main bone with the movement transforms ")
    return

initSceneProperties(bpy.context.scene)

# HUD // Heads up display
class DialogOperator(bpy.types.Operator):
    bl_idname = "object.dialog_operator"
    bl_label = "Stage 2 : Animate The bones colision "

    def execute(self, context):
        return {'FINISHED'}
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
bpy.utils.register_class(DialogOperator)

# HUD // Heads up display

class UIPanel(bpy.types.Panel):
    bl_label = " Quick Tail anim panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    
    def draw(self, context):
        layout = self.layout
        scn = context.scene
        
        col = layout.column(align=True)
        col.operator("reset.reset", text=' Priview Action',icon="PLAY").reset = "reset"
        if STEP < 3:
            col.prop(scn, 'MySpeedFloat')
            col.prop(scn, 'MyString')

        if TIP == True and STEP < 3:
            layout.label(text = "Step2: Assign keyframes to bones ")
        
        if STEP < 3:
            col = layout.column(align=True)
            col.operator("reset.reset", text=' Bake Action',icon="KEYINGSET").reset = "bake_A"
            
        if TIP == True and STEP == 2:
            layout.label(text = "Step 3: Add overlap action ")    
            
        col = layout.column(align=True)
        
        if STEP == 2:
            
            col.operator("reset.reset", text=' Polish Action',icon="MOD_DYNAMICPAINT").reset = "polish"
            col.operator("reset.reset", text=' Clear Action frames',icon="ERROR").reset = "bake_B"
        
        if TIP == True and STEP == 2 :
            
            layout.label(text = "↑↑ creates animator friendly keys") 
            
        col = layout.column(align=True)
        col.operator("reset.reset", text='Tool tip',icon="INFO").reset = "tips"
        
        
        
class OBJECT_OT_ResetButton(bpy.types.Operator):
    bl_idname = "reset.reset"
    bl_label = "Say Hello"
    reset = bpy.props.StringProperty()
 
    def execute(self, context):
        if self.reset == 'reset':
            global TIP
            TIP = False 
            bpy.context.scene.MySpeedFloat = bpy.context.scene.MySpeedFloat
            bpy.context.scene.MyString = bpy.context.scene.MyString
            bpy.context.scene.frame_current = 0
               
            bpy.ops.screen.animation_play()

        
        if self.reset == 'bake_A':
            global STEP
            STEP = 2
            
            bpy.context.scene.frame_current = 0
            bake_Anim()
            # Invoke the dialog when loading
            bpy.ops.object.dialog_operator('INVOKE_DEFAULT')

        if self.reset == 'polish':
            Offest_Anim()
                
        if self.reset == 'tips':
            global TIP
            TIP = True       

        if self.reset == 'bake_B':
            global STEP
            STEP = 3
            bake_Anim() 
            
        return{'FINISHED'} 


def Offest_Anim():
    bone_names = [b.name for b in bpy.context.selected_pose_bones]
    fcurves = bpy.context.active_object.animation_data.action.fcurves
    obj_count = len(objlist)+1 # counts how many objects they are 

    for i in range (0,(obj_count*10),10):
        for curve in fcurves:
            if curve.data_path.split('"')[1] in bone_names:
                #1
                keyframePoints = fcurves[4+i].keyframe_points # selects action channel's axis / attribute 
                for keyframe in keyframePoints:# moves the selected channel axis/ attribute
                    for t in range (0,obj_count):                     
                        keyframe.co[0] += (t*(i+1))/(obj_count*1000) # animation curve handle centre
                        keyframe.handle_left[0] += (t*(i+1))/(obj_count*1000)# animation curve centre left handle 
                        keyframe.handle_right[0] += (t*(i+1))/(obj_count*1000) # animation curve centre right handle 
def bake_Anim():
    bpy.ops.pose.select_all(action='DESELECT')
    bpy.ops.pose.select_all(action='TOGGLE')
    range_Start  = bpy.data.scenes[0].frame_start#bone attached to the tail 
    range_End = bpy.data.scenes[0].frame_end#bone attached to the tail 
    
    bpy.ops.nla.bake(step=5,frame_start=range_Start, frame_end=range_End, bake_types={'POSE'})
 
#rty main bone location Y 
#rry main bone rotatation X   

def The_action(scene):

    
    bone_names = [b.name for b in bpy.context.selected_pose_bones]
    fcurves = bpy.context.active_object.animation_data.action.fcurves
    
    for curve in fcurves:
        if curve.data_path.split('"')[1] in bone_names:
            keyframePoints = fcurves[4].keyframe_points # selects action channel's axis / attribute 
            for keyframe in keyframePoints:
                L_FRAME = keyframe.co[0] #last animation frame

    smooth_value = bpy.context.scene['MySpeedFloat']
    frame = scene.frame_current
    root_bone = bpy.context.scene['MyString']#bone attached to the tail 
    bpy.ops.object.select_pattern(pattern=root_bone, case_sensitive=False, extend=True)
    #AXIS's
    rootTZ = bpy.context.object.pose.bones[root_bone].location[2]#MAIN BONE Translate Z
    rootRX = bpy.context.object.pose.bones[root_bone].rotation_quaternion[1]#MAIN BONE Rotate X
    rootRZ = bpy.context.object.pose.bones[root_bone].rotation_quaternion[3]#MAIN BONE Rotate Z// turn
    
    for i in range(len(objlist)):
        bones_list = bpy.context.object.pose.bones[objlist[i]]
  
        if (rootTZ  > 0.1 ):#GOING UP
            bones_list.rotation_quaternion[1] = -rootTZ/smooth_value
            
        if frame > (L_FRAME+10):
            bones_list.rotation_quaternion[1] = 0.02
            bones_list.rotation_quaternion[3] = 0.02

        if (rootTZ  < -0.2):#GOING DOWN
            bones_list.rotation_quaternion[1] = -rootTZ/smooth_value   
        
        if ( rootRX  > 0.2  ):#FACING DOWN 
            bones_list.rotation_quaternion[1] = rootTZ/smooth_value
            
        if ( rootRX  < 0.4  ):#FACING DOWN 
            bones_list.rotation_quaternion[1] = -rootTZ/(smooth_value*2)
            
        if ( rootRX  < -0.1  ):#FACING DOWN 
            bones_list.rotation_quaternion[1] = rootTZ/(smooth_value*2)
            
        if ( int(rootRX*10)  in range(1,2)  ):#FACING DOWN 
            bones_list.rotation_quaternion[1] = 0
            
        if ( rootRZ > 0.1  ):#FACING DOWN 
            bones_list.rotation_quaternion[3] = rootRZ/2
            
        if ( rootRZ  < 0.1  ):#FACING DOWN 
            bones_list.rotation_quaternion[3] = rootRZ/2
            
        if ( int(rootRZ*10)  in range(-1,1)  ):#FACING DOWN 
            bones_list.rotation_quaternion[3] = 0

bpy.app.handlers.frame_change_pre.append(The_action)
proxies= 'A,B,C'#list of objects to attach the expression to
objlist = proxies.split(",")#splits every word as an object wherever theres a comma ,


Add_driver()
bpy.utils.register_module(__name__)
