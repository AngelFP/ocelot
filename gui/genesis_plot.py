'''
user interface for viewing genesis simulation results
'''

import sys, os, csv
import time
import matplotlib
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from numpy import matlib

from pylab import * #tmp

# font = {'family' : 'normal',
#        'weight' : 'bold',
#        'size'   : 20}
params = {'backend': 'ps', 'axes.labelsize': 15, 'font.size': 15, 'legend.fontsize': 24, 'xtick.labelsize': 19,  'ytick.labelsize': 19, 'text.usetex': True}
rcParams.update(params)
rc('text', usetex=True) # required to have greek fonts on redhat

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 15}

matplotlib.rc('font', **font)

h = 4.135667516e-15
c = 299792458.0

max_yticks = 7

def gen_outplot_e(g, figsize=(8,10), legend = True, fig_name = None, save=False):
    import matplotlib.ticker as ticker

    print('    plotting e-beam evolution')

    font_size = 1
    if fig_name is None:
        if g.filename is '':
            fig = plt.figure('Electrons')
        else:
            fig = plt.figure('Electrons '+g.filename)
    else:
        fig = plt.figure(fig_name)
    
    fig.set_size_inches(figsize,forward=True)
    plt.rc('axes', grid=True)
    plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
    # left, width = 0.1, 0.85
    plt.clf()

    ax_und=fig.add_subplot(4, 1, 1)
    ax_und.clear()
    ax_size_tpos=fig.add_subplot(4, 1, 2,sharex=ax_und)
    ax_size_tpos.clear()
    ax_energy=fig.add_subplot(4, 1, 3,sharex=ax_und)
    ax_energy.clear()
    ax_bunching=fig.add_subplot(4, 1, 4,sharex=ax_und)
    ax_bunching.clear()

    for ax in ax_size_tpos, ax_energy, ax_und, ax_bunching:
        if ax!=ax_bunching:
            for label in ax.get_xticklabels():
                label.set_visible(False)

    # for tick in ax.yaxis.get_major_ticks():
    #     tick.label.set_fontsize(14)
    #     # specify integer or one of preset strings, e.g.
    #     #tick.label.set_fontsize('x-small')
    #     tick.label.set_rotation('vertical')
    fig.subplots_adjust(hspace=0)

    ax_und.plot(g.z, g.aw, 'b-',linewidth=1.5)
    ax_und.set_ylabel('K (rms)')

    ax_quad = ax_und.twinx()
    ax_quad.plot(g.z, g.qfld, 'r-',linewidth=1.5)
    ax_quad.set_ylabel('Quad')
    ax_quad.grid(False)

    #sys.exit()
    ax_size_tpos.plot(g.z, np.mean(g.xrms,axis=0)*1e6, 'g-',g.z, np.mean(g.yrms,axis=0)*1e6, 'b-')
    ax_size_tpos.set_ylabel('$\sigma_{x,y}$ [$\mu$m]')


    # ax_energy.plot(g.z, np.average(g.el_energy*0.511e-3, weights=g.I, axis=0), 'b-',linewidth=1.5) #with current as weight 
    ax_energy.plot(g.z, np.average(g.el_energy*0.511e-3, axis=0), 'b-',linewidth=1.5)
    ax_energy.set_ylabel('E [GeV]')
    ax_energy.ticklabel_format(axis='y', style='sci', scilimits=(-3, 3), useOffset=False)
    ax_spread = ax_energy.twinx()
    ax_spread.plot(g.z, np.average(g.el_e_spread*0.511e-3*1000, weights=g.I, axis=0), 'm--', g.z, np.amax(g.el_e_spread*0.511e-3*1000, axis=0), 'r--',linewidth=1.5)
    ax_spread.set_ylabel('$\sigma_E$ [MeV]')
    ax_spread.grid(False)
    
    ax_bunching.plot(g.z, np.average(g.bunching, weights=g.I, axis=0), 'k-', g.z, np.amax(g.bunching, axis=0), 'grey',linewidth=1.5)
    ax_bunching.set_ylabel('Bunching')

    ax_bunching.set_xlabel('z [m]')
    
    ax_size_tpos.set_ylim(ymin=0)
    ax_spread.set_ylim(ymin=0)
    ax_bunching.set_ylim(ymin=0)
    
    number_ticks=6
    
    ax_und.yaxis.major.locator.set_params(nbins=number_ticks)
    ax_quad.yaxis.major.locator.set_params(nbins=number_ticks)
    ax_energy.yaxis.major.locator.set_params(nbins=number_ticks)
    ax_spread.yaxis.major.locator.set_params(nbins=number_ticks)
    ax_bunching.yaxis.major.locator.set_params(nbins=number_ticks)
    ax_size_tpos.yaxis.major.locator.set_params(nbins=number_ticks)
    # yloc = plt.MaxNLocator(max_yticks)
    # ax_size_tpos.yaxis.set_major_locator(yloc)
    # ax_energy.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1e'))
    
    plt.xlim(g.z[0], g.z[-1])
    
    fig.subplots_adjust(top=0.95, bottom=0.1, right=0.85, left=0.15)
    
    #plot undulator K rms. if there is tapering and K!=0, plot is scaled to viwew the tapering profile
    if np.amax(g.aw)!=0:
        aw_tmp=np.array(g.aw)[np.array(g.aw)!=0]
        if np.amax(aw_tmp)!=np.amin(aw_tmp):
            diff=np.amax(aw_tmp)-np.amin(aw_tmp)
            ax_und.set_ylim([np.amin(aw_tmp)-diff/10,np.amax(aw_tmp)+diff/10])
    else:
        ax_und.set_ylim([0,1])
    ax_und.tick_params(axis='y', which='both', colors='b')
    ax_und.yaxis.label.set_color('b')
    ax_quad.tick_params(axis='y', which='both', colors='r')
    ax_quad.yaxis.label.set_color('r') 
    ax_energy.tick_params(axis='y', which='both', colors='b')
    ax_energy.yaxis.label.set_color('b')    
    ax_spread.tick_params(axis='y', which='both', colors='r')
    ax_spread.yaxis.label.set_color('r') 

    if save!=False:
        if save==True:
            save='png'
        fig.savefig(g.path+'_elec.'+str(save),format=save)
        
    return fig



def gen_outplot_ph(g, figsize=(8, 10), legend = True, fig_name = None, save=False):
    import matplotlib.ticker as ticker
    
    print('    plotting radiation evolution')
    
    font_size = 1
    if fig_name is None:
        if g.filename is '':
            fig = plt.figure('Radaition')
        else:
            fig = plt.figure('Radiation '+g.filename)
    else:
        fig = plt.figure(fig_name)

    fig.set_size_inches(figsize,forward=True)

    plt.rc('axes', grid=True)
    plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
    plt.clf()

    
    if g('itdp')==True:
        ax_pow=fig.add_subplot(3, 1, 1)
        ax_pow.clear()
        ax_spectrum=fig.add_subplot(3, 1, 2,sharex=ax_pow)
        ax_spectrum.clear()
        ax_size_t=fig.add_subplot(3, 1, 3,sharex=ax_pow)
        ax_size_t.clear()
        for ax in ax_pow, ax_spectrum, ax_size_t:
            if ax!=ax_size_t:
                for label in ax.get_xticklabels():
                    label.set_visible(False)
    else:
        ax_pow=fig.add_subplot(2, 1, 1)
        ax_pow.clear()
        ax_size_t=fig.add_subplot(2, 1, 2,sharex=ax_pow)
        ax_size_t.clear()
        for ax in ax_pow, ax_size_t:
            if ax!=ax_size_t:
                for label in ax.get_xticklabels():
                    label.set_visible(False)



    # for tick in ax.yaxis.get_major_ticks():
    #     tick.label.set_fontsize(14)
    #     # specify integer or one of preset strings, e.g.
    #     #tick.label.set_fontsize('x-small')
    #     tick.label.set_rotation('vertical')

    #
    fig.subplots_adjust(hspace=0)

    ax_pow.plot(g.z, np.amax(g.p_int, axis=0), 'g-',linewidth=1.5)
    ax_pow.text(0.98, 0.02,'$P_{end}$= %.2e W\n$E_{end}$= %.2e J' %(np.amax(g.p_int[:,-1]),np.mean(g.p_int[:,-1],axis=0)*g('xlamds')*g('zsep')*g.nSlices/c), fontsize=12, horizontalalignment='right', verticalalignment='bottom', transform = ax_pow.transAxes)#horizontalalignment='center', verticalalignment='center',
    ax_pow.set_ylabel('P [W]')
    ax_pow.get_yaxis().get_major_formatter().set_useOffset(False)
    ax_pow.get_yaxis().get_major_formatter().set_scientific(True)
