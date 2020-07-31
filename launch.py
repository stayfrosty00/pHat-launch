#test

import argparse
import time

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

fontsize = 16
font = ImageFont.truetype("resources/Amble-Regular.ttf", fontsize)

#Scrapes SpaceFlightNow.com's launch schedule. (Thank you)
res = requests.get("https://spaceflightnow.com/launch-schedule/")
if res.status_code == 200:
	soup = BeautifulSoup(res.content, "lxml")
	print("Website loaded")
else:
	exit("website did not load")

#Prints the raw code from website
#print(soup.prettify())

def get_data(data,i):
	"""
	data=the type of data you want. (.launchdate, .mission, .missiondata)
	i=launch number
	"""
	output = soup.select(data)
	#try:
	#	output.replace("TBD","(TBDEDTL")
	return(output[i].text)

def draw_data(i):
	"""
	creates the image that will later be sent to the display
	i=launch number
	"""
	draw.text((2, 2), "Next Launch: " + get_data(".mission",i).split(" •")[0], inky_display.WHITE, font)
	draw.text((2, 26), get_data(".mission",i).split("• ")[1], inky_display.BLACK, font)
	try:
		draw.text((2, 52), get_data(".launchdate",i) + " @ " + get_data(".missiondata",i).split("(")[1].split("EDT")[0], inky_display.BLACK, font)
	except IndexError:
		draw.text((2, 52), get_data(".launchdate",i) + " @ " + "TBD", inky_display.BLACK, font)
	draw.text((2, 78), get_data(".missiondata",i).split("site: ")[1], inky_display.BLACK, font)

for b in range(5):
	"""Calls on functions to get data and draw image, then sends image to the Inky pHat"""
	img = Image.open("resources/launchbackground.png")
	draw = ImageDraw.Draw(img)
	draw_data(b)
	print("Sending image " + str(b+1) + " to display")
	inky_display.set_image(img)
	inky_display.show()
	#time.sleep(5)
