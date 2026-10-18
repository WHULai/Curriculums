"""Vector diagrams for the sensing-principle review chapter."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc

OUT = Path(__file__).resolve().parents[1] / 'img'
BLUE, RED, GRAY = '#2d6fb1', '#b34145', '#757575'
plt.rcParams.update({'font.family': 'DejaVu Serif', 'mathtext.fontset': 'dejavuserif',
                     'font.size': 9, 'axes.labelsize': 10, 'pdf.fonttype': 42})


def save(fig, name):
    fig.savefig(OUT / name, bbox_inches='tight', pad_inches=.12)
    plt.close(fig)


def capacitance():
    fig, aa = plt.subplots(1, 2, figsize=(7.2, 2.15), constrained_layout=True)
    r = np.linspace(-.3, .3, 500)
    aa[0].plot(r, 1/(1-r)-1, color=BLUE, label=r'$\Delta C/C_0=r/(1-r)$')
    aa[0].plot(r, r, '--', color=GRAY, label='Small-displacement approximation')
    aa[1].plot(r, 2*r/(1-r*r), color=RED, label=r'$(C_1-C_2)/C_0$')
    aa[1].plot(r, r, color=BLUE, label=r'$(C_1-C_2)/(C_1+C_2)=r$')
    aa[1].plot(r, 2*r, '--', color=GRAY, label=r'$2r$')
    for a in aa:
        a.set_xlabel(r'$r=x/\delta_0$'); a.set_ylabel('Normalized output')
        a.spines[['top', 'right']].set_visible(False); a.grid(alpha=.2)
        a.legend(frameon=False, fontsize=7, loc='upper left')
    aa[0].set_title('(a) Single variable-gap capacitor', fontsize=10)
    aa[1].set_title('(b) Differential capacitors', fontsize=10)
    save(fig, 'ch4-capacitance.pdf')


def crack_detection():
    fig, aa = plt.subplots(1, 2, figsize=(7.2, 2.15), constrained_layout=True)
    for a in aa:
        a.set_xlim(0, 5); a.set_ylim(0, 3); a.axis('off')
        a.add_patch(Rectangle((.25,.25),4.5,1.1, facecolor='#e5e5e5',edgecolor=GRAY))
    a=aa[0]
    a.text(2.5,2.78,'(a) Eddy-current inspection',ha='center')
    for dx in np.linspace(-.55,.55,7):
        a.add_patch(Arc((2.5+dx,2),.3,.7,theta1=0,theta2=350,color=BLUE))
    a.text(2.5,2.45,'AC coil',ha='center',color=BLUE)
    for dx in [-.8,.8]:
        a.add_patch(Arc((2.5+dx,.88),1,.45,theta1=0,theta2=320,color=RED,lw=1.3))
    a.plot([2.5,2.5],[.75,1.35],color='white',lw=5)
    a.plot([2.5,2.5],[.75,1.35],color=GRAY,lw=1)
    a.annotate('Crack disturbs current paths', (2.5,1.1), (2.5,.05),ha='center',
               fontsize=8,arrowprops={'arrowstyle':'->','lw':.7})
    a=aa[1]
    a.text(2.5,2.78,'(b) Ultrasonic pulse-echo inspection',ha='center')
    a.add_patch(Rectangle((1.65,1.35),1.15,.45,facecolor='#d5e6f6',edgecolor=BLUE))
    a.text(2.225,2.05,'Piezoelectric probe',ha='center',color=BLUE)
    a.plot([1.8,3.1],[.75,.75],color=RED,lw=2)
    a.annotate('',(2,.78),(2,1.33),arrowprops={'arrowstyle':'->','color':BLUE})
    a.annotate('',(2.5,1.33),(2.5,.78),arrowprops={'arrowstyle':'->','color':RED})
    a.annotate('Defect echo', (2.5,1.1), (3.25,1.85),fontsize=8,
               arrowprops={'arrowstyle':'->','lw':.7})
    a.text(2.5,.35,'Internal interface / defect',ha='center',fontsize=8)
    save(fig,'ch4-crack-detection.pdf')


def optical_fiber():
    fig, aa=plt.subplots(1,2,figsize=(7.2,2.0),constrained_layout=True)
    for a in aa: a.set_xlim(0,5); a.set_ylim(0,3); a.axis('off')
    a=aa[0]; a.text(2.5,2.8,'(a) Pressure: mechanical conversion',ha='center')
    a.plot([.4,2],[1.8,1.8],color=BLUE,lw=4); a.plot([.4,2],[.9,.9],color=RED,lw=4)
    a.text(.35,2.1,'Transmit fiber',fontsize=8,color=BLUE)
    a.text(.35,.45,'Receive fiber',fontsize=8,color=RED)
    a.plot([3.8,3.8],[.35,2.4],color=GRAY,lw=3)
    a.plot([2,3.8,2],[1.8,1.35,.9],color=BLUE,lw=1.2)
    a.annotate('',(3.85,1.35),(4.7,1.35),arrowprops={'arrowstyle':'->','color':RED})
    a.text(4.2,1.7,'Pressure',fontsize=8,color=RED)
    a.text(2.65,.08,'Diaphragm displacement changes coupling',ha='center',fontsize=7.5)
    a=aa[1]; a.text(2.5,2.8,'(b) Displacement: target motion',ha='center')
    a.plot([.4,2],[1.8,1.8],color=BLUE,lw=4); a.plot([.4,2],[.9,.9],color=RED,lw=4)
    a.plot([3.6,3.6],[.35,2.35],color=GRAY,lw=3)
    a.plot([2,3.6,2],[1.8,1.35,.9],color=BLUE,lw=1.2)
    a.annotate('',(4.3,2.45),(3.1,2.45),arrowprops={'arrowstyle':'<->','color':RED})
    a.text(3.7,2.55,'x',color=RED,ha='center')
    a.text(2.5,.08,'Calibrate intensity versus gap on one monotonic branch',ha='center',fontsize=7.5)
    save(fig,'ch4-fiber-pressure-displacement.pdf')


def encoder():
    fig,a=plt.subplots(figsize=(6.8,1.6),constrained_layout=True)
    t=np.linspace(0,2,1200)
    a.plot(t,(np.sin(2*np.pi*t)>=0).astype(float)+1.6,color=BLUE,label='A')
    a.plot(t,(np.sin(2*np.pi*t-np.pi/2)>=0).astype(float),color=RED,label='B')
    a.set_yticks([.5,2.1],['B','A']); a.set_ylim(-.3,3)
    a.set_xlabel('Time / period'); a.spines[['top','right','left']].set_visible(False)
    a.text(.32,1.3,r'A leads B by $90^\circ$',fontsize=9)
    for p in [.25,.5,.75,1]: a.axvline(p,color=GRAY,lw=.6,ls=':')
    save(fig,'ch4-encoder.pdf')


if __name__=='__main__':
    capacitance(); crack_detection(); optical_fiber(); encoder()
