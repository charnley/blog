import schemdraw
from schemdraw import Drawing, ImageFormat
from schemdraw import flow
from schemdraw.drawing_stack import DrawingType
import schemdraw.elements as elm

import numpy as np

# import matplotlib.pyplot as plt
# plt.xkcd()

d = Drawing()

# op = elm.Opamp(leads=True)
# elm.Line().down().at(op.in2).length(d.unit/4)
# elm.Ground(lead=False)
# Rin = elm.Resistor().at(op.in1).left().idot().label('$R_{in}$', loc='bot').label('$v_{in}$', loc='left')
# elm.Line().up().at(op.in1).length(d.unit/2)
# elm.Resistor().tox(op.out).label('$R_f$')
# elm.Line().toy(op.out).dot()
# elm.Line().right().at(op.out).length(d.unit/4).label('$v_{o}$', loc='right')

# d += elm.Resistor()
# d += elm.Capacitor()
# d.add(elm.Diode())   # Same as `drawing +=`

with Drawing(file="art_overview.svg") as d:

    delta = 4
    null = np.array([delta, delta])
    dx = np.array([1,0])
    dy = np.array([0,1])
    d.config(fontsize=10, unit=.5)

    # desktop = flow.Process().label('Desktop Computer')
    canvas = flow.Terminal().label('Picture Server').at(null-5*dx)

    esp32 = flow.Terminal().label('ESP32').at(null)
    # flow.ArcLoop(arrow='<-').at(a_esp32.NW).to(a_esp32.NNE).label('Sleep', halign='center')

    # a_rpi= flow.Terminal().label('Raspberry Pi')


    elm.Arc2(arrow='<-').at(esp32.SW).to(canvas.SE).label('image.png')
    elm.Arc2(arrow='<-').at(canvas.NE).to(esp32.NW).label('wget image.png')


# d.draw()
# d.save('art_circut.svg')

# image_bytes = d.get_imagedata(ImageFormat.SVG)


