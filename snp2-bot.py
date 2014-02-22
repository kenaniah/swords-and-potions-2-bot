import glob
import os
import random
import signal
import sys
import time

def signal_handler(signum, frame):
	print "Now exiting..."
	exit()

signal.signal(signal.SIGINT, signal_handler)

# Environment setup
os.chdir(os.path.dirname(__file__))
sys.path.append(r"C:\automa\library.zip")
from automa.api import *

Config.wait_interval_secs = 0.15

# Figure out which window to use
switch_to('Edgebee')

# Global definitions go here
employees = glob.glob("employees/*.png")

# Array of things that should always be clicked
alwaysClick = [
	"buttons/closebtn.png", 
	"buttons/closecomponentmissing.png", 
	"buttons/closeitemselect.png", 
	"buttons/closeitembroken.png",
	"buttons/ok.png", 
	"buttons/next.png", 
	"buttons/start.png"
]

customers = glob.glob("customers/*.png")
suggest = "customer-interactions/suggest.png"
customerInteractions = [
	"customer-interactions/buy.png",
	"customer-interactions/sell.png",
	"customer-interactions/thanks.png",
	suggest,
	"customer-interactions/refuse.png",
	"customer-interactions/sorry.png"
]

sleep_for = [
	"buttons/start.png",
	"buttons/next.png",
	"buttons/done.png"
]

# Returns whether the given image was clicked 
def clickImage(img, similarity = 0.75):
	
	# Determine if we're going to sleep after click
	sleepy = 0
	if img in sleep_for:
		sleepy = 1.5
		
	is_suggestion = img == suggest
	
	# Convert to an image
	found = True
	if img == str(img):
		img = Image(img, similarity)
		found = img.exists()
		
	# Search for the image
	print "check for image " + str(img)
	if found:
		print "found image " + str(img)
		try:

			# Click it
			click(img)
			
			# Handle customer suggestions
			if is_suggestion:
				suggestSomething()
			
			if sleepy:
				time.sleep(sleepy)
		except Exception as e:
			print e
			print "couldn't click it"
			found = False
	return found

# Attempts to interact with an employee
def employeeInteraction():
	
	# Checks whether an item was built
	def wasBuilt():
		return not (clickImage("buttons/ok.png") or clickImage("buttons/closecomponentmissing.png"))
	
	# Check for employees
	for img in employees:
		
		if clickImage(img):
			
			# Attempt to build something that we're out of
			outOf = find_all(Image("out-of-stock.png"))
			while len(outOf):
				target = outOf.pop()
				print "attempting to build (out of stock) " + str(target)
				if clickImage(target) and wasBuilt():
					return True
				
			# Otherwise attempt to build a random item
			lvlTargets = find_all(Image("lvl-target.png"))
			random.shuffle(lvlTargets)
			while len(lvlTargets):
				target = lvlTargets.pop()
				print "attempting to build (in stock) " + str(target)
				if clickImage(target) and wasBuilt():
					return True
				
			# Time to give up
			clickImage("buttons/closeitemselect.png")
			
	return False

# Attempts to interact with customers
def customerInteraction():
	found = False
	# Search for customer
	for img in customers:
		if clickImage(img):
			if not Image("customer-interactions/check-if-opened.png").exists():
				continue
			found = True
			# Interact with customer
			for img in customerInteractions:
				if clickImage(img, 0.95):
					break
	return found

# Attempts to suggest an item to the customer
def suggestSomething():
	
	time.sleep(1)
	
	# Otherwise attempt to build a random item
	lvlTargets = find_all(Image("lvl-target.png"))
	print "there are " + str(len(lvlTargets)) + " suggestions available"
	while len(lvlTargets):
		if clickImage(lvlTargets.pop()):
			return

# Main script execution
print "Now starting..."

while True:
	
	# Keep clicking on employees when available
	while employeeInteraction():
		pass
	
	# Keep clicking on customers when available
	while customerInteraction():
		employeeInteraction() # Check for an employee again
		pass
	
	# Check for other buttons and such only if nothing else matched
	for img in alwaysClick:
		clickImage(img)
	
	while clickImage("buttons/done.png"):
		pass