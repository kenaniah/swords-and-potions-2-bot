import gc
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

Config.wait_interval_secs = 0.2

# Figure out which window to use
switch_to('Edgebee')

# Global definitions go here
employees = glob.glob("employees/*.png")

# Array of things that should always be clicked
always_click = [
	"buttons/closebtn.png", 
	"buttons/closecomponentmissing.png", 
	"buttons/closeitemselect.png", 
	"buttons/closeitembroken.png",
	"buttons/ok.png",
	"buttons/small-ok.png",  # needed for achievements
	"buttons/small-ok-2.png",  # needed for can't select items
	"buttons/next.png", 
	"buttons/start.png",
	"customer-interactions/refuse.png",
	"customer-interactions/sorry.png",
	"customer-interactions/ok.png" # needed for adventures
]

customers = glob.glob("customers/*.png")
suggest = "customer-interactions/suggest.png"
customer_interactions = [
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
def clickImage(img, similarity = 0.75): #can not go higher than 0.8 due to close item select button
	
	# Determine if we're going to sleep after click
	sleepy = 0
	if img in sleep_for:
		sleepy = 0.75
		
	is_suggestion = img == suggest
	
	# Convert to an image
	found = True
	if img == str(img):
		if img == "buttons/next.png":
			similarity = 0.5
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

# Checks whether an item was built
def wasSuccessful():
	return not (clickImage("buttons/ok.png") or clickImage("buttons/closecomponentmissing.png"))

# Attempts to interact with an employee
def employeeInteraction(loop=True):
	
	# Check for employees
	found = False
	for img in employees:
		
		if clickImage(img):
			
			if not Image("employee-interactions/empty-queue.png", 0.75).exists():
				# This employee is already building something
				clickImage("buttons/closeitemselect.png")
				continue
				
			# Otherwise attempt to build a random item
			targets = find_all(Image("lvl-target.png"))
			random.shuffle(targets)
			while len(targets):
				target = targets.pop()
				if target.y > 600: 
					continue # Don't count level targets that are too low
				print "attempting to build " + str(target)
				if clickImage(target):
					if wasSuccessful():
						found = True
						if not loop:
							return found
						break
				
			# Time to give up
			clickImage("buttons/closeitemselect.png")
			clickImage("buttons/closeresource.png")
			
	return found

# Attempts to interact with customers
def customerInteraction():
	found = False
	# Search for customer
	for img in customers:
		if clickImage(img):
			if not Image("customer-interactions/check-if-opened.png").exists():
				clickImage("buttons/closeitemselect.png")
				clickImage("buttons/closeresource.png")
				clickImage("buttons/closeconstruction.png")
				continue
			found = True
			# Interact with customer
			for img in customer_interactions:
				if clickImage(img, 0.95):
					break
			if random.randint(0, 1):
				# Check for an employee again
				employeeInteraction(loop=False)
			
	return found

# Attempts to suggest an item to the customer
def suggestSomething():
	
	# Attempt to build something that we're out of
	targets = find_all(Image("lvl-target.png"))
	while len(targets):
		target = targets.pop()
		if target.y > 600: 
			continue # Don't count level targets that are too low
		print "attempting to suggest " + str(target)
		if clickImage(target):
			if not clickImage("buttons/small-ok.png"):
				return True

# Main script execution
print "Now starting..."

while True:
	
	# Keep clicking on employees when available
	employeeInteraction(loop=True)
	
	# Keep clicking on customers when available
	loop = 0
	while customerInteraction():
		loop = loop + 1
		employeeInteraction(loop=False) # Check for an employee again
		if loop > 4:
			break
		pass
	
	# Check for other buttons and such only if nothing else matched
	for img in always_click:
		clickImage(img)
	
	while clickImage("buttons/done.png"):
		pass
	
	print "Garbage collected " + str(gc.collect()) + " objects"