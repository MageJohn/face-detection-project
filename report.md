---
title: Using robust features when training an AAM model with in-the-wild data
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

This report details an investigation into using Active Appearance Models (AAM),
a well established framework in computer vision for the task of fitting a set of
landmarks to images of objects with variable shape and appearance (human faces
being the classic example). State of the art techniques for image
pre-processing and non-linear function optimisation, along with modern datasets
of images collected in the wild, are used in the AAM framework, and the results
are compared against other recent solutions to the same problem.

Computer vision is a field of computer science that deals with getting computers
to "see". The subject has a long history, dating back to the 1960s when it was
thought that the problem would be essentially solved over a summer project
[@paper1966a]. It proved significantly more difficult of course, and it is only
with the modern advances in imaging and computing technologies that progress has
accelerated, both by making new things possible and increasing the demand for
solutions to computer vision problems [@forsyPonce2012a]. Fields where computer
vision has been applied include include medical imaging, robotics,
human-computer interaction, security, manufacturing, and more [@szeli2022a].

A deformable shape model in computer vision is used to describe the shape of
objects in images whose shape varies in a non-rigid manner. The shape is
described as a set of landmark points marking key parts of the object, like in
[@fig:landmarkExample]. Non-rigid variation means that in different instances of
the object the points may be in different positions relative to each other, as
opposed to only being different by scaling, rotation, etc. This variation can be
due to the non-rigid nature of the object themselves, but could also just
represent variation between different objects of the same class. Human faces,
one of the most common examples used, vary both non-rigidly themselves and
between instances. Bones, on the other hand, also vary non-rigidly between
instances, but each instance is of course rigid on its own. Bones have been used
as examples for tasks involving deformable shape models, where they are useful
for analysis of medical imagery [@stegm2000a]; however in this work we focus on
human faces. This is due to the general popularity of faces for computer vision,
which has resulted in many high-quality datasets being made available
[@belhuJacobEtAl2011a; @leBrandEtAl2012a; @zhuRaman2012a; @sagonTzimiEtAl2013b].

```{#fig:landmarkExample .matplotlib caption="An image from the LFPW
[@belhuJacobEtAl2011a] training set annotated with a set of landmarks."}
from experiments.datasets import DATASETS_PATH
from menpo.io import import_image

import_image(DATASETS_PATH / "lfpw/trainset/image_0265.png").view_landmarks()
```

There have been many approaches to deformable model fitting.
Examples include Constrained Local Models [@cristCoote2006a; @saragLuceyEtAl2011a;
@zhuRaman2012a] and various regression methods, both cascaded [@yanLeiEtAl2013a;
@kazemSulli2014a; @xiongDeLala2013a; @zhangShanEtAl2014a], and not
[@dantoGallEtAl2012a; @yangPatra2013a]. These will be further discussed in
[@sec:other-landmarking-methods] in this report. One method that stands
out for it's relative simplicity, while still achieving good results, is AAM.

AAMs are generative statistical models of appearance and shape. They
parametrically describe the variations in appearance and shape seen in objects,
and can be fit to an unseen image by minimising the difference between it and
the image generated by the model. The resulting model instance is a relatively
compact description of the object that can be used in further analysis. For
example, an instance of an AAM trained on human faces could be used to estimate
head pose from the shape, or gender from the appearance.

## Motivation, aims, and objectives

Recent research has focused on deep learning methods for solving problems of
deformable shape model fitting and object recognition in general. There has been
great success in this area, in many cases pushing the state of the art.
Traditional statistical models have thus fallen by the wayside to some extent.

However these models do have advantages over deep learning methods that should
not be forgotten. Deep learning is still very computationally intensive, for
example, requiring specialised hardware such as GPUs or heavy code optimisation
to use effectively. In many cases traditional techniques are fast enough to run
on ordinary CPUs, while still achieving excellent performance.

Deep learning can also sometimes be treated as a black box, producing good
results that are difficult to explain. Traditional techniques on the other hand
are built on an understanding of every step, allowing a fuller view of how they
do their thing.

