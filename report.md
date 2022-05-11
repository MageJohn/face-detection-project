---
title: Evaulation of facial landmarking methods
author: "Yuri Pieters"
date: "25th May 2022"
subtitle: University of York, Department of Computer Science
...

\listoffigures

# Executive Summary {.unnumbered}

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
understanding of the human face from a very young age, and we quickly learn to
interpret the faces of others to tell us who they are, where they are looking,
what they are feeling, and more; the face is a rich form of non-verbal
communication [@kanwiYovel2009a]. The ease with which we do this belies the
difficulty we have had in teaching computers to do the same, however. Trying to
infer something as subtle as emotion from a collection of pixels, full of noise
arising from lighting conditions, camera properties, accessories such as hats
and glasses, or simply the diversity of human faces, is a non-trivial task. The
solution, of course, is to pre-process the data somehow to extract only relevant
features [@martiValst2016a]. This breaks a difficult problem (such analysing
facial expressions), into more manageable sub-problems, which can be tackled
separately. One such pre-processing technique that turns out to be useful for
multiple different tasks is facial landmarking [@martiValst2016a;
@murphTrive2009a].


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

The goal of facial landmarking is to fit a set of points to an image of a face
such that they mark the locations of key facial parts [@wuJi2019a].
[@Fig:landmarkExample] shows an example of a face fitted with a set of such
landmarks. Landmarks points may either mark a well defined facial part, such as
the tip of the nose or the corner of the eye, or they may be part of a group
marking a boundary, such as the edge of the face.


There are several approaches to achieving this goal, but they can largely be
divided into three categories [@wuJi2019a]: generative holistic methods,
Constrained Local Models, and regression based methods. In the holistic methods,
a model of the global appearance of the face is related to a global model of the
landmark positions; the classic version of this method is called Active
Appearance Models (AAM) from Cootes et al. [@cooteEdwarEtAl2001a]. Constrained
Local Model (CLM) approaches train a set of independent models for each of the
facial landmarks, but constrain the locations of the landmarks based on a global
model of the face shape; CLM models can be traced back work by
Cristinacce and Cootes [@cristCoote2006a]. Lastly, the regression based methods
do not explicitly model the global face shape at all, instead directly relating
image data to landmark locations.

### Holistic methods

**Describe active appearance models and their variations**

### Constrained Local Models

The central idea of CLM is to model, for each landmark, the likelihood that it
should be placed on a certain part of the image, but to then constrain the final
landmark locations to so to fit a model of the face shape as a whole. **more
detail, and variations**

### Regression based methods

**More varied. Give overview, but choose one (which you have an implementation
for), and describe it in more detail**


# Methods

Approach: 

Use RMSE to compare algorithms. Segment based on pose.

Pose segmentation done using semi-automated approach. 

#. First ran a head-pose estimation tool (OpenFace)
#. Then classified the results into frontal and extreme poses
   - assume failures are an extreme pose
#. Go through the results manually and reclassify any errors.

Algorithm choices; justify based on literature review and availability.

- Approach
- What was done
- Justification for above; include reference to ethics.

# Results

- What happened
- Analysis of what happened

# Conclusion

- Final wrap up what happened
- Project aims

# Bibliography {.unnumbered}

:::{#refs}
:::
