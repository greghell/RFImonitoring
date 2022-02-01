## plots weather at various candidate sites

import numpy as np
import datetime
import json
import glob
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

site = 'RV';
allfiles = glob.glob('/home/user/T3_detect/satellite/weatherdsa2000/*'+site+'*');
nfiles = len(allfiles);
datarray = np.zeros((nfiles));
weatharray = np.zeros((5,nfiles));


for k in range(nfiles):
    f = open(allfiles[k]);
    data = json.load(f);
    datarray[k] = mdates.date2num(datetime.datetime.strptime(allfiles[k].split('/')[-1][:-(1+len(site))],'%Y-%m-%d_%H:%M:%S'));
    weatharray[0,k] = data['main']['temp'];
    weatharray[1,k] = data['main']['humidity'];
    weatharray[2,k] = data['wind']['speed'];
    weatharray[3,k] = data['wind']['gust'];
    try:weatharray[4,k] = data['snow']['1h'];
    except:weatharray[4,k] = 0;
    f.close();

arso = np.argsort(datarray);

plt.figure();
plt.subplot(5,1,1);
plt.plot_date(datarray[arso], weatharray[0,arso],'-');
plt.grid();
plt.ylabel('temperature [C]');
plt.subplot(5,1,2);
plt.plot_date(datarray[arso], weatharray[1,arso],'-');
plt.grid();
plt.ylabel('humidity [%]');
plt.subplot(5,1,3);
plt.plot_date(datarray[arso], weatharray[2,arso],'-');
plt.grid();
plt.ylabel('wind speed [m/s]');
plt.subplot(5,1,4);
plt.plot_date(datarray[arso], weatharray[3,arso],'-');
plt.grid();
plt.ylabel('wind gust [m/s]');
plt.subplot(5,1,5);
plt.plot_date(datarray[arso], weatharray[4,arso],'-');
plt.grid();
plt.ylabel('snow [mm]');
plt.xlabel('date');
plt.suptitle('Railroad Valley');
plt.tight_layout();
plt.show();


