---
title: Evaulation of facial landmarking methods
author: "Yuri Pieters"
date: '`DRAFT - \today`{=latex}'

header-includes:
  - |
    ```{=latex}
    \setkomafont{subject}{ \normalfont\normalcolor\large }
    \setkomafont{publishers}{ \large }

    \titlehead{%
      \hfill Department of Computer Science\\
      \vspace{32pt}
      \begin{center}
        \includegraphics[height=1in]{images/UOY-Logo-Stacked-shield-Black.png}
      \end{center}
    }
    \subject{Submitted in part fulfilment for the degree of BSc.}
    \publishers{Supervisor: Nick Pears}
    ```
  - |
    ```{=latex}
    \setmathrm{TeX Gyre Pagella}
    ```
...

# Executive Summary {.unnumbered}

*the following is an outline*

Aim: The goal of this work was to understand, compare, and evaluate a range of
different techniques used for landmark localisation on faces. In this report I
present the models I chose to evaluate, the datasets I evaluated them against,
and the results of the evaluation. I also present a review of the field overall,
which motivates the particular models and datasets I choose.

Motivation:

- Computer vision is an important part of many topics at the bleeding edge of
  computer science: robotics, self driving cars, human computer interfaces.
- Computer vision techniques aren't one size fits all. To pick between them
  requires understanding of the differences.
- Recognition of faces is an important and frequently used application of
  computer vision.
- Therefore understanding and picking between face recognition algorithms is
  important.

Methods: I evaluated the algorithms by running them on the same set of data, and
calculating how closely they reproduced the true landmark points.

Results: I found that ....

Social and ethical issues of face detection and landmarking:

- Human faces have a huge variety
- Everyone has a right to be able to use the technology that may be supported by
  computer vision
- Therefore both the computer vision techniques and actual implementation of
  those techniques (e.g. the actual training images used) should be developed
  with the full diversity of humans in mind.


# Introduction

Automatic analysis of human faces is a complex problem. Humans have an intuitive
understanding of the human face from a very young age ([@fig:baby]), and we
quickly learn to interpret the faces of others to tell us who they are, where
they are looking, what they are feeling, and more; the face is a rich form of
non-verbal communication [@kanwiYovel2009a]. The ease with which we do this
belies the difficulty we have had in teaching computers to do the same, however.
Trying to infer something as subtle as emotion from a collection of pixels, full
of noise arising from lighting conditions, camera properties, accessories such
as hats and glasses, or simply the diversity of human faces, is a non-trivial
task. The solution, of course, is to pre-process the data somehow to extract
only relevant features [@martiValst2016a]. This breaks a difficult problem (such
analysing facial expressions), into more manageable sub-problems, which can be
tackled separately. One such pre-processing technique that turns out to be
useful for multiple different tasks is facial landmarking [@martiValst2016a;
@murphTrive2009a].

