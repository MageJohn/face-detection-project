---
title: Reflections on final year project
author: Yuri Pieters
date: '`\today`{=latex}'

documentclass: scrartcl
classoption:
- titlepage
- parskip=full

mainfont: "TeX Gyre Heros"
sansfont: "TeX Gyre Heros"
fontsize: 12pt

geometry:
- left=4cm
- right=4cm
- top=2.5cm
- bottom=4cm

indent: true # stops pandoc overriding parskip
colorlinks: true
...

# Project specification and changes

The original project specification was titled "Evaluation of face detection and
landmarking in 2D images". I've included some extracted parts of the original
project description, the full version of which is in an
[appendix](#sec:appendix).

> [...] investigate a variety of different techniques used in face detection and
> landmarking in [...] you should be able to recommend various algorithms for
> various circumstances and even suggest and test possible algorithmic
> improvements that impact on performance [...]

> [...] A successful project will contain strong elements of literature review,
> design, implementation and performance evaluation.

Over the course of this project the focus narrowed down significantly however.
The main reason for this was time constraints; I had a difficult time this year,
and didn't start the project in earnest until approximately a month before
hand-in. The early work on the project followed the specification more closely,
but it became clear after discussing a draft with my supervisor that the
direction I was going in wouldn't show enough of the implementation element.
Therefore I determined to narrow down my focus to a particular technique for
facial landmarking, hoping to reduce the workload enough to be able to complete
the spirit of the original.

Despite this I feel I have shown the elements of literature review, design,
implementation, and performance evaluation, though whether these come through
strongly enough remains to be seen. For example, literature review is one area I
know I can now do better than before. At the start I remember having a difficult
time even getting through a single academic paper, let alone comprehending
enough literature in a field to write a literature review. Over the course of
the project though I adapted quickly and now feel I understand properly how to
read a paper to get the most out of it, as well as follow webs of references to
gain an overview of a field.

Fully exploring the topic of the project was difficult in the time I had, and in
the end the project will not be able to fully fulfil the goals. However I feel I
have been able to complete significant work towards them in spite of this.

# Skills reflection

My skills in communication were tested in this project by the need to adapt to
academic writing, which for me was a relatively unfamiliar style of
communication. I was writing about complex topics and was expected to present
them in a way suitable for any academic, and so couldn't rely on much
domain-specific knowledge of the reader. As I mentioned in the previous section
I had difficulty early on comprehending some of the academic publications; while
this was partly a problem of my approach, in many cases it was also partly the
fault of the writers. As I continued I found that other publications I read
covered topics of the same complexity, yet were not so dense, and I came to take
pleasure in a well written paper. I took note of what worked when I noticed it,
and tried to apply this in the project report. I think I have managed to pull
this off to some extent, as evidenced by the fact that non-academic family
members who proofread the report were able to follow it.

I mentioned before that I ended up with about a month to do the whole project;
this was without a doubt the biggest problem I had while completing it. To be
able to do it I had focus 100% of my effort onto working on the project. As I
already didn't have any other classes, I decided to stay home rather than go to
campus after the Easter holiday; this meant I could benefit from extra family
support. Something I thought I knew before this experience was the value of
talking to people around me when problems arise, but in the end it took me way
to long to actually do it and I ended up badly behind on the work. In future I
hope I'll be quicker to recognise when problems like this start to happen,
letting me get out ahead of them.

I had to learn to take responsibility for my own timekeeping to complete the
project. Because of my ADHD this is a problem for me. Something I had come to
rely on in my previous years of study is a busy timetable from the university to
keep me on track, but this year left the timekeeping for the project almost
entirely up to me. While actually stepping up to do it happened very late,
affecting the quality of the final result, I hope that this experience has
taught me to take more responsibility for things like this in future.

\newpage 

# Appendix: Full original project specification {#sec:appendix}

This project will investigate a variety of different techniques used in face
detection and landmarking in 2D images. It will apply existing algorithms that
are available 'off-the-shelf' to various datasets and evaluate their
performance. Examples of successful algorithms include the 'Mixture of Trees'
method of Zhu and Ramanan, Asthana et al's 'Constrained Local Model approach,
and the fast 'Ensemble of Regression Trees' method of Kazemi and Sullivan. These
are listed in the references below. Datasets will be selected where the
performance at low image resolution and different facial poses and expressions
will be explored. By exploring the performance characterisation of each
algorithm, you should be able to recommend various algorithms for various
circumstances and even suggest and test possible algorithmic improvements that
impact on performance from the point of view of accuracy and/or speed.

At the end of the project you will have a good working knowledge of 2D face
detection and landmarking and how to evaluate generic 2D image processing
algorithms. A successful project will contain strong elements of literature
review, design, implementation and performance evaluation.

CVIS is essential. INNS and MLPG are desirable.

References: 1) X. Zhu, D. Ramanan. Face detection, pose estimation and landmark
localization in the wild. IEEE Computer Vision and Pattern Recognition (CVPR
2012) Providence, Rhode Island, June 2012. 2) A. Asthana, S. Zafeiriou, S. Cheng
and M. Pantic. Robust Discriminative Response Map Fitting with Constrained Local
Models . IEEE Computer Vision and Pattern Recognition (CVPR 2013). 3) V. Kazemi
and J. Sullivan. One Millisecond Face Alignment with an Ensemble of Regression
Trees. IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2014) 4)
Forsyth, D.A. and Ponce, J., 2003. Computer Vision: A modern approach. Prentice
Hall.