#    if np.amin(g.p_int)>0:
    if np.amax(g.p_int)>0:
        ax_pow.set_yscale('log')



    ax_en = ax_pow.twinx()
    ax_en.plot(g.z, np.mean(g.p_int,axis=0)*g('xlamds')*g('zsep')*g.nSlices/c, 'k--',linewidth=1.5)
    ax_en.set_ylabel('E [J]')
    ax_en.get_yaxis().get_major_formatter().set_useOffset(False)
    ax_en.get_yaxis().get_major_formatter().set_scientific(True)
    if np.amax(g.p_int)>0:
        ax_en.set_yscale('log')


    if g('itdp')==True:
        n_pad=1
        # print len(g.z),len(g.xrms[0,:]),len(np.mean(g.yrms,axis=0))
        power=np.pad(g.p_mid, [(int(g.nSlices/2)*n_pad, (g.nSlices-(int(g.nSlices/2))))*n_pad, (0, 0)], mode='constant')
        phase=np.pad(g.phi_mid, [(int(g.nSlices/2)*n_pad, (g.nSlices-(int(g.nSlices/2))))*n_pad, (0, 0)], mode='constant')
        spectrum = abs(fft(np.sqrt( np.array(power)) * np.exp( 1.j* np.array(phase) ) , axis=0))**2/sqrt(g.nSlices)/(2*g.leng/g('ncar'))**2/1e10
        e_0=1239.8/g('xlamds')/1e9
        # print e_0
    
        g.freq_ev1 = h * fftfreq(len(spectrum), d=g('zsep') * g('xlamds') / c)+e_0
        lamdscale=1239.8/g.freq_ev1
        lamdscale_array=np.swapaxes(np.tile(lamdscale,(g.nZ,1)),0,1)    
        
    #    print spectrum.shape
        spectrum_norm=np.sum(spectrum,axis=0)#avoiding division by zero
        spectrum_norm[spectrum_norm==0]=1
    #    print spectrum_norm.shape
        spectrum_lamdpos=np.sum(spectrum*lamdscale_array/spectrum_norm,axis=0)
    #    print "spectrum lamdpos", spectrum_lamdpos
        spectrum_lamdwidth=sqrt(np.sum(spectrum*(lamdscale_array-spectrum_lamdpos)**2/spectrum_norm,axis=0))    
        
        spectrum_lamdwidth1=np.empty(g.nZ)
        for zz in range(g.nZ):
            if np.sum(spectrum[:,zz])!=0:
                peak=fwhm3(spectrum[:,zz])
                #spectrum_lamdwidth1[zz]=abs(lamdscale[peak[0]]-lamdscale[peak[0]+1])*peak[1] #the FWHM of spectral line (error when paekpos is at the edge of lamdscale)
                spectrum_lamdwidth1[zz]=abs(lamdscale[0]-lamdscale[1])*peak[1] #the FWHM of spectral line (error when paekpos is at the edge of lamdscale)
            else:
                spectrum_lamdwidth1[zz]=0
    
    
    
        ax_spectrum.plot(g.z, np.amax(spectrum,axis=0), 'r-',linewidth=1.5)
        ax_spectrum.text(0.5, 0.98,r"(on axis)", fontsize=10, horizontalalignment='center', verticalalignment='top', transform = ax_spectrum.transAxes)#horizontalalignment='center', verticalalignment='center',
        ax_spectrum.set_ylabel('P$(\lambda)_{max}$ [a.u.]')
        # if np.amin(np.amax(spectrum,axis=0))>0:
        if np.amax(np.amax(spectrum,axis=0))>0:
            ax_spectrum.set_yscale('log')
        
        #fix!!!
        ax_spec_bandw = ax_spectrum.twinx()
        ax_spec_bandw.plot(g.z, spectrum_lamdwidth*2, 'm--')
        ax_spec_bandw.set_ylabel('$2\sigma\lambda$ [nm]')
        # fix and include!!!
    
    
        s=g.t*c*1.0e-15*1e6
        s_array=np.swapaxes(np.tile(s,(g.nZ,1)),0,1)    
        p_int_norm=np.sum(g.p_int,axis=0)#avoiding division by zero
        p_int_norm[p_int_norm==0]=1
        rad_longit_pos=np.sum(g.p_int*s_array/p_int_norm,axis=0)
        rad_longit_size=sqrt(np.sum(g.p_int*(s_array-rad_longit_pos)**2/p_int_norm,axis=0)) #this is standard deviation (sigma)
    
        #g.p_int=np.amax(g.p_int)/1e6+g.p_int # nasty fix from division by zero
        if np.amax(g.p_int)>0:
            weight=g.p_int+np.amin(g.p_int[g.p_int!=0])/1e6
        else:
            weight=np.ones_like(g.p_int)
            
        
        ax_size_l = ax_size_t.twinx() #longitudinal size
        ax_size_l.plot(g.z, rad_longit_size*2, color='indigo', linestyle='dashed',linewidth=1.5)
        ax_size_l.set_ylabel('longitudinal [$\mu$m]')

        ax_size_t.plot(g.z, np.average(g.r_size*2*1e6, weights=weight, axis=0), 'b-',linewidth=1.5)
        ax_size_t.plot([np.amin(g.z), np.amax(g.z)],[g.leng*1e6, g.leng*1e6], 'b-',linewidth=1.0)
        ax_size_t.set_ylabel('transverse [$\mu$m]')
    else:
        ax_size_t.plot(g.z, g.r_size.T*2*1e6, 'b-',linewidth=1.5)
        ax_size_t.plot([np.amin(g.z), np.amax(g.z)],[g.leng*1e6, g.leng*1e6], 'b-',linewidth=1.0)
        ax_size_t.set_ylabel('transverse [$\mu$m]')



    plt.xlim(g.z[0], g.z[-1])

    fig.subplots_adjust(top=0.95, bottom=0.1, right=0.85, left=0.15)


    ax_pow.tick_params(axis='y', which='both', colors='g')
    ax_pow.yaxis.label.set_color('g')  
    ax_en.tick_params(axis='y', which='both', colors='k')
    ax_en.yaxis.label.set_color('k') 
    ax_en.grid(False)
    ax_size_t.tick_params(axis='y', which='both', colors='b')
    ax_size_t.yaxis.label.set_color('b') 
    ax_size_t.set_xlabel('z [m]')
    ax_size_t.set_ylim(ymin=0)
    ax_pow.yaxis.get_offset_text().set_color(ax_pow.yaxis.label.get_color())
    ax_en.yaxis.get_offset_text().set_color(ax_en.yaxis.label.get_color())

    if g('itdp')==True:
        ax_spectrum.tick_params(axis='y', which='both', colors='r')
        ax_spectrum.yaxis.label.set_color('r')  
        ax_spec_bandw.tick_params(axis='y', which='both', colors='m')
        ax_spec_bandw.yaxis.label.set_color('m')
        ax_spec_bandw.grid(False)
        ax_size_l.tick_params(axis='y', which='both', colors='indigo')
        ax_size_l.yaxis.label.set_color('indigo') 
        ax_size_l.grid(False)
        ax_size_l.set_ylim(ymin=0)    
        ax_spec_bandw.set_ylim(ymin=0)


    # #attempt to fix overlapping label values
# #    for a in [ax_size_l,ax_size_t,ax_spec_bandw,ax_spectrum]:
# #        xticks = a.yaxis.get_major_ticks()
# #        xticks[-1].label.set_visible(False)  
    
# #    labels = ax_size_t.get_yticklabels()
# ##    print dir(labels), labels
# #    labels[0] = ""
# #    ax_size_t.set_yticklabels(labels)    

    if save!=False:
        if save==True:
            save='png'
        fig.savefig(g.path+'_rad.'+str(save),format=save)
    return fig



def gen_outplot_z(g, figsize=(8, 10), legend = True, fig_name = None, z=inf, save=False):
#    max_yticks = 7
    if g('itdp')==False:
        print('    plotting bunch profile at '+str(z)+' [m]')
        print('!     not applicable for steady-state')
        return
    
    import matplotlib.ticker as ticker
    
    if z==inf:
#        print 'Showing profile parameters at the end of undulator'
        z=np.amax(g.z)

    elif z>np.amax(g.z):
#        print 'Z parameter too large, setting to the undulator end'
        z=np.amax(g.z)
    
    elif z<np.amin(g.z):
