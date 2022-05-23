# Motivation

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
