#!/bin/bash
convert -resize '1012' -sharpen 0x1.0 -gravity center -fill white -colorize 15%  $1 ${1%.*}_filter.jpg
