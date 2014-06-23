#base skript for subprocesses and filter by benjamin maus, Osc Send Function stolen from redfrik. smashed together by paul and laurenz


import exceptions
import logging
import os
import signal
import subprocess

#############
import OSC
import time

sc= OSC.OSCClient()
sc.connect(('127.0.0.1', 57120)) #send locally to sc
#############

logging.basicConfig(level=logging.DEBUG)    # User logging.INFO for less output
logger = logging.getLogger(__name__)


FIELD_DELIM = ';'
VALUE_DELIM = ','

TSHARK_CMD = ['tshark', '-I', '-i', 'mon0',
              '-T', 'fields', '-l',
              '-e', 'wlan.fc.type', '-e', 'wlan.fc.subtype',
              '-e', 'wlan.bssid', '-e', 'wlan.addr', '-e', 'data.len', 
              '-e', 'data.data',
              '-E', 'separator=' + FIELD_DELIM,
              '-E', 'aggregator=' + VALUE_DELIM,
              '-E', 'header=n']

# FIXME: Different for Linux...
      

def parse_float(s):
    """ Parses a float from a string. Returns None if the string is wrong """
    try:
        return float(s)
    except exceptions.ValueError:
        return None


def parse_int(s):
    """ Parses an int from a string. Returns None if the string is wrong """
    try:
        return int(s)
    except exceptions.ValueError:
        return None


def start_capture_and_process_loop():
    """
    Starts capture by running the tshark process and reads its output
    line by line.
    """

    # Why all the hassle?
    #  http://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
    logger.info('Starting "%s"', ' '.join(TSHARK_CMD))

    proc = subprocess.Popen(TSHARK_CMD, bufsize=0, stdout=subprocess.PIPE, preexec_fn=os.setsid)

    try:
        while True:
            line = proc.stdout.readline()
        
            if line:
                process_line(line.rstrip())
            else:   # EOF. Escape!
                break
    finally:    # Make sure we kill the process!
        os.killpg(proc.pid, signal.SIGTERM)


def process_line(line):
    """ Responsible for parsing each line and determining what to do with it """

    #logger.debug('Line "%s"', line)

    pieces = line.split(FIELD_DELIM)

    if len(pieces) == 6:    # we should get 5 fields in the same order as in the command
        wlan_type = pieces[0].split(VALUE_DELIM)[0].strip()     # only first value (or single)
        wlan_subtype = pieces[1].split(VALUE_DELIM)[0].strip()
        wlan_bssid = pieces[2].split(VALUE_DELIM)[0].strip()
        wlan_addr_list = pieces[3].split(VALUE_DELIM)
        data_len = pieces[4].split(VALUE_DELIM)[0].strip()
        data_data = pieces[5].split(VALUE_DELIM)[0].strip()


        #if wlan_type == '0':    # Management frame
            #logger.debug('Management frame')
            #e = GenerateValue(data_data,'Management frame')
            #if wlan_subtype == '4':     # Probe request
                #logger.debug('    Probe request')

            #if wlan_subtype == '5':     # Probe response
                #logger.debug('    Probe response')
                #d = GenerateValue(data_data,'Probe response')

        #if wlan_type == '1':    # Control frame
            #logger.debug('Control frame')

        if wlan_type == '2':    # Data frame
            l = parse_int(data_len)
            #logger.debug(data_data)
            #d = GenerateValue(data_data,)


            if l > 400:
                logger.debug('big DataPacket')
                #logger.debug('Data frame with length %d', l)
                a = GenerateValue(data_data,'big DataPacket')
            elif l > 100:
                logger.debug('medium DataPacket')
                b = GenerateValue(data_data,'medium DataPacket')
            elif l > 1:
                logger.debug('small DataPacket')
                c = GenerateValue(data_data,'small DataPacket')

            else:
                logger.debug('Data frame with missing length')

    else:
        logger.warning('Malformed line: "%s"', line)

def GenerateValue(value,information):
        rawhexarray= value.split(':')
        #print len(rawhexarray)
        for i in rawhexarray[25:30]:

            decodedvalues = i.encode('hex')
            a = parse_int(decodedvalues)

            sendOSC(information, a)
           # logger.debug(decodedvalues)

        #logger.debug(rawhexarray)
        if information == 'Probe response':
            sendOSC(information, 1)

        elif information == 'Management frame':
            sendOSC(information, 1)


##############
def sendOSC(name, val):
        msg= OSC.OSCMessage()
        msg.setAddress(name)
        msg.append(val)
        try:
                sc.send(msg)
        except:
                1+1 # dummy
        #print msg

        time.sleep(0.05)
##############

      
if __name__ == "__main__":
    start_capture_and_process_loop()
