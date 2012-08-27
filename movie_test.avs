loadplugin("avsplugins\HistogramAdjust.dll")
#loadplugin("avsplugins\unblock.dll")
LoadPlugin("avsplugins\Cnr2.dll")
LoadPlugin("avsplugins\gradfun2db.dll")
LoadPlugin("avsplugins\flash3kyuu_deband.dll")

#complete sequence
#ret = ImageSource("images_enhanced\0000MD9999%06dE1_DXXX.png", 1, 1504, 4)
#ret = ret.Trim(23,200)
#
#shorter sequence
ret = ImageSource("images_enhanced\0000MD9999%06dE1_DXXX.png", 23, 800, 4)

#needed for unblock
ret = ret.converttoYV12()

#Applying unblocking filter
#ret = ret.unblock() #photo=true)

#crop the edges
#ret = ret.Crop(32,4,-24,0)

#resizing for testing. What method should we use?
#ret = BilinearResize(ret,824,600)
ret = ReduceBy2(ret)

#adjusting histogram. Default seems to work well enough
ret = HistogramAdjust(ret,1,55,100,70,255,5,type="match",table=true, window=true,w=59,h=55, limit=10)

#debanding attempt on dark segment. need to work on that one..
#ret = ret.Cnr2("xxx",4,5,255) # my suggestion to remove rainbows.
#ret = ret.Cnr2("oxx",8,35,192,47,255,47,255,false)
#ret = gradfun2db(ret,100)
#ret = f3kdb_dither(ret)

#returning clip. #changing to 25 frames only necessary for xvid. didn't like 4 frames/sec
ret.ConvertToRGB32().ChangeFPS(25)
