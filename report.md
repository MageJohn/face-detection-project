---
title: Facial detection and landmarking
author: "Yuri Pieters"
date: "8th June 2022"
subtitle: University of York, Department of Computer Science
documentclass: scrreprt
classoption:
- titlepage
- parskip=full
bibliography: bibliography.yaml
csl: ieee.csl
link-citations: true
link-bibliography: true
indent: true # stops pandoc overriding parskip
mainfont: "TeX Gyre Heros"
fontsize: 12pt
geometry:
- left=4cm
- right=4cm
- top=2.5cm
- bottom=4cm
toc: true
toc-depth: 2
colorlinks: true
...

\listoffigures

# Executive Summary

- State aim
- Motivation: why is worth doing this?
- Methods: how was it done?
- Results: what was found
- Issues: what should people be mindful of with regards to this subject?

The goal of this work was to understand, compare, and evaluate a range of different techniques used in the detection and landmarking of human faces by computers. In this report I present the models I chose to evaluate, the datasets I evaluated them against, and the results of the evaluation. I also present a review of the field overall, which motivates the particular models and datasets I choose.

Motivation:

- Computer vision is an important part of many topics at the bleeding edge of computer science: robotics, self driving cars, human computer interfaces.
- Computer vision techniques aren't one size fits all. To pick between them requires understanding of the differences.
- Recognition of faces is an important and frequently used application of computer vision.
- Therefore understanding and picking between face recognition algorithms is important.

Social and ethical issues of face detection and landmarking:

- Human faces have a huge variety
- Everyone has a right to be able to use the technology that may be supported by computer vision
- Therefore both the computer vision techniques and actual implementation of those techniques (e.g. the actual training images used) should be developed with the full diversity of humans in mind.


# Introduction

## Notes

- Subject area intro/background
- Narrow to specific background for this work
- Restate motivation
- Restate aims

<!-- -->

- Object detection and landmarking are general problems. Faces are a popular subject though.
- Overall aim of face detection/landmarking algorithms
- Difference between statistical models and neural networks
- Stages of a typical algorithm
- Stages in detail (I think it's detection then landmarking)
  - Detection
    - Overview of model categories
    - What is state of the art like?
  - Landmarking
    - Overview of model categories
    - What is state of the art like?

- What particular problems often occur with face detection/landmarking?
  - Occlusion
  - Extreme poses
  - More varied faces than the detector was trained on

Aims:

- Investigate a variety of techniques used in face detection and landmarking
- Evaluate a cross-section of these techniques using a unified data set

Face analysis categories:

- Face detection: answer's the question "is there a face in this image". Can
  typically be extended to answer "where are the faces in this image" by running
  the detector on all sub-regions of the image.
- Facial landmarking: going beyond detecting the presence of a face, landmarking
  identifies the position of the individual face parts. Different techniques use
  different numbers of landmarks. Some aim to fit a contour around every part,
  and some may just place points on the eyes, nose and mouth. The landmarks can
  be used as a precursor to other face processing tasks such as recognising
  emotions or identifying individuals.

## Introduction

The problems of face detection and landmarking are related but typically
distinct problems in the field of computer vision. The goal of face detection is
to detect the presence of faces in an image, often with the further goal of
placing a bounding box around the face; this is a good start for other face
analysis algorithms which assume the presence of a face, and is used in
applications such as cameras to help auto-focus. The goal of landmarking a face
is to place a set of points onto key parts of the face, as in
[@fig:landmarkExample]; the landmarks could then be used in further processing,
such as identity recognition, facial behaviour analysis, lip reading, 3D face
reconstruction, or face editing, to name a few examples
[@dengMenpoBenchmarkMultipose2019].

```{
    #fig:landmarkExample
    .gnuplot
    format=PNG
    dependencies="[gnuplot/render_pts.gp, gnuplot/process_pts.awk]"
    caption="Example of a face from the 300W face database [@sagonas300FacesInTheWild2016] with a set of 68 landmark points annotated. The 68 point pattern was first used for the Multi-PIE [@grossMultiPIE2010] database, but has since been used on many other databases [@sagonas300FacesInTheWild2016]."
    }
call "gnuplot/render_pts.gp" "Datasets/300w_cropped/01_Indoor/indoor_225.png" "Datasets/300w_cropped/01_Indoor/indoor_225.pts"
```

<!-- Rethink this paragraph. The assertion that combining detection and
landmarking is recent may be unfounded -->

Historically the problems of face detection and landmarking were tackled
separately; however more recent work, such as that done by Zhu and Ramanan
[@zhuFaceDetectionPose2012], has resulted in algorithms unifying both goals. In
addition, the performance of some algorithms for landmarking is strongly
affected by where they are initialised, and this initialisation is done with a
face detector. To get the best performance in this case, the detection algorithm
should be tailored to the one for landmarking [@sagonas300FacesInTheWild2016].

In this project different off-the-shelf algorithms for facial detection and
landmarking are compared, examining their performance at different image
resolutions. 

The 300 Faces In-The-Wild challenge [@sagonas300FacesInTheWild2016] and similar
competitions
([@dengMenpoBenchmarkMultipose2019;@everinghamPascalVisualObject2015;@nadaPushingLimitsUnconstrained2018])
have compared a variety of 

While they are special cases of the more general problems in object recognition,
faces are frequently the case chosen in the literature, even when the algorithm
in question is more generally applicable (e.g
[@asthanaRobustDiscriminativeResponse2013; @saragihDeformableModelFitting2011;
@ioffeMixturesTreesObject2001a]). This may just be because it is easier to
compare new work to old when using the same class of objects, but faces are also
a generally good class to use for this comparison: they are non-rigid and diverse,
making them a relatively difficult problem, and it is easy for a human to
qualitatively judge the result.


<!-- First attempt -->

Faces hold a special place in the human mind. As highly visual, social creatures
our faces are an important part of how we navigate the world. With our faces we
can communicate complex emotion, and they are one of the primary ways we
recognise one another. Therefore the ability to recognise faces is hard-wired
into our brains, so much so that we'll happily see them in everything from burnt
toast to clouds. Its no wonder then that faces are a popular subject for
computer vision research. However, writing a computer program to analyse human
faces (or images of objects in general, actually) turns out to be easier said
than done, and so has been the subject of much research over the last few
decades. This research has produced many practical techniques already in use
around us, such as face detectors helping to auto-focus your camera, or
auto-tagging of identities in photo libraries. There is still much room for
improvement, as most of these programs are still easily outperformed by humans.
Research continues, however, and the state of the art continues to get closer to
human level every year.

The goal of facial recognition is a broad one, and can be broken down further.
Some tasks that can be included in facial recognition are

Face detection

  ~ Detect the presence of a face in in image. The result may be a bounding box
  around the face, and is a good starting point for further analysis which
  assumes the presence of a face.

Classification

  ~ Classify faces into categories such as gender, age, skin color, etc.



:::{#fig:faceexamples}
![](./Datasets/300W/01_Indoor/indoor_168.png){ width=45% }
\hspace{1em}
![](./Datasets/300W/01_Indoor/indoor_225.png){ width=45% }

Two images from the 300w dataset, showing some of the range of human faces.
:::

# Methods

- Approach
- What was done
- Justification for above; include reference to ethics.

# Results

- What happened
- Analysis of what happened

# Conclusion

- Final wrap up what happened
- Project aims

# Bibliography

:::{#refs}
:::
