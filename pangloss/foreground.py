import numpy as np
import matplotlib.pyplot as plt
import os
from astropy.table import Table, Column

import pangloss

# ============================================================================

class ForegroundCatalog(pangloss.Catalog):
    """
    NAME
        ForegroundCatalog

    PURPOSE
        Store, interrogate and plot a collection of foreground galaxy
        data for a given patch of skys.

    COMMENTS
        Inherits from the base class Catalog in catalog.py

    INITIALISATION
        filename:       A string of the catalog filename (likely .txt)
        config:         A config object containing structure of catalog metadata

    METHODS
        findGalaxies: Find all galaxies in the catalog that are within the inputted
                      magnitude, mass, redhsift, and coordinate cutoff ranges,
                      and then return the locations and masses of each galaxy.

        returnGalaxies: Same as the findGalaxies() method, but returns all columns
                        of the catalog for galaxies that satisfy the cutoffs.

        plotForeground: Make a scatterplot of foreground galaxy positions at their
                        respective world coordinates. Only galaxies in the catalog
                        whose attributes are within the optional magnitude, mass,
                        redshift, and coordiante cutoff arguments are displayed.

    BUGS


    AUTHORS
      This file is part of the Pangloss project, distributed under the
      GPL v2, by Tom Collett (IoA) and  Phil Marshall (Oxford).
      Please cite: Collett et al 2013, http://arxiv.org/abs/1303.6564

    HISTORY
      2015-07-2  Started Everett (SLAC)
    """

    def __init__(self,filename,config):
        # Calls the superclass init
        pangloss.Catalog.__init__(self,filename,config)

        # Parsing the file name
        # 0 <= x,y <= 7, each (i,j) map covers 4x4 square degrees
        input_parse = self.filename.split('_') # Creates list of filename elements separated by '_'
        self.map_x = eval(input_parse[3]) # The x location of the map grid
        self.map_y = eval(input_parse[4]) # The y location of the map grid

        # 0 <= i,j <= 3, each (i,j) field covers 1x1 square degree
        self.field_i = eval(input_parse[5]) # The i location of the field grid in the (x,y) map
        self.field_j = eval(input_parse[6]) # The j location of the field grid in the (x,y) map

        # Catalog attributes
        self.galaxyCount = np.shape(self.data)[0]
        self.maxZ = max(self.data['z_obs'])
        self.minZ = min(self.data['z_obs'])
        self.maxM = max(self.data['Mstar_obs'])
        self.minM = min(self.data['Mstar_obs'])
        self.maxMag = max(self.data['mag'])
        self.minMag = min(self.data['mag'])

        # Find world coordinate limits, used for plotting
        self.ra_max = np.rad2deg((-self.data['nRA']).max())
        self.ra_min = np.rad2deg((-self.data['nRA']).min())
        self.dec_max = np.rad2deg(self.data['Dec'].max())
        self.dec_min = np.rad2deg(self.data['Dec'].min())

        return

    def __str(self):
        # Add more!
        return 'Foreground catalog with {} galaxies, '+ \
               'with redshifts ranging from {} to {}'\
                .format(self.galaxyCount,self.minZ,self.maxZ)


    def findGalaxies(self,mag_cutoff=[0,24],mass_cutoff=[0,10**20],z_cutoff=[0,1.3857],ra_cutoff=None,dec_cutoff=None):
        '''
        Retrieve list of galaxy world coordinates and their masses with values within inputted cutoffs.
        '''

        # If no ra or dec cutoff are given, use all galaxies
        if ra_cutoff == None: ra_cutoff = [self.ra_max, self.ra_min] # RA flipped because RA is left-handed
        if dec_cutoff == None: dec_cutoff = [self.dec_min, self.dec_max]

        # Convert world coordinate limits to radians
        ra_cutoff, dec_cutoff = np.deg2rad(ra_cutoff), np.deg2rad(dec_cutoff)


        # Select only the ra, dec, and mass values from galaxies that satisfy all cutoffs
        ra = -np.rad2deg(self.data['nRA'][(self.data['mag']>mag_cutoff[0]) & (self.data['mag']<mag_cutoff[1]) \
                                        & (self.data['Mstar_obs']>mass_cutoff[0]) & (self.data['Mstar_obs']<mass_cutoff[1]) \
                                        & (self.data['z_obs']>mag_cutoff[0]) & (self.data['z_obs']<mag_cutoff[1]) \
                                        & (-self.data['nRA']>ra_cutoff[1]) & (-self.data['nRA']<ra_cutoff[0]) \
                                        & (self.data['Dec']>dec_cutoff[0]) & (self.data['Dec']<dec_cutoff[1])])

        dec = np.rad2deg(self.data['Dec'][(self.data['mag']>mag_cutoff[0]) & (self.data['mag']<mag_cutoff[1]) \
                                        & (self.data['Mstar_obs']>mass_cutoff[0]) & (self.data['Mstar_obs']<mass_cutoff[1]) \
                                        & (self.data['z_obs']>mag_cutoff[0]) & (self.data['z_obs']<mag_cutoff[1]) \
                                        & (-self.data['nRA']>ra_cutoff[1]) & (-self.data['nRA']<ra_cutoff[0]) \
                                        & (self.data['Dec']>dec_cutoff[0]) & (self.data['Dec']<dec_cutoff[1])])

        mass = self.data['Mstar_obs'][(self.data['mag']>mag_cutoff[0]) & (self.data['mag']<mag_cutoff[1]) \
                                        & (self.data['Mstar_obs']>mass_cutoff[0]) & (self.data['Mstar_obs']<mass_cutoff[1]) \
                                        & (self.data['z_obs']>mag_cutoff[0]) & (self.data['z_obs']<mag_cutoff[1]) \
                                        & (-self.data['nRA']>ra_cutoff[1]) & (-self.data['nRA']<ra_cutoff[0]) \
                                        & (self.data['Dec']>dec_cutoff[0]) & (self.data['Dec']<dec_cutoff[1])]

        return ra, dec, mass


    def returnGalaxies(self,mag_cutoff=[0,24],mass_cutoff=[0,10**20],z_cutoff=[0,1.3857],ra_cutoff=None,dec_cutoff=None):
        '''
        Return catalog of galaxies that satisfy the inputted cutoffs.
        '''

        # If no ra or dec cutoff are given, use all galaxies
        if ra_cutoff == None: ra_cutoff = [self.ra_max, self.ra_min] # RA flipped because RA is left-handed
        if dec_cutoff == None: dec_cutoff = [self.dec_min, self.dec_max]

        # Convert world coordinate limits to radians
        ra_cutoff, dec_cutoff = np.deg2rad(ra_cutoff), np.deg2rad(dec_cutoff)

        # Select only galaxies that meet the cutoff criteria
        galaxies = self.data[(self.data['mag']>mag_cutoff[0]) & (self.data['mag']<mag_cutoff[1]) \
                                        & (self.data['Mstar_obs']>mass_cutoff[0]) & (self.data['Mstar_obs']<mass_cutoff[1]) \
                                        & (self.data['z_obs']>mag_cutoff[0]) & (self.data['z_obs']<mag_cutoff[1]) \
                                        & (-self.data['nRA']>ra_cutoff[1]) & (-self.data['nRA']<ra_cutoff[0]) \
                                        & (self.data['Dec']>dec_cutoff[0]) & (self.data['Dec']<dec_cutoff[1])]

        return galaxies

    def plot(self,subplot=None,mag_cutoff=[0,24],mass_cutoff=[0,10**20],z_cutoff=[0,1.3857],fig_size=10):
        '''
        Plots the positions of galaxies in the foreground catalog in world coordinates.
        The optional input fig_size is in inches and has a default value of 10.
        The other optional inputs are cutoffs with default values, which limit
        the number of galaxies that are to be plotted by the respective attribute.
        '''

        # Get current figure and image axes (or make them if they don't exist)
        fig = plt.gcf()
        if fig._label == 'Convergence':
            image = fig.axes[0]
            world = fig.axes[1]

        else:
            image, world = pangloss.make_axes(fig)

        if subplot is None:
            # Default subplot is entire image
            ai, di = self.ra_max, self.dec_min
            af, df = self.ra_min, self.dec_max
            subplot = [ai,af,di,df]

        ai, af = subplot[0], subplot[1]    # RA limits for subplot
        di, df = subplot[2], subplot[3]    # DEC limits for subplot

        # Find world coordinates and masses of galaxies that meet cutoff criteria
        ra_cutoff, dec_cutoff = [ai, af], [di, df]     # RA flipped because RA is left-handed
        ra, dec, mass = self.findGalaxies(mag_cutoff,mass_cutoff,z_cutoff,ra_cutoff,dec_cutoff)

        # Set current axis to world coordinates and set the limits
        fig.sca(world)
        world.set_xlim(subplot[0],subplot[1])
        world.set_ylim(subplot[2],subplot[3])

        # Scale galaxy plot size by its mass
        scale = ((np.log10(mass)-9.0)/(12.0-9.0))
        floor = 0.01
        size = 1000.0*(scale*(scale > 0) + floor)

        # Make a scatter plot of the galaxy locations
        plt.scatter(ra,dec,s=size,color='orange',alpha=0.2,edgecolor=None)
        plt.xlabel('Right Ascension / deg')
        plt.ylabel('Declination / deg')

        return
