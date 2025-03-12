

# all:
# 	ffmpeg \
# 	-i ./V_20250312_180253_ES0.mp4 \
# 	-r 15 \
# 	-vf "scale=512:-1,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
# 	-ss 00:00:00 -to 00:32:00 \
# 	output.gif

input=./V_20250312_180253_ES0.mp4

all:
	ffmpeg -i ${input} -filter_complex "scale=w=480:h=-1:flags=lanczos, palettegen=stats_mode=diff" palette.png

frames:
	ffmpeg -i ${input} -r 50 \
	-ss 00:00:00 -to 00:32:00 \
	-f image2 image_%06d.png

images = $(wildcard export/*)
fix_images:
	mkdir -p convert_export
	for x in $(images); do convert +repage -crop 1500x900+0+0 -resize '900' -sharpen 0x1.0 -fill white -colorize 15\% $$x convert_$$x; done

gif:
	ffmpeg -start_number 694 -framerate 50 -i convert_export/image_%06d.png -i palette.png -pix_fmt rgb24 output.gif

reduce_size:
	gifsicle --optimize=3 --lossy=100 -o output2.gif output.gif
