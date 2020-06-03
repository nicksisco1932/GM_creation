import fnmatch
import multiprocessing as mp
import os
from time import sleep
from tkinter import *
from tkinter import filedialog

# To run free surfer; in command line type:
# >  export SUBJECTS_DIR=<path>
# > recon-all -i some_image.nii.gz -s bert -all -openmp 10
# This will take forever, but hopefully benefit from using 10 CPUs.

# This script was created by Nicholas J. Sisco, Ph.D. by modifying a bash script from Maricio Bergamino, Ph.D. in the
# lab of Ashley Stokes, Ph.D. while at Barrow Neurological Institute.

# The first part of this scrip will convert the .mgz to .nii, which is read in by the fslmaths program. If you try to
# use .mgz, you'll get an error.

# The second part of the script will generate a grey matter mask with from the ROI's generated from the fslmaths.

# I you have questions, email me at nicholas.sisco at barrowneuro dot org

rois = ['roi_8', 'roi_9', 'roi_10', 'roi_11', 'roi_12', 'roi_13', 'roi_18', 'roi_47', 'roi_48', 'roi_49', 'roi_50',
        'roi_51', 'roi_52', 'roi_54', 'roi_55']


def main():
    # path = '/Volumes/MacOS_encrypted/Patient_data/FS_outputs'  # The path where all of the Free Surfer data resides.

    root = Tk()
    root.withdraw()
    path = filedialog.askdirectory()
    pool = mp.Pool(processes=os.cpu_count())
    p = []
    p2 = []
    for i in os.listdir(path):
        if os.path.isdir(os.path.join(path, i)):
            print(i)
            p = pool.apply_async(work, args=(path, i,))
            print('Stage 1 Finished for %s' % os.path.join(path, i))
        else:
            pass
    p.get()
    # work(path,i)
    # for i in os.listdir(path):
    #     if os.path.isdir(os.path.join(path, i)):
    #         p2 = pool.apply_async(coreg, args=(path, i))
    #         print('Stage 2 finished for %s' % os.path.join(path, i))
    #     else:
    #         pass
    # p2.get()
    print('DONE')


def work(path, i):
    print('Doing some work for %s' % i)
    if os.path.isdir(os.path.join(path, i)):
        for j in os.listdir(os.path.join(path, i)):  # start here
            if fnmatch.fnmatch(j, 'FreeSurfer'):
                path_2_FS = os.path.join(path, i, j)
                for g in os.listdir(path_2_FS):
                    if fnmatch.fnmatch(g, 'mri'):
                        path2mri = os.path.join(path_2_FS, g)
                        if os.path.isfile(os.path.join(path2mri, 'GreyMM_mask.nii.gz')):
                            pass
                        else:
                            for mgz in os.listdir(path2mri):
                                if os.path.isdir(os.path.join(path2mri, 'aseg.nii')):
                                    pass
                                else:
                                    os.system('mri_convert %s %s' % (os.path.join(path2mri, mgz),
                                                                     os.path.join(path2mri, 'aseg.nii')))
                                if os.path.isdir(os.path.join(path2mri, 'lh.ribbon.nii')):
                                    pass
                                else:
                                    os.system('mri_convert %s %s' % (os.path.join(path2mri, mgz),
                                                                     os.path.join(path2mri, 'lh.ribbon.nii')))
                                if os.path.isdir(os.path.join(path2mri, 'rh.ribbon.nii')):
                                    pass
                                else:
                                    os.system('mri_convert %s %s' % (os.path.join(path2mri, mgz),
                                                                     os.path.join(path2mri, 'rh.ribbon.nii')))
                            tmp = 1
                            maths_fsl(tmp)
                            roi(tmp)
                        if os.path.isfile(os.path.join(path2mri, 'T1_FS.nii.gz')):
                            pass
                        else:
                            print('Make T1_FS.nii.gz')
                            if os.path.isfile(os.path.join(path2mri, 'T1.mgz')):
                                os.system('mri_convert -it mgz -ot nii -i %s -o %s'
                                          % (os.path.join(path2mri, 'T1.mgz'),
                                             os.path.join(path2mri, 'T1_FS.nii.gz')))
                            else:
                                pass
                        if not os.path.isfile(os.path.join(path2mri, 'T1_FS.nii.gz')):
                            pass
                        else:
                            print('Orient T1_FS.nii.gz')
                            os.system('fslreorient2std %s %s'
                                      % (os.path.join(path2mri, 'T1_FS.nii.gz'),
                                         os.path.join(path2mri, 'T1_FS.nii.gz')))
                        if os.path.isfile(os.path.join(path2mri, 'brain_mask_FS.nii.gz')):
                            pass
                        else:
                            print('Make brain_mask_FS.nii.gz')
                            if os.path.isfile(os.path.join(path2mri, 'T1.mgz')):
                                os.system('mri_convert -it mgz -ot nii -i %s -o %s'
                                          % (os.path.join(path2mri, 'brainmask.mgz'),
                                             os.path.join(path2mri, 'brain_mask_FS.nii.gz')))
                                os.system('fslmaths %s -bin %s' % (os.path.join(path2mri, 'brain_mask_FS.nii.gz'),
                                                                   os.path.join(path2mri, 'brain_mask_FS.nii.gz')))
                            else:
                                pass
                        if not os.path.isfile(os.path.join(path2mri, 'brain_mask_FS.nii.gz')):
                            pass
                        else:
                            print('Orient brain_mask_FS.nii.gz')
                            os.system('fslreorient2std %s %s'
                                      % (os.path.join(path2mri, 'brain_mask_FS.nii.gz'),
                                         os.path.join(path2mri, 'brain_mask_FS.nii.gz')))
                        if os.path.isfile(os.path.join(path2mri, 'T1w_pre.nii.gz')):
                            pass
                        else:
                            print('Remake T1w_pre.nii.gz')
                            if os.path.isfile(os.path.join(path2mri, 'T1.mgz')):
                                os.system('mri_convert -it mgz -ot nii -i %s -o %s'
                                          % (os.path.join(path2mri, 'orig/001.mgz'),
                                             os.path.join(path2mri, 'T1w_pre.nii.gz')))
                            else:
                                pass
                        if not os.path.isfile(os.path.join(path2mri, 'T1w_pre.nii.gz')):
                            pass
                        else:
                            print('Orient T1w_pre.nii.gz')
                            os.system('fslreorient2std %s %s'
                                      % (os.path.join(path2mri, 'T1w_pre.nii.gz'),
                                         os.path.join(path2mri, 'T1w_pre.nii.gz')))
    else:
        pass


