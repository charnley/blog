#!/bin/bash
convert -resize '915' -sharpen 0x1.0 -gravity center -fill white -colorize 15%  $1 $2
