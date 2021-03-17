# Bake Blender Textures
Blender addon to bake the textures of a 3d mesh generated by Meshroom

## Requisites:
Blender 2.91

## Installing the addon
Open Blender and go to Edit -> Preferences and open the Addons panel at the left. Click on Install and search for the python file bake_and_export.py. Then, search for the addon using the serach bar and making sure you are on the Comumnity section. With the addon selected, make sure that the check box is checked, so that the addon is enabled in Blender. 

## Using the addon
After you imported your OBJ file and you perform the mesh cleanup, make sure to select your object (in Object Mode) and press the N key to show the right toolbar. If the addon was installed correctly, you should see a panel called Bake. Open the panel and click on the only button, Bake Textures. It will open a window to select the folder in which the files will be saved. 
After some seconds, there should be 4 files in the selected folder, the final mesh in .dae, .fbx and .stl formats, and a baked texture file.


## Modifying the script
To modify the script, you should go to the file that is stored inside the Blender internal folder, rather than modifying the original file. The scrips are usually stored in 
C:\Users\USER\AppData\Roaming\Blender Foundation\Blender\2.91\scripts\addons . After modifying it, you have to load all the scripts again. To do that, click on the blender logo at the top left corner -> system -> reload script.
