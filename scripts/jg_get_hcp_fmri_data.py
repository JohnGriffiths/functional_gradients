
import os,sys,glob

cdb_dir = '/scratch/hpc3230/Data/connectomeDB/downloaded_HCP900'

#subs = ['100307']
subs = [s[:-1] for s in open('HCP_900.txt', 'r').readlines()][:300]


s3cmd_pfx = 's3cmd get s3://hcp-openaccess/HCP_900'

fnames = ['MNINonLinear/Results/tfMRI_WM_LR/tfMRI_WM_LR_Atlas_MSMAll.dtseries.nii',
          'MNINonLinear/Results/tfMRI_WM_RL/tfMRI_WM_RL_Atlas_MSMAll.dtseries.nii']

cwd = os.getcwd()

for sub in subs:

  for fname in fnames:

    outfile = '%s/%s/%s' %(cdb_dir,sub,fname)
    
    s3cmd = '%s/%s/%s' %(s3cmd_pfx,sub,fname)

    outdir = os.path.split(outfile)[0]
    if not os.path.isdir(outdir): os.makedirs(outdir)

    if not os.path.isfile(outfile):
      print 'downloading data for sub %s' %sub
      print '%s' %s3cmd
      os.chdir(outdir)
      os.system(s3cmd)


os.chdir(cwd)

