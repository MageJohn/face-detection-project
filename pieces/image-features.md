# Image features

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
(SIFT) and histogram of oriented gradients (HOG) features like this. These
preserve shape, but lose spacial accuracy, as points can only be localised to
the area of the sub-region. Therefore the feature must be dense, i.e. computed
at every pixel.

Features tested were

- Dense HOG
- Dense SIFT
- DAISY
- Image Gradient Orientation (IGO)

*need details*
