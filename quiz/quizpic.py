from PIL import Image, ImageDraw, ImageFont

d = {'category 1': [100,200,300,400],
     'category 2': [100,200,300,400],
     'category 3': [100,200,300,400],
     'category 4': [100,200,300,400],
     'category 5': [100,200,300,400],
     }

h = 300
w = 420
k = 7
step = int(h / 5)
w = step * k

im = Image.new('RGB', (w, h), (49,140,231))
draw = ImageDraw.Draw(im)
for i in range(0, 6):
  draw.line((0, step * i, w, step * i), fill='white', width=1)

for i in range(3, k+1):
  draw.line((step * i-1, 0, step * i-1, h), fill='white', width=1)

draw.line((0, 0, 0, h), fill='white', width=1)

for key, i in zip(d.keys(), range(0, k)):
  draw.text((10,step*i+int(step/2)-5), key, font = None, fill=(255,255,255,0))
  for j, n in zip(d[key], range(3, k+1)):
    draw.text((step*n+int(step/2)-5, step*i+int(step/2)-5), str(j), font = None, fill=(255,255,255,0))

im.show()

im