import fnmatch
import multiprocessing as mp
import os

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

#TODO: Get rid of the multiprocessing since it is not used.
#TODO: Remove the commented lines that are not being used.

rois = ['roi_8', 'roi_9', 'roi_10', 'roi_11', 'roi_12', 'roi_13', 'roi_18', 'roi_47', 'roi_48', 'roi_49', 'roi_50',
        'roi_51', 'roi_52', 'roi_54', 'roi_55']


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


def main():
    path = '/Volumes/MacOS_encrypted/Patient_data/FS_outputs'

    os.chdir(path)
    for i in os.listdir():
        if not os.path.isfile(i):
            for j in os.listdir(i):
                if fnmatch.fnmatch(j, 'FreeSurfer'):
                    # path_2_FS = os.getcwd() + '/' + i + '/' + j
                    path_2_FS = os.path.join(path, i, j)
                    for g in os.listdir(path_2_FS):
                        if fnmatch.fnmatch(g, 'mri'):
                            # path2mri = path_2_FS + '/' + g
                            path2mri = os.path.join(path_2_FS, g)
                            # os.chdir(path2mri)
                            if os.path.isfile(os.path.join(path2mri, 'GreyMM_mask.nii.gz')):
                                pass
                            else:
                                for mgz in os.listdir(path2mri):
                                    if fnmatch.fnmatch(mgz, 'aseg.mgz'):
                                        os.system('mri_convert %s %s' % (os.path.join(path2mri, mgz),
                                                                         os.path.join(path2mri, 'aseg.nii')))
                                        print(mgz)
                                    elif fnmatch.fnmatch(mgz, 'lh.ribbon.mgz'):
                                        os.system('mri_convert %s %s' % (os.path.join(path2mri, mgz),
                                                                         os.path.join(path2mri, 'lh.ribbon.nii')))
                                    elif fnmatch.fnmatch(mgz, 'rh.ribbon.mgz'):
                                        os.system('mri_convert %s %s' % (os.path.join(path2mri, mgz),
                                                                         os.path.join(path2mri, 'rh.ribbon.nii')))
                                    else:
                                        pass
                                tmp = 1
                                pool1 = mp.Pool(processes=12)
                                pool1.apply_async(maths_fsl, args=(tmp,))
                                pool1.close()
                                pool1.join()
                                pool2 = mp.Pool(processes=12)
                                pool2.apply(roi, args=(tmp,))
                                pool2.close()
                                pool2.join()
                                os.chdir(path)
                            if os.path.isfile(os.path.join(path2mri, 'T1_FS.nii.gz')):
                                pass
                            else:
                                print('Make T1_FS.nii.gz')
                                if os.path.isfile(os.path.join(path2mri, 'T1.mgz')):
                                    os.system('mri_convert -it mgz -ot nii -i %s -o %s'
                                              % (os.path.join(path2mri,'T1.mgz'),
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
                                    # os.system('mri_convert -it mgz -ot nii -i brainmask.mgz -o brain_mask_FS.nii.gz')
                                    os.system('mri_convert -it mgz -ot nii -i %s -o %s'
                                              % (os.path.join(path2mri, 'brainmask.mgz'),
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
                                    # os.system('mri_convert -it mgz -ot nii -i orig/001.mgz -o T1_FS.nii.gz')
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

    print('DONE')


if __name__ == '__main__':
    main()
