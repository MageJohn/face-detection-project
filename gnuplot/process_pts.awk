# print out lines with coordinates.
FNR==4,FNR==71 { print }

# store points that begin closed shapes.
FNR==40||FNR==46||FNR==52||FNR==64 { startPt = $0 }
# print a copy of the point that started the closed shape.
FNR==45||FNR==51||FNR==63||FNR==71 { print startPt }
# print a blank line between distinct shapes.
FNR==20||FNR==25||FNR==30||FNR==34||FNR==39||FNR==45||FNR==51||FNR==63 { print "" }
