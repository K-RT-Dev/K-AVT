
import sysconfig
import os
import shutil

site_packages_path = sysconfig.get_paths()["purelib"]
project_path = os.getcwd()

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
