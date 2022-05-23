## Datasets

<!-- old --> 

*Choose subset of data not used for training any of the evaluated models.
Describe the datasets.*

The training data was divided between extreme and frontal poses. Many algorithms
struggle when the face is not pointing mostly towards the camera. However, many
situations in which face landmarking can be employed mostly involve frontal
faces anyway; think of analysing faces in an online video call, for example.
Therefore, good performance on frontal faces could still be valuable when
coupled with good computational performance.

The segmentation between frontal and extreme poses was done in a semi-automated
manner using an off-the-shelf head pose estimation algorithm. The algorithm used
was from the OpenFace 2.0 toolkit [@baltrZadehEtAl2018a], which uses the
algorithm in [@zadehBaltrEtAl2017a] to fit a set of three-dimensional facial
landmarks, from which rotation (and translation) relative to the camera is
inferred. The accuracy is limited in this case, as it relies in part on knowing
camera properties. Accuracy is not necessary in this situation, however, because
the all that is needed is an approximation of frontal or extreme pose;
nonetheless, manual verification of the process was performed. The procedure
then for building the two subsets was:

#. Run the head pose estimation tool on the data
#. Classify into *frontal* and *extreme*:
   - Frontal was defined as a rotation in all directions less than *what?*
   - The remaining faces were classified as extreme. Note that this includes
   faces where the head-pose estimator returned no value.
#. Go through the two sets; reclassify any errors.



