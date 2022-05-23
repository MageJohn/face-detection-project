# Advancements in AAMs

The limiting factor for AAMs is largely speed. The appearance model is typically
high dimensional, in the order of 10^1 -- 10^2 principle components are typical,
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
more accurate.

Table: Algorithmic complexity for main AAM inference algorithms [@antonAlaboEtAl2015a]. {#tbl:algorithmicComplexity}

Algorithm Complexity
--------- --------------------
POIC      $O(N_S L_A + N_S^2)$
SIC       $O((N_S + N_A)^2 L_A + (N_S + N_A)^3)$
AIC       $O(N_S^2 N_A^2 + (N_S + N_A)L_A + N_S^3)$

In [@tbl:algorithmicComplexity], $N_S$ is the number of shape components, $N_A$
is the number of appearance components, and $L_A$ is the length of the
appearance vector.
