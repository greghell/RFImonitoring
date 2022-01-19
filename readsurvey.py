import matplotlib.pyplot as plt
import numpy as np

fname = 'C:\\Users\\gregh\\Desktop\\siglent_DSA_RFI_survey\\survey_220113162522_0.016666666666666666h.txt';
f = open(fname, "r")
tmp = f.readlines();
f.close();

numspec = len(tmp);
wf = np.zeros((numspec,750));
for k in range(numspec):
    wf[k,:] = list(map(float,tmp[k].split(',')[1:-1]));

plt.imshow(wf,aspect='auto');plt.show()