#        print 'Z parameter too small, setting to the undulator entrance'    
        z=np.amin(g.z)
        
    zi=np.where(g.z>=z)[0][0]
    z=g.z[zi];
    
    print('    plotting bunch profile at '+str(z)+' [m]')



    font_size = 1
    if fig_name is None:
        if g.filename is '':
            fig = plt.figure('Bunch profile at '+str(z)+'m')
        else:
            fig = plt.figure('Bunch profile at '+str(z)+'m '+g.filename)
    else:
        fig = plt.figure(fig_name)
    fig.set_size_inches(figsize,forward=True)
    plt.rc('axes', grid=True)
    plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
    # left, width = 0.1, 0.85
    
    plt.clf()
    
    ax_curr=fig.add_subplot(4, 1, 1)
    ax_curr.clear()
    ax_energy=fig.add_subplot(4, 1, 2,sharex=ax_curr)
    ax_energy.clear()    
    ax_phase=fig.add_subplot(4, 1, 3,sharex=ax_curr)
    ax_phase.clear()
    ax_spectrum=fig.add_subplot(4, 1, 4)
    ax_spectrum.clear()

    for ax in ax_curr, ax_phase, ax_spectrum, ax_energy:
        if ax!=ax_spectrum and ax!=ax_phase:
            for label in ax.get_xticklabels():
                label.set_visible(False)

    #
    
    
    fig.subplots_adjust(hspace=0)
 
    s=g.t*c*1.0e-15*1e6
    
    
        
    
    ax_curr.plot(s, g.I/1e3, 'k--')
    ax_curr.set_ylabel('I [kA]')
    ax_curr.set_ylim(ymin=0)
    ax_curr.text(0.02, 0.98,r"Q= %.2f pC" %(g.beam_charge*1e12), fontsize=12, horizontalalignment='left', verticalalignment='top', transform = ax_curr.transAxes)#horizontalalignment='center', verticalalignment='center',


    ax_power = ax_curr.twinx()
    ax_power.grid(False)
    ax_power.plot(s,g.p_int[:,zi],'g-',linewidth=1.5)    
    ax_power.set_ylabel('Power [W]')
    ax_power.set_ylim(ymin=0)
    # if np.amax(g.p_int[:,zi])!=np.amin(g.p_int[:,zi]):
        # ax_power.set_ylim([0, np.amax(g.p_int[:,zi])])
    ax_power.get_yaxis().get_major_formatter().set_useOffset(False)
    ax_power.get_yaxis().get_major_formatter().set_scientific(True)
    ax_power.get_yaxis().get_major_formatter().set_powerlimits((-3, 4))#[:,75,75]
    
#    ax_power.get_xaxis().get_offset_text().set_x(1.1)

    ax_energy.plot(s, g.el_energy[:,zi]*0.511e-3, 'b-', s, (g.el_energy[:,zi]+g.el_e_spread[:,zi])*0.511e-3, 'r--',s, (g.el_energy[:,zi]-g.el_e_spread[:,zi])*0.511e-3, 'r--')
    ax_energy.set_ylabel('$E\pm\sigma_E$ [GeV]')
#    ax_energy.ticklabel_format(axis='y', style='sci', scilimits=(-3, 3), useOffset=False)
    ax_energy.ticklabel_format(useOffset=False, style='plain')   

    ax_bunching = ax_energy.twinx()
    ax_bunching.plot(s,g.bunching[:,zi],'grey',linewidth=0.5)
    ax_bunching.set_ylabel('Bunching')
    ax_bunching.set_ylim(ymin=0)
    ax_bunching.grid(False)
    
    
    n_pad=1
    power=np.pad(g.p_mid, [(int(g.nSlices/2)*n_pad, (g.nSlices-(int(g.nSlices/2))))*n_pad, (0, 0)], mode='constant')
    phase=np.pad(g.phi_mid, [(int(g.nSlices/2)*n_pad, (g.nSlices-(int(g.nSlices/2))))*n_pad, (0, 0)], mode='constant') #not supported by the numpy 1.6.2


    spectrum = abs(fft(np.sqrt( np.array(power)) * np.exp( 1.j* np.array(phase) ) , axis=0))**2/sqrt(g.nSlices)/(2*g.leng/g('ncar'))**2/1e10
    e_0=1239.8/g('xlamds')/1e9
    g.freq_ev1 = h * fftfreq(len(spectrum), d=g('zsep') * g('xlamds') / c)+e_0
    lamdscale=1239.8/g.freq_ev1

    lamdscale_array=np.swapaxes(np.tile(lamdscale,(g.nZ,1)),0,1)    
    
#    for std calculation
#    spectrum_lamdpos=np.sum(spectrum*lamdscale_array/np.sum(spectrum,axis=0),axis=0)
#    spectrum_lamdwidth=sqrt(np.sum(spectrum*(lamdscale_array-spectrum_lamdpos)**2/np.sum(spectrum,axis=0),axis=0))
    

    ax_spectrum.plot(fftshift(lamdscale), fftshift(spectrum[:,zi]), 'r-')
    ax_spectrum.text(0.98, 0.98,r"(on axis)", fontsize=10, horizontalalignment='right', verticalalignment='top', transform = ax_spectrum.transAxes)#horizontalalignment='center', verticalalignment='center',
    ax_spectrum.set_ylabel('P($\lambda$) [a.u.]')
    ax_spectrum.set_xlabel('$\lambda$ [nm]')
    ax_spectrum.set_ylim(ymin=0)
    ax_spectrum.get_yaxis().get_major_formatter().set_useOffset(False)
    ax_spectrum.get_yaxis().get_major_formatter().set_scientific(True)
    ax_spectrum.get_yaxis().get_major_formatter().set_powerlimits((-3, 4))#[:,75,75]
    if np.amin(lamdscale) != np.amax(lamdscale):
        ax_spectrum.set_xlim([np.amin(lamdscale), np.amax(lamdscale)])
    ax_phase.set_xlabel('s [$\mu$m]')


    maxspectrum_index=np.argmax(spectrum[:,zi])
    maxspectrum_wavelength=lamdscale[maxspectrum_index]*1e-9

    phase=unwrap(g.phi_mid[:,zi])
    
    phase_cor=np.arange(g.nSlices)*(maxspectrum_wavelength-g('xlamds'))/g('xlamds')*g('zsep')*2*pi
    phase_fixed=phase+phase_cor
    n=1
    phase_fixed = ( phase_fixed + n*pi) % (2 * n*pi ) - n*pi
    ax_phase.plot(s, phase_fixed, 'k-',linewidth=0.5)
    ax_phase.text(0.98, 0.98,r"(on axis)", fontsize=10, horizontalalignment='right', verticalalignment='top', transform = ax_phase.transAxes)#horizontalalignment='center', verticalalignment='center',
    ax_phase.set_ylabel('$\phi$ [rad]')
    ax_phase.set_ylim([-pi, pi])

    number_ticks=6

    # ax_spectrum.yaxis.major.locator.set_params(nbins=number_ticks)
    
    ax_phase.xaxis.major.locator.set_params(nbins=number_ticks)
    ax_power.yaxis.major.locator.set_params(nbins=number_ticks)
    ax_energy.yaxis.major.locator.set_params(nbins=number_ticks)
    ax_spectrum.yaxis.major.locator.set_params(nbins=number_ticks)
    ax_bunching.yaxis.major.locator.set_params(nbins=number_ticks)
    ax_curr.yaxis.major.locator.set_params(nbins=number_ticks)

    # ax_energy.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1e'))

    plt.xlim(s[0], s[-1])

    fig.subplots_adjust(top=0.95, bottom=0.2, right=0.85, left=0.15)

    #fig.set_size_inches((8,8),forward=True)
    
    pos1 = ax_spectrum.get_position() # get the original position 
    pos2 = [pos1.x0 + 0, pos1.y0 - 0.1,  pos1.width / 1.0, pos1.height / 0.9] 
    ax_spectrum.set_position(pos2)

    ax_spectrum.tick_params(axis='y', which='both', colors='r')
    ax_spectrum.yaxis.label.set_color('r')    
    ax_energy.tick_params(axis='y', which='both', colors='b')
    ax_energy.yaxis.label.set_color('b')    

    ax_bunching.tick_params(axis='y', which='both', colors='grey')
    ax_bunching.yaxis.label.set_color('grey')  
    
    ax_power.tick_params(axis='y', which='both', colors='g')
    ax_power.yaxis.label.set_color('g')    
    ax_power.yaxis.get_offset_text().set_color(ax_power.yaxis.label.get_color())
    ax_spectrum.yaxis.get_offset_text().set_color(ax_spectrum.yaxis.label.get_color())
    

    if save!=False:
        if save==True:
            save='png'
        fig.savefig(g.path+'_z_'+str(z)+'m.'+str(save),format=save)
    
    return fig



