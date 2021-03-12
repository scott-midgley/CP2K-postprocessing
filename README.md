# CP2K-postprocessing
Codes that may be useful for post processing and analysis of CP2K molecular dynamics simulation. 

This program reads CP2K .inp and .ener files. Molecular dyndamics energies are saved to either a .xlsx or .tsv file for further processing, and are plotted as a funtion of time. Running averages over increments of 1000 steps are also plotted as saved, as a tool for assessment of equilibration. The plotted datapoints represent the average energies over the last n steps of the MD simulation, in increments of 1000 steps.

The user will be prompted to enter a desired bin size, this is for the calculation of standard deviation. It is recommended that the user chose a large bin relative to the total number of MD steps, so that statistical anomalies are averages out in each bin. As a rough guide, a 40,000 step simulaiton should contain four bins, therefore the bin size should be set to 10,000. 
