# PROMOTE_VBS_scenarios

Scenario configuration files and configuration scripts for PROMOTE.

## Processing Scripts
### Volatility Space Creation

```design_vbs_dist.py``` This is the script for constructing the emitted VBS distributions, using the "pseudo-age" parameter.

## Scenario Configurations
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
