#!/bin/bash

# Note that this has only been lightly tested. Hopefully if it breaks it still
# servers as documentation on the required links.

# IMPORTANT: this will expire after Sun, 15 May 2022 10:58:08 GMT. If this is
# needed after it does, download one of the links below in a browser, fill in
# the form, and copy the new sessionid cookie here.
cookies='Cookie: sessionid=62b0334bd44139fe0a920747af44cb49'

links=(
  "https://ibug.doc.ic.ac.uk/download/annotations/300w.zip.001"
  "https://ibug.doc.ic.ac.uk/download/annotations/300w.zip.002"
  "https://ibug.doc.ic.ac.uk/download/annotations/300w.zip.003"
  "https://ibug.doc.ic.ac.uk/download/annotations/300w.zip.004"
  "https://ibug.doc.ic.ac.uk/download/annotations/300w_cropped.zip"
  "https://ibug.doc.ic.ac.uk/download/annotations/afw.zip"
  "https://ibug.doc.ic.ac.uk/download/annotations/helen.zip"
  "https://ibug.doc.ic.ac.uk/download/annotations/ibug.zip"
  "https://ibug.doc.ic.ac.uk/download/annotations/lfpw.zip"
)

sets=("300w" "300w_cropped" "afw" "helen" "ibug" "lfpw")

for link in "${links[@]}"
do
  echo "Downloading ${link}"
  curl -L -O "${link}" -H "${cookies}"
done

for set in "${sets[@]}"
do
  echo unzip "$set" -d "$set"
done
