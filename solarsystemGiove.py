#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from astropy.time import Time
from astroquery.jplhorizons import Horizons

sim_start_date = "2021-05-01"  # data di inizio
fpd=6 # frames al giorno
sim_duration = 30*fpd  # mettere 29, 30 o 31 a seconda della data dell'ultimo frame, dipende dalle approssimazioni

class Object:  # definisce i corpi, i 4 pianeti interni e le sonde del sistema solare
    def __init__(self, name, rad, color, r, v):
        self.name = name
        self.r = np.array(r, dtype=float)
        self.v = np.array(v, dtype=float)
        self.xs = []
        self.ys = []
        self.color = color
        self.plot = ax.scatter(r[0], r[1], color=color, s=rad**2, edgecolors=None, zorder=10)
        self.line, = ax.plot([], [], color=color, linewidth=1.4)
        self.annotation= ax.annotate(text=name, xy=(r[0],r[1]), xytext=(r[0],r[1]))
        self.freccia = ax.annotate(text=name, xy=(7,7), xytext=(7,7),arrowprops=dict(arrowstyle='<-', color='white',lw=0.5,ls='-'))

class SolarSystem:
    def __init__(self, thesun):
        self.thesun = thesun
        self.planets = []
        self.time = None
        self.timestamp = ax.text(.03, .94, 'Data: ', color='w', transform=ax.transAxes, fontsize='x-large')

    def add_planet(self, planet):
        self.planets.append(planet)

    def evolve(self):  # evolve the trajectories
        dt = 1.0/fpd
        self.time += dt
        plots = []
        lines = []
        annotations = []
        for p in self.planets:
            p.r += p.v * dt
            acc = -2.959e-4 * p.r / np.sum(p.r**2)**(3. / 2)  # in units of AU/day^2
            p.v += acc * dt
            if abs(p.r[0]) <2 and abs(p.r[1]) <2: # il caso di un corpo dentro le 2 au
                p.xs.append(p.r[0])
                p.ys.append(p.r[1])
                p.plot.set_offsets(p.r[:2])
                p.line.set_xdata(p.xs)
                p.line.set_ydata(p.ys)
                p.annotation.set_position(p.r + 0.03)
                if len(p.name)>20: p.annotation.set_va('center')
            else : # le 4 sonde nel sistema solare esterno
                lung=0.6*(p.r[0]**2+p.r[1]**2)**.5
                if p.name=='New Horizons': lung=lung*1.15 #da usare solo fin quando New Horizons e Voygar 2 sono quasi allineati con la Terra
                a=p.r[0]/lung
                b=p.r[1]/lung
                inizio=(a*0.8,b*0.8)
                fine=(a,b)
                p.freccia.set_ha('center')
                p.freccia.xyann = fine
                p.freccia.xy=inizio
            plots.append(p.plot)
            lines.append(p.line)
            annotations.append(p.annotation)
        intestazione = 'Giorno: ' + Time(self.time, format='jd').iso    
        self.timestamp.set_text(intestazione[:18]) #primi 18 caratteri
        return plots + lines + annotations + [self.timestamp]

plt.style.use('dark_background')
fig = plt.figure(figsize=[6, 6])
ax = plt.axes([0., 0., 1., 1.], xlim=(-1.8, 1.8), ylim=(-1.8, 1.8))
ax.set_aspect('equal')
ax.axis('off')
ss = SolarSystem(Object("Sole", 5, 'yellow', [0, 0, 0], [0, 0, 0]))
ss.time = Time(sim_start_date).jd
colors = ['gray', 'orange', 'cyan', 'chocolate', 'white', 'white', 'white', 'white',
    'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white']
corpo=[[1, 2, 3, 4, -96, -144, -37, -121, 101955, -234, -61, -98, -31, -32],
    ['Mercurio', 'Venere: Akatsuki', 'L1: 5 missioni\nLuna: 5 missioni\nL2: 2 missioni', 'Marte: 11 missioni',
    'Parker Solar Probe', 'Solar Orbiter', 'Hayabusa 2', 'BepiColombo',
    'Osiris-REx', 'Stereo A', 'Juno', 'New Horizons', 'Voyager 1','Voyager 2']]

for i, nasaid in enumerate(corpo[0]):
    obj = Horizons(id=nasaid, location="@sun", epochs=ss.time, id_type='id').vectors()
    ss.add_planet(Object(corpo[1][i], 2, colors[i],
               [np.double(obj[xi]) for xi in ['x', 'y', 'z']],
               [np.double(obj[vxi]) for vxi in ['vx', 'vy', 'vz']]))
def animate(i):
    return ss.evolve()

ani = animation.FuncAnimation(
    fig,
    animate,
    repeat=False,
    frames=sim_duration,
    blit=True,
    interval=200,
)

plt.show() #output IDE

#writergif = animation.PillowWriter(fps=7)   #output gif scrittura
#ani.save('solarsystem.gif', writer=writergif) #output gif file

#writervideo = animation.FFMpegWriter(fps=30)  #output mp4 writer
#ani.save('solarsystemfullmay.mp4', writer=writervideo) #output mp4 file