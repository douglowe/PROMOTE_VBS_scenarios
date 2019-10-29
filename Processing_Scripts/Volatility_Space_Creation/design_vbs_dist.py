# -*- coding: utf-8 -*-
"""
Short script for creating an example VBS distribution.

Start with all mass in the most volatile bin, and apply a dimensionless
aging rate to all compounds (except the least volatile, which we assume
cannot be aged anymore).

The distribution for each time step is stored as a row in the "vbs_store"
array - we calculate the index for each of these using the size of this
array.


Doug Lowe (27/11/2018)
"""

#%%
import appnope
appnope.nope()

#%%

import numpy as np
import matplotlib.pyplot as plt
import math
from numba import jit

#%% functions for partitioning the mass, and returning a scaling factor

@jit()
def partition_mass(mass_dist,volatility_dist):
    
    condensed_fraction = np.ones(shape=(1,9))
    
    condensed_mass_dist = mass_dist*condensed_fraction
    condensed_mass_total = np.sum(condensed_mass_dist)
    
    proc_counter = 0
    
    while True:
        new_condensed_fraction = 1.0/(1.0 + volatility_dist/condensed_mass_total )
        
        new_condensed_mass_dist = mass_dist*new_condensed_fraction
        new_condensed_mass_total = np.sum(new_condensed_mass_dist)
        
        proc_counter += 1
        
        #print("new mass dist is: ",new_condensed_mass_dist)
        #print("proc_counter is: ",proc_counter)
        
        if new_condensed_mass_total == condensed_mass_total:
            break
        elif np.sum(new_condensed_fraction) < 1e-100:
            condensed_fraction  = np.zeros(shape=(1,9))
            condensed_mass_dist = np.zeros(shape=(1,9))
            condensed_mass_total= 0.0
            break
        elif proc_counter > 999:
            break
        else:
            condensed_fraction   = new_condensed_fraction
            condensed_mass_dist  = new_condensed_mass_dist
            condensed_mass_total = new_condensed_mass_total 
    
    
    return condensed_mass_dist, condensed_fraction


@jit()
def scale_factor_calc(mass_dist_orig,volatility_dist):
    
    scale_factor = 1.0
    condensed_mass_target = np.sum(mass_dist_orig)
    
    proc_counter = 0
    
    while True:
    
        scaled_mass_dist = mass_dist_orig * scale_factor
        
        cond_mass_dist, cond_frac = partition_mass(scaled_mass_dist,volatility_dist)
        
        cond_mass  = np.sum(cond_mass_dist)
        
        proc_counter += 1
        
        #if cond_mass == condensed_mass_target:
        if math.isclose(cond_mass,condensed_mass_target,rel_tol=1e-03, abs_tol=0.0):
            break
        elif proc_counter > 999:
            print("hit count limit - exiting")
            print("cond mass = ", cond_mass)
            print("target    = ", condensed_mass_target)
            break
        else:
            scale_factor = scale_factor - (cond_mass - condensed_mass_target)/condensed_mass_target
        
    
    return (scale_factor, cond_frac)



#%% universal settings for our 9-bin VBS scheme

## initialise the reactant and product arrays
reactant_index = np.arange(1,9,1)
product_index = np.arange(0,8,1)

## initialise the volatility information (C*)
volatility = np.zeros(shape=(1,9))
volatility[0][0] = 1e-2
volatility[0][1] = 1e-1
volatility[0][2] = 1e0
volatility[0][3] = 1e1
volatility[0][4] = 1e2
volatility[0][5] = 1e3
volatility[0][6] = 1e4
volatility[0][7] = 1e5
volatility[0][8] = 1e6



#%% creating the evolution information for the VBS distribution


## initialise the mass array
vbs_mass = np.zeros(shape=(1,9))
vbs_mass[0][6] = 1.0
## initialise the storage array
vbs_store = np.copy(vbs_mass)

## initialise the ageing rate and counter information
age_rate = 0.01
age_counter = 0

## determine the initial partitioning of our vbs mass
return_values = scale_factor_calc(vbs_mass,volatility)
scale_fac = return_values[0]


condensed_fraction = np.zeros(shape=(1,9))

