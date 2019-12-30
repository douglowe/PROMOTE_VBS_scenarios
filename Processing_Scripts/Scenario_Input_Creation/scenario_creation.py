#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 16:36:41 2019

Script for generating scenario configuration files for VBS gaussian space analysis.

Inputs required:
    1) gaussian scenario configuration file
    2) vbs "age" space configuration file


Outputs:
    Individual scenario configuration files containing the data:
        ### these are always 1.0
        BB_VBS_SCALE="1.0"
        AN_VBS_SCALE="1.0"
        ### these are passed direct from the scenario configuration
        BB_VBS_AGERATE="1.0e-13"
        AN_VBS_AGERATE="1.0e-13"
        BB_VBS_OXIDATE="0.075"
        AN_VBS_OXIDATE="0.075"

        ### these are calculated from the scenario and vbs "age" configurations
        BB_VBS_FRAC_1="0"
        BB_VBS_FRAC_2="0.12"
        BB_VBS_FRAC_3="0.24"
        BB_VBS_FRAC_4="0.24"
        BB_VBS_FRAC_5="0.21"
        BB_VBS_FRAC_6="0.13"
        BB_VBS_FRAC_7="0.04"
        BB_VBS_FRAC_8="0"
        BB_VBS_FRAC_9="0"

        AN_VBS_FRAC_1="0"
        AN_VBS_FRAC_2="0.12"
        AN_VBS_FRAC_3="0.24"
        AN_VBS_FRAC_4="0.24"
        AN_VBS_FRAC_5="0.21"
        AN_VBS_FRAC_6="0.13"
        AN_VBS_FRAC_7="0.04"
        AN_VBS_FRAC_8="0"
        AN_VBS_FRAC_9="0"



