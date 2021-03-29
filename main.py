#!/usr/bin/env python
import PySimpleGUI as sg
import os
from PIL import Image, ImageTk
import io

"""Place Number Trainer v1.0
   -------------------------
   
   
Source derived from:
https://github.com/PySimpleGUI/PySimpleGUI/tree/master/DemoPrograms
https://moonbooks.org/Articles/How-to-overlay--superimpose-two-images-using-python-and-pillow-/

This desktop application work on basis of generating a mix of
background place and peg sistem in forefront.
Useful for learning porpouses of memory palace.

Remember place pictures of locations in the folder called "places"
Remember place pictures of peg system in the folder called "numbers"



Simple Image Browser based on PySimpleGUI
--------------------------------------------
There are some improvements compared to the PNG browser of the repository:
1. Paging is cyclic, i.e. automatically wraps around if file index is outside
2. Supports all file types that are valid PIL images
3. Limits the maximum form size to the physical screen
4. When selecting an image from the listbox, subsequent paging uses its index
5. Paging performance improved significantly because of using PIL
Dependecies
------------
Python3
PIL
"""

# FOR PLACES
# Get the folder containing the images of places from the user
places = '/home/marco/Documentos/place_number_trainer/places'
if not places:
    sg.popup_cancel('Cancelling')
    raise SystemExit()

# PIL supported image types
img_types = (".png", ".jpg", "jpeg", ".tiff", ".bmp")

# get list of files in folder
plist0 = os.listdir(places)

# create sub list of image files (no sub folders, no wrong file types)
pnames = [f for f in plist0 if os.path.isfile(
    os.path.join(places, f)) and f.lower().endswith(img_types)]

# number of iamges found
num_files = len(pnames)                
if num_files == 0:
    sg.popup('No files in folder')
    raise SystemExit()

# no longer needed
del plist0                             

# FOR NUMBERS

# Get the folder containing the images of places from the user
numbers = '/home/marco/Documentos/place_number_trainer/numbers'
if not numbers:
    sg.popup_cancel('Cancelling')
    raise SystemExit()

# PIL supported image types
img_types = (".png", ".jpg", "jpeg", ".tiff", ".bmp")

# get list of files in folder
nlist0 = os.listdir(numbers)

# create sub list of image files (no sub folders, no wrong file types)
nnames = [f for f in nlist0 if os.path.isfile(
    os.path.join(numbers, f)) and f.lower().endswith(img_types)]

# number of iamges found
num_files = len(nnames)                
if num_files == 0:
    sg.popup('No files in folder')
    raise SystemExit()

# no longer needed
del nlist0                             
# ------------------------------------------------------------------------------
# use PIL to read data of one image
# ------------------------------------------------------------------------------


def get_mix_img_data(p,n, maxsize=(500, 500), first=False):
    """Generate image data using PIL
    """
    img = Image.open(p).convert("RGBA")
    img.thumbnail(maxsize)
    peg = Image.open(n).convert("RGBA")
    peg.thumbnail((100,100))
    img.paste(peg, (200,200),peg)
    if first:                     # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)
# ------------------------------------------------------------------------------


# make these 2 elements outside the layout as we want to "update" them later
# initialize to the first file in the list
pfilename = os.path.join(places, pnames[0])  # name of first file in list
nfilename = os.path.join(numbers, nnames[0])  # name of first file in list
image_elem = sg.Image(data=get_mix_img_data(pfilename,nfilename, first=True)) # PUt pic in wondow
filename_display_elem = sg.Text(pfilename, size=(80, 3)) # display elem
file_num_display_elem = sg.Text('File 1 of {}'.format(num_files), size=(15, 1))

# define layout, show and read the form
col = [[filename_display_elem],
       [image_elem]]

# [sg.Listbox(values=fnames, change_submits=True, size=(60, 30), key='listbox')],
col_files = [[sg.Button('Next', size=(8, 2)), sg.Button('Prev', size=(8, 2)), file_num_display_elem]]

layout = [[sg.Column(col_files), sg.Column(col)]]

window = sg.Window('Place Number Trainer', layout, return_keyboard_events=True,
                   location=(0, 0), use_default_focus=False)

# loop reading the user input and displaying image, filename
i = 0
while True:
    # read the form
    event, values = window.read()
    # perform button and keyboard operations
    if event == sg.WIN_CLOSED:
        break
    elif event in ('Next', 'MouseWheel:Down', 'Down:40', 'Next:34'):
        i += 1
        if i >= num_files:
            i -= num_files
        pfilename = os.path.join(places, pnames[i])
        nfilename = os.path.join(numbers, nnames[i])

    elif event in ('Prev', 'MouseWheel:Up', 'Up:38', 'Prior:33'):
        i -= 1
        if i < 0:
            i = num_files + i
        pfilename = os.path.join(places, pnames[i])
        nfilename = os.path.join(numbers, nnames[i])
    elif event == 'listbox':            # something from the listbox
        f = values["listbox"][0]            # selected filename
        pfilename = os.path.join(places, f)  # read this file
        i = pnames.index(f)                 # update running index
    else:
        pfilename = os.path.join(places, pnames[i])

    # update window with new image
    image_elem.update(data=get_mix_img_data(pfilename, nfilename, first=True))
    # update window with filename
    filename_display_elem.update(pfilename)
    # update page display
    file_num_display_elem.update('File {} of {}'.format(i+1, num_files))

window.close()