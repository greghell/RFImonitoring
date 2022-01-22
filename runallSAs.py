# code to run after all SA are set and connected
# procedure:
# 1- connect USB hub to laptop
# 2- connect all SAs to hub
# 3- connect hard drive to hub
# 4- turn on SAs
# 5- launch program
#
#'USB0::0xF4EC::0x1305::SSA3PCDX5R0432::INSTR' : RFI#1
#'USB0::0xF4EC::0x1305::SSA3PCDX5R0431::INSTR' : RFI#2
#'USB0::0xF4EC::0x1305::SSA3PCDC5R0345::INSTR' : RFI#3


import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import time
from csv import writer
from datetime import datetime,timedelta


howlong = 1.;   # survey duration in hours
fRes = 100;     # frequency resolution in kHz
fStart = 400;   # start frequency in MHz
fStop = 3200;   # stop frequency in MHz

# toggle calibration or data (only impacts data file name)
mode = 'calib'; # calibration mode
#mode = 'data';  # data capture mode

BW = fStop - fStart;    # total bandwidth in MHz
obsBW = 751.*fRes/1000.;    # observed bandwidth (751 points per scan)
NumWin = int(np.ceil(BW/obsBW)); # number of windows
fStart = fStop - NumWin*obsBW;  # new start frequency given the number of analysis windows

# define the spectrum analyzers names
siglent1 = "USB0::0xF4EC::0x1305::SSA3PCDX5R0432::INSTR";
siglent2 = "USB0::0xF4EC::0x1305::SSA3PCDX5R0431::INSTR";
siglent3 = "USB0::0xF4EC::0x1305::SSA3PCDC5R0345::INSTR";

