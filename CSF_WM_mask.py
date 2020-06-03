import fnmatch
import multiprocessing as mp
import os

import nipype.interfaces.fsl as fsl_nipype  # fsl


def work(path, i, nifti_dir):
    T1w = file(nifti_dir, 'PT' + i)

    # for k in os.listdir(path):
    leve1 = os.path.join(path, i)

    for j in os.listdir(leve1):
        level2 = os.path.join(leve1, j)
        if os.path.isdir(level2):
            # for dir in os.listdir(level2):
            if os.path.isdir(os.path.join(level2, 'mri')):
                level3 = os.path.join(level2, 'mri')
                # for mri in os.listdir(level3):
                temp = os.path.split(path)
                temp2 = os.path.splitext(temp[1])
                # temp3 = os.path.splitext(temp2[0])
                main_dir = temp[0]
                out_file = os.path.join(level3, 'WM_mask_2_MPRAGE')

                os.system('mri_convert -it mgz -ot nii -i %s -o %s'
                          % (os.path.join(level3, 'T1.mgz'),
                             os.path.join(level3, 'T1_FS.nii.gz')))
                os.system('fslreorient2std %s %s'
                          % (os.path.join(level3, 'T1_FS.nii.gz'),
                             os.path.join(level3, 'T1_FS_reoriented2std.nii.gz')))
                os.system('mri_convert -it mgz -ot nii -i %s -o %s'
                          % (os.path.join(level3, 'aseg.mgz'),
                             os.path.join(level3, 'aseg.nii.gz')))
                os.system('gunzip -f %s' % os.path.join(level3, 'aseg.nii.gz'))
                os.system('fslreorient2std %s %s'
                          % (os.path.join(level3, 'aseg.nii'),
                             os.path.join(level3, 'reoriented_aseg.nii.gz')))
                omat2T1 = registrations_FLIRT(os.path.join(level3, 'T1_FS_reoriented2std.nii.gz'), T1w)
                
                os.system('fslmaths %s -thr 1.9 -uthr 2.1 -bin %s' %
                          (os.path.join(level3, 'reoriented_aseg.nii.gz'),
                           os.path.join(level3, 'left_cerebral_wm_temp.nii.gz')))
                os.system('fslmaths %s -thr 6.9 -uthr 7.1 -bin %s' %
                          (os.path.join(level3, 'reoriented_aseg.nii.gz'),
                           os.path.join(level3, 'left_cerebellar_wm_temp.nii.gz')))
                os.system('fslmaths %s -thr 40.9 -uthr 41.1 -bin %s' %
                          (os.path.join(level3, 'reoriented_aseg.nii.gz'),
                           os.path.join(level3, 'right_cerebral_wm_temp.nii.gz')))
                os.system('fslmaths %s -thr 45.9 -uthr 46.1 -bin %s' %
                          (os.path.join(level3, 'reoriented_aseg.nii.gz'),
                           os.path.join(level3, 'right_cerebellar_wm_temp.nii.gz')))
                os.system('fslmaths %s -thr 23.9 -uthr 24.1 -bin %s' %
                          (os.path.join(level3, 'reoriented_aseg.nii.gz'),
                           os.path.join(level3, 'CSF_temp.nii.gz')))
                # os.system('fslmaths %s -thr 222.9 -uthr 223.1 -bin %s' %
                #           (os.path.join(level3, 'reoriented_aseg.nii.gz'),
                #            os.path.join(level3, 'edge_cerebral_wm_temp.nii.gz')))
                os.system('fslmaths %s -add %s -add %s -add %s -bin %s' %
                          (os.path.join(level3, 'right_cerebral_wm_temp.nii.gz'),
                           os.path.join(level3, 'left_cerebral_wm_temp.nii.gz'),
                           os.path.join(level3, 'left_cerebellar_wm_temp.nii.gz'),
                           os.path.join(level3, 'right_cerebellar_wm_temp.nii.gz'),
                           os.path.join(level3, 'WM_mask_1.nii.gz')))
                os.system(
                    'flirt -in %s -applyxfm -init %s -out %s -paddingsize 0.0 -interp trilinear -ref %s'
                    % (os.path.join(level3, 'WM_mask_1.nii.gz'),
                       omat2T1,
                       os.path.join(level3, 'WM_2_MPRAGEres.nii.gz'),
                       T1w))
                os.system(
                    'flirt -in %s -applyxfm -init %s -out %s -paddingsize 0.0 -interp trilinear -ref %s'
                    % (os.path.join(level3, 'CSF_temp.nii.gz'),
                       omat2T1,
                       os.path.join(level3, 'CSF_2_MPRAGEres.nii.gz'),
                       T1w))
                # os.system('gunzip -f %s' % os.path.join(level3, 'WM_2_MPRAGEres.nii.gz'))
                # os.system('gunzip -f %s' % os.path.join(level3, 'CSF_2_MPRAGEres.nii.gz'))
                # os.system('fslreorient2std %s %s' %
                #           (os.path.join(level3, 'WM_2_MPRAGEres.nii'),
                #            os.path.join(level3, 'WM_mask_reoriented.nii.gz'))
                #           )
                # reorient = nipype.interfaces.fsl.utils.Reorient2Std()
                #
                # reorient.inputs.in_file = os.path.join(level3, 'WM_2_MPRAGEres.nii')
                # reorient.inputs.out_file = os.path.join(level3, 'WM_mask_reoriented.nii.gz')
                # reorient.cmdline
                # reorient.run()
                #
                # reorient = nipype.interfaces.fsl.utils.Reorient2Std()
                # reorient.inputs.in_file = os.path.join(level3, 'CSF_2_MPRAGEres.nii')
                # reorient.inputs.out_file = os.path.join(level3, 'CSF_mask_reoriented.nii.gz')
                # reorient.cmdline
                # reorient.run()

                # os.system('fslreorient2std %s %s' %
                #           (os.path.join(level3, 'CSF_2_MPRAGEres.nii'),
                #            os.path.join(level3, 'CSF_mask_reoriented.nii.gz'))
                #           )


