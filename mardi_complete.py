import os
import shutil
import sys

#path+filename from directory and frame number
def get_filename(directory,frame,ext="jpg"):
    fn = os.path.join(directory,"0000MD9999%06dE1_DXXX.%s" % (frame,ext))
    return fn

if __name__ == '__main__':
    input_directory = "images_new"
    output_directory = "images_png"
    ext = "png"
    start = 1
    end = 1504

    #find the first frame
    found = False
    for j in range(start,end+1):
        if os.path.exists(get_filename(input_directory,j,ext)):
            found = True
            break

    if found is False:
        print "couldn't find any MARDI images in %s" % input_directory
        sys.exit(0)

    #copy to destination directory
    start = j
    print "Found first frame at %d" % start
    for i in range(start,end):
        fn_input = get_filename(input_directory,i,ext)
        fn_output = get_filename(output_directory,i,ext)
        
        if os.path.exists(fn_input):
            j = i
        else:
            print "filled in missing frame %d" % i
            fn_input = get_filename(input_directory,j,ext)

        shutil.copyfile(fn_input,fn_output)
