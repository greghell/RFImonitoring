# -*- coding: utf-8 -*-
"""
quick look at data files for one given timestamp (as given in file name)
"""

import matplotlib.pyplot as plt
import numpy as np
import csv

tstamp = '220120142412'
fname1 = 'D:\\big_smoky_valley\\RFI1_survey_'+tstamp+'_1.0h.csv';
fname2 = 'D:\\big_smoky_valley\\RFI2_survey_'+tstamp+'_1.0h.csv';
fname3 = 'D:\\big_smoky_valley\\RFI3_survey_'+tstamp+'_1.0h.csv';

with open(fname1) as file_name:
    array1 = np.loadtxt(file_name, delimiter=",");
with open(fname2) as file_name:
    array2 = np.loadtxt(file_name, delimiter=",")
with open(fname3) as file_name:
    array3 = np.loadtxt(file_name, delimiter=",")

plt.figure();
plt.subplot(221);
plt.imshow(array1[:,:-1],aspect='auto');
plt.title('RFI#1');
plt.subplot(222);
plt.imshow(array2[:,:-1],aspect='auto');
plt.title('RFI#2');
plt.subplot(223);
plt.imshow(array3[:,:-1],aspect='auto');
plt.title('RFI#3');
plt.show();

plt.figure();
plt.subplot(221);
plt.plot(np.linspace(0.5,3.2,array1.shape[1]-1),np.mean(array1[:,:-1],axis=0));
plt.grid('on');
plt.title('RFI#1');
plt.subplot(222);
plt.plot(np.linspace(0.5,3.2,array1.shape[1]-1),np.mean(array2[:,:-1],axis=0));
plt.grid('on');
plt.title('RFI#2');
plt.subplot(223);
plt.plot(np.linspace(0.5,3.2,array1.shape[1]-1),np.mean(array3[:,:-1],axis=0));
plt.grid('on');
plt.title('RFI#3');
plt.show();


# plt.figure();
# plt.plot(np.linspace(0.5,3.2,array1.shape[1]-1),np.mean(array1[:27,:-1],axis=0))
# plt.plot(np.linspace(0.5,3.2,array1.shape[1]-1),np.mean(array1[40:40+27,:-1],axis=0))
# plt.plot(np.linspace(0.5,3.2,array1.shape[1]-1),np.mean(array1[110:110+27,:-1],axis=0))
# plt.show()
