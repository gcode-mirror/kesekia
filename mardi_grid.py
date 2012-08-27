import Image,ImageDraw

fn = "0000MD9999000506E1_DXXX.jpg"
fn = "test.jpg"

im = Image.open(fn)
w,h = im.size

draw = ImageDraw.Draw(im)

for x in range(0,w,8):
    draw.line((x,0,x,h),width=1,fill=(255,255,255))

for y in range(0,h,8):
    draw.line((0,y,w,y),width=1,fill=(255,255,255))

im.save(fn[:-3]+"png")

