# PROMOTE_VBS_scenarios

Scenario configuration files and configuration scripts for PROMOTE.

## Processing Scripts
### Volatility Space Creation

```design_vbs_dist.py``` This is the script for constructing the emitted VBS distributions, using the "pseudo-age" parameter, and for creating the vbs "pseudo-age" parameter input file.

### Scenario_Input_Creation

```scenario_creation.py``` The script for creating the scenario chemistry files, this requires the gaussian parameter input file, as well as the vbs "pseudo-age" parameter input file. This script is designed to be run from the command line, providing the names of the input files as parameters (see script help for more details: ```python scenario_creation.py -h```).

## Scenario Configurations
### Config_Inputs
Contains the ```vbs_age_data.csv``` input file, created using the ```design_vbs_dist.py``` script.

### scenario_chemistry_files
Contains the training and validation chemistry configuration files, created using the ```scenario_creation.py``` script.

### example_chemistry_files
Example chemical configuration files. These define (for anthropogenic and biomass burning emissions, respectively):
 * VBS volatility distribution: over 9 volatility bins, as a fraction of the original OM emissions)
 * VBS emission scaling factor: can be used to ensure that the emitted condensed mass is close to that of the original OM emissions, or set to 1.0
 * VBS reaction rate
 * VBS oxidation fraction: the increase (as a fraction of the non-oxygen mass) in oxygen mass at each reaction step

### example_date_files
Example time period configuration files. These define:
 * start and end dates
 * anthropogenic emission file to use (by month / year)
 * flag to determine if the simulation is started fresh, or if a restart file from a previous simulation should be used
