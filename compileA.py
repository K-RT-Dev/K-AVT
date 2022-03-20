
import sysconfig
import os
import shutil

site_packages_path = sysconfig.get_paths()["purelib"]
project_path = os.getcwd()

###---Modify (hack) source files---###

#Pyinstaller hook-shapely.py intervention
#Create new hook-shapely.py with custom folder dlls path
with open(os.path.join(project_path, "compile_aux", "boilerplate-hook-shapely.py"), 'r') as file :
  filedata = file.read()
filedata = filedata.replace('XXX', os.path.join(project_path, "dlls"))
with open(os.path.join(project_path, "compile_aux", "hook-shapely.py"), 'w') as file:
  file.write(filedata)
#Replace default hook-shapely.py with the new one
shutil.copyfile(os.path.join(project_path, "compile_aux", "hook-shapely.py"), os.path.join(site_packages_path, "_pyinstaller_hooks_contrib", "hooks", "stdhooks", "hook-shapely.py"))

#Replace paddle/dataset/image.py file from Paddle with modify one
shutil.copyfile(os.path.join(project_path, "compile_aux", "image.py"), os.path.join(site_packages_path, "paddle", "dataset", "image.py"))

###---Add new hooks---###

# Copy custom hook for Pyinstaller
shutil.copyfile(os.path.join(project_path, "compile_aux", "hook-paddle.py"), os.path.join(site_packages_path, "PyInstaller", "hooks", "hook-paddle.py"))