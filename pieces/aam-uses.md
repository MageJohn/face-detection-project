# AAM Uses

To put AAMs into context, we have included a brief review of their uses.

As models of shape, AAMs are often used for landmarking images. In these uses,
the appearance component is not used in the further processing of the image.

Landmarking is the process of fitting a set of points to an object. It is
another term for deformable shape model fitting.

Active appearance models combine two tasks into one, deformable model fitting
and appearance modelling. They therefore find use for both these tasks.

One of the reasons that a deformable shape model may be fitted to an object is
so the shape may be removed before analysing the appearance. Because AAMs
already do this these uses for a shape model are not further discussed here.

Models of shape have more direct uses though. Consider fitting a deformable
shape model to images of faces, a classic use case. Once you this model it can
be used to infer stuff about the face it models, such as inferring the pose of
the head, classifying facial expressions, or (when used to fit each frame in a
video) track lip movement for lip reading. Other uses can be found in fields
such as medical imaging, where fitting the shape of the spine could be used to
understand or recognise issues.

A model of appearance can be used any task which needs o work with how the
object looks regardless of its shape. So an AA for faces again could be used for
classifying things like gender, age, eye colour, or the like. 

Appearance and shape together are also meaningful. Recognising identity for
example would probably be more effective when shape is combined with appearance.