def run_monitor(howlong,fRes,fStart,fStop):

    rm = pyvisa.ResourceManager();

    # check which SA respond, ignore if they don't
    sa1on = True;sa2on = True;sa3on = True;
    sa1onerr = True;sa2onerr = True;sa3onerr = True;    # in case of SA error during the observation
    # open SA connections
    try:sa1 = rm.open_resource(siglent1);
    except:sa1on = False;
    try:sa2 = rm.open_resource(siglent2);
    except:sa2on = False;
    try:sa3 = rm.open_resource(siglent3);
    except:sa3on = False;
    
    # test write parameter in SA
    try:sa1.write(':BWIDth ' + str(fRes) + ' KHz');
    except:sa1on = False;
    try:sa2.write(':BWIDth ' + str(fRes) + ' KHz');
    except:sa2on = False;
    try:sa3.write(':BWIDth ' + str(fRes) + ' KHz');
    except:sa3on = False;

    # set up data file names
    rightnow = datetime.now();
    if mode == 'calib':
        if sa1on:fname1 = 'D:\\big_smoky_valley\\RFI1_CALIB_'+rightnow.strftime('%y%m%d%H%M%S')+'_'+str(howlong)+'h.csv';
        if sa2on:fname2 = 'D:\\big_smoky_valley\\RFI2_CALIB_'+rightnow.strftime('%y%m%d%H%M%S')+'_'+str(howlong)+'h.csv';
        if sa3on:fname3 = 'D:\\big_smoky_valley\\RFI3_CALIB_'+rightnow.strftime('%y%m%d%H%M%S')+'_'+str(howlong)+'h.csv';
    elif mode == 'data':
        if sa1on:fname1 = 'D:\\big_smoky_valley\\RFI1_DATA_'+rightnow.strftime('%y%m%d%H%M%S')+'_'+str(howlong)+'h.csv';
        if sa2on:fname2 = 'D:\\big_smoky_valley\\RFI2_DATA_'+rightnow.strftime('%y%m%d%H%M%S')+'_'+str(howlong)+'h.csv';
        if sa3on:fname3 = 'D:\\big_smoky_valley\\RFI3_DATA_'+rightnow.strftime('%y%m%d%H%M%S')+'_'+str(howlong)+'h.csv';
    
    # open data files
    if sa1on:f_object1 = open(fname1, 'a', newline='');
    if sa2on:f_object2 = open(fname2, 'a', newline='');
    if sa3on:f_object3 = open(fname3, 'a', newline='');

    try:
        
        print('starting survey at '+str(rightnow));
        print('writing to:');
        if sa1on:print(fname1);
        if sa2on:print(fname2);
        if sa3on:print(fname3);

        # write parameters
        if sa1on:sa1.write(':BWIDth:VIDeo:RATio 1');
        if sa2on:sa2.write(':BWIDth:VIDeo:RATio 1');
        if sa3on:sa3.write(':BWIDth:VIDeo:RATio 1');

        if sa1on:sa1.write(':POWer:GAIN ON');
        if sa2on:sa2.write(':POWer:GAIN ON');
        if sa3on:sa3.write(':POWer:GAIN ON');

        if sa1on:sa1.write(':POWer:ATTenuation 0');
        if sa2on:sa2.write(':POWer:ATTenuation 0');
        if sa3on:sa3.write(':POWer:ATTenuation 0');

        # create csv writer object
        if sa1on:writer_object1 = writer(f_object1);
        if sa2on:writer_object2 = writer(f_object2);
        if sa3on:writer_object3 = writer(f_object3);

        # start timer for duration of file
        rightnow = datetime.now();
        now = datetime.now();
        while now <= rightnow + timedelta(hours=howlong):
        # spectra np array + extra value for time stamp
            spc1 = np.zeros((int(751*NumWin)+1));spc2 = np.zeros((int(751*NumWin)+1));spc3 = np.zeros((int(751*NumWin)+1));
            for k in range(NumWin):
                
                # change start frequency for every window
                if sa1on:
                    try:sa1.write(':FREQuency:STARt ' + str(fStart+k*obsBW) + ' MHz');
                    except:sa1on = False;sa1onerr=True;
                if sa2on:
                    try:sa2.write(':FREQuency:STARt ' + str(fStart+k*obsBW) + ' MHz');
                    except:sa2on = False;sa2onerr=True;
                if sa3on:
                    try:sa3.write(':FREQuency:STARt ' + str(fStart+k*obsBW) + ' MHz');
                    except:sa3on = False;sa3onerr=True;
                
                # change stop frequency for every window
                if sa1on:
                    try:sa1.write(':FREQuency:STOP ' + str(fStart+(k+1)*obsBW) + ' MHz');
                    except:sa1on = False;sa1onerr=True;
                if sa2on:
                    try:sa2.write(':FREQuency:STOP ' + str(fStart+(k+1)*obsBW) + ' MHz');
                    except:sa2on = False;sa2onerr=True;
                if sa3on:
                    try:sa3.write(':FREQuency:STOP ' + str(fStart+(k+1)*obsBW) + ' MHz');
                    except:sa3on = False;sa3onerr=True;
                
                # timer to let the SA analyze the spectral window
                time.sleep(0.14);
                # get trace
                if sa1on:
                    try:spc1[751*k:751*(k+1)] = sa1.query_ascii_values('TRACE?');
                    except:sa1on = False;sa1onerr=True;
                if sa2on:
                    try:spc2[751*k:751*(k+1)] = sa2.query_ascii_values('TRACE?');
                    except:sa2on = False;sa2onerr=True;
                if sa3on:
                    try:spc3[751*k:751*(k+1)] = sa3.query_ascii_values('TRACE?');
                    except:sa3on = False;sa3onerr=True;
                # if sa1on:sa1.write(':FREQuency:STARt ' + str(fStart+k*obsBW) + ' MHz');
                # if sa2on:sa2.write(':FREQuency:STARt ' + str(fStart+k*obsBW) + ' MHz');
                # if sa3on:sa3.write(':FREQuency:STARt ' + str(fStart+k*obsBW) + ' MHz');
                
                # if sa1on:sa1.write(':FREQuency:STOP ' + str(fStart+(k+1)*obsBW) + ' MHz');
                # if sa2on:sa2.write(':FREQuency:STOP ' + str(fStart+(k+1)*obsBW) + ' MHz');
                # if sa3on:sa3.write(':FREQuency:STOP ' + str(fStart+(k+1)*obsBW) + ' MHz');
                
                # time.sleep(0.14);
                # if sa1on:spc1[751*k:751*(k+1)] = sa1.query_ascii_values('TRACE?');
                # if sa2on:spc2[751*k:751*(k+1)] = sa2.query_ascii_values('TRACE?');
                # if sa3on:spc3[751*k:751*(k+1)] = sa3.query_ascii_values('TRACE?');
            
            # include time stamp in the current spectrum
            curr_dt = datetime.now().timestamp();
            if sa1on:spc1[-1] = curr_dt;
            if sa2on:spc2[-1] = curr_dt;
            if sa3on:spc3[-1] = curr_dt;
            
            # write spectrum to data file
            if sa1on:writer_object1.writerow(list(spc1));
            if sa2on:writer_object2.writerow(list(spc2));
            if sa3on:writer_object3.writerow(list(spc3));
            
            # update time variable for length of file
            now = datetime.now();
            print(str((rightnow + timedelta(hours=howlong) - now))+' left');

        # close data file
        if sa1on or sa1onerr:f_object1.close();
        if sa2on or sa1onerr:f_object2.close();
        if sa3on or sa1onerr:f_object3.close();
        
        # clear and close connection to SA
        if sa1on:sa1.clear();sa1.close();
        if sa2on:sa2.clear();sa2.close();
        if sa3on:sa3.clear();sa3.close();
        
        # close pyVISA resource manager
        rm.close();
    
    except:
        # in case anything prevents the code to run (e.g. keyboard stop)
        # close files
        if sa1on or sa1onerr:f_object1.close();
        if sa2on or sa1onerr:f_object2.close();
        if sa3on or sa1onerr:f_object3.close();
        
        # clear and close connection to SA
        if sa1on:sa1.clear();sa1.close();
        if sa2on:sa2.clear();sa2.close();
        if sa3on:sa3.clear();sa3.close();
        
        # close resource manager
        rm.close();
        
        # launch monitoring again
        run_monitor(howlong,fRes,fStart,fStop);

# run always the monitoring....
while(True):
    run_monitor(howlong,fRes,fStart,fStop);
