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
    dx = np.array([3,0])
    dy = np.array([0,2])
    d.config(fontsize=10, unit=.5)

    desktop = flow.Terminal().label('Desktop Computer').at(null-3.5*dx+dy)
    canvas = flow.Terminal().label('Picture Server').at(null-2*dx)
    db = flow.State().label('database\nsqlite3').at(null-3*dx-1.2*dy)

    elm.Arc3(arrow='<->').at(db.N).to(canvas.SW).label('R/W')
    elm.Arc2(arrow='->').at(desktop.SE).to(canvas.NW).label('GET status')
    elm.Arc2(arrow='->').at(canvas.NW).to(desktop.SE).label('POST [image.png]')

    esp32 = flow.Terminal().label('ESP32').at(null-dy)
    eink_esp32 = flow.Terminal().label('E-ink\nDisplay').at(null+1.1*dx-dy)

    rpi= flow.Terminal().label('Raspberry Pi').at(null-2*dy)
    eink_rpi = flow.Terminal().label('E-ink\nDisplay').at(null-2*dy + 1.1*dx)

    #.at(a.NW).to(a.NNE)
    elm.ArcLoop(arrow='->').at(esp32.N).to(esp32.NNE).label('sleep')
    elm.Arc2(arrow='-').at(esp32.E).to(eink_esp32.W).label('')
    elm.Arc2(arrow='-').at(rpi.E).to(eink_rpi.W).label('')

    elm.ArcZ(arrow='<-').at(canvas.NE).to(esp32.W).label('GET image.png')
    elm.ArcZ(arrow='<-').at(rpi.W).to(canvas.SE).label('POST image.png')


# d.draw()
# d.save('art_circut.svg')

# image_bytes = d.get_imagedata(ImageFormat.SVG)


