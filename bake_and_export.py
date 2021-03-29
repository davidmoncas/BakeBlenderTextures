bl_info = {
    "name": "Export baked file",
    "blender" : (2,91,0),
    "category" : "Object",
    "author": "David Montoya <davidmoncas@gmail.com>",
    "location" : " ",
    "description": "Bake all the textures of one mesh into a single file and then exports the file into FBX, DAE and STL",
}

import bpy
import os 


#Open a folder selection window to save the files there
class CustomDrawOperator(bpy.types.Operator):
    """Bakes the texture files into one and exports it in the desired formats"""
    bl_idname = "mesh.bake_textures"
    bl_label = "Bake Textures"
 
    filepath = bpy.props.StringProperty(name="Outdir Path",
        description="Where I will save my stuff"
        # subtype='DIR_PATH' is not needed to specify the selection mode.
        # But this will be anyway a directory path.
        )
 
 
    def execute(self, context):
        main(self.filepath)
        return {'FINISHED'}
 
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
 
    def draw(self, context):
        layout = self.layout



def main(destinationPath):

    b=bpy.ops 
    c=bpy.context 

    # Create the destination folder
    if not os.path.exists(destinationPath):
        os.mkdir(destinationPath) 


    # Check the selected object
    selected_objects = bpy.context.selected_objects

    if len(selected_objects) == 0 :
        print("please select the object")
        return
        
    elif len(selected_objects) > 1:
        print ("select exactly one object")
        return

    else:
        M = selected_objects[0]
    
    # Create a new UV map
    print("creating a new UV map")
    b.mesh.uv_texture_add()
    M.data.uv_layers.active_index = 1
    M.data.uv_layers[-1].name = "baked"

    # Unwrap the 3d model
    print("unwraping the model")
    b.object.editmode_toggle()
    b.uv.smart_project(scale_to_bounds=True)
    b.object.editmode_toggle()

    # Create a new image
    print("creating a new image")
    b.image.new(name="texture", width=8192, height=8192, color=(0.0, 0.0, 0.0, 1.0), alpha=False, generated_type='BLANK', float=False, use_stereo_3d=False)

    #Change the materials with the node editor
    print("copying the texture in each node")
    for material in M.material_slots:
        
        print("working in: " + material.name) 
        material.material.use_nodes=True
        newNode=material.material.node_tree.nodes.new("ShaderNodeTexImage")
        newNode.image=bpy.data.images["texture"]
       
       #Deselect all the nodes except for the new one
        for node in material.material.node_tree.nodes:
            node.select=False
        
        newNode.select = True
        material.material.node_tree.nodes.active = newNode
        
    # Switch to Cycles
    c.scene.render.engine = 'CYCLES'

    # Starting the bake
    print("Baking...")
    bpy.ops.object.bake(type="DIFFUSE", pass_filter={"COLOR"},use_selected_to_active = False, margin = 3, use_clear = True)
    print("finished")

    #Saving the image in the desired folder
    print("saving texture image")
    bpy.data.images['texture'].filepath_raw = destinationPath + "texture.png"
    bpy.data.images['texture'].file_format = 'PNG'
    bpy.data.images['texture'].save()
    print("image saved")


    # switching to the new UV Map
    c.view_layer.objects.active = M
    M.data.uv_layers["baked"].active_render = True
    M.data.uv_layers.active_index=0
    b.mesh.uv_texture_remove()


    # Removing all the previous materials
    for x in M.material_slots: #For all of the materials in the selected object:
        bpy.context.object.active_material_index = 0 #select the top material
        bpy.ops.object.material_slot_remove() #delete it


    # Create a new material
    bpy.data.materials.new("baked_tex_mat")
    mat=bpy.data.materials['baked_tex_mat']
    mat.use_nodes=True

    # Create a new extra material, apparently Meshlab needs at least 2 materials to show the textures correctly
    bpy.data.materials.new("mat2")
    mat2=bpy.data.materials['mat2']

    node_tree = bpy.data.materials['baked_tex_mat'].node_tree
    node = node_tree.nodes.new("ShaderNodeTexImage")
    node.select = True
    node_tree.nodes.active = node

    node.image=bpy.data.images['texture']

    node_2=node_tree.nodes['Principled BSDF']
    node_tree.links.new(node.outputs["Color"], node_2.inputs["Base Color"])

    # Assign the material to the object
    M.data.materials.append(mat)
    M.data.materials.append(mat2)

    #Export the mesh as FBX, STL and DAE
    print("Exporting to FBX...")
    bpy.ops.export_scene.fbx(filepath=destinationPath + 'finalMesh.fbx')
    print("Exported to FBX")
    print("Exporting to DAE...")
    bpy.ops.wm.collada_export(filepath=destinationPath + 'finalMesh')
    print("Exported to DAE)")
    print("Exporting to STL...")
    bpy.ops.export_mesh.stl(filepath=destinationPath + 'finalMesh.stl')
    print("Exported to STL")


class VIEW3D_PT_bake_and_export(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Bake"
    bl_label = "Bake"

    def draw (self , context):
        self.layout.operator('mesh.bake_textures')
        pass 

    
def menu_func(self, context):
    self.layout.operator(CustomDrawOperator.bl_idname)

    
def register():
    bpy.utils.register_class(CustomDrawOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func)

    bpy.utils.register_class(VIEW3D_PT_bake_and_export)
    print("success!")

    
def unregister():
     bpy.utils.unregister_class(CustomDrawOperator)
     bpy.utils.unregister_class(VIEW3D_PT_bake_and_export)
    
