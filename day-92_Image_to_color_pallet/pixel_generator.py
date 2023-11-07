from colorthief import ColorThief
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
import requests

API = "https://x-colors.yurace.pro/api/rgb2hex?value="


def reg2hex(rgb):
    response = requests.get(API + f"{rgb[0]}-{rgb[1]}-{rgb[2]}")
    # to dictionary
    return response.json()


color_thief = ColorThief('test.jpg')

# ask the user for the number of colors they want to generate
color_count = int(input("Enter the number of colors you want to generate: "))

# get the dominant color
dominant_color = color_thief.get_color(quality=1)
print("The most dominant color is: ", dominant_color)

# build a color palette
palette = color_thief.get_palette(color_count=color_count)

# Create a figure with a larger width to accommodate the labels
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4))

# Load the image and display it in the left subplot
image = mpimg.imread('test.jpg')
ax1.imshow(image, extent=[0, 1, 0, 1])

# convert horizontal array to vertical array
ax2.imshow([[palette[i]] for i in range(color_count)])

# Display the colors using matplotlib
ax1.axis('off')
ax2.axis('off')

print("Making api calls to get color names...")
color_names = [reg2hex(palette[i]) for i in range(color_count)]

# Add color names as text labels
for i, name in enumerate(color_names):
    ax2.text(0.6, i, str(name), ha='left', va='bottom')

# add a title
ax2.set_title(f"Color Palette with {color_count} colors")

plt.show()