def main():
    path = '/Volumes/MacOS_encrypted/Patient_data/FS_outputs'  # The path where all of the Free Surfer data resides.
    nifti_dir = '/Volumes/MacOS_encrypted/Patient_data/nifti_files'

    proc = 2
    if proc == 1:
        for i in os.listdir(path):
            if os.path.isdir(os.path.join(path, i)):
                work(path, i, nifti_dir)

    elif proc == 2:
        pool = mp.Pool(processes=12)
        for i in os.listdir(path):
            if os.path.isdir(os.path.join(path, i)):

                f = pool.apply_async(work, args=(path, i, nifti_dir,))
            else:
                pass
        pool.close()
        pool.join()


def file(p1, i):
    if os.path.isdir(os.path.join(p1, i)):
        level1 = os.path.join(p1, i)
        for k in os.listdir(level1):
            if fnmatch.fnmatch(k, 'PT13190*-WIP_AX_3D_T1_dicomr*'):
                file = os.path.join(level1, k)
                # print(file2)
                return file
            else:
                pass


def registrations_FLIRT(input, ref):
    temp = os.path.split(input)
    temp2 = os.path.splitext(temp[1])
    temp3 = os.path.splitext(temp2[0])
    main_dir = temp[0]
    omatFile = os.path.join(main_dir, temp3[0] + '_2_MPRAGE_res.txt')
    outfile = os.path.join(main_dir, temp3[0] + '_2_MPRAGE_res.nii.gz')
    if os.path.isfile(outfile):
        flirt = fsl_nipype.FLIRT()
        print(temp3[0] + '_2_MPRAGE_res.nii.gz exists, skipping registration')
        return omatFile
    else:
        flirt = fsl_nipype.FLIRT()
        flirt.inputs.searchr_x = [-90, 90]
        flirt.inputs.searchr_y = [-90, 90]
        flirt.inputs.searchr_z = [-90, 90]
        try:
            in_file = os.path.join(temp[0], temp[1] + '.gz')
            flirt.inputs.in_file = in_file
            flirt.inputs.reference = ref
            flirt.inputs.out_matrix_file = omatFile
            flirt.inputs.out_file = outfile
            flirt.inputs.interp = 'trilinear'
            flirt.inputs.bins = 256
            flirt.inputs.cost = 'corratio'
            flirt.inputs.dof = 12
            print(flirt.cmdline)
            flirt.run()
            return omatFile
        except:
            flirt.inputs.in_file = input
            flirt.inputs.reference = ref
            flirt.inputs.out_matrix_file = omatFile
            flirt.inputs.out_file = outfile
            flirt.inputs.interp = 'trilinear'
            flirt.inputs.bins = 256
            flirt.inputs.cost = 'corratio'
            flirt.inputs.dof = 12
            print(flirt.cmdline)
            flirt.run()
            return omatFile


if __name__ == '__main__':
    main()
