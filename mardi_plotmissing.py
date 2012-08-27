import os
import sys
import numpy as np
import time

import matplotlib.pyplot as plt
import matplotlib.ticker as tkr

from matplotlib.patches import Rectangle

import datetime
import Image
import scipy
import scipy.misc
import scipy.cluster

#path+filename from directory and frame number
def get_filename(directory,frame):
    fn = os.path.join(directory,"0000MD9999%06dE1_DXXX.jpg" % frame)
    return fn

#http://stackoverflow.com/questions/3241929/python-find-dominant-most-common-colour-in-an-image
def get_colour(im):
    NUM_CLUSTERS = 5

    w,h = im.size
    im = im.resize((w/32,h/32),Image.NEAREST)      # optional, to reduce time

    ar = scipy.misc.fromimage(im)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2])

    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
    counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

    index_max = scipy.argmax(counts)                    # find most frequent
    peak = codes[index_max]
    colour = ''.join(chr(c) for c in peak).encode('hex')

    return "#"+colour

#http://stackoverflow.com/questions/8271564/matplotlib-comma-separated-number-format-for-axis
def func(frame,pos):
    #timestamps from the Sol0 raw image page
    time_f1504 = time.mktime(time.strptime("2012-08-06 05:21:48 UTC","%Y-%m-%d %H:%M:%S %Z"))
    time_f1 = time.mktime(time.strptime("2012-08-06 05:15:21 UTC","%Y-%m-%d %H:%M:%S %Z"))
    frame_duration = (time_f1504-time_f1) / (1504.-1.)

    frame_time = time_f1 + (frame - 1) * frame_duration
    return "%d\n%s" % (frame,time.strftime("%H:%M:%S",time.gmtime(frame_time)))
    
def plot_graph(input_directory,start,end):
    fig = plt.figure(figsize=(16,3))
    fig.subplots_adjust(left=0.03, right=0.98, hspace=0.25, wspace=0.25,top=0.88,bottom=0.25)

    ax1 = plt.subplot(111)
    plt.setp(ax1.get_yticklabels(),visible=False)

    for i in range(end-start):
        frame_i = start+i
        fn = get_filename(input_directory,frame_i)

        if os.path.exists(fn):
            im = Image.open(fn)
            colour = get_colour(im)
            print 'Frame %d dominant colour is %s' % (frame_i,colour)
        else:
            if frame_i == 0:
                #helping matplotlib finding the 0 on the x axis
                colour = 'k'
            else:
                colour = 'r'
                print 'Frame %d is missing' % frame_i

        #ax1 in frames
        rect = Rectangle((frame_i, 0), 1, 1, facecolor=colour,edgecolor='none')
        ax1.add_patch(rect)

    time_format = tkr.FuncFormatter(func)
    ax1.xaxis.set_major_formatter(time_format) # set formatter to needed axis
    
    ax1.set_ylim(0,1)
    ax1.set_xlim(start,end)

    ax1.set_title('Dominant frame colour - Missing frames in red (as of %s)' % time.asctime())
    ax1.set_xlabel('Frame number and Time (UTC)')

    fig.savefig("missing_frames.png")
    plt.show()

if __name__ == '__main__':
    input_directory = "images"
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

    plot_graph(input_directory,start,end)

