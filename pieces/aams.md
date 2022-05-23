# AAMs

AAMs are combined models of shape and appearance.

The shape model is a point distribution model (PDM), which describes the
distribution of a set of landmarks. It describes their positions as arising from
the equation

$$\vec{s}_i = \bar{\vec{s}} + \mat{\Phi}_s \vec{p}_{i} + \epsilon_i$$

Where $\vec{s}_i = [x_1, y_1, x_2, y_2, ..., x_{L_S}, y_{L_S}]^T$ is a vector
of $L_S$ landmarks, $\bar{\vec{s}}$ is the mean shape, $\mat{\Phi}_s$ is an
orthogonal matrix whose $N_S$ columns are the principle components of the shape
model, $\epsilon_i$ is a noise term, and $\vec{p}_i$ is the model parameters.
The idea is that as long as $N_S << L_S$ and $\epsilon_i$ is small, then

$$ \vec{s}_i \approx \bar{\vec{s}} + \mat{\Phi}_S \vec{p}_i$$

The appearance model is founded on the same principle.
