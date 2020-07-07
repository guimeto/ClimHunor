# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 08:26:06 2020

@author: guillaume
"""

import xarray as xr
import warnings; warnings.filterwarnings(action='ignore')
from matplotlib import pyplot as plt

plt.rcParams['figure.figsize'] = (8,5)

unique_dataDIR1 = './RCMs/RCA4-v1_AFR-44_ECMWF-ERAINT_tasmin_ll_2010_06_M.nc4'
TASMIN = xr.open_dataset(unique_dataDIR1)

unique_dataDIR2 = './RCMs/RCA4-v1_AFR-44_ECMWF-ERAINT_pr_ll_2010_06_M.nc4'
PR = xr.open_dataset(unique_dataDIR2)