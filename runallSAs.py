# code to run after all SA are set and connected
# procedure:
# 1- connect USB hub to laptop
# 2- connect all SAs to hub
# 3- turn on SAs
# 4- configure SAs
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


howlong = 1./60.;    # survey duration in hours
fRes = 100; # frequency resolution in kHz
fStart = 500;   # start frequency in MHz
fStop = 3200;   # stop frequency in MHz

def run_monitor(howlong,fRes,fStart,fStop):

    rm = pyvisa.ResourceManager();
    
    # define the spectrum analyzers names
    siglent1 = "USB0::0xF4EC::0x1305::SSA3PCDX5R0432::INSTR";
    siglent2 = "USB0::0xF4EC::0x1305::SSA3PCDX5R0431::INSTR";
    siglent3 = "USB0::0xF4EC::0x1305::SSA3PCDC5R0345::INSTR";

    # check which SA respond, ignore if they don't
    sa1on = True;sa2on = True;sa3on = True;
    try:sa1 = rm.open_resource(siglent1);
    except:sa1on = False;
    try:sa2 = rm.open_resource(siglent2);
    except:sa2on = False;
    try:sa3 = rm.open_resource(siglent3);
    except:sa3on = False;
    
    try:sa1.write(':BWIDth ' + str(fRes) + ' KHz');
    except:sa1on = False;
    try:sa2.write(':BWIDth ' + str(fRes) + ' KHz');
    except:sa2on = False;
    try:sa3.write(':BWIDth ' + str(fRes) + ' KHz');
    except:sa3on = False;

    rightnow = datetime.now();
    if sa1on:fname1 = 'C:\\Users\\gregh\\Desktop\\siglent_DSA_RFI_survey\\3SA\\RFI1_survey_'+rightnow.strftime('%y%m%d%H%M%S')+'_'+str(howlong)+'h.csv';
    if sa2on:fname2 = 'C:\\Users\\gregh\\Desktop\\siglent_DSA_RFI_survey\\3SA\\RFI2_survey_'+rightnow.strftime('%y%m%d%H%M%S')+'_'+str(howlong)+'h.csv';
    if sa3on:fname3 = 'C:\\Users\\gregh\\Desktop\\siglent_DSA_RFI_survey\\3SA\\RFI3_survey_'+rightnow.strftime('%y%m%d%H%M%S')+'_'+str(howlong)+'h.csv';
    
    if sa1on:f_object1 = open(fname1, 'a', newline='');
    if sa2on:f_object2 = open(fname2, 'a', newline='');
    if sa3on:f_object3 = open(fname3, 'a', newline='');

    try:
        
        print('starting survey at '+str(rightnow));
        print('writing to:');
        if sa1on:print(fname1);
        if sa2on:print(fname2);
        if sa3on:print(fname3);

        BW = fStop - fStart;    # total bandwidth in MHz
        obsBW = 751.*fRes/1000.;    # observed bandwidth (751 points per scan)
        NumWin = int(np.ceil(BW/obsBW)); # number of windows
        fStart = fStop - NumWin*obsBW;  # new start frequency given the number of analysis windows

        if sa1on:sa1.write(':BWIDth:VIDeo:RATio 1');
        if sa2on:sa2.write(':BWIDth:VIDeo:RATio 1');
        if sa3on:sa3.write(':BWIDth:VIDeo:RATio 1');

        if sa1on:sa1.write(':POWer:GAIN ON');
        if sa2on:sa2.write(':POWer:GAIN ON');
        if sa3on:sa3.write(':POWer:GAIN ON');

        if sa1on:sa1.write(':POWer:ATTenuation 0');
        if sa2on:sa2.write(':POWer:ATTenuation 0');
        if sa3on:sa3.write(':POWer:ATTenuation 0');

        if sa1on:writer_object1 = writer(f_object1);
        if sa2on:writer_object2 = writer(f_object2);
        if sa3on:writer_object3 = writer(f_object3);

        rightnow = datetime.now();
        now = datetime.now();
        while now <= rightnow + timedelta(hours=howlong):
            spc1 = np.zeros((int(751*NumWin)));spc2 = np.zeros((int(751*NumWin)));spc3 = np.zeros((int(751*NumWin)));
            for k in range(NumWin):
                
                if sa1on:sa1.write(':FREQuency:STARt ' + str(fStart+k*obsBW) + ' MHz');
                if sa2on:sa2.write(':FREQuency:STARt ' + str(fStart+k*obsBW) + ' MHz');
                if sa3on:sa3.write(':FREQuency:STARt ' + str(fStart+k*obsBW) + ' MHz');
                
                if sa1on:sa1.write(':FREQuency:STOP ' + str(fStart+(k+1)*obsBW) + ' MHz');
                if sa2on:sa2.write(':FREQuency:STOP ' + str(fStart+(k+1)*obsBW) + ' MHz');
                if sa3on:sa3.write(':FREQuency:STOP ' + str(fStart+(k+1)*obsBW) + ' MHz');
                
                time.sleep(0.15);
                if sa1on:spc1[751*k:751*(k+1)] = sa1.query_ascii_values('TRACE?');
                if sa2on:spc2[751*k:751*(k+1)] = sa2.query_ascii_values('TRACE?');
                if sa3on:spc3[751*k:751*(k+1)] = sa3.query_ascii_values('TRACE?');
                
            if sa1on:writer_object1.writerow(list(spc1));
            if sa2on:writer_object2.writerow(list(spc2));
            if sa3on:writer_object3.writerow(list(spc3));
            
            now = datetime.now();
            print(str((rightnow + timedelta(hours=howlong) - now))+' left');

        if sa1on:f_object1.close();
        if sa2on:f_object2.close();
        if sa3on:f_object3.close();
        
        if sa1on:sa1.clear();sa1.close();
        if sa2on:sa2.clear();sa2.close();
        if sa3on:sa3.clear();sa3.close();
        
        rm.close();
    
    except:
    
        if sa1on:f_object1.close();
        if sa2on:f_object2.close();
        if sa3on:f_object3.close();
        
        if sa1on:sa1.clear();sa1.close();
        if sa2on:sa2.clear();sa2.close();
        if sa3on:sa3.clear();sa3.close();
        
        rm.close();
        
        run_monitor(howlong,fRes,fStart,fStop);

while(True):
    run_monitor(howlong,fRes,fStart,fStop);
