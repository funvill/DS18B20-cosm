import os
import glob
import time
import eeml
import eeml.datastream
import eeml.unit
# from eeml import CosmError

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

FEED   	= 123456789
API_KEY 	= 'YOUR_API_KEY'
API_URL 	= '/v2/feeds/{feednum}.xml' .format(feednum = FEED)
 
base_dir 	= '/sys/bus/w1/devices/'
device_folders  = glob.glob(base_dir + '28*') 

def read_temp_raw( filename ):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    return lines

def ReadSingleSensor( i, sensor_file ):
    device_name = sensor_file.replace( base_dir, '' ).replace( '/w1_slave', '' ) 
    print( device_name ) 

    lines = read_temp_raw( sensor_file )
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw( sensor_file )

    print( lines )	   
       
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0 

    #open up your cosm feed
    pac = eeml.datastream.Cosm(API_URL, API_KEY)

    #send celsius data
    pac.update([eeml.Data(device_name, str( temp_c ), unit=eeml.unit.Celsius())])
    
    pac.put()
    print(pac.geteeml())
    time.sleep(1)  

def ReadSensors():
    for (i, item) in enumerate(device_folders):
        sensor_file = item + '/w1_slave'
        # print( sensor_file ) 
        ReadSingleSensor( i, sensor_file ) 
        
while True: 
    try: 
        ReadSensors() 
    
    # except CosmError, e:
    #     print('ERROR: pac.put(): {}'.format(e))
    except StandardError:
        print('ERROR: StandardError')
    except:
        print('ERROR: Unexpected error')

    time.sleep(10)      
