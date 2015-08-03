# Introduction #

First, a big thank-you to NASA for making so many of [Curiosity's raw images](http://mars.jpl.nasa.gov/msl/multimedia/raw/?s=0) available to the public at large.

Out of 1504 frames from Curiosity's descent, we now have 1377 high-res images to play with. I saw the amazing video user stealthispost made a while back, and more people are contributing material as we speak, over at the [/r/curiosityrover](http://www.reddit.com/r/curiosityrover) subreddit.

Hopefully this is something we can do together and (definitely for me) learn something in the process.

# Copyrights / acknowledgements #
Hopefully, it's OK to link to images / image sequence and host images here. [This notice](http://www.nasa.gov/audience/formedia/features/MP_Photo_Guidelines.html) should cover our use of the MARDI images.

# Videos so far #
  * [Official video](http://www.jpl.nasa.gov/video/index.cfm?id=1126)
  * [Godd2](http://www.reddit.com/r/curiosityrover/comments/yv52e/i_just_spent_the_last_four_days_straight/)
  * [PsySal](http://www.reddit.com/r/curiosityrover/comments/yneiu/curiosity_landing_hd_1080p_real_time_with_synced/) - sound sync
  * [stealthispost](http://www.reddit.com/r/curiosityrover/comments/yik3y/curiosity_mars_landing_video_version_2_1080p/) v2
  * [impreprex](http://www.reddit.com/r/curiosityrover/comments/yikk8/mardis_view_of_curiosity_latest_with_850_frames/)
  * [stealthispost](http://www.reddit.com/r/curiosityrover/comments/ydncv/i_spent_the_week_enhancing_the_images_of_the/) v1

# Ideas #

Here is a list of some ideas we're looking into.

## Standardizing tools and processes ##

First things first, allow me to be boring for a sec. Whatever we do, I think it would be really neat to try and explain _how_ we're doing things, and if it involves coding, make it available for others to use. One advantage is that while images take a lot of space and a lot of bandwidth to transmit, a few lines of Python or avisynth code don't.

I also personally think that sharing the tools is just as important (if not more) as sharing results. Go for it, take the code, add something to the mix and come-up with your own result. Use, abuse, and spread the good word (but only if you feel like it).

I propose Python, avisynth and virtualdub scripts made available [here](http://code.google.com/p/kesekia/source/browse?repo=default) or elsewhere, public Dropbox folders to share images, and the odd closed source tool, which if we can't share, will need detailing on a wiki.

Please make suggestions and add to the list! Hopefully we can also make the images available at each step of the way.

## Image quality ##

Anyone studying JPEG compression? Is there any way we can enhance the quality of the raw images?

I had a go with [JPEG enhancer](http://www.vicman.net/jpegenhancer/). I used a [Python script](http://code.google.com/p/kesekia/source/browse/mardi_enhancer.py) (win32) to generate the appropriate keystrokes (ctrl-o, filename.jpg, wait, ctrl-a filename.png wait) to walk through the 1400-odd raw images. This is something I learned over on [/r/programming](http://www.reddit.com/r/programming/comments/xtxq2/beating_the_google_doodle_in_22_lines_of_python/). Thanks guys!

The script requires Jpeg Enhancer to be opened first, and do load one image from the raw\_images directory and save it (OK to save as BMP). Sometimes the script can do this automatically, sometimes it won't. Do adjust the "processing" and "saving" delays for your windows install. Mine was about 8 and 16 seconds. Took about 2 days to process the images :)

If you're not sure whether the right image was saved, run [this script](http://code.google.com/p/kesekia/source/browse/mardi_checkenhanced.py).

XXX will add images before / after.

Eventually, images will be available in 3 large (around 450MB) zip files:
[1-402](http://dl.dropbox.com/u/99151572/mardi/images_enhanced_1to402.zip)
[403-804](http://dl.dropbox.com/u/99151572/mardi/images_enhanced_403to804.zip)
[805-1206](http://dl.dropbox.com/u/99151572/mardi/images_enhanced_805to1206.zip)
[1207-1504](http://dl.dropbox.com/u/99151572/mardi/images_enhanced_1207to1504.zip)

## Enhancing the sequence's contrast ##

User stealthispost enhanced the contrast of his sequence (XXX need details). This is something I'm looking into doing automatically using an Avisynth plugin, [HistogramAdjust](http://avisynth.org/vcmohan/HistogramAdjust/HistogramAdjust.html).

However... enhancing low contrast dark frames (roughly 615-715) introduces banding artifacts due to the limited quantization range we're trying to stretch [ref 1](http://www.jdvandenberghe.com/) [ref 2](http://enblend.sourceforge.net/banding.htm). Something avisynth may or may not be able to deal with.

## Motion compensation ##

[Deshaker](http://www.guthspot.se/video/deshaker.htm) (virtualdub plugin) seems to work nicely. Need to experiment with the parameters.

## Lens distortion ##

Haven't looked into this yet.

## Slowmovideo ##

User stealthispost proposed to use [Slowmovideo](http://slowmovideo.granjow.net/)- When we get all the kinks sorted, the result will be mind blowing.

Here is what we know: The windows binary barfed, but the 64 bit Linux binary almost worked for me. Couldn't compile it (need to check the intructions more carefully), couldn't install the .deb package, but ar -x and running the extracted exacutable almost worked.

## Embedded timestamps ##

Once a video sequence is exported as images in Virtualdub, we can use Python + PIL to embed a UTC timestamp on every image.

# Sequence images #

## Download ##

How do I download the MARDI images? [Python script](http://code.google.com/p/kesekia/source/browse/mardi_download.py)

Images will be placed in a raw\_images directory (if you agree to having the directory created).

Cloning the git repository will also give you access to the images.

## Missing frames ##

The following is a linear representation of the MARDI sequence, coded by dominant colour. Red lines represent missing frames. This is [the script I wrote](http://code.google.com/p/kesekia/source/browse/mardi_plotmissing.py) to generate the image below (needs numpy / scipy and matplotlib).

![http://wiki.kesekia.googlecode.com/git/images/missing_frames.png](http://wiki.kesekia.googlecode.com/git/images/missing_frames.png)

We still have a few missing frames, [this script](http://code.google.com/p/kesekia/source/browse/mardi_complete.py) duplicates existing frames to fill-in missing frames. This is important for the virtualdub deshaker script.

## Basic aviynth script ##

This [avisynth script](http://code.google.com/p/kesekia/source/browse/movie_test.avs) turns the images into a video sequence.

# Taks #

Here's the TODO list, I'll update as I go along:
  * Enhance the raw Jpeg images
  * Motion Compensation and...
  * Enhance the sequence's contrast and...
  * Lens distortion and...
  * export as PNGs
  * New PNGs will be used for Slowmovideo