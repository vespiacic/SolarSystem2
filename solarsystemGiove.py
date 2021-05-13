#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from astropy.time import Time
from astroquery.jplhorizons import Horizons

sim_start_date = "2021-05-01"  # simulating a solar system starting from this date
fpd=6 # frames per day
sim_duration = 30*fpd  #2 * 365                # (int) simulation duration in days
m_earth = 5.9722e24 / 1.98847e30  # Mass of Earth relative to mass of the sun
m_moon = 7.3477e22 / 1.98847e30

class Object:  # define the objects: the Sun, Earth, Mercury, etc
    def __init__(self, name, rad, color, r, v):
        self.name = name
        self.r = np.array(r, dtype=float)
        self.v = np.array(v, dtype=float)
        self.xs = []
        self.ys = []
        self.color = color
        self.plot = ax.scatter(r[0],
                               r[1],
                               color=color,
                               s=rad**2,
                               edgecolors=None,
                               zorder=10)
        self.line, = ax.plot([], [], color=color, linewidth=1.4)
        self.annotation= ax.annotate(text=name, xy=(r[0],r[1]), xytext=(r[0],r[1]))
        #self.freccia = ax.annotate(text=name, xy=(0,0), xytext=(0,0),arrowprops=dict(arrowstyle='<-', color='white',lw=0.5,ls='-'))


class SolarSystem:
    def __init__(self, thesun):
        self.thesun = thesun
        self.planets = []
        self.time = None
        self.timestamp = ax.text(.03,
                                 .94,
                                 'Data: ',
                                 color='w',
                                 transform=ax.transAxes,
                                 fontsize='x-large')

    def add_planet(self, planet):
        self.planets.append(planet)

    def evolve(self):  # evolve the trajectories
        dt = 1.0/fpd
        scarto = [1,1]
        self.time += dt
        plots = []
        lines = []
        annotations = []
        arrows =[]
        for p in self.planets:
            p.r += p.v * dt
            acc = -2.959e-4 * p.r / np.sum(p.r**2)**(3. / 2
                                                     )  # in units of AU/day^2
            p.v += acc * dt
            if abs(p.r[0]) <2 and abs(p.r[1]) <2:
                p.xs.append(p.r[0])
                p.ys.append(p.r[1])
                p.plot.set_offsets(p.r[:2])
                p.line.set_xdata(p.xs)
                p.line.set_ydata(p.ys)
                #ax.text(p.r[0],p.r[1],p.name,color=p.color,zorder=1000,ha='center',fontsize='small')
                #ax.annotate(p.name,(p.r[0],p.r[1]),(p.r[0],p.r[1]*1.1))
                scarto=p.v[1]/abs(p.v[1]) #non funziona, scarto fisso alla riga sotto
                p.annotation.set_position(p.r + 0.03)
            else :
                lung=0.6*(p.r[0]**2+p.r[1]**2)**.5
                if p.name=='New Horizons': lung=lung*1.15 #da usare solo fin quando New Horizons e Voygar 2 sono quasi allineati con la Terra
                a=p.r[0]/lung
                b=p.r[1]/lung
                inizio=(a*0.8,b*0.8)
                fine=(a,b)
                p.xs.append(a*0.8)
                p.ys.append(b*0.8)
                p.annotation.set_position(fine)
                p.annotation.set_ha('center')
                p.annotation.update(arrowprops=dict(arrowstyle='<-', color='white',lw=0.5,ls='-'))
                #p.annotation=ax.annotate(text=p.name, xy=inizio, xytext=fine,ha='center', arrowprops=dict(arrowstyle='<-', color='white',lw=0.5,ls='-'))
                #p.annotation.set_position((p.r[0],p.r[1])/lung)
                #p.freccia.arrow_patch.set_color('red')
                #p.freccia.set_x(p.r[0])
                #p.freccia.set_y(p.r[1])
            plots.append(p.plot)
            lines.append(p.line)
            annotations.append(p.annotation)
            #arrows.append(p.freccia)
            
        #self.timestamp.set_text(
        #    'Giorno: ' + Time(self.time, format='jd', out_subfmt='date').iso)
        intestazione = 'Giorno: ' + Time(self.time, format='jd').iso + 'Marte: y=' + str(p.r[1])    
        self.timestamp.set_text(intestazione[:18]) #primi 18 caratteri
        #self.timestamp.set_text(intestazione) #stringa completa
       #     'Giorno: ' + Time(self.time, format='jd').iso)
        return plots + lines + annotations + [self.timestamp]


plt.style.use('dark_background')
fig = plt.figure(figsize=[6, 6])
ax = plt.axes([0., 0., 1., 1.], xlim=(-1.8, 1.8), ylim=(-1.8, 1.8))
ax.set_aspect('equal')
ax.axis('off')
ss = SolarSystem(Object("Sole", 5, 'yellow', [0, 0, 0], [0, 0, 0]))
ss.time = Time(sim_start_date).jd
colors = [
    'gray', 'orange', 'cyan', 'chocolate', 'white', 'white', 'white', 'white',
    'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white']
sizes = 0.1  #sizes = [0.1, 0.1, 0.1, 0.1]
corpo=[[1, 2, 3, 4, -96, -144, -37, -121, 101955, -234, -61, -98, -31, -32], ['Mercurio', 'Venere: Akatsuki', 'L1: 5 missioni\nLuna: 5 missioni\nL2: 2 missioni', 'Marte: 11 missioni',
    'Parker Solar Probe', 'Solar Orbiter', 'Hayabusa 2', 'BepiColombo',
    'Osiris-REx', 'Stereo A', 'Juno', 'New Horizons', 'Voyager 1','Voyager 2']]
names = ['Mercurio', 'Venere: Akatsuki', 'Luna,L1,L2: 12 missioni', 'Marte: 11 missioni',
    'Parker Solar Probe', 'Solar Orbiter', 'Hayabusa 2', 'BepiColombo',
    'Osiris-REx', 'Stereo A', 'altro', 'altro', 'altro'] #ma questo lo sto ancora usando?
#texty = [.47, .73, 1, 1.5]

#for i, nasaid in enumerate(
#    [1, 2, 3, 4, -96, -144, -37, -121, -64,
#     -234]):  # The 1st, 2nd, 3rd, 4th planet in solar system
for i, nasaid in enumerate(corpo[0]):
    obj = Horizons(id=nasaid, location="@sun", epochs=ss.time,
                   id_type='id').vectors()
    ss.add_planet(
        Object(corpo[1][i], 20 * sizes, colors[i],
               [np.double(obj[xi]) for xi in ['x', 'y', 'z']],
               [np.double(obj[vxi]) for vxi in ['vx', 'vy', 'vz']]))
def animate(i):
    return ss.evolve()

"""
esterni=[[-61, -98, -31, -32],['Juno', 'New Horizons', 'Voyager 1', 'Voyager 2']]
for i, nasaid in enumerate(esterni[0]):
    obj = Horizons(id=nasaid, location="@sun", epochs=ss.time,
                   id_type='id').vectors()
    plt.arrow(0, 0, np.double(obj['x']), np.double(obj['y']))
"""    

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