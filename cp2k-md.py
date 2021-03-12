#!/usr/bin/env python
# coding: utf-8

# In[1]:


#---------------------------------------------
### Scott Midgley ###
### Scope: CP2K AIMD post processing
#---------------------------------------------


# In[2]:


import matplotlib.pyplot as plt
import numpy as np
import time
import os
import pandas as pd


# In[3]:


start_time = time.time()


# In[4]:


rundir = os.getcwd()


# In[5]:


### Specify input files
print('Specify CP2K files for analysis.  \n')
enerfilename = input('Enter the name of the CP2K energy file: ')
enerfile = open(enerfilename,'r').read().splitlines()
inpfilename = input('Enter the name of the CP2K input file: ')
inpfilename = open(inpfilename, 'r').read().splitlines()


# In[6]:


### MD potential energy
ener = []
for line in enerfile:
    split_line = line.split()
    if len(split_line) == 7:
        ener.append(float(split_line[4]))
ener_ev = []
for i in ener:
    ener_ev.append(i * 27.2114)
count_steps = float(len(ener_ev))


# In[7]:


### Convert list to Numpy array
ener_ev_arr = np.array(ener_ev)


# In[8]:


### Read number of completed MD steps
for line in inpfilename:
        if "TIMESTEP" in line:
                split_line = line.split()
                ts = (float(split_line[1]))

md_runtime = (float(ts) * float(count_steps))
print('\nTotal simulation length: ', md_runtime , 'fs')


# In[24]:


### Running averages
n = 0
n_increment = 1000
running_averages = []
dfra = pd.DataFrame()
while n < count_steps:
    ener_last = ener_ev[-int(n):]
    x =(sum(ener_last)/len(ener_last))
    running_averages.append('{:.10f}'.format(x))
    n += n_increment
print(running_averages)


# In[10]:


### Convert list to Numpy array
ra_arr = np.array(running_averages)


# In[11]:


### Build dataframe
energies_df = pd.DataFrame(columns=['MD'])
energies_df['MD_(eV)'] = ener_ev_arr
energies_df.loc[:,'Running_Average_(eV)'] = pd.Series(ra_arr)
energies_df['Running_Average_(eV)'] = energies_df['Running_Average_(eV)'].astype(float)
energies_df.head()


# In[12]:


### Choose whether to display and save rough plots
display = str(input('Do you want to display generated plots? [y/n]:  '))
save = str(input('Do you want to save plots? [y/n]:  '))


# In[13]:


### Plot MD energies
energies_df['MD_(eV)'].plot()
plt.xlabel("MD Step")
plt.ylabel("MD Energy (eV)")
plt.title("MD Energy")
if display == 'y':
    plt.show()
if save == 'y':
    plt.savefig('MD-Energy.pdf')


# In[14]:


### Commit running averages to DataFrame
df_ra = pd.DataFrame()
df_ra['Last n steps'] = list(range(1, int(md_runtime)+1 ,1000))
df_ra['Running_Average_(eV)'] = energies_df['Running_Average_(eV)']


# In[15]:


### Plot running averages
df_ra.plot.scatter(x='Last n steps', y='Running_Average_(eV)')
plt.xlabel('n = %i' %n_increment, fontsize=12)
plt.ylabel('Average MD energy over last n steps (eV)', fontsize=10)
if display == 'y':
    plt.show()
if save == 'y':
    plt.savefig('Running-averages.pdf')


# In[16]:


### Standard deviation analysis
print('Starting Standard Deviation Analysis')
time.sleep(3)


# In[17]:


### Prepare new dataframe with all MD energies
sd_df = pd.DataFrame()
sd_df['MD_(eV)'] = energies_df['MD_(eV)']
print('MD run time = ', md_runtime)
sd_df.head()


# In[18]:


### Ask user for bin size
bins = int(input('Enter bin size (please provide integer value):  '))
print('There will be', int(md_runtime/bins), 'bins in this dataset.')


# In[19]:


### Calculate standard deviation and mean for each bin
GO = 0
GO = GO + bins
STOP = 0
bin_std = []
bin_means = []
while GO < int(md_runtime):
    bin_cut = sd_df.iloc[int(STOP):int(GO)]
    bin_sd = bin_cut['MD_(eV)'].std()
    bin_mean = bin_cut['MD_(eV)'].mean()
    bin_std.append(bin_sd)
    bin_means.append(bin_mean)
    GO += int(bins)
    STOP += int(bins)
print(bin_std)    
print(bin_means)


# In[20]:


### Commit standard deviations and means to new DataFrame
df_bins = pd.DataFrame()
df_bins['SD, bin size: ', bins] = bin_std
df_bins['Mean energy, bin size: ', bins] = bin_means
df_bins.head()


# In[21]:


energies = pd.concat([energies_df,df_bins], axis=1)
energies.head()


# In[22]:


### Print to file
file = str(input('Do you want to save data to Excel file format? [y/n]:  '))
if file == 'y':
    print('Saving data to .xlsx.')
    energies.to_excel('energies.xlsx')
else:
    print('Saving data to tab separated file.')
    energies.to_csv('energies.tsv', sep='\t')


# In[23]:


### Print run time
print("\nPython 3 run time:", round((time.time() - start_time), 2) , "s")

