#!/bin/bash
convert -resize '900' -sharpen 0x1.0 -gravity center -fill white -colorize 15%  $1 ${1%.*}_filter.jpg
# convert -resize '900'  $1 ${1%.*}_filter.jpg
