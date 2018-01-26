
# coding: utf-8

# # Step 2
# ## Match the gradients to working memory task time-series and predict task condition
# 
# In this step we take use the three non-trivial gradients with highest eigenvalues and match them to task time-series. This will allow us to re-express the task-related BOLD time-series as a time series of gradients. The steps are the following:
# 
# 1. Load single run of task time-series.
# 2. Normalize the task time-series to have mean = 0 and variance = 1 (z-score).
# 3. For each volume independently, compute coefficients of a linear regression model with gradients as predictors.
# 
# To reproduce the results, you need to provide your own copy of HCP working memory task data.  

# In[1]:


import glob
import h5py as h5
import time
import os

code_dir = '/home/hpc3230/Code/libraries_of_mine/github/functional_gradients' # JG_ADD
data_dir = '/scratch/hpc3230/Data/connectomeDB' # JG_ADD
import sys
sys.path.append(code_dir)


import nibabel as nib
import numpy as np
from fgrad.regress import regress_subject, trim_data


cdb_dir = '/scratch/hpc3230/Data/connectomeDB/downloaded_HCP900'


# In[2]:


gradients = nib.load('../data/rsFC_eigenvectors.dscalar.nii').get_data().T


# In[5]:

subjects = [s[:-1] for s in open('HCP_900.txt', 'r').readlines()][:300] # JG_MOD
#Subjects = sorted(glob.glob('/Users/marcel/projects/HCP/data/*'))

# JG_ADD: need to remove subs with missing files
subswithout_dat = ['116120', '126931', '129432', '129533', '131621', '143527',
                   '146634', '165032', '165840', '168038', '169040']
subjects = [s for s in subjects if s not in subswithout_dat]



n_sub = len(subjects)
n_runs = 2 # maximum number of runs per subject
n_grad = 10 # number of gradients to fit
n_tp = 405 # maximum number of time points in time series

ts_gradients = np.zeros([n_sub, n_runs, n_tp, n_grad])


# In[6]:


for j, s in enumerate(subjects):
    print("Subject %s, %d of %d" % (s, j+1, n_sub))  # JG_MOD
    #files = sorted(glob.glob('%s/MNINonLinear/Results/tfMRI_WM_*/tfMRI_*_Atlas_MSMAll.dtseries.nii' % s))

    files = sorted(glob.glob('%s/%s/MNINonLinear/Results/tfMRI_WM_*/tfMRI_*_Atlas_MSMAll.dtseries.nii' % (cdb_dir,s))) # JG_MOD
 

    print "Found %d runs" %len(files)
    if len(files) > 0:
        for i, f in enumerate(files):
            t = time.time()
            ts_gradients[j, i, :, :] = regress_subject(files[0], gradients[:,0:n_grad])
            print ("Run %d/%d took %.2f seconds" % (i+1, len(files), time.time() - t))
    else:
        print ("Found no runs for subject %s!" % s)

ts_gradients, r, subjects = trim_data(ts_gradients, subjects)


# In[9]:


if os.path.isfile('../data/reconstructed_WM.hdf5'):
    os.remove('../data/reconstructed_WM.hdf5')

f = h5.File('../data/reconstructed_WM.hdf5')
g = f.create_group('Working_memory')
g.create_dataset('LR', data = ts_gradients[:,0,:,:], compression = "gzip", chunks = (1,n_tp,n_grad))
g.create_dataset('RL', data = ts_gradients[:,1,:,:], compression = "gzip", chunks = (1,n_tp,n_grad))
g.create_dataset('Subjects', data = s)

f.close()