def is_running(pid):
    stat = os.system("ps -p %s &> /dev/null" % pid)
    return stat == 0


def coreg(path, i):
    for j in os.listdir(os.path.join(path, i)):
        if fnmatch.fnmatch(j, 'FreeSurfer'):
            path_2_FS = os.path.join(path, i, j)
            for g in os.listdir(path_2_FS):
                if fnmatch.fnmatch(g, 'mri'):
                    path2mri = os.path.join(path_2_FS, g)
                    # for flirty in os.listdir(path2mri): # take this out
                    if not os.path.isfile(os.path.join(path2mri, 'T1_FS_to_NATIVE.mat')):
                        os.system('flirt -in %s -ref %s -out %s -omat %s -bins 256 -cost corratio '
                                  '-searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 6 -interp '
                                  'trilinear'
                                  % (os.path.join(path2mri, 'T1_FS.nii.gz'),
                                     os.path.join(path2mri, 'T1w_pre.nii.gz'),
                                     os.path.join(path2mri, 'T1_FS_to_NATIVE'),
                                     os.path.join(path2mri, 'T1_FS_to_NATIVE.mat')))
                        print('Done with %s' % path2mri)
                    else:
                        print('Done with %s' % path2mri)
                        pass
                    while not os.path.isfile(os.path.join(path2mri, 'T1_FS_to_NATIVE.nii.gz')):
                        print('Waiting to start %s' % path2mri)
                        sleep(5)
                    os.system('flirt -in %s -ref %s -out %s -applyxfm -init %s -paddingsize 0.0 '
                              '-interp nearestneighbour'  # British spelling
                              % (os.path.join(path2mri, 'brain_mask_FS.nii.gz'),
                                 os.path.join(path2mri, 'T1w_pre.nii.gz'),
                                 os.path.join(path2mri, 'brain_mask_FS_to_NATIVE.nii.gz'),
                                 os.path.join(path2mri, 'T1_FS_to_NATIVE.mat')))
                    while not os.path.isfile(os.path.join(path2mri, 'brain_mask_FS_to_NATIVE.nii.gz')):
                        print('Waiting to start second phase for %s' % path2mri)
                        sleep(5)
                    os.system('flirt -in %s -ref %s -out %s -applyxfm -init %s -paddingsize 0.0 '
                              '-interp nearestneighbour'  # British spelling
                              % (os.path.join(path2mri, 'GreyMM_mask.nii.gz'),
                                 os.path.join(path2mri, 'T1w_pre.nii.gz'),
                                 os.path.join(path2mri, 'GM_FS_to_NATIVE.nii.gz'),
                                 os.path.join(path2mri, 'T1_FS_to_NATIVE.mat')))

def maths_fsl(tmp):
    print(tmp)
    thr = [7.9, 8.9, 9.9, 10.9, 11.9, 12.9, 17.9, 46.9, 47.9, 48.9, 49.9, 50.9, 51.9, 53.9, 54.9]
    uthr = [8.1, 9.1, 10.1, 11.1, 12.1, 13.1, 18.1, 47.1, 48.1, 49.1, 50.1, 51.1, 52.1, 54.1, 55.1]

    for i in range(0, 15):
        if os.path.isfile('aseg.nii.gz'):
            os.system('fslmaths aseg.nii.gz -thr %s -uthr %s -bin %s' % (thr[i], uthr[i], rois[i]))
        elif os.path.isfile('aseg.nii'):
            os.system('fslmaths aseg.nii -thr %s -uthr %s -bin %s' % (thr[i], uthr[i], rois[i]))
        else:
            pass  # do nothing.


def roi(tmp):
    print(tmp)
    os.system('fslmaths lh.ribbon.nii.gz -add rh.ribbon.nii.gz -add roi_8.nii.gz -add roi_9.nii.gz -add roi_10.nii.gz '
              '-add roi_11.nii.gz -add roi_12.nii.gz -add roi_13.nii.gz -add roi_18.nii.gz -add roi_47.nii.gz -add '
              'roi_48.nii.gz -add roi_49.nii.gz -add roi_50.nii.gz -add roi_51.nii.gz '
              '-add roi_52.nii.gz -add roi_54.nii.gz -add roi_55.nii.gz  -bin GreyMM_mask')

    for i in range(0, 15):
        os.remove(rois[i] + '.nii.gz')


if __name__ == '__main__':
    main()