![An expert face analyser[^1]](./images/sleeping_baby.jpg){#fig:baby width=60%}

[^1]: "[Sleeping Baby](https://www.flickr.com/photos/biblicone/2533285432/)"
([CC BY-NC-SA 2.0](https://creativecommons.org/licenses/by-nc-sa/2.0/)) by
bikesandwich on Flickr


The goal of facial landmarking is to fit a parameterised shape model to an image
of a face such that its points correspond to consistent locations on the face
[@saragLuceyEtAl2011a]. [@Fig:landmarkExample] shows an example of a face fitted
with such a model. Landmarks points may either correspond to well defined facial
part, such as the tip of the nose or the corner of the eye, or they may be part
of a group marking a boundary, such as the edge of the face. The exact
configuration and meaning of the landmark points can vary between datasets used,
and several different configurations are in use. One of the most popular however
is the 68 point annotation used originally by the Multi-PIE dataset
[@grossMatthEtAl2010a].

```{
    #fig:landmarkExample
    .gnuplot
    format=PNG
    dependencies="[images/gnuplot/render_pts.gp, images/gnuplot/process_pts.awk]"
    caption="Example of a face from the 300W face dataset [@sagonAntonEtAl2016a]
    with a set of landmark points annotated."
    width=60%
    }
call "images/gnuplot/render_pts.gp" \
     "Datasets/300w_cropped/01_Indoor/indoor_225.png" \
     "Datasets/300w_cropped/01_Indoor/indoor_225.pts"
```

Facial landmarking can be used to as part of the process of solving more
difficult facial analysis problems in different ways. Most obviously, landmarks
can be used directly as input data for a model. A model for head pose estimation
for example may not actually need most of the information encoded in the image
pixels; the pose of the head can be inferred from the relative positions of the
various facial features, which is what the landmarks encode [@murphTrive2009a].
Alternatively, the landmarks can be used as part of additional pre-processing
steps such as registration and feature extraction [@martiValst2016a]. In
registration the idea is to remove variation in rotation and scale; this can be
done by first computing a transformation that places the landmarks onto a
predefined reference shape, and then applying the same transformation to the
image itself. In feature extraction the goal is to compute summaries of the
image data that keeps relevant information while getting rid of nuisance
factors. Landmarks can help localise the features, so that each feature
represents the same part of the face in every example. Features can also be
computed directly on the landmarks themselves, encoding geometric relationships
between different parts of the face.

In the following, I present an overview of facial landmarking methods, followed
by a more detailed explanation of a few specific algorithms. Those algorithms
are then evaluated against a common dataset, before concluding with with some
recommendations on the suitability of the tested algorithms in certain
circumstances.

## Landmarking configurations

*consider moving or rewriting this*

Before going deeper into methods of computing landmarks, I shall talk briefly
about landmark configurations. Different landmarking schemes exist, with varying
numbers of landmarks and with the landmarks localised to different parts of the
face [@sagonAntonEtAl2016a]. The different configurations have arisen from the
different decisions made by people collecting and annotating datasets, and
appear to be mostly arbitrary. One of the most widely used is the 68 point
configuration from the Multi-PIE dataset (which is the one shown in
[@fig:landmarkExample]). Thanks to the work done for the 300 Faces In-The-Wild
challenge [@sagonAntonEtAl2016a], there are now annotations using the 68 point
configuration available for several public datasets.

## Overview of landmarking methods

There have been many approaches taken to the problem of landmark fitting, but
they can largely be divided into three categories [@wuJi2019a]: *holistic
methods*, *Constrained Local Models*, and *regression based methods*. The
categories are based on how the facial appearance and facial shape patterns are
modelled and related. In the holistic methods, a model of the global appearance
of the face is related to a global model of the landmark positions. Constrained
Local Model (CLM) approaches train a set of independent models for each of the
facial landmarks, but constrain the locations of the landmarks based on a global
model of the face shape. Lastly, the regression based methods do not explicitly
model the global face shape at all, instead directly relating image data (either
local or global) to landmark locations.

### Holistic methods

The holistic methods for facial landmarking are a family of generative
statistical models, whose prototypical version is known as Active Appearance
Models (AAM), as proposed by Cootes et al [@cooteEdwarEtAl2001a]. AAM works by
learning two connected models using Principle Component Analysis (PCA): a model
of face shape, and a model of global face appearance. These are connected
through sharing the same set of parameters; the joint parameterisation allows
the model to capture appearance variation due to shape, such as teeth appearing
when the mouth is open [@princ2012a]. To simplify the model and make it more
robust, Procrustes analysis [@gower1975a] is used on the training data to remove
variation due to global transformations, and to find the mean face shape; the
images are then warped so that each landmark is moved to its mean location, so
that the appearance model is independent of shape. The goal when fitting the
model to new images is to find both the optimal model parameters and the correct
global transform. In the classic version of this model, fitting is done by
iteratively calculating the error between the image as generated by the current
parameters, and calculating an update to the parameters based on the error
[@wuJi2019a].

*Discuss extensions to the algorithms*

### Constrained Local Models

The central idea of CLM is to model, for each landmark, the likelihood that it
should be placed on a certain part of the image, but to then constrain the final
landmark locations to fit a model of the face shape as a whole. 

CLM models can be traced back work by Cristinacce and Cootes
[@cristCoote2006a]. *Describe basic form of CLM*

*Discuss extensions to the algorithms*

### Regression based methods

*Describe class of algorithm and discuss extensions*

# Evaluations

## Evaluated algorithms

- Holistic: [@tzimiPanti2013a]
- CLM: [@zadehBaltrEtAl2017a]
- Regression based: [@kazemSulli2014a].

*Give more details on each algorithm*

## Testing data

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

## Evaluation criteria

The algorithms were evaluated on the point-to-point error between the fitted
shape the ground truth annotations, normalised by the
distance between the outer corners of the eye, as used in
[@sagonAntonEtAl2016a]. Specifically, given a set of $N$ fitted landmark points
$\symbf{s}^f = \{\symbf{x}^f_i\}_{i=1}^{N}$ and a corresponding set of $N$ ground
truth landmark points $\symbf{s}^g = \{\symbf{x}^g_i\}_{i=1}^{N}$, the error is:

$$
\mathrm{Error} = \frac{1}{d_{\mathit{outer}}N}\sum_{i=1}^{N}\lVert\symbf{x}^f_i - \symbf{x}^g_i\rVert
$$

# Results

- What happened
- Analysis of what happened

# Conclusion

- Final wrap up what happened
- Project aims

# Bibliography {.unnumbered}

:::{#refs}
:::
