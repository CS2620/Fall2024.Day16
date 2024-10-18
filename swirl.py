from PIL import Image
import math

image_start = Image.open("code.image.jpg")
data_start = image_start.load()

image_out = Image.new("RGB", (image_start.width, image_start.height))
data_out = image_out.load()

# To prevent us from swirling outside the image, constrain the max radius
min_dimension = min(image_start.width, image_start.height)
max_radius = min_dimension/2

for y in range(image_out.height):
    for x in range(image_out.width):
        
        cx, cy = x - image_out.width/2 , y - image_out.height/2 # Center pixel

        theta, radius = math.atan2(cy, cx), math.sqrt(cx**2+cy**2) # Convert to polar coordinates

        new_radius = min(1, radius/max_radius)
        new_theta = theta 

        sample_x = round(math.cos(new_theta) * radius + image_out.width/2)
        sample_y = round(math.sin(new_theta) * radius + image_out.height/2)

        if (sample_x < 0 or sample_x >= image_out.width or sample_y < 0 or sample_y >= image_out.height):
            data_out[x, y] = (0, 0, 0)
        else:
          data_out[x, y] = data_start[sample_x, sample_y]


image_out.save("code.out.png")