This work is in large part inspired by the work in [@tzimiPanti2013a], which
introduced a new AAM fitting algorithm they named Fast-SIC, but has since been
termed alternating inverse-compositional (AIC). They showed that, using this
algorithm to fit an AAM trained on in-the-wild data, state-of-the art
performance could be achieved on generic face fitting problems, even without the
use of robust features.

The aim of this work is to evaluate AAMs that do use robust features against the
current state-of-the-art deep learning methods that require GPUs to use. The
result should illuminate the state of deep learning methods and reveal what is
possible relatively less computationally expensive statistical methods.

To do this, AAMs using several different dense image features will be compared
against off-the-shelf deep learning algorithms in the task of generic face
fitting.

<!--

One of the more popular subjects for computer vision is human faces. Humans have
an intuitive understanding of the human face from a very young age
([@fig:baby]), and we quickly learn to interpret the faces of others to tell us
who they are, where they are looking, what they are feeling, and more; the face
is a rich form of non-verbal communication [@kanwiYovel2009a]. As with other
tasks in computer vision however, trying to infer something as subtle as emotion
from a collection of pixels is a non-trivial task. The solution, of course, is
to pre-process the data somehow to extract only relevant features
[@martiValst2016a]. This breaks a difficult problem (such analysing facial
expressions), into more manageable sub-problems, which can be tackled
separately. One such pre-processing technique that turns out to be useful for
multiple different tasks is facial landmarking [@martiValst2016a;
@murphTrive2009a].

![An expert face analyser[^babyref]](./images/sleeping_baby.jpg){#fig:baby
width=60%}

[^babyref]: "[Sleeping Baby](https://www.flickr.com/photos/biblicone/2533285432/)"
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

