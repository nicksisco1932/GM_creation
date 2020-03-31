#  A basic Python code that can be used to make and convert grey matter mask from Free Surfer output 
There are a couple sections on this script. Originally this was used with MPRAGE MRI data, but it has been reformated here to make grey matter masks and convert them back to the original image space to use in the single and gradient echo (SAGE) MS analysis. 
1) It generates a grey matter mask from Free Surfer outputs
2) It then converts T1 weighted, skull stripped brainmask, and original T1 weighted pre-C .mgz data to nifti
  2a) one of the images from 2 can be replaced with MPRAGE or something like that. 
3) Next the images are reoriented to the standard image space
4) Maurizio Bergamino says that the brain masks need to be in binary and that each of the images need to be floating-point, so those funcitons are applied.
5) Next the images are coregistiered back to native space. 

# Multiprocessing
I got impatient so I got the MP to go. Check CPU number accordingly and adjust processes line to you CPU specs.