def gen_outplot_scanned_z(g, figsize=(8, 10), legend = True, fig_name = None, z=inf, save=False):
#    max_yticks = 7
    if g('itdp')==True:
        print('    plotting scan at '+str(z)+' [m]')
        print('!     Not implemented yet for time dependent, skipping')
        return
        
    if g('iscan')==0 and g('scan')==0:
        print('    plotting scan at '+str(z)+' [m]')
        print('!     Not a scan, skipping')
        return
    
    import matplotlib.ticker as ticker
    
    if z==inf:
#        print 'Showing profile parameters at the end of undulator'
        z=np.amax(g.z)

    elif z>np.amax(g.z):
#        print 'Z parameter too large, setting to the undulator end'
        z=np.amax(g.z)
    
    elif z<np.amin(g.z):
#        print 'Z parameter too small, setting to the undulator entrance'    
        z=np.amin(g.z)
        
    zi=np.where(g.z>=z)[0][0]
    z=g.z[zi];
    
    print('    plotting scan at '+str(z)+' [m]')



    font_size = 1
    if fig_name is None:
        if g.filename is '':
            fig = plt.figure('Genesis scan at '+str(z)+'m')
        else:
            fig = plt.figure('Genesis scan at '+str(z)+'m '+g.filename)
    else:
        fig = plt.figure(fig_name)
    fig.set_size_inches(figsize,forward=True)
    plt.rc('axes', grid=True)
    plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
    # left, width = 0.1, 0.85
    
    plt.clf()
    
    ax_curr=fig.add_subplot(2, 1, 1)
    ax_curr.clear()
    ax_energy=fig.add_subplot(2, 1, 2,sharex=ax_curr)
    ax_energy.clear()    
#    ax_phase=fig.add_subplot(4, 1, 3,sharex=ax_curr)
#    ax_phase.clear()
#    ax_spectrum=fig.add_subplot(4, 1, 4)
#    ax_spectrum.clear()

    for ax in [ax_curr]:#, ax_energy: #ax_phase, ax_spectrum, 
        for label in ax.get_xticklabels():
            label.set_visible(False)

    #
    
    
    fig.subplots_adjust(hspace=0)
    
    s=g.scv #scan value is written to current colunm
        
    
    ax_curr.plot(s, np.linspace(g('curpeak'),g('curpeak'),len(s)), 'k--')
    ax_curr.set_ylabel('I[kA]')


    ax_power = ax_curr.twinx()
    ax_power.grid(False)
    ax_power.plot(s,g.p_int[:,zi],'g-',linewidth=1.5)    
    ax_power.set_ylabel('Power [W]')
    ax_power.set_ylim([0, np.amax(g.p_int[:,zi])])
    ax_power.get_yaxis().get_major_formatter().set_useOffset(False)
    ax_power.get_yaxis().get_major_formatter().set_scientific(True)
    ax_power.get_yaxis().get_major_formatter().set_powerlimits((-3, 4))#[:,75,75]
    
#    ax_power.get_xaxis().get_offset_text().set_x(1.1)

    ax_energy.plot(s, g.el_energy[:,zi]*0.511e-3, 'b-', s, (g.el_energy[:,zi]+g.el_e_spread[:,zi])*0.511e-3, 'r--',s, (g.el_energy[:,zi]-g.el_e_spread[:,zi])*0.511e-3, 'r--')
    ax_energy.set_ylabel('$E\pm\sigma_E$\n[GeV]')
#    ax_energy.ticklabel_format(axis='y', style='sci', scilimits=(-3, 3), useOffset=False)
    ax_energy.ticklabel_format(useOffset=False, style='plain')   
    ax_energy.get_xaxis().get_major_formatter().set_useOffset(False)
    ax_energy.get_xaxis().get_major_formatter().set_scientific(True)


    ax_bunching = ax_energy.twinx()
    ax_bunching.plot(s,g.bunching[:,zi],'grey',linewidth=0.5)
    ax_bunching.set_ylabel('Bunching')
    ax_bunching.grid(False)
    
    
#    ax_power.yaxis.major.locator.set_params(nbins=number_ticks)
#    ax_energy.yaxis.major.locator.set_params(nbins=number_ticks)

    # ax_energy.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1e'))

    plt.xlim(s[0], s[-1])

    fig.subplots_adjust(top=0.95, bottom=0.2, right=0.85, left=0.15)

    #fig.set_size_inches((8,8),forward=True)
    
   
    ax_energy.tick_params(axis='y', which='both', colors='b')
    ax_energy.yaxis.label.set_color('b')    

    ax_bunching.tick_params(axis='y', which='both', colors='grey')
    ax_bunching.yaxis.label.set_color('grey')
    
    ax_power.tick_params(axis='y', which='both', colors='g')
    ax_power.yaxis.label.set_color('g')    
    ax_power.yaxis.get_offset_text().set_color(ax_power.yaxis.label.get_color())
    
    if save!=False:
        if save==True:
            save='png'
        fig.savefig(g.path+'_z_'+str(z)+'m_scan.'+str(save),format=save)
    
    return fig


def gen_outplot(handle=None,save='png',show=False,debug=0,all=False,vartype_dfl=complex128):
    #picks as an input "GenesisOutput" object, file path of directory as strings. 
    #plots e-beam evolution, radiation evolution, initial and final simulation window
    #If folder path is provided, all *.gout and *.out files are plotted
    import os
    from ocelot.adaptors.genesis import GenesisOutput, readGenesisOutput, readRadiationFile
    
    print('')
    print('  plotting genesis output:')
    plotting_time = time.time()
    
    plt.ioff()
    
    if save==True:
        save='png'
    
    if os.path.isdir(str(handle)):
        handles=[]
        for root, dirs, files in os.walk(handle):
            for name in files:
                if name.endswith('.gout') or name.endswith('.out'):
                    handles.append(os.path.join(root, name))
        print('\n  plotting all files in '+str(handle))
    else:
        handles=[handle]
    
    for handle in handles:
    
        if os.path.isfile(str(handle)):
            handle=readGenesisOutput(handle,readall=1,debug=debug)
            
        if isinstance(handle,GenesisOutput):
            f1=gen_outplot_e(handle,save=save)
            f2=gen_outplot_ph(handle,save=save)
            f3=gen_outplot_z(handle, z=0,save=save)
            f4=gen_outplot_z(handle, z=inf,save=save)
        
        if os.path.isfile(handle.path+'.dfl') and all:
            dfl=readRadiationFile(handle.path+'.dfl', handle.ncar, vartype=vartype_dfl)
            f5=gen_outplot_dfl(dfl, handle,save=save)
            f6=gen_outplot_dfl(dfl, handle,far_field=1,freq_domain=0,auto_zoom=0,save=save)
            f7=gen_outplot_dfl(dfl, handle,far_field=0,freq_domain=1,auto_zoom=0,save=save)
            
    if show==True:
        print('    showing plots, close all to proceed')
        plt.show()
        
    if save!=False:
        print('    plots recorded to *.'+str(save)+' files')
    
    print ('    total plotting time %.2f seconds' % (time.time() - plotting_time))
    
    # return [f1,f2,f3,f4]


