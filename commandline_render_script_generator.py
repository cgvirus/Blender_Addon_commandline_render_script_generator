# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


import bpy
from bpy.types import Menu, Panel
import os
import sys


bl_info = {
    "name": "commandline render script generator",
    "description": "Generates script for commandline render",
    "author": "Fahad Hasan Pathik CGVIRUS",
    "version": (1, 0),
    "blender": (2, 79, 0),
    "category": "Render",
    "warning":     ""
    }


def create_script(context):
    
    scn = bpy.context.scene
    data = bpy.data.scenes
    scname = scn.name

    appdir = os.path.dirname(bpy.app.binary_path)
    startframe = data[scname].frame_start
    endframe = data[scname].frame_end
    projectfile = bpy.data.filepath
    renderdir =  scn.render.filepath

    #Creates Linux strings
    def linux_string():
        lnx_out = "cd '{0}'\n./blender -b '{1}' -o '{2}#####' -s {3} -e {4} -a"\
        .format(appdir,projectfile,renderdir,startframe,endframe)
        return (lnx_out)

    #Creates Linux shell File
    def creatfile_lnx():
        textfile = open(str(renderdir)+".sh","w")
        textfile.write(linux_string())
        textfile.close()


    #Creates Windows strings
    def win_string():
        win_out = 'cd ""{0}"\nblender -b "{1}" -o "{2}#####" -s {3} -e {4} -a"'\
        .format(appdir,projectfile,renderdir,startframe,endframe)
        return (win_out)

    #Creates Windows bat File
    def creatfile_win():
        textfile = open(str(renderdir)+".bat","w")
        textfile.write(win_string())
        textfile.close()

    #Creates Mac strings
    def mac_string():
        mac_out = "cd '{0}'\n./blender.app/Contents/MacOS/blender -b '{1}' -o '{2}#####' -s {3} -e {4} -a"\
        .format(appdir,projectfile,renderdir,startframe,endframe)
        return (mac_out)

    #Creates Mac shell File
    def creatfile_mac():
        textfile = open(str(renderdir)+".sh","w")
        textfile.write(mac_string())
        textfile.close()
    
    #OS Specific output
    if sys.platform.startswith('linux'):
        creatfile_lnx()
    elif sys.platform.startswith('win32'):
        creatfile_win()
    elif sys.platform.startswith('darwin'):
        creatfile_mac()


class CmdlineRenderScript(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "render.cmdline_script_gen"
    bl_label = "Comandline Render Script Generator"
    
    def execute(self, context):
        if bpy.data.is_dirty == False:
            create_script(context)
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, 'Please specify output directory\nIf done save the project first')
            return {'CANCELLED'}

#UI

class CmdlineRenderScriptPanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_label = "Command Line Render"
    bl_idname = "RENDER_PT_cmdlinerenderscript"

    def draw(self, context):
        layout = self.layout

        row = layout.row(align = True)
        row.operator("render.cmdline_script_gen", \
        text="Generate Commanline Script", icon='FILE_TEXT')
        
def register():
    
    bpy.utils.register_class(CmdlineRenderScript)
    bpy.utils.register_class(CmdlineRenderScriptPanel)

def unregister():

    bpy.utils.unregister_class(CmdlineRenderScript)
    bpy.utils.unregister_class(CmdlineRenderScriptPanel)
    
if __name__ == "__main__":
    register()
