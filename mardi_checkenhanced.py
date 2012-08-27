import os
import win32gui
import win32com.client as comclt
wsh= comclt.Dispatch("WScript.Shell")
import time
import sys
import Image
import numpy

#path+filename from directory and frame number
def get_filename(directory,frame):
    fn = os.path.join(directory,"0000MD9999%06dE1_DXXX.jpg" % frame)
    return fn

def send_sequence(s,delay=0.5):
    wsh= comclt.Dispatch("WScript.Shell")
    time.sleep(delay)
    for c in s:
        print c
        wsh.SendKeys(c)
        time.sleep(delay)

def meandiff(fn_in,fn_out):
    arr_in = numpy.array(Image.open(fn_in)).astype(int)
    arr_out = numpy.array(Image.open(fn_out)).astype(int)
    m = numpy.mean(numpy.abs(arr_in-arr_out))
    return m

def jpeg_checkenhanced(input_directory,start,end):
    for frame_i in range(start,end+1):
        fn_in = os.path.abspath(get_filename(input_directory,frame_i))
        fn_out = fn_in[:-3]+"png"
        _,fi = os.path.split(fn_in)
        _,fo = os.path.split(fn_out)

        #does the input file exist?
        if os.path.exists(fn_in) and os.path.exists(fn_out):
            m = meandiff(fn_in,fn_out)
            if m > 3:
                print frame_i,fi,m
            
if __name__ == '__main__':
    input_directory = "images_new"
    start = 0
    end = 1504

    time.sleep(5)

    #input directory
    if len(sys.argv) > 1:
        input_directory = sys.argv[1]

    #start and end
    if len(sys.argv) > 2:
        start = int(sys.argv[2])
        if start < 0:
            start = 0

    if len(sys.argv) > 3:
        end = int(sys.argv[3])
        if end > 1504:
            end = 1504

    if not os.path.exists(input_directory):
        print "Need to specify a valid input directory"
        sys.exit(0)

    jpeg_checkenhanced(input_directory,start,end)




