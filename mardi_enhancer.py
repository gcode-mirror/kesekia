import os
import win32gui
import win32com
import win32com.client as comclt
import win32process
import time
import sys
import mardi_checkenhanced

def activate_enhancer():
    #recipe from: http://stackoverflow.com/questions/8095266/set-focus-to-window-based-on-id-using-win32com-clients-appactivate
    hwnd = win32gui.GetForegroundWindow()
    
    _, current_pid = win32process.GetWindowThreadProcessId(hwnd)
    wsh = comclt.Dispatch("WScript.Shell")

    hwnd = win32gui.FindWindowEx(0,0,0, "Jpeg Enhancer")
    win32gui.SetForegroundWindow(hwnd)
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    wsh.AppActivate(pid)

    return current_pid
    

#path+filename from directory and frame number
def get_filename(directory,frame):
    fn = os.path.join(directory,"0000MD9999%06dE1_DXXX.jpg" % frame)
    return fn

def send_sequence(s,delay=0.5):
    wsh= comclt.Dispatch("WScript.Shell")
    time.sleep(delay)
    for c in s:
        wsh.SendKeys(c)
        time.sleep(delay)

def jpeg_enhancer(input_directory,start,end,check_existing=False):
    wsh= comclt.Dispatch("WScript.Shell")
    frame_i = start
    first_go = True
    first_go = False
    while 1:
        fn = os.path.abspath(get_filename(input_directory,frame_i))
        fn_out = fn[:-3]+"png"

        abs_dir,fi = os.path.split(fn)
        _,fo = os.path.split(fn_out)

        #check that if we have both images, it's the right frame. 3 seems to work
        if check_existing and os.path.exists(fn) and os.path.exists(fn_out):
            m = mardi_checkenhanced.meandiff(fn,fn_out)
            if m > 3:
                print "removing suspicious %s (m=%.2f)" % (fo,m)
                os.remove(fn_out)

        #does the input file exist?
        if os.path.exists(fn) and not os.path.exists(fn_out):
            print "processing %s" % fi
            #Open file
            send_sequence("%fo",delay=0.2)

            if first_go is True:
                wsh.SendKeys("%s{enter}" % abs_dir)
                time.sleep(0.2)
                first_go = False

            wsh.SendKeys("%s{enter}" % fn)
            #wsh.SendKeys("%s{enter}" % fi)
            time.sleep(8)

            #Save file
            send_sequence("%fa",delay=0.2)
            wsh.SendKeys("%s{enter}" % fn_out)

            #enhancer busy... throttle!!
            time.sleep(16)

            if os.path.exists(fn_out):
                frame_i += 1
            else:
                print "Jpeg Enhancer did not save %s - Check and relaunch the python script" % fo
                break
        else:
            #non existant input file, or file already processed
            frame_i += 1

        if frame_i > end:
            break

if __name__ == '__main__':
    input_directory = "images_new"
    start = 0
    end = 1504

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

    try:
        current = activate_enhancer()
    except:
        print "Open Jpeg Enhancer first"
        sys.exit(0)

    jpeg_enhancer(input_directory,start,end)

    #give focus back to command...
    wsh = comclt.Dispatch("WScript.Shell")
    wsh.AppActivate(str(current))