```{#fig:landmarkExample .matplotlib dpi=160 tight_bbox=true width=70%
    caption="Example of a face from the 300W face dataset [@sagonAntonEtAl2016a]
    with a set of landmark points annotated."
}
import menpo
img = menpo.io.import_image('Datasets/300w_cropped/01_Indoor/indoor_225.png')
img.landmarks['PTS'] = menpo.landmark.face_ibug_68_to_face_ibug_68(img.landmarks['PTS'])
img.crop_to_landmarks_proportion(0.2).view_landmarks(render_lines=True, marker_size=5)
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
-->


## Report overview

The structure of the rest of this report is as follows. *to be written once finished*

# Literature review

In this section we present a review of the literature on deformable model
fitting and prior work on AAMs.

We start with an overview of solutions to the deformable model fitting problem,
placing AAM into context. We then present a description of the basic formulation
of an AAM, setting the stage for a review of various enhancements that have
been proposed. Finally, because we compare AAMs with different image features we
we review these.

## Other landmarking methods

There have been many approaches taken to the problem of landmark fitting, but
they can largely be divided into three categories [@wuJi2019a]: *holistic
methods*, *Constrained Local Models*, and *regression based methods*. The
categories are based on how the facial appearance and facial shape patterns are
modelled and related. For holistic methods, the main example is AAM; the
category is named because the holistic appearance is used to fit the landmarks.
Constrained Local Model (CLM) approaches train a set of independent models for
each of the facial landmarks, but constrain the locations of the landmarks based
on a global model of the face shape. Lastly, the regression based methods do not
explicitly model the global face shape at all, instead directly relating image
data (either local or global) to landmark locations.

### Holistic methods

This category is largely defined by AAMs. AAMs were first explored in the work
of Edwards et al. [@edwarTayloEtAl1998a] in the late 90s. There was much
interest at the time in interpretation by synthesis, a by which images are
interpreted by synthesising a parametric version of the image.

Briefly, AAMs work by combining a model of shape and a model of appearance. The
model of appearance is for the whole face, which is what makes it holistic. They
generate (or synthesise) a face by generating the appearance in a reference
shape and then warping it to the shape generated by the shape model. 

More details of AAM are given in [@sec:active-appearance-model-design].


### Constrained Local Models

The central idea of CLM is to model, for each landmark, the likelihood that it
should be placed on a certain part of the image, but to then constrain the final
landmark locations to fit a model of the face shape as a whole.

CLM was first named as such in [@cristCoote2006a], but the definition used here
comes from [@saragLuceyEtAl2011a], where they identify the earliest paper that
uses the method of CLM as [@cooteTaylo1992a]. In CLM, a set of simple detectors
is trained for each landmark. On their own these detectors are not powerful
enough to correctly place a landmark, as they do not take in enough context.
Therefore their output is combined with a shape model which helps to
disambiguate the possible locations for each landmark by constraining their
positions to ones that make sense, e.g. are anatomically correct in the case of
fitting faces. [@Fig:clm] illustrates the model.

![An illustration of CLM and its components, copied from [@saragLuceyEtAl2011a].
The left shows how each local model is run on an image patch taken from around a
landmark point, producing a response map. The right illustrates the face shape
model. They are combined during optimisation (centre) by picking landmark
locations that are likely in the local models and fit the face shape
model.](./images/saragih_clm.png){#fig:clm}

There have been many variations on CLM in the literature. They typically vary in
local appearance model, face shape model, and optimisation method [@wuJi2019a]. 


In [@saragLuceyEtAl2011a] they introduce a method for optimising a point
distribution model for the shape and the local detector outputs jointly; they
identify a number of previous works which this directly improves on
[@cooteTaylo1992a; @nickeHutch2002a; @zhouGuptaEtAl2005a; @wangLuceyEtAl2008a;
@guKanad2008a]. 

### Regression based methods

Regression based methods learn a mapping from face image appearance to landmark
locations directly, without a parametric model for shape. They may use local
image patch detectors as in CLM, but the models are powerful enough not to need
the shape constraint. 

## Active Appearance Model design

An AAM is defined by the shape model, the appearance model, an image warping
algorithm, and the fitting algorithm. Closely related butt not strictly part of
the AAM is the choice of image feature. This is typically applied as a
pre-processing step, and while it can have a great effect on performance, it
doesn't typically affect the structure of the model. Image features are examined
in [@sec:image-features].

The shape and appearance model both have a similar structure:

$$
\vec{s} = \bar{\vec{s}} + \mat{\Phi}_{\vec{s}} \vec{p}_{\vec{s}} \\
\vec{a} = \bar{\vec{a}} + \mat{\Phi}_{\vec{a}} \vec{p}_{\vec{a}}
$$

They are both modeled as a mean vector ($\bar{\vec{s}}$, $\bar{\vec{a}}$) added
to a linear combination of of basis vectors ($\mat{\Phi}_{\vec{s}}$,
$\mat{\Phi}_{\vec{s}}$) which are weighted by a parameter ($\vec{p}_{\vec{s}}$,
$\vec{p}_{\vec{s}}$). This structure comes from both being constructed with
principle component analysis (PCA), a technique for expressing high dimensional
data in fewer dimensions. This throws away some of the variability in the
original data, but this is considered to be the variability due to noise. The
basis vectors $\mat{\Phi}$ are a subset of the eigenvectors of the co-variance
matrix of the data.

The shape model is known as a point distribution model (PDM)
[@cooteTayloEtAl1992a]. It is learned from a set of training images annotated
with a set of landmark points. The landmark points have both global position
variation, due objects being in different parts of the images, and shape
variation duo to non-rigid variation of the objects. This is too complex to
learn directly, so first the global variation is removed. For this an algorithm
called generalised Procrustes analysis is used, which iteratively work out how
to rotate, translate, and scale each shape so to be nearly on top of each other.
With this the mean shape $\bar{\vec{s}}$ and the covariance $\mat{\Sigma}$ of
the points can be calculated, and finding the eigendecomposition of
$\mat{\Sigma}$ gives the basis vectors. The subset of eigenvectors to keep is a
trade-off between accuracy and speed, as more vectors means more parameters to
be found when fitting, but fewer and there may not be enough to accurately
capture the variation in the object. In this work 15 eigenvectors are kept for
each model.

To learn the appearance model the images must be warped to a reference shape,
typically the mean shape $\bar{\vec{s}}$. This produces a shape free image
patch, which allows appearance to be learned in the absence of shape. PCA is
then applied again to the shape free patches to find $\mat{\Phi}_{\vec{a}}$.

The images are warped by a piecewise affine warp, which is the most common
choice. It requires the points to be triangulated, as in
[@fig:triangulatedLandmarks]. Each triangular piece can then be warped to the
new shape.

```{#fig:triangulatedLandmarks .matplotlib caption="An image annotated with the
traingles necessary for piecewise affine warping"}
from experiments.datasets import DATASETS_PATH
from menpo.io import import_image
from menpo.landmark import labeller, face_ibug_68_to_face_ibug_68_trimesh

img = import_image(DATASETS_PATH / "lfpw/trainset/image_0265.png")
labeller(img, "PTS", face_ibug_68_to_face_ibug_68_trimesh)
img.view_landmarks(group='face_ibug_68_trimesh')
```

The final piece of AAM is the inference algorithm. This is typically formed as a
least squares error minimisation problem for which Gauss-Newton optimisation is
used. The Gauss-Newton algorithm is an iterative gradient descent algorithm,
where the parameters are updated at each step by moving down the gradient of the
error function.

## AAM variations and advancements

The limiting factor for AAMs is largely speed. The appearance model is typically
high dimensional, in the order of 10^1^--10^2^ principle components are typical,
especially with multichannel images (or with multi-channel features as in this
work). Traditional Gauss-Newton optimisation requires computing and inverting
large Hessian matrices to find the gradient and this is computationally
expensive. Advances in AAMs then have mostly focused on this optimisation step.

In the original work on AAMs, computing the parameter update analytically was
prohibitive on the hardware of the time \marginpar{\raggedright Justify this with more
careful reading of the literature}. Therefore they used an additional step
during learning to learn a linear approximation of the update step based on the
image. The idea was to that the gradient direction on the training images would
generalise to unseen images. There several iterations of this idea, improving
the model for the parameter update. However, these methods trade away a fair bit
of accuracy, robustness, and generalisability for their speed.

The other form of improvement for fitting was in the analytical methods for
computing the update, along with increasing computing power making expensive
algorithms more viable. An early breakthrough was the project-out
inverse-compositional (POIC) algorithm of Matthews and Baker [@matthBaker2004a],
which simplified the optimisation problem by decoupling the shape and appearance
variation by "projecting-out" the appearance variation, working a subspace that
is the orthogonal complement of the appearance variation as a result
[@antonAlaboEtAl2015a]. This algorithm is very fast, but not very robust,
sacrificing accuracy for speed. It tends to break down when fitted to an image
with high appearance variation or outliers.

There is also simultaneous inverse composition (SIC), which is a slow but
accurate algorithm. A more recent algorithm, alternating inverse-composition
(AIC), has been shown [@tzimiPanti2013a] to be equivalent to SIC (produces the
same update step) but much faster. While not quite as fast as POIC, AIC is much
more accurate. As AIC is the algorithm used in this work, it is detailed below
in [@sec:inference-algorithm].

Table: Algorithmic complexity for some of the main AAM inference algorithms
[@antonAlaboEtAl2015a]. {#tbl:algorithmicComplexity}

Algorithm Complexity
--------- --------------------
POIC      $\BigO(N_{\symup{S}} L_{\symup{A}} + N_{\symup{S}}^2)$
SIC       $\BigO((N_{\symup{S}} + N_{\symup{A}})^2 L_{\symup{A}} + (N_{\symup{S}} + N_{\symup{A}})^3)$
AIC       $\BigO(N_{\symup{S}}^2 N_{\symup{A}}^2 + (N_{\symup{S}} + N_{\symup{A}})L_{\symup{A}} + N_{\symup{S}}^3)$

In [@tbl:algorithmicComplexity], $N_{\symup{S}}$ is the number of shape
components, $N_{\symup{A}}$ is the number of appearance components, and
$L_{\symup{A}}$ is the length of the appearance vector.

## Image features

An image feature is a measurement extracted from an image that attempts to
describe the contents. By this definition, the pixel intensity values themselves
are image features, though typically weak ones. The term feature makes no
guarantees of strength or usefulness. Looked at from another angle, the fitted
AAM instance is itself an image feature. It is an attempt to describe the image
contents after all. Indeed, higher level algorithms may treat AAM as a black box
feature extraction algorithm.

For the purposes of AAM itself however, image features have a few requirements.
There are features such as SURF which summarise the properties of a few
subregions of the image; for AAM this isn't useful as the shape of the image is
lost. The feature must preserve shape. Some features summarise an image in a
regular grid of sub-regions. The default scale-invariant feature transform
(SIFT) and histogram of oriented gradients (HOG) features are like this. These
preserve shape, but lose spacial accuracy, as points can only be localised to
the area of the sub-region. Therefore the feature must be dense, i.e. computed
at every pixel.

Features tested were

- Image Gradient Orientation (IGO)
- Dense HOG
- Dense SIFT
- DAISY

A dense feature image is computed by applying a feature extraction function to
an image. The function produces a vector of values for each pixel, turning a
greyscale image with size $W \times H \times 1$ into an feature image with size
$W \times H \times C$, where $W$, $H$, and $C$ are the width, height, and
feature vector sizes respectively. The value of $C$ varies between features and
can be affected by parameters for the feature function.

In the following sub-sections the 4 image features selected for this work are
examined.

### Image Gradient Orientation

IGO is a image feature introduced in [@tzimiZafeiEtAl2012a] and applied to
principle component analysis of faces. The feature image is computed in the
following manner:

#. Compute $\mat{G}_x = \mat{F}_x \ast \mat{I}$, $\mat{G}_y = \mat{F}_y \ast
\mat{I}$; that is, convolve the image with a horizontal and vertical first
derivative filter to produce the horizontal and vertical gradient component
images. Examples of such filters are the central difference operator, Prewitt,
and Sobel filters.
#. Compute $\mat{\Phi} = \arctan \frac{\mat{G}_y}{\mat{G}_x}$
#. The final image is $\frac{1}{\sqrt{N}}[\cos \mat{\Phi}\tran, \sin
\mat{\Phi}\tran]\tran$. Thus $C = 2$ for IGO.

### Histogram of Oriented Gradients

HOG is a feature introduced in [@dalalTrigg2005a]. It uses gradient orientations
similarly to IGO, but instead of each pixel only capturing the local gradient a
histogram of the orientations in the local area is produced.

The process of computing a HOG feature image is as follows [@princ2012a;
@antonAlaboEtAl2015a]. First the image amplitude and orientation of the image
gradients are computed as in IGO. The gradients are then summarised at two
levels, cells and blocks. A cell is a small $N_{\mathup{cell}} \times
N_{\mathup{cell}}$ region, potentially overlapping with its neighbours, in which
the orientations are summarised into histogram with $N_{\mathup{bins}}$ bins. A
block is a region of $N_{\mathup{block}} \times N_{\mathup{block}}$ cells. The
block is normalised using the Euclidean norm, and a final vector is produced for
each block by concatenating the histograms of its cells. Thus $C =
N_{\mathup{bins}}N_{\mathup{blocks}}^2$ for HOG. Computing a dense HOG means
extracting a vector for a block centered at every pixel of the original image. 

HOG is a powerful feature that has shown good performance in tasks such as face
recognition [@antonAlaboEtAl2015a] and human detection [@dalalTrigg2005a].

### Scale Invariant Feature Transform 

The SIFT descriptor aims to 

# Methodology and implementation

In this section we define the requirements we need for the experiments. After
this we detail the design and implementation choices made to fulfill those
requirements. This section provides the background details, and the actual
experiments that were run are detailed in [@sec:experiments-and-results].

To evaluate AAMs we will need suitable image datasets. To evaluate the use of
AAM in real world scenarios we want our datasets to reflect real world images,
and not be artificially controlled. In [@sec:datasets] we give details of
various options and select the ones used. We also need a way to evaluate fitting
results for accuracy; it's helpful as well to make these criteria compatible
with prior work, to make it possible to compare results across different papers.
We cover this in [@sec:evaluation-criteria]. Finally we will need a way to
actually implement the algorithms used. In [@sec:algorithm-implementation] we
cover this was done.

<!--
- Add description of plotting the cumulative error. 
-->

## Datasets

There are several popular datasets available that are suitable for deformable
shape model fitting. Faces are a popular subject.

The 300 Faces In-The-Wild Challenge [@sagonTzimiEtAl2013b; @sagonAntonEtAl2016a]
provides an excellent source for suitable datasets. As part of setting up the
challenge several existing sets of images were annotated with the same 68 point
landmark configuration. These datasets had existing annotations, but all had
different configurations making cross-dataset comparison difficult. The sets
they provided new annotations for were:

Multi-PIE

  ~ The CMU Multi-Pose Illumination, Illumination, and Expression dataset
  [@grossMatthEtAl2010a].
  ~ 750,000 image dataset captured in controlled conditions. Available for a fee.

XM2VTS

  ~ The Extended Multi Modal Verification for Teleservices and Security
  applications dataset [@messeMatasEtAl2000a].
  ~ 2360 images captured in controlled conditions. Available for a fee.

FRGC-V2

  ~ The Face Recognition Grand Challange Version 2.0 dataset
  [@phillFlynnEtAl2005a].
  ~ 4950 images captured in controlled conditions. Available on a case-by-case
  basis after a license is signed by a research institution.

AR

  ~ The AR Face Database [@martiBenav1998a].
  ~ 4000 uncompressed images captured in controlled conditions. Available on
  request from a university affiliated email address.

LFPW

  ~ The Labeled Face Parts in the Wild dataset [@belhuJacobEtAl2011a].
  ~ 1287 links to images on the internet. Only a subset of 811 training images
  and 224 testing images could be downloaded for [@grossMatthEtAl2010a].
  Available openly for reasearch.

HELEN

  ~ The HELEN dataset [@leBrandEtAl2012a]
  ~ 2330 images downloaded from the flickr.com web service. Available openly for
  research.

AFW

  ~ The Annotated Faces in-the-Wild dataset [@zhuRaman2012a].
  ~ 250 images (468 faces) collected from the flickr.com web service. Available
  openly for research.

They also provided a new dataset referred to as **IBUG** which was collected for
the competition, with 135 images downloaded from the web showing wide variation
in expression, illumination, and pose.

In addition to these datasets provided for training, they also collected a new
dataset for testing the contestants entries on. This dataset consists of 300
images taken indoors and 300 taken outdoors, hence the name of the challenge.
All the images were found on the web. This dataset (600 images in total) is
referred to as **300W**.

Any datasets that were not collected in-the-wild were not suitable for this
project. In [@tzimiPanti2013a] it was shown that training an AAM with
in-the-wild data greatly improves its generalisability. Because of this LFPW,
HELEN, AFW, IBUG, and 300W were chosen. The IBUG dataset and LFPW training set
were used for training (946 images), with the remaining 3022 images used for
testing.


## Result evaluation methodology

\newcommand{\fit}{^{\symup{f}}}
\newcommand{\gt}{^{\symup{g}}}

The accuracy of the algorithms was evaluated on the Euclidean distance between
the fitted shape and the ground truth annotations on a point-to-point basis,
normalised by the size of the ground truth annotation bounding box, as used in
[@zhuRaman2012a; @antonAlaboEtAl2015a]. Denoting $\vec{s}\fit = [x\fit_1,
y\fit_1, \ldots, x\fit_{L_{\vec{s}}}, y\fit_{L_{\vec{s}}}]$ and $\vec{s}\gt =
[x\gt_1, y\gt_1, \ldots, x\gt_{L_{\vec{s}}}, y\gt_{L_{\vec{s}}}]$ as the fitted
and ground truth shape respectively, then the error between them is calculated
as:

$$
\mathrm{Error} =
\frac{1}{s\gt_{\mathup{bb}}L_{\vec{s}}}
\sum_{i=1}^{L_{\vec{s}}}\sqrt{
  (x\fit_i - x\gt_i)^2 + 
  (y\fit_i - y\gt_i)^2
}
$$

Where $s\gt_{\mathup{bb}}$ is the mean side length of the ground truth
shape's bounding box:

$$
s\gt_{\mathup{bb}} = \frac{(\max x\gt_i - \min x\gt_i) + (\max y\gt_i - \min
y\gt_i)}{2}
$$

## Algorithm implementation

To implement the experiments Python and the `menpo`/`menpofit` packages were
used. The AAMs were trained on the LFPW and IBUG datasets, and test on the 300w
challenge dataset.

The selection of Python was driven by the availability of the `menpo` packages.
`menpo` and `menpofit` are Python packages that implement a framework for
deformable object modelling, including extensible AAM classes.

Table: Image feature defaults

-----------------------------------------------------
Feature type  Parameter values              Channels
------------- ----------------------------- ---------
HOG           `\(N_{\mathup{bins}} = 9\),   36
              \(N_{\mathup{block}} = 2\),
              \(\mathup{cell} = 8\times8\)
              `{=latex}

DSIFT         `\(N_{\mathup{bins}} = 9\),   36
              \(N_{\mathup{block}} = 2\),
              \(\mathup{cell} = 8\times8\)
              `{=latex}

DAISY         `\(Q = 2\), \(T = 4\),        36
              \(H = 4\)
              `{=latex}
-----------------------------------------------------

# Experiments and results

In this section we present each experiment with its results. We include a short
discussion in each case.

- Accuracy: what do the fitting errors look like?
- Convergence speed: How many iterations does it take to converge?
- What do some representative results look like?
- What are the failure modes for each image feature?
- 

## Accuracy

The power of each image feature for human face detection with an AAM was
evaluated by building an AAM using each feature and running them against the
testing datasets.

The cumulative error was plotted for each dataset. The result is shown in
[@fig:plotCumErr].

<!--
- Add axis labels
- Add grid
- Add shaped points to make lines distinguishible in greyscale.
- Will plots sharing axes be better?
- Fix the legend so it doesn't overlap the plots.
-->

```{#fig:plotCumErr .matplotlib caption="Cumulative error diagrams" format=PDF
preamble="pandoc-plot/result_plot.py"}
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(5.1, 8.5))
result_plot('lfpw', ax=ax1)
ax1.set_title('(a) LFPW')

result_plot('300w', ax=ax2)
ax2.set_title('(b) 300W')

result_plot('300w-indoor', ax=ax3)
ax3.set_title('(c) 300W Indoors')

result_plot('300w-outdoor', ax=ax4)
ax4.set_title('(d) 300W Outdoors')

handles, labels = ax4.get_legend_handles_labels()
plt.figlegend(handles, labels, loc='upper center')
```

```{.table #tbl:statsTable}
---
caption: 'Table showing the mean and median errors'
markdown: true
include: stats.csv
...
```

On each dataset the HOG feature produces the best results. LFPW is the easiest
dataset and HOG achieves 5% error or less on about 90% of the images.

Interestingly IGO achieves little significant improvement over using pixel
intensity values; this is in contrast to the results of a similar experiment in
[@antonAlaboEtAl2015a], where 

## Comparison to other methods

# Conclusion

- Final wrap up what happened
- Project aims

# Bibliography

:::{#refs}
:::
