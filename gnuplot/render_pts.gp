script_path = system("dirname ".ARG0);
img_path = system("realpath ".ARG1);
pts_path = system("realpath ".ARG2);
old_path = GPVAL_PWD;

cd script_path;

# Use the identify command from ImageMagick to get image height and width for
# the output.
img_w = `identify -format '%w' @img_path`
img_h = `identify -format '%h' @img_path`

# The points are about the right size on a 1000x1000 pixel image, so scale them
# according to that.
if (img_w >= img_h) {
  pt_scale = img_w / 1000.0;
} else {
  pt_scale = img_h / 1000.0;
}

set terminal @GPVAL_TERM crop size img_w,img_h;

# Don't add a key to the plot.
unset key;
# Dont show axis tics.
unset tics;
# Don't draw a border.
unset border;

# Set the y axis to increase downwards, rather than upwards. The landmark
# points would be flipped otherwise.
set yrange [:] reverse;

# Ensure the aspect ratio of the image isn't changed.
set size ratio -1;

# Don't add a margin.
set margin 0, 0, 0, 0;

# Plot the image and the points.
#   flipy: used to plot the image the right way up on the flipped y axis.
#   using spec: for reasons I don't quite understand the points aren't aligned
#               as is, and need to be moved towards the origin a little.
plot img_path binary filetype=auto flipy with rgbimage,\
     "<awk -f process_pts.awk ".pts_path using ($1-1.5):($2-1.5) with linespoints pointtype 7 linecolor 'green' pointsize pt_scale;
