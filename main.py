import winreg
import ctypes
from PIL import Image
import os
import time
import winshell



# convert image to ICO format
def image_Convert(image_path,output_path):
    current_dir = os.getcwd()
    image = Image.open(os.path.join(current_dir, image_path))
    logo_ico_filename = os.path.join(current_dir, output_path)
    logo_ico = image.resize((128, 128))
    logo_ico.save(logo_ico_filename, format="ICO",quality=100)


# set recycle bin icon using winreg
def set_recycle_bin_icon(icon_path):
    # recycle icon path
    icon_path = os.path.realpath(icon_path)
    key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CLSID\{645FF040-5081-101B-9F08-00AA002F954E}\DefaultIcon"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
    except FileNotFoundError:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)

    # Set the new icon path as the default value
    winreg.SetValueEx(key, "", 0, winreg.REG_SZ, icon_path)
    # Notify the system of the change
    ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
 
    

# check if there item in bin 
def is_recycle_bin_empty():
    recycleBin_items = list(winshell.recycle_bin())
    return len(recycleBin_items) == 0



previous_status = is_recycle_bin_empty()
if previous_status:
    set_recycle_bin_icon("pop_cat_open.ico")
else:
    set_recycle_bin_icon("pop_cat_closed.ico")
    
    
while True:
    current_status = is_recycle_bin_empty()

    if current_status != previous_status:
        if current_status:
            set_recycle_bin_icon("pop_cat_open.ico")
            
        else:
            set_recycle_bin_icon("pop_cat_closed.ico")
        
        previous_status = current_status

    time.sleep(0.2)  
