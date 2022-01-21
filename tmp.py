if sa1on:
                    try:sa1.write(':FREQuency:STARt ' + str(fStart+k*obsBW) + ' MHz');
                    except:sa1on = False;
                if sa2on:
                    try:sa2.write(':FREQuency:STARt ' + str(fStart+k*obsBW) + ' MHz');
                    except:sa2on = False;
                if sa3on:
                    try:sa3.write(':FREQuency:STARt ' + str(fStart+k*obsBW) + ' MHz');
                    except:sa3on = False;
                
                if sa1on:
                    try:sa1.write(':FREQuency:STOP ' + str(fStart+(k+1)*obsBW) + ' MHz');
                    except:sa1on = False;
                if sa2on:
                    try:sa2.write(':FREQuency:STOP ' + str(fStart+(k+1)*obsBW) + ' MHz');
                    except:sa2on = False;
                if sa3on:
                    try:sa3.write(':FREQuency:STOP ' + str(fStart+(k+1)*obsBW) + ' MHz');
                    except:sa3on = False;
                
                time.sleep(0.15);
                if sa1on:
                    try:spc1[751*k:751*(k+1)] = sa1.query_ascii_values('TRACE?');
                    except:sa1on = False;
                if sa2on:
                    try:spc2[751*k:751*(k+1)] = sa2.query_ascii_values('TRACE?');
                    except:sa2on = False;
                if sa3on:
                    try:spc3[751*k:751*(k+1)] = sa3.query_ascii_values('TRACE?');
                    except:sa3on = False;
