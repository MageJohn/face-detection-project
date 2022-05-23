# AAM Inference

By fitting an AAM to an unseen image, we produce, hopefully, a compact and
powerful descriptor of the shape and appearance of the modelled object that
appears in the image.

To do this, a set of parameters must be found that reproduce the image as
closely as possible. The most common way to do this is to do this is to minimise
the error between the actual and generated image in a least squares sense:

$$ 
\underset{\vec{p}_a, \vec{p}_s, \mat{\Psi}}{\arg\min}
\left[ 
(\vec{t} - \mathrm{warp}[\bar{\vec{a}} + \mat{\Phi}_a \vec{p}_a ,
\bar{\vec{s}} + \mat{\Phi}_s \vec{p}_s , \mat{\Psi}])
(\vec{t} - \mathrm{warp}[\bar{\vec{a}} + \mat{\Phi}_a \vec{p}_a ,
\bar{\vec{s}} + \mat{\Phi}_s \vec{p}_s , \mat{\Psi}])\tran
\right]
$$
$\vec{t}$ is the vectorised training image.

There have been many methods proposed to perform this optimisation. The basic
method is Gauss-Newton optimisation. This is an iterative gradient descent
algorithm, where at each iteration an update is calculated that moves the
parameters towards the minimum. However, even with PCA the model parameters have
many dimensions, and calculating this update is expensive. Therefore there have
been several different methods proposed to speed up the basic algorithm,
possible trading update speed for accuracy and convergence speed.

One method, which was the one applied in the original work on AAMs
[@edwarTayloEtAl1998a], is to learn the relationship between the current
parameters and the error from the training examples. This results in quite fast
fitting, but suffers fro accuracy issues.

The other method is to improve the speed of analytical update calculation
somehow. Popular version of this include the project-out inverse compositional
and SIC methods. More recent work as continued to improve on these methods, and
the version used to conduct the experiments in this work was the alternating
inverse-compositional method proposed in [@tzimiPanti2013a].
