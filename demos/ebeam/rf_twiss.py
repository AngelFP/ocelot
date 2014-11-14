

from ocelot.cpbd.elements import *
from ocelot.cpbd.optics import *
from ocelot.gui.accelerator import plot_lattice, plot_opt_func
from pylab import *


phi_bc2 = 0.033646252962410

l0 = 0.5
l_bc2 = l0 *phi_bc2 /sin((phi_bc2))

ac_v = 5e+008

bb_393_b2 = Bend(l=l_bc2, angle=phi_bc2, e1=0.000000000, e2=phi_bc2, tilt=1.570796330, id = 'bb_393_b2')
bb_402_b2 = Bend(l=l_bc2, angle=-phi_bc2, e1=-phi_bc2, e2=0.000000000, tilt=1.570796330, id = 'bb_402_b2')
bb_404_b2 = Bend(l=l_bc2, angle=-phi_bc2, e1=0.000000000, e2=-phi_bc2, tilt=1.570796330,  id = 'bb_404_b2')
bb_413_b2 = Bend(l=l_bc2, angle=phi_bc2, e1=phi_bc2, e2=0.000000000, tilt=1.570796330,  id = 'bb_413_b2')

d10cm =   Drift(l=0.1, id = 'd10cm')
cd850cm = Drift(l=8.5 / cos(phi_bc2), id = 'cd850cm')
cd150cm = Drift(l=1.5, id = 'cd150cm')
cd100cm = Drift(l=1, id = 'cd100cm')
d34cm59 = Drift(l=0.3459, id = 'd34cm59')
d13cm =   Drift(l=0.13, id = 'd13cm')
d130cm =  Drift(l=1.3, id = 'd130cm')

bc2  = (d10cm, bb_393_b2, cd850cm, bb_402_b2, cd150cm, bb_404_b2, cd850cm, bb_413_b2,  cd100cm)

qd_415_b2 = Quadrupole(l=0.2000000, k1=0.3, tilt=0.000000000, id = 'qd_415_b2')
qd_417_b2 = Quadrupole(l=0.2000000, k1=-0.2, tilt=0.000000000, id = 'qd_417_b2')
qd_418_b2 = Quadrupole(l=0.2000000, k1=-0.5, tilt=0.000000000, id = 'qd_418_b2')
q_249_l2 =  Quadrupole(l=0.3000000, k1=0.25, tilt=0.000000000, id = 'q_249_l2')
q_261_l2 =  Quadrupole(l=0.3000000, k1=-0.29711100, tilt=0.000000000, id = 'q_261_l2')


c_a3 = Cavity(l=1.0377000, phi=0.0, delta_e = ac_v, freq=1.300e+009, id = 'c_a3')


l3  = (d13cm,qd_415_b2,d130cm, qd_417_b2, d130cm, qd_418_b2,d130cm,
        c_a3, d34cm59, c_a3, d34cm59, c_a3, d34cm59, c_a3, d34cm59,
        c_a3, d34cm59, c_a3, d34cm59, c_a3, d34cm59, c_a3, d13cm ,
        q_249_l2, d34cm59, c_a3, d34cm59, c_a3, d34cm59, c_a3, d34cm59, c_a3, d34cm59,
        c_a3, d34cm59, c_a3, d34cm59, c_a3, d34cm59, c_a3, d13cm, q_261_l2, d130cm)

bc2_l3  = (bc2,l3)



beam = Beam()
beam.E = 2.4
beam.beta_x = 41.1209
beam.beta_y = 86.3314
beam.alpha_x = 1.9630
beam.alpha_y = 4.0972


lat = MagneticLattice(bc2_l3, energy=2.4)

tw0 = Twiss(beam)

tws=twiss(lat, tw0, nPoints = 2000)
plot_opt_func(lat, tws, top_plot = ["E"])
plt.show()

f=plt.figure()
ax = f.add_subplot(211)
ax.set_xlim(0, lat.totalLen)

f.canvas.set_window_title('Betas [m]')
p1, = plt.plot(map(lambda p: p.s, tws), map(lambda p: p.beta_x, tws), lw=2.0)
p2, = plt.plot(map(lambda p: p.s, tws), map(lambda p: p.beta_y, tws), lw=2.0)
plt.grid(True)
plt.legend([p1,p2], [r'$\beta_x$',r'$\beta_y$', r'$D_x$'])

ax2 = f.add_subplot(212)
plot_lattice(lat, ax2, alpha=0.5)

# add beam size (arbitrary scale)

s = np.array(map(lambda p: p.s, tws))

scale = 5000

sig_x = scale * np.array(map(lambda p: np.sqrt(p.beta_x*beam.emit_x), tws)) # 0.03 is for plotting same scale
sig_y = scale * np.array(map(lambda p: np.sqrt(p.beta_y*beam.emit_y), tws))

x = scale * np.array(map(lambda p: p.x, tws))
y = scale * np.array(map(lambda p: p.y, tws))


plt.plot(s, x + sig_x, color='#0000AA', lw=2.0)
plt.plot(s, x-sig_x, color='#0000AA', lw=2.0)

plt.plot(s, sig_y, color='#00AA00', lw=2.0)
plt.plot(s, -sig_y, color='#00AA00', lw=2.0)

#f=plt.figure()
plt.plot(s, x, 'r--', lw=2.0)
#plt.plot(s, y, 'r--', lw=2.0)

plt.show()
