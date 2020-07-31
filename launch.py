import argparse

from inky import InkyPHAT
from PIL import Image, ImageDraw, ImageFont

try:
	import requests
except ImportError:
	exit("This script requires the requests module\nInstall with: sudo pip install requests")

try:
	from bs4 import BeautifulSoup
except ImportError:
	exit("This script requires the bs4 module\nInstall with: sudo pip install beautifulsoup4")

#sets up inky pHat
parser = argparse.ArgumentParser()
parser.add_argument('--color', '-c', type=str, required=True, choices=["red", "black", "yellow"], help="ePaper display color")
args = parser.parse_args()
color = args.color
inky_display = InkyPHAT(color)
inky_display.set_border(inky_display.BLACK)

#Scrapes SpaceFlightNow.com's launch schedule. (Thank you)
res = requests.get("https://spaceflightnow.com/launch-schedule/")
if res.status_code == 200:
	soup = BeautifulSoup(res.content, "lxml")
	print("Website loaded")
else:
	exit("website did not load")

def get_data(data,i):
	"""
	data=the typenof data you want. i.e. launchdate
	i=which launch
	"""
	output = soup.select(data)
	return(output[i].text)


#Loads the background and prints the text on top
fontsize = 16
font = ImageFont.truetype("resources/Amble-Regular.ttf", fontsize)

img = Image.open("resources/launchbackground.png")
draw = ImageDraw.Draw(img)



draw.text((2, 2), "Next Launch: " + get_data(".mission",0).split(" •")[0], inky_display.WHITE, font)
draw.text((2, 26), get_data(".mission",0).split("• ")[1], inky_display.BLACK, font)
draw.text((2, 52), get_data(".launchdate",0) + " @ " + get_data(".missiondata",0).split("(")[1].split("EDT")[0], inky_display.BLACK, font)
draw.text((2, 78), get_data(".missiondata",0).split("site: ")[1], inky_display.BLACK, font)

#Sends the image to the inky pHat
print("Sending image to display")
inky_display.set_image(img)
inky_display.show()
