from PIL import Image
import math

def nearestNeighborInterpolation(data, x,y):
    return data[round(x), round(y)]

def bilinearInterpolation(data, x,y):
    beforeX = math.floor(x)
    afterX = math.ceil(x)
    beforeY = math.floor(y)
    afterY = math.ceil(y)

    remainderX = x - beforeX
    remainderY = y - beforeY

    ul = data[beforeX, beforeY]
    ur = data[afterX , beforeY]
    ll = data[beforeX, afterY ]
    lr = data[afterX , afterY ]

    top    = [(1-remainderX) * ul[index] + remainderX * ur[index]  for index in range(3)]
    bottom = [(1-remainderX) * ll[index] + remainderX * lr[index]  for index in range(3)]

    middle = [(1-remainderY) * top[index] + remainderY * bottom[index] for index in range(3)]

    return tuple([round(middle[index]) for index in range(3)])
    #return data[round(x), round(y)]


image_start = Image.open("code.image.jpg")
data_start = image_start.load()

image_out = Image.new("RGB", (image_start.width, image_start.height))
data_out = image_out.load()


for y in range(image_out.height):
    for x in range(image_out.width):
        data_out[x,y] = bilinearInterpolation(data_start, x/2, y/2)

#image_out.save("code.out.png")

#quit()

# To prevent us from swirling outside the image, constrain the max radius
min_dimension = min(image_start.width, image_start.height)
max_radius = min_dimension/2

for y in range(image_out.height):
    for x in range(image_out.width):
        
        cx, cy = x - image_out.width/2 , y - image_out.height/2 # Center pixel

        theta, radius = math.atan2(cy, cx), math.sqrt(cx**2+cy**2) # Convert to polar coordinates

        new_radius = radius 
        if new_radius < max_radius:
            new_radius=  (radius/max_radius)**2 * max_radius

        sample_x = math.cos(theta) * new_radius + image_out.width/2
        sample_y = math.sin(theta) * new_radius + image_out.height/2

        sample_x = round(sample_x, 10)
        sample_y = round(sample_y, 10)

        data_out[x, y] = bilinearInterpolation(data_start, sample_x, sample_y) #data_start[sample_x, sample_y]

image_out.save("code.out.png")
