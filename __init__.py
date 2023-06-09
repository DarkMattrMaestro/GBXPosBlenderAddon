
bl_info = {
    "name" : "GBXPos",
    "author" : "DarkMattrMaestro",
    "description" : "abcaaaaa",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}



#######################################################
#######################################################
#######################################################



##################### _ Imports _ #####################

import bpy, shutil, json, os, sys, math, numpy, addon_utils, ctypes
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from mathutils import Vector

##################### ^ Imports ^ #####################



############# _ Declare Global Variables _ ############

selectedFileMSG = "No File Selected"
selectedVideoMSG = "No Video Selected"

fileName = None
videoName = None
replayCollectionName = None
carName = None
replayInfoObject = None
cameraTarget = None

loaded = {
    "gbxFile": False,
    "videoFile": False,
    "blocks": False,
    "compositing": False,
    "ghosts": False,
    "camera": False
}

csDir = os.path.join(os.path.dirname(__file__), "GBXPos", "GBXPos", "bin", "Debug")

############# ^ Declare Global Variables ^ ############



####################### _ Math _ ######################



####################### ^ Math ^ ######################



################### _ Message Box _ ###################

def ErrorMessage(message: str):
    title = 'An error occured!'
    ctypes.windll.user32.MessageBoxW(0, message, title, 0)

def ShowMessageBox(title = "Message Box", icon = 'INFO', lines=""):
    myLines=lines
    
    def draw(self, context):
        if (myLines == str(myLines)):
            self.layout.label(text=myLines)
        else:
            for n in myLines:
                self.layout.label(text=n)
            
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

################### ^ Message Box ^ ###################



################## _ Run GBXPos Cs _ ##################

def GBXPosCs():
    lastCWD = os.getcwd()
    
    os.chdir(csDir)
    os.system("GBXPos")
    
    os.chdir(lastCWD)

################## _ Run GBXPos Cs _ ##################



############# _ Select GBXPos JSON File _ #############

class FileSelectOperatorGBXPosJSON(bpy.types.Operator):
    bl_idname = "wm.file_select"
    bl_label = "GBXPos.json File Selection Operator"
    bl_description = "Choose GBX file"
    
    use_setting: BoolProperty(
        name="Example Boolean",
        description="Example Tooltip",
        default=True,
    )

    def execute(self, context):
        GBXPosCs()
        ReadGBXPosJSON(context)
        return {'FINISHED'}

#######################################################

def ReadGBXPosJSON(context):
        print("running ReadGBXPosJSON...")
        
        filepath = os.path.join(os.path.dirname(__file__), "NewReplay.json")
        if not (os.path.isfile(filepath)):
            return
        
        f = open(filepath)
        global replayInfoObject
        replayInfoObject = json.load(f)["Node"]
        f.close()
        
        renamed = os.path.join(os.path.dirname(__file__), "OldReplay.json")
        if (os.path.isfile(renamed)):
            os.remove(renamed)
        os.rename(filepath, renamed)
        
        global selectedFileMSG
        selectedFileMSG = filepath
        
        # Show tooltip with selected file information
        ShowMessageBox(title=str(filepath),icon="FILE",lines=str(replayInfoObject))
        
        global fileName
        fileName = str(filepath).split('\\')[-1].split('.')[0]
        
        global loaded
        loaded["gbxFile"] = True
        
        # Delete default collection
        defaultCollection = bpy.data.collections.get("Collection")
        if (defaultCollection):
            bpy.data.collections.remove(defaultCollection)
        
        # Create new collection
        global replayCollectionName
        replayCollection = bpy.data.collections.new(fileName)
        bpy.context.scene.collection.children.link(replayCollection)
        replayCollectionName = replayCollection.name
        
        # Set scene defaults
        bpy.context.scene.render.fps = 30
        bpy.context.scene.render.engine = "BLENDER_EEVEE"
        bpy.context.scene.render.film_transparent = True
        bpy.context.scene.render.use_motion_blur = True
        #bpy.context.scene.render.motion_blur_shutter = 1
        
        sun = bpy.data.lights.new(name="GBXPosSun",type="SUN")
        sun.angle = math.radians(3)
        sunObject = bpy.data.objects.new("GBXPosSun", sun)
        bpy.data.collections[replayCollectionName].objects.link(sunObject)
        sunObject.rotation_euler.x = math.degrees(45)
        sunObject.rotation_euler.y = math.degrees(-21)
        
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        return

