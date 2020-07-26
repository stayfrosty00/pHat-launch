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



fontsize = 16
font = ImageFont.truetype("/home/pi/.fonts/Amble-Regular.ttf", fontsize)

#Scrapes SpaceFlightNow.com's launch schedule. (Thank you)
res = requests.get("https://spaceflightnow.com/launch-schedule/")
if res.status_code == 200:
	soup = BeautifulSoup(res.content, "lxml")
	mission = (soup.find("span", "mission").text)
	launchdate = (soup.find("span", "launchdate").text)
	launchtimetemp = soup.find("div", "missiondata").get_text()
	timeonly = launchtimetemp.split("(")[1].split("EDT")[0]
	launchsite = launchtimetemp.split("site: ")[1]
else:
	exit("website did not load")

#These print states are used for debugging
#print(mission)
#print(launchdate)
#print(timeonly)
#print(launchsite)

#Loads the background and prints the text on top
fontsize = 16
font = ImageFont.truetype("/home/pi/.fonts/Amble-Regular.ttf", fontsize)

img = Image.open("resources/launchbackground.png")
draw = ImageDraw.Draw(img)

draw.text((2, 2), "Next Launch", inky_display.WHITE, font)
draw.text((2, 25), mission, inky_display.BLACK, font)
draw.text((2, 52), launchdate + " @ " + timeonly, inky_display.BLACK, font)
draw.text((2, 78), launchsite, inky_display.BLACK, font)

#Sends the image to the inky pHat
inky_display.set_image(img)
inky_display.show()