def gen_outplot_dfl(dfl, out=None, z_lim=[], xy_lim=[], figsize=3, legend = True, phase = False, far_field=False, freq_domain=False, fig_name = None, auto_zoom=False, column_3d=True, save=False, show=False, return_proj=False, vartype_dfl=complex64):
    
    #dfl can be either object or the path to dfl file
    #out can be genesis output object
    #z_lim sets the boundaries to CUT the dfl object in z to ranges of e.g. [2,5] um or nm depending on freq_domain=False of True
    #xy_lim sets the boundaries to SCALE the dfl object in x and y to ranges of e.g. [2,5] um or urad depending on far_field=False of True
    #figsize rescales the size of the figure
    #legend not used yet
    #phase can replace Z projection or spectrum with phase front distribution
    #far_field and freq_domain carry out FFT along xy and z dimentions correspondingly
    #fig_name is the desired name of the output figure
    #auto_zoom automatically scales xyz the images to the (1%?) of the intensity limits
    #column_3d plots top and side views of the radiation distribution
    #save and show allow to save figure to image (save='png' (default) or save='eps', etc...) or to display it (slower)
    #return_proj returns [xy_proj,yz_proj,xz_proj,x,y,z] array.
    #vartype_dfl is the data type to store dfl in memory [either complex128 (two 64-bit floats) or complex64 (two 32-bit floats)], may save memory
    
    text_present=1
    
    print('    plotting dfl file')
    start_time = time.time()
    # print dfl.shape
    # print np.fft.ifftshift(dfl,(1,2)).shape
    # print np.fft.fft2(dfl).shape
    
    if out==None: #the case if only path to .dfl or .out is given
        from ocelot.adaptors.genesis import GenesisOutput, readGenesisOutput
        dfl_dir=dfl
        out_dir=dfl_dir.replace('.dfl','')
        out=readGenesisOutput(out_dir,readall=0,debug=0)
    
    if dfl.__class__==str:
        from ocelot.adaptors.genesis import readRadiationFile
        try:
            dfl=readRadiationFile(dfl, out.ncar, vartype=vartype_dfl)
        except IOError:
            print ('      ERR: no such file "'+dfl+'"')
            print ('      ERR: reading "'+out.path+'.dfl'+'"')
            dfl=readRadiationFile(out.path+'.dfl', out.ncar, vartype=vartype_dfl)
    
    # dfl=dfl[100:110,:,:]
    
    suffix=''
    # print dfl.shape
    if dfl.shape[0]!=1:
        ncar_z=dfl.shape[0]
        # if out('isradi')==0: #parameter for dfl output every isradi-th slice #not the case?
        leng_z=out('xlamds')*out('zsep')*ncar_z
        # else:
            # leng_z=out('xlamds')*out('zsep')*out('isradi')*ncar_z
        z = np.linspace(0, leng_z, ncar_z)
    else:
        column_3d=False
        phase = True
        freq_domain=False
    
    dfl=swapaxes(dfl,2,1) # zyx -> zxy

    #Make sure it is time-dependent
    if dfl.shape[0]==1:
        z_lim=[]
    

    
    #number of mesh points
    ncar_x=dfl.shape[1]
    leng_x=out.leng #transverse size of mesh [m], to be upgraded
    ncar_y=dfl.shape[2]
    leng_y=out.leng

    if dfl.shape[0]!=1:
        if freq_domain:
            print('      calculating spectrum')
            calc_time=time.time()
            dfl=np.fft.ifftshift(np.fft.fft(dfl,axis=0),0)/sqrt(ncar_z) # 
            dk=2*pi/leng_z;
            k=2*pi/out('xlamds');
            z = 2*pi/np.linspace(k-dk/2*ncar_z, k+dk/2*ncar_z, ncar_z)
            suffix+='_fd'
            z*=1e3
            unit_z='nm'
            z_label='$\lambda$ ['+unit_z+']'
            z_labelv=r'[arb. units]'
            z_title='Spectrum'
            z_color='red'
            z=z[::-1]
            dfl=dfl[::-1,:,:]
            print('        done in %.2f seconds' %(time.time()-calc_time))
            z*=1e6
            leng_z*=1e6
        else:
            unit_z='$\mu$m'
            z_label='z ['+unit_z+']'
            z_labelv=r'Power [W]'
            z_title='Z projection'
            z_color='blue'
            z*=1e6
            leng_z*=1e6
    else:
        z=[0]


        if z_lim!=[]:
            if len(z_lim)==1:
                z_lim=[z_lim,z_lim]
            if z_lim[0]>z_lim[1]:
                z_lim[0]=-inf
                z_lim[1]=inf
            if z_lim[1]<np.amin(z) or z_lim[1]>np.amax(z):
                z_lim[1]=np.amax(z)
                # print('      set top lim to max')
            if z_lim[0]>np.amax(z) or z_lim[0]<np.amin(z):
                z_lim[0]=np.amin(z)
                # print('      set low lim to min')
            # z_lim_1=np.where(z>=z_lim[0])[0][0]
            # z_lim_2=np.where(z<=z_lim[1])[0][-1]
            print'      setting z-axis limits to ', np.amin(z),':',z_lim[0],'-',z_lim[1],':',np.amax(z) #tmp
            z_lim_1=np.where(z<=z_lim[0])[0][-1]
            z_lim_2=np.where(z>=z_lim[1])[0][0]
            
            if z_lim_1==z_lim_2 and z_lim_1==0:
                z_lim_2=z_lim_1+1
            elif z_lim_1==z_lim_2 and z_lim_1!=0:
                z_lim_1=z_lim_2-1
            print z_lim_1,z_lim_2,len(z) #tmp
            dfl=dfl[z_lim_1:z_lim_2,:,:]
            z=z[z_lim_1:z_lim_2]
            ncar_z=dfl.shape[0]
            suffix+='_zoom_%.2f-%.2f' % (np.amin(z),np.amax(z))  

    # if dfl.shape[0]==1:
        # column_3d=False
        # phase = True

    if far_field:
        print('      calculating far field')
        calc_time=time.time()
        # for i in arange(0,dfl.shape[0]):
            # dfl[i,:,:]=np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(dfl[i,:,:],(0,1))),(0,1))
        # dfl/=sqrt(ncar_x*ncar_y)# sqrt(ncar_x*ncar_y) because of numpy fft function
        dfl=np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(dfl,(1,2))),(1,2))/sqrt(ncar_x*ncar_y) # sqrt(ncar_x*ncar_y) because of numpy fft function
        dx=leng_x/ncar_x
        dy=leng_y/ncar_y
        x = np.linspace(-1/(2*dx)+1/(2*leng_x), 1/(2*dx)-1/(2*leng_x), ncar_x)*out('xlamds')
        y = np.linspace(-1/(2*dy)+1/(2*leng_y), 1/(2*dy)-1/(2*leng_y), ncar_y)*out('xlamds')
        dx=1/(leng_x)*out('xlamds')#check!!!
        dy=1/(leng_y)*out('xlamds')
        unit_xy='$\mu$rad'
        x_label=r'$\theta_x$ ['+unit_xy+']'
        y_label=r'$\theta_y$ ['+unit_xy+']'
        suffix+='_ff'
        x_title='X divergence'
        y_title='Y divergence'
        xy_title='Far field intensity'
        x_y_color='green'
        print('        done in %.2f seconds' %(time.time()-calc_time))
    else:
        dx=leng_x/ncar_x
        dy=leng_y/ncar_y
        x = np.linspace(-leng_x/2, leng_x/2, ncar_x)
        y = np.linspace(-leng_y/2, leng_y/2, ncar_y)
        unit_xy='$\mu$m'
        x_label='x ['+unit_xy+']'
        y_label='y ['+unit_xy+']'
        x_title='X projection'
        y_title='Y projection'
        xy_title='Intensity'
        x_y_color='blue'
    
    dfl=dfl.astype(np.complex64)

    dx*=1e6
    dy*=1e6
    x*=1e6
    y*=1e6

    leng_x*=1e6
    leng_y*=1e6

    if fig_name is None:
        if out.filename is '':
            fig = plt.figure('Radiation distribution')
        else:
            fig = plt.figure('Radiation distribution'+suffix+' '+out.filename)
    else:
        fig = plt.figure(fig_name)
    fig.clf()
    fig.set_size_inches(((3+2*column_3d)*figsize,3*figsize),forward=True)
    # plt.rc('axes', grid=True)
    # plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
    
    cmap_int = plt.get_cmap('jet')#jet inferno viridis #change to convenient
    cmap_ph = plt.get_cmap('hsv')
    
    #calculate transverse projection, remove z dimention
    
    dfl_int=abs(dfl)**2
    #xy_proj_ampl=sqrt((dfl_int).sum(0))
    xy_proj_ampl=sqrt((dfl_int).sum(0))*exp(1j*angle(dfl.sum(0))) #(amplitude-like) view from front, sum of square of amplitudes with phase as sum of phasors (latter is dedicated for illustration purposes: good to see an averaged wavefront)

    yz_proj=sum(dfl_int,1); #intensity view from side
    xz_proj=sum(dfl_int,2); #intensity view from top
    z_proj=sum(dfl_int,(1,2)); #temporal intensity profile
    del dfl_int, dfl
    
    if len(z)!=1 and freq_domain==False:
        E_pulse=np.sum(z_proj)*(z[1]-z[0])/1e6/c
        print('      E_pulse= %.3e J' %(E_pulse))
    elif len(z)!=1 and freq_domain==True:
        E_pulse=np.sum(z_proj)*(z[1]-z[0])
        E_pulse=0

    
    # x_line=xy_proj_ampl[]
    # y_line=xy_proj_ampl[]
    
    xy_proj=abs(xy_proj_ampl)**2
    xy_proj_ph=angle(xy_proj_ampl)
    
    x_proj=sum(xy_proj,1)
    y_proj=sum(xy_proj,0)
    
    x_line=xy_proj[:,int((ncar_y-1)/2)]
    y_line=xy_proj[int((ncar_x-1)/2),:]
    
    if max(x_line)!=0 and max(y_line)!=0:
        x_line,y_line=x_line/max(x_line),y_line/max(y_line)
    
    
    
    #X=sqrt(sum(abs(X).^2,3)).*exp(1i.*angle(mean(X,3))); #%Matlab 2D field calculation
    # normI = BoundaryNorm(levelsI, ncolors=cmapI.N, clip=True)
    # normP = BoundaryNorm(levelsP, ncolors=cmapP.N, clip=True)
    
    
    
    
    
    
    ax_int=fig.add_subplot(2, 2+column_3d, 1)
    # ax_int.pcolormesh(x, y, xy_proj, cmap=cmap_int)
    intplt=ax_int.pcolormesh(x, y, swapaxes(xy_proj,1,0), cmap=cmap_int)
    ax_int.set_title(xy_title, fontsize=15)
    # ax_int.axes.get_xaxis().set_visible(False)
    ax_int.set_xlabel(r''+x_label)
    ax_int.set_ylabel(y_label)
    if len(z)>1 and text_present:
        ax_int.text(0.01,0.01,r'$E_{p}$=%.2e J' %(E_pulse), horizontalalignment='left', verticalalignment='bottom',fontsize=12, color='white',transform=ax_int.transAxes) #
    
    if phase==True:
        ax_ph=fig.add_subplot(2, 2+column_3d, 4+column_3d, sharex=ax_int,sharey=ax_int)
        # ax_ph.pcolormesh(x, y, xy_proj_ph, cmap=cmap_ph)
        ax_ph.pcolormesh(x, y, swapaxes(xy_proj_ph,1,0), cmap=cmap_ph)
        #ax_ph.axis('equal')
        ax_ph.axis([min(x),max(x),min(y),max(y)])
        ax_ph.set_title('Phase', fontsize=15)
        # ax_ph.set_xlabel(r'[$\mu m$]')
        # ax_ph.set_ylabel(r'[$\mu m$]')
    else:
        ax_z=fig.add_subplot(2, 2+column_3d, 4+column_3d)
        ax_z.plot(z,z_proj,linewidth=1.5,color=z_color)
        ax_z.set_title(z_title, fontsize=15)
        ax_z.set_xlabel(z_label)
        ax_z.set_ylabel(z_labelv)
    
    ax_proj_x=fig.add_subplot(2, 2+column_3d, 3+column_3d, sharex=ax_int)
    ax_proj_x.plot(x,x_line,linewidth=2,color=x_y_color)
    ax_proj_x.set_title(x_title, fontsize=15)
    x_line_f, rms_x=gauss_fit(x,x_line) #fit with Gaussian, and return fitted function and rms
    fwhm_x=fwhm3(x_line)[1]*dx #measure FWHM
    ax_proj_x.plot(x,x_line_f,color='grey')
    if text_present:
        ax_proj_x.text(0.95, 0.95,'fwhm= \n'+str(round_sig(fwhm_x,3))+r' ['+unit_xy+']\nrms= \n'+str(round_sig(rms_x,3))+r' ['+unit_xy+']', horizontalalignment='right', verticalalignment='top', transform = ax_proj_x.transAxes,fontsize=12)
    ax_proj_x.set_ylim(ymin=0,ymax=1)

    
    
    ax_proj_y=fig.add_subplot(2, 2+column_3d, 2, sharey=ax_int)
    ax_proj_y.plot(y_line,y,linewidth=2,color=x_y_color)
    ax_proj_y.set_title(y_title, fontsize=15)
    y_line_f, rms_y=gauss_fit(y,y_line)
    fwhm_y=fwhm3(y_line)[1]*dy
    ax_proj_y.plot(y_line_f,y,color='grey')
    if text_present:
        ax_proj_y.text(0.95, 0.95,'fwhm= '+str(round_sig(fwhm_y,3))+r' ['+unit_xy+']\nrms= '+str(round_sig(rms_y,3))+r' ['+unit_xy+']', horizontalalignment='right', verticalalignment='top', transform = ax_proj_y.transAxes,fontsize=12)
    ax_proj_y.set_xlim(xmin=0,xmax=1)

    
    if column_3d:
        if phase==True:
            ax_proj_xz=fig.add_subplot(2, 2+column_3d, 6)
        else:
            ax_proj_xz=fig.add_subplot(2, 2+column_3d, 6,sharex=ax_z)
        ax_proj_xz.pcolormesh(z, x, swapaxes(xz_proj,1,0), cmap=cmap_int)
        ax_proj_xz.set_title('Top view', fontsize=15)

        # 
        ax_proj_xz.set_xlabel(z_label)
        ax_proj_yz=fig.add_subplot(2, 2+column_3d, 3,sharey=ax_int,sharex=ax_proj_xz)
        ax_proj_yz.pcolormesh(z, y, swapaxes(yz_proj,1,0), cmap=cmap_int)
        ax_proj_yz.set_title('Side view', fontsize=15)

        
        
        
        
    cbar=0
    if cbar:
        fig.subplots_adjust(top=0.95, bottom=0.05, right=0.85, left=0.1)
        #fig.subplots_adjust()
        cbar_int = fig.add_axes([0.89, 0.15, 0.015, 0.7])
        cbar=plt.colorbar(intplt, cax=cbar_int)# pad = -0.05 ,fraction=0.01)
        # cbar.set_label(r'[$ph/cm^2$]',size=10)
        cbar.set_label(r'a.u.',size=10)

    # ax_int.get_yaxis().get_major_formatter().set_useOffset(False)
    # ax_int.get_yaxis().get_major_formatter().set_scientific(True)
    # ax_ph.get_yaxis().get_major_formatter().set_useOffset(False)
    # ax_ph.get_yaxis().get_major_formatter().set_scientific(True)


    if auto_zoom!=False:
        size_x=max(abs(x[nonzero(x_line>0.005)][[0,-1]]))
        size_y=max(abs(x[nonzero(x_line>0.005)][[0,-1]]))
        size_xy=max(size_x,size_y)
        if phase==True and column_3d==True and z_lim==[]:
            ax_proj_xz.set_xlim(z[nonzero(z_proj>max(z_proj)*0.01)][[0,-1]])
        elif phase==False and z_lim==[]:
            ax_z.set_xlim(z[nonzero(z_proj>max(z_proj)*0.01)][[0,-1]])
            print '      scaling xy to', size_xy
            ax_proj_xz.set_ylim([-size_xy, size_xy])
        elif column_3d==True:
            ax_proj_xz.set_ylim([-size_xy, size_xy])
        ax_int.axis('equal')
        ax_int.axis([-size_xy, size_xy,-size_xy, size_xy])
        suffix+='_zmd'
        #ax_int.set_ylim(int(ncar_y/2-ind)*dy, int(ncar_y/2+ind)*dy)
        #ax_proj_x.set_xlim(xmin=x[nonzero(x_line>0.01)][0],xmax=x[nonzero(x_line>0.01)][-1])
    else:
        if column_3d==True:
            ax_proj_xz.axis('tight')
            ax_proj_yz.axis('tight')
        elif column_3d==False and phase==False:
            ax_z.axis('tight')
        ax_int.set_aspect('equal')
        ax_int.autoscale(tight=True)
        
    if len(xy_lim)==2:
        ax_int.axis([-xy_lim[0], xy_lim[0],-xy_lim[1], xy_lim[1]])
        ax_proj_xz.set_ylim([-xy_lim[0], xy_lim[0]])
    elif len(xy_lim)==1:
        ax_int.axis([-xy_lim[0], xy_lim[0],-xy_lim[0], xy_lim[0]])
        ax_proj_xz.set_ylim([-xy_lim[0], xy_lim[0]])
        
    subplots_adjust(wspace=0.4,hspace=0.4)
    

    if save!=False:
        if save==True:
            save='png'
        print'      suffix= ',suffix
        fig.savefig(out.path+'_dfl'+suffix+'.'+str(save),format=save)
       
    print(('      done in %.2f seconds' % (time.time() - start_time)))

    if show==True:
        print('    showing dfl')
        plt.show()
    
    if return_proj:
        return [xy_proj,yz_proj,xz_proj,x,y,z]
    else:
        return fig

