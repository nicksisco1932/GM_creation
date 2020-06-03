# TODO: This file dosn't go here
#  TITLE this is a loop to process and convert all dicom files into nifti files that
#  have been sorted using the dicomsort function
# This is not really a necessary script.

import fnmatch
import os
from tkinter import *
from tkinter import filedialog

import dicom2nifti

root = Tk()
root.withdraw()
path = filedialog.askdirectory()

for i in os.listdir(path):
    if os.path.isdir(os.path.join(path, i)):
        for j in os.listdir(os.path.join(path, i)):
            if fnmatch.fnmatch(j, '*SAGEperfusion*'):
                path_sub_dir = os.path.join(path, i)
                path_sub2_dir = os.path.join(path_sub_dir, j)
                for k in os.listdir(path_sub2_dir):
                    if fnmatch.fnmatch(k, 'Series*'):
                        data_dir = os.path.join(path_sub2_dir, k)
                        temp = str.split(k, 'Series')
                        if not os.path.isfile(os.path.join(path_sub_dir, temp[1] + '_wip_inject_sageperfusion.nii.gz')):
                            dicom2nifti.convert_directory(data_dir, path_sub_dir, True, True)
                        else:
                            pass
                    else:
                        pass
                print(i)
            else:
                pass
    else:
        pass
