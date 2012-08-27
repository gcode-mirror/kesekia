import urllib2
import os
import sys

def get_timestamp(html,filename):
    pattern,_ = os.path.splitext(filename)
    n_lines = len(html)

    timestamp = None
    for i in range(n_lines):
        line = html[i]
        if pattern in line:
            timestamp = html[i+4].split(">")[2][:19]+" UTC"
            break

    return timestamp

#from http://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
def download(url):
    data = ""
    file_name = url.split("/")[-1]

    try:
        u = urllib2.urlopen(url)
    except:
        print "%s not found" % file_name
        return None

    meta = u.info()
    if meta.getheaders("Content-Type") == "text/html":
        file_name = "text file"
        filesize = -1
    else:
        file_size = int(meta.getheaders("Content-Length")[0])

    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        data += buffer
        file_size_dl += len(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    return data

def download_mardi(directory,start,end):
    #http://mars.jpl.nasa.gov/msl-raw-images/msss/00000/mrdi/0000MD9999000002E1_DXXX.jpg
    n_images = end-start+1
    i_images = 0
    for i in range(end-start+1):
        frame_i = start+i
        filename = "0000MD9999%06dE1_DXXX.jpg" % frame_i
        url = "http://mars.jpl.nasa.gov/msl-raw-images/msss/00000/mrdi/"+filename
        fn_out = os.path.join(directory,filename)

        if not os.path.exists(fn_out):
            data = download(url)
            if data is not None:
                f = open(fn_out,"wb")
                f.write(data)
                f.close()

                i_images += 1
        else:
            i_images += 1

    return i_images,n_images

if __name__ == '__main__':
    input_directory = "raw_images"
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
        while 1:
            choice=raw_input("Create \"%s\" directory (y/n)?" % input_directory).lower()
            if choice in ["y","n"]:
                break

        if choice == "y":
            os.mkdir(input_directory)
        else:
            sys.exit(0)

    images,total_images = download_mardi(input_directory,start,end)
    print "images=%d - total_images=%d" % (images,total_images)

    if 0:
        #test to see how many files are actually displayed on the sol0 page.
        #Answer is: Less than can be accessed directly!

        html = download("http://mars.jpl.nasa.gov/msl/multimedia/raw/?s=0").splitlines()

        n_images = 1505
        i_images = 0
        for i in range(1,n_images):
            filename = "0000MD9999%06dE1_DXXX.jpg" % i
            ts = get_timestamp(html,filename)

            if ts is not None:
                print i,ts
                i_images +=1

        print "images=%d - total_images=%d" % (i_images,n_images)