def gen_outplot_dpa(out, dpa=None, z=[], figsize=3, legend = True, fig_name = None, auto_zoom=False, column_3d=True, save=False, show=False, return_proj=False, vartype_dfl=complex64):
    
    print('    plotting dpa file')
    start_time = time.time()
    suffix=''
    
    xlamds=out('xlamds')
    zsep=out('zsep')
    nslice=out('nslice')
    nbins=out('nbins')
    npart=out('npart')
    
    if dpa==None:
        dpa=out.path+'.dpa'
    if dpa.__class__==str:
        try:
            dpa=read_particle_file(dpa, nbins=nbins, npart=npart,debug=debug)
        except IOError:
            print ('      ERR: no such file "'+dpa+'"')
            print ('      ERR: reading "'+out.path+'.dpa'+'"')
            dpa=read_particle_file(out.path+'.dpa', nbins=nbins, npart=npart,debug=debug)

    m=np.arange(nslice)
    m=np.tile(m,(nbins,npart/nbins,1))
    m=np.rollaxis(m,2,0)
    
    dpa.z=dpa.ph*xlamds/2/pi+m*xlamds*zsep
    dpa.t=dpa.z/speed_of_light
    
    plt.scatter(dpa.ph[nslice,1,:],dpa.e[nslice,1,:])
    
    # print('    plotting dpa file')
    # start_time = time.time()
    # suffix=''

    # # if os.path.isfile(str(dpa)):
    # # read_particle_file(dpa, nbins=4, npart=[],debug=0):
    
    # particles.e=b[:,0,:,:] #gamma
    # particles.ph=b[:,1,:,:] 
    # particles.x=b[:,2,:,:]
    # particles.y=b[:,3,:,:]
    # particles.px=b[:,4,:,:]
    # particles.py=b[:,5,:,:]
    
    # figure()
    
    # nslice=100
    
    # plt.scatter(particles.ph[nslice,1,:],particles.e[nslice,1,:])
    
    
    
    # if dfl.shape[0]!=1:
        # ncar_z=dfl.shape[0]
        # # if g('isradi')==0: #parameter for dfl output every isradi-th slice #not the case?
        # leng_z=g('xlamds')*g('zsep')*ncar_z
        # # else:
            # # leng_z=g('xlamds')*g('zsep')*g('isradi')*ncar_z
        # z = np.linspace(0, leng_z, ncar_z)
    # else:
        # column_3d=False
    
    # dfl=swapaxes(dfl,2,1) # zyx -> zxy
    
    # #number of mesh points
    # ncar_x=dfl.shape[1]
    # leng_x=g.leng #transverse size of mesh [m], to be upgraded
    # ncar_y=dfl.shape[2]
    # leng_y=g.leng


    # if far_field:
        # print('      calculating far field')
        # calc_time=time.time()
        # # for i in arange(0,dfl.shape[0]):
            # # dfl[i,:,:]=np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(dfl[i,:,:],(0,1))),(0,1))
        # # dfl/=sqrt(ncar_x*ncar_y)# sqrt(ncar_x*ncar_y) because of numpy fft function
        # dfl=np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(dfl,(1,2))),(1,2))/sqrt(ncar_x*ncar_y) # sqrt(ncar_x*ncar_y) because of numpy fft function
        # dx=leng_x/ncar_x
        # dy=leng_y/ncar_y
        # x = np.linspace(-1/(2*dx)+1/(2*leng_x), 1/(2*dx)-1/(2*leng_x), ncar_x)*g('xlamds')
        # y = np.linspace(-1/(2*dy)+1/(2*leng_y), 1/(2*dy)-1/(2*leng_y), ncar_y)*g('xlamds')
        # dx=1/(leng_x)*g('xlamds')#check!!!
        # dy=1/(leng_y)*g('xlamds')
        # unit_xy='$\mu$rad'
        # x_label=r'$\theta_x$ ['+unit_xy+']'
        # y_label=r'$\theta_y$ ['+unit_xy+']'
        # suffix+='_ff'
        # x_title='X divergence'
        # y_title='Y divergence'
        # xy_title='Far field intensity'
        # x_y_color='grey'
        # print('        done in %.2f seconds' %(time.time()-calc_time))
    # else:
        # dx=leng_x/ncar_x
        # dy=leng_y/ncar_y
        # x = np.linspace(-leng_x/2, leng_x/2, ncar_x)
        # y = np.linspace(-leng_y/2, leng_y/2, ncar_y)
        # unit_xy='$\mu$m'
        # x_label='x ['+unit_xy+']'
        # y_label='y ['+unit_xy+']'
        # x_title='X projection'
        # y_title='Y projection'
        # xy_title='Intensity'
        # x_y_color='blue'
    
    # if freq_domain:
        # print('      calculating spectrum')
        # calc_time=time.time()
        # dfl=np.fft.ifftshift(np.fft.fft(dfl,axis=0),0)/sqrt(ncar_z) # sqrt(ncar_x*ncar_y) because of numpy fft function
        # dk=2*pi/leng_z;
        # k=2*pi/g('xlamds');
        # z = 2*pi/np.linspace(k-dk/2*ncar_z, k+dk/2*ncar_z, ncar_z)
        # suffix+='_fd'
        # z*=1e3
        # unit_z='nm'
        # z_label='$\lambda$ ['+unit_z+']'
        # z_labelv=r'[arb. units]'
        # z_title='Spectrum'
        # z_color='red'
        # print('        done in %.2f seconds' %(time.time()-calc_time))
    # else:
        # unit_z='$\mu$m'
        # z_label='z ['+unit_z+']'
        # z_labelv=r'Power [W]'
        # z_title='Z projection'
        # z_color='blue'
        
    # dx*=1e6
    # dy*=1e6
    # x*=1e6
    # y*=1e6
    # z*=1e6
    # leng_x*=1e6
    # leng_y*=1e6
    # leng_z*=1e6
    
    # if fig_name is None:
        # if g.filename is '':
            # fig = plt.figure('Radiation distribution')
        # else:
            # fig = plt.figure('Radiation distribution'+suffix+' '+g.filename)
    # else:
        # fig = plt.figure(fig_name)
    # fig.clf()
    # fig.set_size_inches(((3+2*column_3d)*figsize,3*figsize),forward=True)
    # # plt.rc('axes', grid=True)
    # # plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
    
    # cmap_int = plt.get_cmap('jet')#jet inferno viridis #change to convenient
    # cmap_ph = plt.get_cmap('hsv')
    
    # #calculate transverse projection, remove z dimention
    
    # dfl_int=abs(dfl)**2
    # xy_proj_ampl=sqrt((dfl_int).sum(0))*exp(1j*angle(dfl.sum(0))) #(amplitude-like) view from front, sum of square of amplitudes with phase as sum of phasors (latter is dedicated for illustration purposes: good to see an averaged wavefront)
    # # xy_proj_ampl=sum(dfl,0); #view from front
    # yz_proj=sum(dfl_int,1); #intensity view from side
    # xz_proj=sum(dfl_int,2); #intensity view from top
    # z_proj=sum(dfl_int,(1,2)); #temporal intensity profile
    # del dfl_int, dfl

    
    # # x_line=xy_proj_ampl[]
    # # y_line=xy_proj_ampl[]
    
    # xy_proj=abs(xy_proj_ampl)**2
    # xy_proj_ph=angle(xy_proj_ampl)
    
    # x_proj=sum(xy_proj,1)
    # y_proj=sum(xy_proj,0)
    
    # x_line=xy_proj[:,int((ncar_y-1)/2)]
    # y_line=xy_proj[int((ncar_x-1)/2),:]
    
    # if max(x_line)!=0 and max(y_line)!=0:
        # x_line,y_line=x_line/max(x_line),y_line/max(y_line)
    
    
    
    # #X=sqrt(sum(abs(X).^2,3)).*exp(1i.*angle(mean(X,3))); #%Matlab 2D field calculation
    # # normI = BoundaryNorm(levelsI, ncolors=cmapI.N, clip=True)
    # # normP = BoundaryNorm(levelsP, ncolors=cmapP.N, clip=True)
    
    
    
    
    
    
    # ax_int=fig.add_subplot(2, 2+column_3d, 1)
    # # ax_int.pcolormesh(x, y, xy_proj, cmap=cmap_int)
    # intplt=ax_int.pcolormesh(x, y, swapaxes(xy_proj,1,0), cmap=cmap_int)
    # ax_int.set_title(xy_title, fontsize=15)
    # # ax_int.axes.get_xaxis().set_visible(False)
    # ax_int.set_xlabel(r''+x_label)
    # ax_int.set_ylabel(y_label)
    
    # if phase==True:
        # ax_ph=fig.add_subplot(2, 2+column_3d, 4+column_3d, sharex=ax_int,sharey=ax_int)
        # # ax_ph.pcolormesh(x, y, xy_proj_ph, cmap=cmap_ph)
        # ax_ph.pcolormesh(x, y, swapaxes(xy_proj_ph,1,0), cmap=cmap_ph)
        # #ax_ph.axis('equal')
        # ax_ph.axis([min(x),max(x),min(y),max(y)])
        # ax_ph.set_title('Phase', fontsize=15)
        # # ax_ph.set_xlabel(r'[$\mu m$]')
        # # ax_ph.set_ylabel(r'[$\mu m$]')
    # else:
        # ax_z=fig.add_subplot(2, 2+column_3d, 4+column_3d)
        # ax_z.plot(z,z_proj,linewidth=1.5,color=z_color)
        # ax_z.set_title(z_title, fontsize=15)
        # ax_z.set_xlabel(z_label)
        # ax_z.set_ylabel(z_labelv)
    
    # ax_proj_x=fig.add_subplot(2, 2+column_3d, 3+column_3d, sharex=ax_int)
    # ax_proj_x.plot(x,x_line,linewidth=2,color=x_y_color)
    # ax_proj_x.set_title(x_title, fontsize=15)
    # x_line_f, rms_x=gauss_fit(x,x_line) #fit with Gaussian, and return fitted function and rms
    # fwhm_x=fwhm3(x_line)[1]*dx #measure FWHM
    # ax_proj_x.plot(x,x_line_f,'g-')
    # ax_proj_x.text(0.95, 0.95,'fwhm= \n'+str(round_sig(fwhm_x,3))+r' ['+unit_xy+']\nrms= \n'+str(round_sig(rms_x,3))+r' ['+unit_xy+']', horizontalalignment='right', verticalalignment='top', transform = ax_proj_x.transAxes,fontsize=12)
    # ax_proj_x.set_ylim(ymin=0,ymax=1)

    
    
    # ax_proj_y=fig.add_subplot(2, 2+column_3d, 2, sharey=ax_int)
    # ax_proj_y.plot(y_line,y,linewidth=2,color=x_y_color)
    # ax_proj_y.set_title(y_title, fontsize=15)
    # y_line_f, rms_y=gauss_fit(y,y_line)
    # fwhm_y=fwhm3(y_line)[1]*dy
    # ax_proj_y.plot(y_line_f,y,'g-')
    # ax_proj_y.text(0.95, 0.95,'fwhm= '+str(round_sig(fwhm_y,3))+r' ['+unit_xy+']\nrms= '+str(round_sig(rms_y,3))+r' ['+unit_xy+']', horizontalalignment='right', verticalalignment='top', transform = ax_proj_y.transAxes,fontsize=12)
    # ax_proj_y.set_xlim(xmin=0,xmax=1)


    
    # if column_3d:
        # if phase==True:
            # ax_proj_xz=fig.add_subplot(2, 2+column_3d, 6)
        # else:
            # ax_proj_xz=fig.add_subplot(2, 2+column_3d, 6,sharex=ax_z)
        # ax_proj_xz.pcolormesh(z, x, swapaxes(xz_proj,1,0), cmap=cmap_int)
        # ax_proj_xz.set_title('Top view', fontsize=15)

        # # 
        # ax_proj_xz.set_xlabel(z_label)
        # ax_proj_yz=fig.add_subplot(2, 2+column_3d, 3,sharey=ax_int,sharex=ax_proj_xz)
        # ax_proj_yz.pcolormesh(z, y, swapaxes(yz_proj,1,0), cmap=cmap_int)
        # ax_proj_yz.set_title('Side view', fontsize=15)

        # # 
        
        
        
    # cbar=0
    # if cbar:
        # fig.subplots_adjust(top=0.95, bottom=0.05, right=0.85, left=0.1)
        # #fig.subplots_adjust()
        # cbar_int = fig.add_axes([0.89, 0.15, 0.015, 0.7])
        # cbar=plt.colorbar(intplt, cax=cbar_int)# pad = -0.05 ,fraction=0.01)
        # # cbar.set_label(r'[$ph/cm^2$]',size=10)
        # cbar.set_label(r'a.u.',size=10)

    # # ax_int.get_yaxis().get_major_formatter().set_useOffset(False)
    # # ax_int.get_yaxis().get_major_formatter().set_scientific(True)
    # # ax_ph.get_yaxis().get_major_formatter().set_useOffset(False)
    # # ax_ph.get_yaxis().get_major_formatter().set_scientific(True)


    # if auto_zoom!=False:
        # if phase and column_3d == True:
            # ax_proj_xz.set_xlim(z[nonzero(z_proj>max(z_proj)*0.01)][[0,-1]])
        # elif phase == False:
            # ax_z.set_xlim(z[nonzero(z_proj>max(z_proj)*0.01)][[0,-1]])
        # size_x=max(abs(x[nonzero(x_line>0.01)][[0,-1]]))
        # size_y=max(abs(x[nonzero(x_line>0.01)][[0,-1]]))
        # size_xy=max(size_x,size_y)
        # ax_int.axis('equal')
        # ax_int.axis([-size_xy, size_xy,-size_xy, size_xy])
        # ax_proj_xz.set_ylim([-size_xy, size_xy])
        # #ax_int.set_ylim(int(ncar_y/2-ind)*dy, int(ncar_y/2+ind)*dy)
        # #ax_proj_x.set_xlim(xmin=x[nonzero(x_line>0.01)][0],xmax=x[nonzero(x_line>0.01)][-1])
    # else:
        # ax_proj_xz.axis('tight')
        # ax_proj_yz.axis('tight')
        # ax_int.set_aspect('equal')
        # ax_int.autoscale(tight=True)
        
    # subplots_adjust(wspace=0.4,hspace=0.4)
    

    # if save!=False:
        # if save==True:
            # save='png'
        # fig.savefig(g.path+'_dfl'+suffix+'.'+str(save),format=save)
       
    # print('      done in %.2f seconds' % (time.time() - start_time))
       
    # if return_proj:
        # return [xy_proj,yz_proj,xz_proj,x,y,z]
    # else:
        # return fig
    


