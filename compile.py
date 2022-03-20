
import sysconfig
import os
import shutil
import subprocess
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

###---Verify the version of setuptools in global Python for avoid bug---###
command = "pip install --upgrade setuptools==59.8.0"
subprocess.run(command, capture_output=True, shell=True)

###---Compile with Pyinstaller---###

#Delete current output folders
try:
    shutil.rmtree(os.path.join(project_path, "build"))
    shutil.rmtree(os.path.join(project_path, "dist"))
except:
    pass
#Run Pyinstaller in poetry env
command = "poetry shell && pyinstaller --clean --specpath ./ kavt.spec"
subprocess.run(command, capture_output=True, shell=True)

###---Complement de output compile folder with extra tools---###
#TODO: Optimizar, solo copiar lo necesario
#Copy fluid
try:
  shutil.rmtree(os.path.join(project_path, "dist", "kavt", "paddle", "fluid"))
except:
  pass
shutil.copytree(os.path.join(site_packages_path, "paddle", "fluid"), os.path.join(project_path, "dist", "kavt", "paddle", "fluid"))

#Copy Shapely
shutil.copytree(os.path.join(site_packages_path, "Shapely.libs"), os.path.join(project_path, "dist", "kavt", "Shapely.libs"))

#Copy ppocr
shutil.copytree(os.path.join(site_packages_path, "paddleocr", "ppocr"), os.path.join(project_path, "dist", "kavt", "ppocr"))

#Copy easyocr character
shutil.copytree(os.path.join(site_packages_path, "easyocr", "character"), os.path.join(project_path, "dist", "kavt", "easyocr", "character"))