## looping through time, exit once we have aged almost everything
while True:
    vbs_aged_fraction = vbs_mass[0][reactant_index]*age_rate*(1.0-condensed_fraction[0][reactant_index])
    vbs_mass[0][reactant_index] -= vbs_aged_fraction
    vbs_mass[0][product_index] += vbs_aged_fraction
    age_counter += 1
    
    vbs_store = np.append(vbs_store,vbs_mass,axis=0)
    
    #scale_temp, condensed_fraction = scale_factor_calc(vbs_mass,volatility)
    return_values = scale_factor_calc(vbs_mass,volatility)
    scale_temp = return_values[0]
    condensed_fraction = return_values[1]
    
    scale_fac = np.append(scale_fac,scale_temp)
    
    
    if vbs_mass[0][0] > 0.9:
        break
    else:
        print("age is ",age_counter)
        print("VBS array is: ",vbs_mass)
        print("Scaling factor is: ",scale_temp)
        print("condensed fraction is:",condensed_fraction)
        
        
#%% create IVOC distribution
ivoc_mass = np.zeros(shape=(1,9))

ivoc_mass[0][6] = 0.2
ivoc_mass[0][7] = 0.5
ivoc_mass[0][8] = 0.8



#%% plotting function
        
def plot_section(ax,point):
    
     
    ax.bar(x_range,vbs_store[pos[point]][:])
    ax.bar(x_range,ivoc_mass[0][:],bottom=vbs_store[pos[point]][:]) # add the IVOC
    ax.set_ylim(0,0.9)    
    #ax.set_title(pos_temp[point])
    label_text = 'age = '+str(pos_temp[point])+', scale = '+str(round(scale_fac[pos[point]],3))
    ax.text(-2, 0.7, label_text, fontsize=12)


#%% function for finding the VBS fractional distribution for a given "age"
    
def vbs_frac_dist_at_age(age,vbs_array):
    
    position = age * vbs_array.shape[0]
    pos_int = np.int64(np.round(position))
    
    return(vbs_array[pos_int][:])


#%% function for prettifing the VBS fractional list

def vbs_list_pretty(vbs_list):
    
    pos = 1
    for val in vbs_list:    
        print('AN_VBS_FRAC%d="%6.4f"'%(pos,val))
        pos += 1

    pos = 1
    for val in vbs_list:    
        print('BB_VBS_FRAC%d="%6.4f"'%(pos,val))
        pos += 1



#%% example distributions for stuff
#
#  a: minimum mass
#  b: maximum mass
#  c: High O:C ratios
#

case_a = vbs_frac_dist_at_age(0.1,vbs_store)

case_b = ( vbs_frac_dist_at_age(0.1,vbs_store) + ivoc_mass[0][:] ) * 3.0

case_c = vbs_frac_dist_at_age(0.05,vbs_store) * 3.0



#%% plot distributions across the whole time frame

fig, axes = plt.subplots(6, 1, sharex='all', sharey='all')
fig.set_size_inches(5.5, 8.5)

#pos_temp = np.arange(0,0.9,0.1)

pos_temp = np.array([0.05,0.3,0.4,0.6,0.7,0.95])
pos_temp2 = pos_temp * vbs_store.shape[0]
pos = pos_temp2.astype('int64')

x_range = [-2,-1,0,1,2,3,4,5,6]

plot_section(axes[0],0)
plot_section(axes[1],1)
plot_section(axes[2],2)
plot_section(axes[3],3)
plot_section(axes[4],4)
plot_section(axes[5],5)

axes[3].set_ylabel('mass (dimensionless)')
axes[5].set_xlabel('log10(C*)')


fig.savefig("test1.pdf", bbox_inches='tight')


#%% plot distributions across a selected period of time

fig, axes = plt.subplots(6, 1, sharex='all', sharey='all')
fig.set_size_inches(5.5, 8.5)

#pos_temp = np.arange(0,0.9,0.1)

#pos_temp = np.array([0.2,0.3,0.4,0.5,0.6,0.7])
pos_temp = np.array([0.05,0.08,0.1,0.15,0.2,0.5])
pos_temp2 = pos_temp * vbs_store.shape[0]
pos = pos_temp2.astype('int64')

x_range = [-2,-1,0,1,2,3,4,5,6]

plot_section(axes[0],0)
plot_section(axes[1],1)
plot_section(axes[2],2)
plot_section(axes[3],3)
plot_section(axes[4],4)
plot_section(axes[5],5)

axes[3].set_ylabel('mass (dimensionless)')
axes[5].set_xlabel('log10(C*)')


fig.savefig("test2.pdf", bbox_inches='tight')