def round_sig(x, sig=2):
    from math import log10, floor
    return round(x, sig-int(floor(log10(x)))-1)
    
    
def gauss_fit(X,Y):
    import numpy as np
    import scipy.optimize as opt
    
    def gauss(x, p): # p[0]==mean, p[1]==stdev p[2]==peak
        return p[2]/(p[1]*np.sqrt(2*np.pi))*np.exp(-(x-p[0])**2/(2*p[1]**2))
        
    p0 = [0,max(X)/2,max(Y)]
    errfunc = lambda p, x, y: gauss(x, p) - y
    p1, success = opt.leastsq(errfunc, p0[:], args=(X, Y))
    fit_mu,fit_stdev,ampl = p1
    Y1=gauss(X,p1)
    RMS = fit_stdev
    return (Y1, RMS)

def fwhm3(valuelist, height=0.5, peakpos=-1):
    """calculates the full width at half maximum (fwhm) of some curve.
    the function will return the fwhm with sub-pixel interpolation. It will start at the maximum position and 'walk' left and right until it approaches the half values.
    INPUT: 
    - valuelist: e.g. the list containing the temporal shape of a pulse 
    OPTIONAL INPUT: 
    -peakpos: position of the peak to examine (list index)
    the global maximum will be used if omitted.
    OUTPUT:
    -fwhm (value)
    """
    if peakpos== -1: #no peakpos given -> take maximum
        peak = np.max(valuelist)
        peakpos = np.min( np.nonzero( valuelist==peak  )  )

    peakvalue = valuelist[peakpos]
    phalf = peakvalue * height

    # go left and right, starting from peakpos
    ind1 = peakpos
    ind2 = peakpos   

    while ind1>2 and valuelist[ind1]>phalf:
        ind1=ind1-1
    while ind2<len(valuelist)-1 and valuelist[ind2]>phalf:
        ind2=ind2+1  
    #ind1 and 2 are now just below phalf
    grad1 = valuelist[ind1+1]-valuelist[ind1]
    grad2 = valuelist[ind2]-valuelist[ind2-1]
    #calculate the linear interpolations
    p1interp= ind1 + (phalf -valuelist[ind1])/grad1
    p2interp= ind2 + (phalf -valuelist[ind2])/grad2
    #calculate the width
    width = p2interp-p1interp
    return (peakpos,width,np.array([ind1,ind2]))