#######################################################

class FileSelectionPanel(bpy.types.Panel):
    # Creates a Panel in the VIEW_3D UI
    bl_label = "GBXPos.json File Selection"
    bl_idname = "FileSelectionPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GBXPos'
    bl_order = 0

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Selected GBXPos.json File:")
        
        row = layout.row()
        row.operator(FileSelectOperatorGBXPosJSON.bl_idname, text="Choose file", icon="SEQUENCE_COLOR_04" if loaded["gbxFile"] else "SEQUENCE_COLOR_09")
        
        row = layout.row()
        global selectedFileMSG
        row.label(text=selectedFileMSG, icon="FILE")

############# ^ Select GBXPos JSON File ^ #############

############# _ Select Video File _ #############

class VideoSelectOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "wm.video_select"
    bl_label = "Video Selection Operator"
    bl_description = "Choose AVI video file"
    
    # ImportHelper mixin class uses this
    filename_ext = ".avi"
    
    filter_glob: StringProperty(
        default="*.avi",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    
    use_setting: BoolProperty(
        name="Example Boolean",
        description="Example Tooltip",
        default=True,
    )
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        return LoadVideo(context, self.filepath, self.use_setting)

#######################################################

def LoadVideo(context, filepath, use_some_setting):
        clip = bpy.data.movieclips.load(filepath)
        
        global selectedVideoMSG
        selectedVideoMSG = filepath
        
        global videoName
        videoName = clip.name
        
        global loaded
        loaded["videoFile"] = True
        
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        return {'FINISHED'}

#######################################################

class VideoSelectionPanel(bpy.types.Panel):
    # Creates a Panel in the VIEW_3D UI
    bl_label = "Background Video Selection"
    bl_idname = "VideoSelectionPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GBXPos'
    bl_order = 1

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.label(text="Selected AVI Video File:")
        
        row = layout.row()
        row.operator(VideoSelectOperator.bl_idname, text="Choose video", icon="SEQUENCE_COLOR_04" if loaded["videoFile"] else "SEQUENCE_COLOR_09")
        
        row = layout.row()
        global selectedVideoMSG
        row.label(text=selectedVideoMSG, icon="FILE_MOVIE")

############# ^ Select Video File ^ #############



################## _ Loading Panel _ ##################

class LoadingPanel(bpy.types.Panel):
    #Creates a Panel in the VIEW_3D UI
    bl_label = "Load Components"
    bl_idname = "LoadingPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GBXPos'
    bl_order = 2

    def draw(self, context):
        layout = self.layout
        
        global loaded

        row = layout.row()
        row.operator(LoadBlocksOperator.bl_idname, text="Load Blocks", icon="SEQUENCE_COLOR_04" if loaded["blocks"] else "SEQUENCE_COLOR_09")
        row.enabled = loaded["gbxFile"]
        
        row = layout.row()
        row.operator(SetupCompositingOperator.bl_idname, text="Setup Compositing", icon="SEQUENCE_COLOR_04" if loaded["compositing"] else "SEQUENCE_COLOR_09")
        row.enabled = loaded["videoFile"]
        
        row = layout.row()
        row.operator(LoadGhostsOperator.bl_idname, text="Load Ghosts", icon="SEQUENCE_COLOR_04" if loaded["ghosts"] else "SEQUENCE_COLOR_09")
        row.enabled = loaded["gbxFile"]
        
        row = layout.row()
        row.operator(LoadCameraOperator.bl_idname, text="Load Camera", icon="SEQUENCE_COLOR_04" if loaded["camera"] else "SEQUENCE_COLOR_09")
        row.enabled = loaded["ghosts"] and loaded["gbxFile"] and loaded["videoFile"]

################## _ Loading Panel _ ##################



################### _ Load Blocks _ ###################

class LoadBlocksOperator(bpy.types.Operator):
    bl_idname = "wm.load_blocks"
    bl_label = "Block Loading Operator"
    bl_description = "Load Blocks From GBXPos.json File"

    def execute(self, context):
        global replayInfoObject
        LoadBlocks(replayInfoObject["Challenge"]["Blocks"])
        
        return {'FINISHED'}



def AbsCeilByInterval(num, interval):
    answer = math.ceil(abs(num/interval))*interval
    if num < 0: answer *= -1
    
    return answer



def GetBlockSizeMax(obj):
    # Get the bounding box corners
    bbox_corners1 = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    
    max1 = (min([corner.x + 0.1 for corner in bbox_corners1]), min([corner.y + 0.1 for corner in bbox_corners1]))
    
    return max1



def GetBlockSizeMin(obj):
    # Get the bounding box corners
    bbox_corners1 = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    
    min1 = (max([corner.x - 0.1 for corner in bbox_corners1]), max([corner.y - 0.1 for corner in bbox_corners1]))
    
    return min1



def ApplyTransparencyTexture(baseObject):
    for slot in baseObject.material_slots:
        slot.material.blend_method = 'BLEND'
        slot.material.shadow_method = 'HASHED'
        slot.material.show_transparent_back = True
        slot.material.use_backface_culling = True
        
        color = (0.55, 0, 0.5)
        
        nodeTree = slot.material.node_tree
        
        texImageNode = None
        for node in nodeTree.nodes:
            print(node.bl_idname)
            if (not node.bl_idname == "ShaderNodeTexImage"):
                nodeTree.nodes.remove(node)
            else:
                texImageNode = node
            
        if not texImageNode:
            continue
        
        ogTex = texImageNode.image
        ogTexPath = bpy.path.abspath(ogTex.filepath, library=ogTex.library)
        print(ogTexPath)
        
        newPath = os.path.join(bpy.context.scene.outputFolder, str(bpy.context.scene.depth1), str(bpy.context.scene.depth2), bpy.context.scene.blockName, ogTexPath.split("\\")[-1])
        print(os.path.dirname(newPath))
        
        if not os.path.exists(os.path.dirname(newPath)):
            os.makedirs(os.path.dirname(newPath), exist_ok=True)
        
        newTexPath = shutil.copyfile(ogTexPath, newPath)
        
        texImageNode.location = (-500, -100)
        texImageNode.use_custom_color = True
        texImageNode.color = color
        texImageNode.image = bpy.data.images.load(newTexPath)
        
        holdoutNode = nodeTree.nodes.new(type="ShaderNodeHoldout")
        holdoutNode.location = (-200, -300)
        holdoutNode.use_custom_color = True
        holdoutNode.color = color
        
        bsdfTransparentNode = nodeTree.nodes.new(type="ShaderNodeBsdfTransparent")
        bsdfTransparentNode.location = (-200, -200)
        bsdfTransparentNode.use_custom_color = True
        bsdfTransparentNode.color = color
        
        mixShaderNode = nodeTree.nodes.new(type="ShaderNodeMixShader")
        mixShaderNode.location = (0, -100)
        mixShaderNode.use_custom_color = True
        mixShaderNode.color = color
        
        outputMaterialNode = nodeTree.nodes.new(type="ShaderNodeOutputMaterial")
        outputMaterialNode.location = (200, -100)
        outputMaterialNode.use_custom_color = True
        outputMaterialNode.color = color
        
        # Connecting Sockets
        
        nodeTree.links.new(holdoutNode.outputs[0], mixShaderNode.inputs[2])
        nodeTree.links.new(bsdfTransparentNode.outputs[0], mixShaderNode.inputs[1])
        nodeTree.links.new(mixShaderNode.outputs[0], outputMaterialNode.inputs["Surface"])
        nodeTree.links.new(texImageNode.outputs["Alpha"], mixShaderNode.inputs["Fac"])



def LoadBlocks(_blocks):
    global replayCollectionName
    
    for block in _blocks:
        ressourcesDir = os.path.join(os.path.dirname(__file__), "resources", "Blocks")
        
        blockDirectory = None
        for root, dirs, files in os.walk(ressourcesDir, topdown=False):
            for name in dirs:
                if (name == block["Name"]):
                    blockDirectory = os.path.join(root, name)
        
        fbxName = ("ground" if block["IsGround"] else "air") + "-" + str(block["Variant"] + 1) + ".fbx" # + "-" + str(block["subVariant"] + 1)
        print("fbx name: " + fbxName)
        blockPath = os.path.join(blockDirectory, fbxName)
        print(blockPath)
        if not os.path.isfile(blockPath):
            return
        
        bpy.ops.import_scene.fbx(filepath=blockPath)
        bpy.context.scene.render.fps = 30
        blockObject = bpy.context.selected_objects[0]
        
        print(blockObject.name)
        
        for collection in blockObject.users_collection:
            collection.objects.unlink(blockObject)
        bpy.data.collections[replayCollectionName].objects.link(blockObject)
        blockObject.rotation_euler.x = 0
        blockObject.rotation_euler.y = 0
        blockObject.rotation_euler.z = math.radians(-90 * block["Direction"])
        minimum = GetBlockSizeMin(blockObject)
        maximum = GetBlockSizeMax(blockObject)
        location = (AbsCeilByInterval(abs(maximum[0] - minimum[0]), 32)/2, AbsCeilByInterval(abs(maximum[1] - minimum[1]), 32)/2)
        print("Minimum: " + str(minimum) + " ; Maximum: " + str(maximum) + " ; Location: " + str(location))
        blockObject.location.x = -block["Coord"]["X"] * 32 - location[1]
        blockObject.location.y = block["Coord"]["Z"] * 32 + location[0]
        blockObject.location.z = block["Coord"]["Y"] * 8 + 1
        
        ApplyTransparencyTexture(blockObject)
    
    global loaded
    loaded["blocks"] = True

################### ^ Load Blocks ^ ###################



################### _ Setup Compositing _ ###################

class SetupCompositingOperator(bpy.types.Operator):
    bl_idname = "wm.setup_compositing"
    bl_label = "Setup Compositing Operator"
    bl_description = "Setup Compositing"

    def execute(self, context):
        SetupCompositing()
        
        return {'FINISHED'}

#######################################################

def SetupCompositing():
    bpy.context.scene.use_nodes = True
    
    color = (0.55, 0, 0.5)
    
    nodeTree = bpy.context.scene.node_tree
    
    for node in nodeTree.nodes:
        node.mute = True
    
    renderLayersNode = nodeTree.nodes.new(type="CompositorNodeRLayers")
    renderLayersNode.location = (-280, -100)
    renderLayersNode.use_custom_color = True
    renderLayersNode.color = color
    
    movieClipNode = nodeTree.nodes.new(type="CompositorNodeMovieClip")
    global videoName
    movieClip = bpy.data.movieclips.get(videoName)
    movieClipNode.clip = movieClip
    movieClipNode.location = (-180, -480)
    movieClipNode.use_custom_color = True
    movieClipNode.color = color
    
    scaleNode = nodeTree.nodes.new(type="CompositorNodeScale")
    scaleNode.space = 'RENDER_SIZE'
    scaleNode.location = (0, -480)
    scaleNode.use_custom_color = True
    scaleNode.color = color
    
    alphaOverNode = nodeTree.nodes.new(type="CompositorNodeAlphaOver")
    alphaOverNode.location = (180, -300)
    alphaOverNode.use_custom_color = True
    alphaOverNode.color = color
    
    compositeNode = nodeTree.nodes.new(type="CompositorNodeComposite")
    compositeNode.location = (360, -300)
    compositeNode.use_custom_color = True
    compositeNode.color = color
    compositeNode.select = True
    
    # Connecting Sockets
    nodeTree.links.new(renderLayersNode.outputs["Image"], alphaOverNode.inputs[2])
    nodeTree.links.new(movieClipNode.outputs["Image"], scaleNode.inputs["Image"])
    nodeTree.links.new(scaleNode.outputs["Image"], alphaOverNode.inputs[1])
    nodeTree.links.new(alphaOverNode.outputs["Image"], compositeNode.inputs["Image"])
    
    global loaded
    loaded["compositing"] = True

################### ^ Setup Compositing ^ ###################



################### _ Load Ghosts _ ###################

class LoadGhostsOperator(bpy.types.Operator):
    bl_idname = "wm.load_ghosts"
    bl_label = "Ghost Loading Operator"
    bl_description = "Load Ghosts From GBXPos.json File"

    def execute(self, context):
        global replayInfoObject
        for _ghost in replayInfoObject["Ghosts"]:
            LoadGhost(_ghost)
        
        return {'FINISHED'}

#######################################################

def LoadGhost(_ghost) :    
    ressourcesDir = os.path.join(os.path.dirname(__file__), "resources")
    carModelPath = os.path.join(ressourcesDir, "StadiumCar1.stl")
    bpy.ops.import_mesh.stl(filepath=carModelPath)
    ghostObject = bpy.context.active_object
    
    global replayCollectionName
    bpy.context.scene.collection.objects.unlink(ghostObject)
    bpy.data.collections[replayCollectionName].objects.link(ghostObject)
    
    global carName
    carName = ghostObject.name
    
    ApplyTransparencyTexture(ghostObject)
    
    ghostObject.rotation_mode = "QUATERNION"
    
    clipEnd = _ghost["RaceTime"]["TotalMilliseconds"]
    
    if (bpy.context.scene.frame_end < 3*clipEnd/100):
        print(str(bpy.context.scene.frame_end) + " < " + str(int(3*clipEnd/100)))
        bpy.context.scene.frame_end = int(3*clipEnd/100)
    
    for sample in _ghost["SampleData"]["Samples"]:
        currentFrame = int(3*sample["Timestamp"]["TotalMilliseconds"]/100)
        
        position = sample["Position"]
        print("Current frame: " + str(currentFrame) + " | " + str(position))
        
        ghostObject.location.x = -position["X"]
        ghostObject.location.y = position["Z"]
        ghostObject.location.z = position["Y"]
        
        rotation = sample["Rotation"]
        
        ghostObject.rotation_quaternion.w = -rotation["W"]
        ghostObject.rotation_quaternion.x = rotation["X"]
        ghostObject.rotation_quaternion.y = -rotation["Z"]
        ghostObject.rotation_quaternion.z = -rotation["Y"]
        
        ghostObject.keyframe_insert(data_path='location', frame=currentFrame)
        ghostObject.keyframe_insert(data_path='rotation_quaternion', frame=currentFrame)
    
    global loaded
    loaded["ghosts"] = True
    return

################### _ Load Ghosts _ ###################



################### _ Load Camera _ ###################

class LoadCameraOperator(bpy.types.Operator):
    bl_idname = "wm.load_camera"
    bl_label = "Camera Loading Operator"
    bl_description = "Load Camera From GBXPos.json File\nRequires loaded Ghost"

    def execute(self, context):
        global replayInfoObject
        for track in replayInfoObject["Clip"]["Tracks"]:
            if track["Name"] == "Camera Custom":
                LoadCameraCustom(track["Blocks"][0])
        
        return {'FINISHED'}

#######################################################

def LoadCameraCustom(_cameraCustom) :
    cameraCustomData = bpy.data.cameras.new(name="CameraCustom | ")# + str(_cameraCustom["name"]))
    cameraCustomData.lens_unit = 'FOV'
    cameraCustomData.angle = math.radians(90)
    global videoName
    movieClip = bpy.data.movieclips.get(videoName)
    cameraCustomData.show_background_images = True
    backgroundImage = cameraCustomData.background_images.new()
    backgroundImage.clip = movieClip
    backgroundImage.source = "MOVIE_CLIP"
    cameraCustomObject = bpy.data.objects.new("CameraCustom | "  , cameraCustomData) # + str(_cameraCustom["name"])
    bpy.context.scene.camera = cameraCustomObject
    
    global replayCollectionName
    bpy.data.collections[replayCollectionName].objects.link(cameraCustomObject)
    
    for keyframe in _cameraCustom["Keys"]:
        currentFrame = int(3*keyframe["Time"]["TotalMilliseconds"]/100)
        
        if (bpy.context.scene.frame_end < currentFrame):
            print(str(bpy.context.scene.frame_end) + " < " + str(currentFrame))
            bpy.context.scene.frame_end = currentFrame
        
        position = keyframe["Position"]
        
        print("Current frame: " + str(currentFrame) + " | " + str(position))
        
        cameraCustomObject.location.x = -position["X"]
        cameraCustomObject.location.y = position["Z"]
        cameraCustomObject.location.z = position["Y"]
        
        cameraCustomObject.keyframe_insert(data_path='location', frame=currentFrame)
        
        interpolation = keyframe["Interpolation"]
        
        SetInterpolationModeXYZ(cameraCustomObject, interpolation, 'location', currentFrame)
        
        target = keyframe["Target"]
        print("Potential target..." + str(target))
        
        if (target == 0 or target == 1):
            print("Yes target!")
            global carName
            ghostObject = bpy.data.objects[carName]
            
            global cameraTarget
            
            constraint = None
            
            targetPosition = keyframe["TargetPosition"]
            
            if (cameraCustomObject.constraints.get('Track To')):
                constraint = cameraCustomObject.constraints.get('Track To')
                if (constraint.influence != 1):
                    constraint.influence = 0
                    constraint.keyframe_insert(data_path='influence', frame=currentFrame-1)
                    constraint.influence = 1#aa
                    constraint.keyframe_insert(data_path='influence', frame=currentFrame)
                
                cameraTarget.location.x = -targetPosition["X"]
                cameraTarget.location.y = targetPosition["Z"]
                cameraTarget.location.z = targetPosition["Y"]
                cameraTarget.keyframe_insert(data_path='location', frame=currentFrame)
                SetInterpolationModeXYZ(cameraTarget, interpolation, 'location', currentFrame)
            else:
                if (cameraTarget == None):
                    cameraTarget = bpy.data.objects.new("Camera Target", None)
                    cameraTarget.empty_display_type = 'PLAIN_AXES'
                    bpy.data.collections[replayCollectionName].objects.link(cameraTarget)
                    cameraTarget.parent = ghostObject
                    
                    cameraTarget.location.x = -targetPosition["X"]
                    cameraTarget.location.y = targetPosition["Z"]
                    cameraTarget.location.z = targetPosition["Y"] + 0.07
                    cameraTarget.keyframe_insert(data_path='location', frame=currentFrame)
                    SetInterpolationModeXYZ(cameraTarget, interpolation, 'location', currentFrame)
                
                constraint = cameraCustomObject.constraints.new(type='TRACK_TO')
                constraint.target = cameraTarget
                constraint.influence = 0
                constraint.keyframe_insert(data_path='influence', frame=currentFrame-1)
                constraint.influence = 1
                constraint.keyframe_insert(data_path='influence', frame=currentFrame)
        elif (target == -1):
            print("No target")
            if (cameraCustomObject.constraints.get('Track To')):
                constraint = cameraCustomObject.constraints.get('Track To')
                
                constraint.influence = 1
                constraint.keyframe_insert(data_path='influence', frame=currentFrame-1)
                constraint.influence = 0
                constraint.keyframe_insert(data_path='influence', frame=currentFrame)
            
            pitchYawRoll = keyframe["pitchYawRoll"]
            
            cameraCustomObject.rotation_euler.x = pitchYawRoll["X"]
            cameraCustomObject.rotation_euler.y = pitchYawRoll["Z"]
            cameraCustomObject.rotation_euler.z = pitchYawRoll["Y"]
            cameraCustomObject.keyframe_insert(data_path='rotation_euler', frame=currentFrame)
    
    global loaded
    loaded["camera"] = True
    return

#######################################################

def SetInterpolationModeXYZ(_object, _interpolationMode: int, _dataPath: str, _currentFrame: int):
    _action = _object.animation_data.action
    
    interpolationModes = [
        "None",
        "Hermite",
        "Linear",
        "FixedTangent"
    ]
    
    selectedMode = interpolationModes[_interpolationMode]
    
    if _action:
        fc = _action.fcurves
        for i in range(3):
            loc_curve = fc.find(_dataPath, index=i)
            
            for k in loc_curve.keyframe_points:
                if (k.co[0] == _currentFrame):
                    if (selectedMode == "None"):
                        k.interpolation = 'CONSTANT'
                    elif (selectedMode == "Hermite"):
                        ErrorMessage("Replay contained an interpolation not yet supported: \"Hermite\".")
                        bpy.ops.wm.quit_blender()
                        #k.interpolation = 'CONSTANT'
                    elif (selectedMode == "Linear"):
                        k.interpolation = 'LINEAR'
                    elif (selectedMode == "FixedTangent"):
                        ErrorMessage("Replay contained an interpolation not yet supported: \"FixedTangent\".")
                        bpy.ops.wm.quit_blender()
                        #k.interpolation = 'CONSTANT'

################### _ Load Camera _ ###################



################# _ Reset Variables _ #################

def resetVars():
    global selectedFileMSG, replayInfoObject
    selectedFileMSG = "No File Selected"
    replayInfoObject = None

################# ^ Reset Variables ^ #################



############## _ Register / Unregister _ ##############

def register():
    bpy.utils.register_class(FileSelectOperatorGBXPosJSON)
    bpy.utils.register_class(FileSelectionPanel)
    
    bpy.utils.register_class(VideoSelectOperator)
    bpy.utils.register_class(VideoSelectionPanel)
    
    bpy.utils.register_class(LoadBlocksOperator)
    bpy.utils.register_class(SetupCompositingOperator)
    bpy.utils.register_class(LoadGhostsOperator)
    bpy.utils.register_class(LoadCameraOperator)
    bpy.utils.register_class(LoadingPanel)
    
    bpy.utils.register_class(TestOperator)
    bpy.utils.register_class(TestPanel)
    
    resetVars()


def unregister():
    bpy.utils.unregister_class(FileSelectOperatorGBXPosJSON)
    bpy.utils.unregister_class(FileSelectionPanel)
    
    bpy.utils.unregister_class(VideoSelectOperator)
    bpy.utils.unregister_class(VideoSelectionPanel)
    
    bpy.utils.unregister_class(LoadBlocksOperator)
    bpy.utils.unregister_class(SetupCompositingOperator)
    bpy.utils.unregister_class(LoadGhostsOperator)
    bpy.utils.unregister_class(LoadCameraOperator)
    bpy.utils.unregister_class(LoadingPanel)
    
    bpy.utils.unregister_class(TestOperator)
    bpy.utils.unregister_class(TestPanel)


if __name__ == "__main__":
    register()

############## ^ Register / Unregister ^ ##############



####################################################################################################
##################### _ Testing _ #####################

def TestFunction():
    blockId = "StadiumRoadMain"
    isGround = True
    variant = 0
    subVariant = 0
    
    ressourcesDir = os.path.join(os.path.dirname(__file__), "resources", "Blocks")
    
    blockDirectory = None
    for root, dirs, files in os.walk(ressourcesDir, topdown=False):
        for name in dirs:
            if (name == blockId):
                blockDirectory = os.path.join(root, name)
    
    fbxName = ("ground" if isGround else "air") + "-" + str(variant + 1) + "-" + str(subVariant + 1) + ".fbx"
    blockPath = os.path.join(blockDirectory, fbxName)
    print("fbx name: " + fbxName)
    print(blockPath)
    if not os.path.isfile(blockPath):
        return
    
    bpy.ops.import_scene.fbx(filepath=blockPath)
    blockObject = bpy.context.active_object

#######################################################

class TestOperator(bpy.types.Operator):
    bl_idname = "wm.test"
    bl_label = "Test Operator"
    bl_description = "Button used for testing"

    def execute(self, context):
        TestFunction()
        
        return {'FINISHED'}

#######################################################

class TestPanel(bpy.types.Panel):
    # Creates a Panel in the VIEW_3D UI
    bl_label = "Test"
    bl_idname = "TestPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GBXPos'
    bl_order = 1000

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator(TestOperator.bl_idname, text="Test", icon="ERROR")

##################### ^ Testing ^ #####################
####################################################################################################