
import numpy
import matplotlib.pyplot as plt
from wlmap import WLMap

arcmin2rad = (1.0/60.0)*numpy.pi/180.0
rad2arcmin = 1.0/arcmin2rad
deg2rad = numpy.pi/180.0
rad2deg = 1.0/deg2rad

vb = False

# ============================================================================

class Shearmap(WLMap):
    """
    NAME
        Shearmap

    PURPOSE
        Read in, store, transform and interrogate a shear map.

    COMMENTS
        A "physical" coordinate system is used, where x = -RA (rad) 
        and y = Dec (rad). This is the system favoured by Hilbert et al.

    INITIALISATION
        shearfile      List of files containing a shear map
        FITS           Data file format (def=True)
            
    METHODS
        plot(self,fig_size=10,subplot=None): Plots either the whole image or a 
                                             given sub-image in physical
                                             coordinates

    BUGS

    AUTHORS
      This file is part of the Pangloss project, distributed under the
      GPL v2, by Tom Collett (IoA) and  Phil Marshall (Oxford). 
      Please cite: Collett et al 2013, http://arxiv.org/abs/1303.6564

    HISTORY
      2015-06-25  Everett (SLAC)
    """

# ----------------------------------------------------------------------------

    def __init__(self,shearfile,FITS=True):

        self.name = 'Shear map kappa from Millenium Simulation, zs = 1.6'
        # Calls the WLMap superclass
        WLMap.__init__(self,shearfile,FITS)

# ----------------------------------------------------------------------------

    def __str__(self):
        ## Add more information!!
        return 'Shear map'

# ----------------------------------------------------------------------------
# Plot the convergence as grayscale:
    
    def plot(self,fig_size=10,subplot=None,coords='pixel'): # fig_size in inches

        gamma1 = self.values[0]
        gamma2 = self.values[1]
        
        # Pixel sampling rate for plotting of shear maps
        N = 100
        
        # Set limits and number of points in grid
        X,Y = numpy.meshgrid(numpy.arange(0,self.NX[0]),numpy.arange(0,self.NX[0]))
        X = X[::N,::N]
        Y = Y[::N,::N]
        
        # Calculate the modulus and angle of each shear
        mod_gamma = numpy.sqrt(numpy.square(gamma1)+numpy.square(gamma2))
        phi_gamma = numpy.arctan(numpy.divide(gamma2,gamma1))/2.0
        
        # Create the vector components of the shear sticks
        stick1 = numpy.multiply(mod_gamma,numpy.cos(phi_gamma))
        stick2 = numpy.multiply(mod_gamma,numpy.sin(phi_gamma))
        
        # Plot image
        plt.quiver(X,Y,stick1[::N,::N],stick2[::N,::N],color='r',headwidth=0,pivot='middle')        
        #plt.imshow(self.values[0],cmap = 'gray_r',origin = 'lower')
        #plt.imshow(self.values[1],cmap = 'gray_r',origin = 'lower')
        plt.title('Shear map of '+self.input[0])
        
        fig = plt.gcf()
        fig.set_size_inches(fig_size,fig_size)

        '''
        Old plot for kappamap.py:
        
        # Default subplot is entire image
        if subplot is None:
            subplot = [0,self.NX[0],0,self.NX[0]]
            
        xi, xf = subplot[0], subplot[1]    # x-limits for subplot
        yi, yf = subplot[2], subplot[3]    # y-limits for subplot
        Lx = xf-xi    # length of x-axis subplot
        Ly = yf-yi    # length of y-axis subplot
        # Number of axis ticks
        if Lx/Ly < 0.6:
            N = 5
        else:
            N = 8
        
        # N-sampled axis values
        xl = numpy.arange(xi,xf+Lx/N*numpy.sign(xf),Lx/N)
        yl = numpy.arange(yi,yf+Ly/N*numpy.sign(yf),Ly/N)
        
        if coords == 'pixel':        
            # Convert axes to physical coordinates, scale correctly with subplot
            xlNew = []; ylNew = [];
        
            for x in xl:
                xN,yN = self.image2physical(x,0)
                xlNew.append(xN)
            for y in yl:
                xN,yN = self.image2physical(0,y)
                ylNew.append(yN)
        
            # Format coordinates
            xlabels = ['%.3f' % a for a in xlNew]
            ylabels = ['%.3f' % a for a in ylNew]
        
        elif coords == 'physical':
            # Label values are already in physical coordinates
            xlabels = ['%.3f' % a for a in xl]
            ylabels = ['%.3f' % a for a in yl]
            
            # Convert subplot bounds to pixel values
            xi,yi = self.physical2image(xi,yi)
            xf,yf = self.physical2image(xf,yf)
            Lx = xf-xi
            Ly = yf-yi
        
        else:
            raise IOError('Error: Subplot bounds can only be in pixel or physical coordinates.')
        
        # Location of tick marks
        xlocs = numpy.arange(0,Lx,Lx/N)
        ylocs = numpy.arange(0,Ly,Ly/N)
        
        # Plot image        
        plt.imshow(self.values[0][yi:yf,xi:xf],cmap = 'gray_r',origin = 'lower')
        plt.title('Convergence map of '+self.input[0])
        
        # Label axes
        plt.xticks(xlocs,xlabels)
        plt.yticks(ylocs,ylabels)
        plt.xlabel('Physical Coordinate (rad)')
        plt.ylabel('Physical Coordinate (rad)')

        fig = plt.gcf()
        fig.set_size_inches(fig_size,fig_size)
        '''
        return None
        