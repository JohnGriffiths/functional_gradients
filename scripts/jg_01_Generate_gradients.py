
# coding: utf-8

# # Step 1 
# ## Create the low-dimensional embedding
# 
# In this notebook, we will create a low-dimensional representation from the dense connectome - a 91282x91282 connectivity matrix based on Human Connectome Project.
# 
# #### Warning: this process requires ~130 GB of RAM!

# In[6]:

# JG_ADD:
code_dir = '/home/hpc3230/Code/libraries_of_mine/github/functional_gradients' # JG_ADD
data_dir = '/scratch/hpc3230/Data/connectomeDB' # JG_ADD
import sys
sys.path.append(code_dir)
outfile = code_dir + '/data/rsFC_eigenvectors.dscalar.nii'

sys.path.append('/home/hpc3230/Code/libraries_of_others/github/mapalign')

import numpy as np



from fgrad import embed


# In[ ]:


#DC = '/Users/marcel/projects/HCP/dense_connectome/HCP_S900_820_rfMRI_MSMAll_groupPCA_d4500ROW_zcorr.dconn.nii'
DC = data_dir + '/HCP_S900_820_rfMRI_MSMAll_groupPCA_d4500ROW_zcorr.dconn.nii' # JG_MOD


# ### Preprocess the dense connectome

# In[7]:



# alternative if times out before finished: read from file
#DC_affinity = embed.preprocess_dense_connectome(DC)

print 're-loading affinity matrix'

DC_affinity = np.load(code_dir + '/data/aff.npy')


# ### Embed the dense connectome

# In[ ]:


print 'embedding affinity matrix'

embedding = embed.embed_dense_connectome(DC_affinity)


# ### Write the embedding to file

# In[ ]:


print 'saving embedding'

#save_embedding(embedding, "../data/rsFC_eigenvectors.dscalar.nii")
embed.save_embedding(embedding,outfile) # JG_MOD