@author: mbessdl2
"""
#%%
#import appnope
#appnope.nope()

#%%

import pandas as pd
from collections import defaultdict
import sys, getopt, os

#%% file prototype text, plus writing subroutine

file_prototype = '''
# Chemical settings for scenario {SCENARIO}
#  Inputs:
#  ANTH_VBS_AGERATE     {ANTH_VBS_AGERATE}   
#  ANTH_SVOC_VOLDIST    {ANTH_SVOC_VOLDIST}
#  ANTH_SVOC_OXRATE     {ANTH_SVOC_OXRATE}
#  ANTH_IVOC_SC         {ANTH_IVOC_SC}
#  ANTH_SVOC_SC         {ANTH_SVOC_SC}
#  BB_VBS_AGERATE       {BB_VBS_AGERATE}
#  BB_SVOC_VOLDIST      {BB_SVOC_VOLDIST}
#  BB_SVOC_OXRATE       {BB_SVOC_OXRATE}
#  BB_IVOC_SC           {BB_IVOC_SC}   
#  BB_SVOC_SC           {BB_SVOC_SC}   


BB_VBS_SCALE="1.0"
AN_VBS_SCALE="1.0"
BB_VBS_AGERATE="{BB_VBS_AGERATE:12.6e}"
AN_VBS_AGERATE="{ANTH_VBS_AGERATE:12.6e}"
BB_VBS_OXIDATE="{BB_SVOC_OXRATE:12.6e}"
AN_VBS_OXIDATE="{ANTH_SVOC_OXRATE:12.6e}"

BB_VBS_FRAC_1="{BB_VBS_FR1:12.6e}"
BB_VBS_FRAC_2="{BB_VBS_FR2:12.6e}"
BB_VBS_FRAC_3="{BB_VBS_FR3:12.6e}"
BB_VBS_FRAC_4="{BB_VBS_FR4:12.6e}"
BB_VBS_FRAC_5="{BB_VBS_FR5:12.6e}"
BB_VBS_FRAC_6="{BB_VBS_FR6:12.6e}"
BB_VBS_FRAC_7="{BB_VBS_FR7:12.6e}"
BB_VBS_FRAC_8="{BB_VBS_FR8:12.6e}"
BB_VBS_FRAC_9="{BB_VBS_FR9:12.6e}"

AN_VBS_FRAC_1="{ANTH_VBS_FR1:12.6e}"
AN_VBS_FRAC_2="{ANTH_VBS_FR2:12.6e}"
AN_VBS_FRAC_3="{ANTH_VBS_FR3:12.6e}"
AN_VBS_FRAC_4="{ANTH_VBS_FR4:12.6e}"
AN_VBS_FRAC_5="{ANTH_VBS_FR5:12.6e}"
AN_VBS_FRAC_6="{ANTH_VBS_FR6:12.6e}"
AN_VBS_FRAC_7="{ANTH_VBS_FR7:12.6e}"
AN_VBS_FRAC_8="{ANTH_VBS_FR8:12.6e}"
AN_VBS_FRAC_9="{ANTH_VBS_FR9:12.6e}"
'''




def write_scenario_file(filepath,filename,var_dict):
    with open(filepath+filename,"w") as text_file:
        text_file.write(file_prototype.format_map(var_dict))
    

#%% scenario setup subroutines

def read_scenario_file(filepath):
    
    setup_list = pd.read_csv(filepath,sep=' ')
    
    return(setup_list)
    
    
def read_vbsage_file(filepath):
    
    vbsage_list = pd.read_csv(filepath,sep=',')

    vbsage_list = vbsage_list.set_index('Age')

    return(vbsage_list)

        
def create_scenario_setup(inputs,vbsage):
    
    copy_keys = ['SCENARIO',\
                 'BB_VBS_AGERATE','BB_SVOC_OXRATE',\
                 'ANTH_VBS_AGERATE','ANTH_SVOC_OXRATE']
    
    vdict = defaultdict()

    for ckey in copy_keys:
        vdict[ckey] = inputs[ckey]


    vdict.update(create_vbs_dist('BB',inputs,vbsage))
    vdict.update(create_vbs_dist('ANTH',inputs,vbsage))
    
    
    return(vdict)


def create_vbs_dist(vstring,inputs,vbsage):
    
    # create key list for specified VBS scheme (BB or ANTH)
    vbs_ids = ['Frac_1','Frac_2','Frac_3','Frac_4','Frac_5','Frac_6','Frac_7','Frac_8','Frac_9']
    vbs_dist_ids = [ii.replace('Frac_',vstring+'_VBS_FR') for ii in vbs_ids]
    
    # initialise the IVOC base values
    ivoc_base = {}
    ivoc_base['Frac_1']=0.0
    ivoc_base['Frac_2']=0.0
    ivoc_base['Frac_3']=0.0
    ivoc_base['Frac_4']=0.0
    ivoc_base['Frac_5']=0.0
    ivoc_base['Frac_6']=0.0
    ivoc_base['Frac_7']=0.2
    ivoc_base['Frac_8']=0.5
    ivoc_base['Frac_9']=0.8
    
    # get the VBS age index
    vbs_pos = vbsage.index.get_loc(inputs[vstring+'_SVOC_VOLDIST'],method='nearest')

    # pull out the scaling factors for this scheme
    ivoc_scale = inputs[vstring+'_IVOC_SC']
    svoc_scale = inputs[vstring+'_SVOC_SC']

    # populate the extra dictionary with fractional distribution    
    vdict_extra = {}    
    for pos in range(len(vbs_ids)):
        svoc_value = vbsage.iloc[vbs_pos][vbs_ids[pos]] * svoc_scale * vbsage.iloc[vbs_pos]['Scale']
        ivoc_value = ivoc_base[vbs_ids[pos]] * ivoc_scale
        vdict_extra[vbs_dist_ids[pos]] = svoc_value + ivoc_value
        
    return(vdict_extra)
    

def usage():

    usage_string = '''
    The usage options are:
        -h / --help: this message
        -s[] / --scenariofile=[]: (required) scenario input file
        -a[] / --vbsagefile=[]: (required) VBS "age" distribution input file
        -o[] / --outputdirectory=[]: location for output files
        
        Paths to files & directories can be relative or absolute. The
        input files (scenario and VBS "age") must be specified. If an
        output directory is not specified then the current working 
        directory will be used.
    '''
    
    print(usage_string)

#%%

if __name__ == '__main__':
    
    fullCmdArguments = sys.argv
    argumentList = fullCmdArguments[1:]
    long_opt  = ["help", "scenariofile=", "vbsagefile=", "outputdirectory="]
    short_opt = "hs:a:o:" 
    
    try:
        arguments, values = getopt.getopt(argumentList,short_opt,long_opt)
    except getopt.error as err:
        print("Error: "+str(err))
        usage()
        sys.exit(2)
    
    outdir = "./"  # default output directory
    
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-h", "--help"):
            usage()
            sys.exit()
        elif currentArgument in ("-s", "--scenariofile"):
            if os.path.exists(currentValue):
                scenfile = currentValue
            else:
                print("Error: scenario file doesn't exist:\n"+currentValue)
        elif currentArgument in ("-a", "--vbsagefile"):
            if os.path.exists(currentValue):
                vbsfile = currentValue
            else:
                print("Error: VBS age file doesn't exist:\n"+currentValue)
        elif currentArgument in ("-o", "--outputdirectory"):
            if os.path.exists(currentValue):
                outdir = currentValue
            else:
                print("Error: output directory doesn't exist:\n"+currentValue)
                
    try:
        scenfile
        vbsfile
    except:
        print("Please provide all required options - see information below.")
        usage()
        sys.exit(2)
    
    
    slist  = read_scenario_file(scenfile)
    vbsage = read_vbsage_file(vbsfile)
    
    for pos in slist.index:
        vdict = create_scenario_setup(slist.iloc[pos],vbsage)
        vdict.update(slist.iloc[pos])
        write_scenario_file(filepath=outdir,filename=vdict['SCENARIO']+'.txt',var_dict=vdict)

 
    
    