#!/bin/bash

clear;

echo ">> You need these files from FreeSurfer in nii.gz format"
echo "1) aseg.nii.gz"
echo "2) lh_ribbon.nii.gz"
echo "3) rh_ribbon.nii.gz"
echo "and FSL installed"
echo ""

#AFNI code:
#3dcalc -a lh_ribbon.nii.gz -b rh_ribbon.nii.gz -c aseg.nii.gz -expr 'step(step(a) + step(b) + amongst(c, 8, 9, 10, 11, 12, 13, 18, 47, 48, 49, 50, 51, 52, 54, 55))' -prefix GreyMM_mask.nii.gz -float

echo "!! Running GM creation..."

#FSL code
fslmaths aseg.nii.gz -thr 7.9 -uthr 8.1 -bin roi_8
fslmaths aseg.nii.gz -thr 8.9 -uthr 9.1 -bin roi_9
fslmaths aseg.nii.gz -thr 9.9 -uthr 10.1 -bin roi_10
fslmaths aseg.nii.gz -thr 10.9 -uthr 11.1 -bin roi_11
fslmaths aseg.nii.gz -thr 11.9 -uthr 12.1 -bin roi_12
fslmaths aseg.nii.gz -thr 12.9 -uthr 13.1 -bin roi_13
fslmaths aseg.nii.gz -thr 17.9 -uthr 18.1 -bin roi_18
fslmaths aseg.nii.gz -thr 46.9 -uthr 47.1 -bin roi_47
fslmaths aseg.nii.gz -thr 47.9 -uthr 48.1 -bin roi_48
fslmaths aseg.nii.gz -thr 48.9 -uthr 49.1 -bin roi_49
fslmaths aseg.nii.gz -thr 49.9 -uthr 50.1 -bin roi_50
fslmaths aseg.nii.gz -thr 50.9 -uthr 51.1 -bin roi_51
fslmaths aseg.nii.gz -thr 51.9 -uthr 52.1 -bin roi_52
fslmaths aseg.nii.gz -thr 53.9 -uthr 54.1 -bin roi_54
fslmaths aseg.nii.gz -thr 54.9 -uthr 55.1 -bin roi_55

fslmaths lh_ribbon.nii.gz -add rh_ribbon.nii.gz -add roi_8 -add roi_9 -add roi_10 -add roi_11 -add roi_12 -add roi_13 -add roi_18 -add roi_47 -add roi_48 -add roi_49 -add roi_50 -add roi_51 -add roi_52 -add roi_54 -add roi_55  -bin GreyMM_mask

rm roi_8.nii.gz
rm roi_9.nii.gz
rm roi_10.nii.gz
rm roi_11.nii.gz
rm roi_12.nii.gz
rm roi_13.nii.gz
rm roi_18.nii.gz
rm roi_47.nii.gz
rm roi_48.nii.gz
rm roi_49.nii.gz
rm roi_50.nii.gz
rm roi_51.nii.gz
rm roi_52.nii.gz
rm roi_54.nii.gz
rm roi_55.nii.gz

echo "DONE"
