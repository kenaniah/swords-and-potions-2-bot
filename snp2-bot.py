import glob
import os
import random
import signal
import sys

def signal_handler(signum, frame):
	print "Now exiting..."
	exit()

signal.signal(signal.SIGINT, signal_handler)

# Environment setup
os.chdir(r"C:\automa\Kenaniah.automa")
sys.path.append(r"C:\automa\library.zip")
from automa.api import *

# Figure out which window to use
switch_to('Edgebee')

# Global definitions go here
employees = {
	"shopkeeper": ["employees/shopkeeper-1.png", "employees/shopkeeper-2.png"],
	"carpenter": ["employees/carpenter-1.png", "employees/carpenter-2.png"],
	"blacksmith": ["employees/blacksmith-1.png", "employees/blacksmith-2.png"],
	"druid": ["employees/druid-1.png", "employees/druid-2.png"]
}

# Array of things that should always be clicked
alwaysClick = [
	"buttons/closebtn.png", 
	"buttons/closecomponentmissing.png", 
	"buttons/closeitemselect.png", 
	"buttons/closeitembroken.png",
	"buttons/ok.png", 
	"buttons/next.png", 
	"buttons/start.png", 
	"buttons/done.png"
]

customers = glob.glob("customers/*.png")
suggest = "customer-interactions/suggest.png"
customerInteractions = [
	"customer-interactions/buy.png",
	"customer-interactions/sell.png",
	"customer-interactions/thanks.png",
	#suggest,
	"customer-interactions/refuse.png"
]

# Returns whether the given image was clicked 
def clickImage(img, similarity = 0.7):
	if not isinstance(img, Image):
		img = Image(img, similarity)
	found = img.exists()
	print "checking " + str(img)
	if found:
		print "found image " + str(img)
		try:
			#hover(img)
			click(img)
		except Exception as e:
			print e
			print "couldn't click it"
			found = False
	return found

# Attempts to interact with an employee
def employeeInteraction():
	# Check for employees
	for employee, imgArray in employees.items():
		for img in imgArray:
			if clickImage(img):
				# Attempt to build something that we're out of
				if clickImage("out-of-stock.png"):
					break
				# Otherwise attempt to build a random item
				lvlTargets = find_all(Image("lvl-target.png"))
				random.shuffle(lvlTargets)
				while len(lvlTargets):
					target = lvlTargets.pop()
					if clickImage(lvlTargets[target]):
						# Ensure we ended up building it
						if not clickImage("buttons/ok.png"):
							break
						
				

# Main script execution
print "Now starting..."

while True:

	# Close whatever may be open
	for img in alwaysClick:
		clickImage(img)
			
	# Click on customers
	for img in customers:
		if clickImage(img):
			break;
	
	# Interact with customer
	for img in customerInteractions:
		if clickImage(img, 0.95):
			break	
	
	# Interact with employees
	employeeInteraction()
	