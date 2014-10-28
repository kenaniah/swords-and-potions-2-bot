# Swords and Potions 2 Bot

This was a small personal project I started to automate the (sometimes) mundane task of playing [SNP2](http://www.edgebee.com/games?id=5). **Please read the FAQ below before opening an issue.**

## Environment

I initially wrote it for Python 2.7, but you can easily run it in Python 3.x by converting it with the [2to3](https://docs.python.org/2/library/2to3.html) tool first.

There is a dependency on [Automa](http://www.getautoma.com/download), which unfortunately is not free software (currently they offer a 30-day trial). I assume you install Automa to `C:\automa`, but you can easily change that path in the script.

The bot requires that a browser tab with `Edgebee` in the title be open. You should already be logged into the game before starting the bot. If you would like to play the game from Kongregate, simply change the name of the window in the `switch_to()` call.

The bot is designed to be run from the command line, so a simple `python snp2-bot.py` will suffice. 

All relevant images are loaded at startup, so swapping out images requires a restart of the bot.

## How it Works

Images are broken down into sub-directories by type:
 * **build-cycles** - should have a subdirectory per worker (builds of items are attempted in alphabetic order of the image names)
 * **buttons** - contains miscellaneous buttons that need to be clicked at certain points
 * **customer-interactions** - contains the images that are clicked when interacting with customers
 * **customers** - mugshots of the customers that visit you (put customers you don't have access to in an ignore subdirectory)
 * **employee-interactions** - you've guessed it...
 * **employees** - mugshots of the workers you are currently using (put the rest in the ignore directory)

### Bot Logic

 1. Attempt to interact with any and all available employees
   1. Attempt to build the next item in the employee's build cycle
   2. Attempt to build a random item upon failure
 2. Attempt to interact with a customer
   1. Buy if possible
   2. Sell if possible. $$profit$$
   3. Suggest an item if possible. $$moar profit$$
   4. Loops up to 8 times if successful
   5. Attempts to check for an employee after handling a customer
 3. Check for other random / unexpected buttons to handle bad clicks, etc.
 4. Attempt to click the done / next day buttons

Due to Automa's speed, all of your customers will end up mad after a few minutes when you hit the midgame. But it's a small price to pay for waking up to millions after a single night. 

## FAQ

<dl>
 <dt>The bot crashes instead of starting. Why?</dt>
 <dd>You are either using the wrong version of Python (Automa is very specific) or the game's window was not found.</dd>
 <dt>Why is the bot not able to find matches for my screenshots?</dt>
 <dd>Screenshot images need to have as little background noise as possible. Automa performs a grey-scale image similarity match, and it is not capable of filtering out backgrounds that are not part of what you are trying to match.</dd>
 <dt>Is there a way to make the bot faster? Image searching seems slow.</dt>
 <dd>Unfortunately Automa does not currently support parallel processing, range-constrained searches, nor the recognition of multiple patterns from a single screenshot. If these are the features you are looking for, you could always fork and rewrite the bot using OpenCV. Good luck (you'll need it).</dd>
 <dt>There's a memory leak / my computer bluescreened</dt>
 <dd>Welcome to Automa. I was able to workaround this by putting the bot on a scheduled task that killed / restarted it every 10 minutes or so.</dd>
</dl>

## Tips

Automa greyscales images, so color differences should not matter. 

Most of the images provided were taken at a zoom of 125%, so if you play the game at the normal 100% zoom instead, some of the images may need to be retaken or scaled to match. 

To get the best performance out of the bot, your browser window should be sized down to show only the contents of the flash game. A smaller window size means faster scans when attempting image searches.

Make sure you only include the images you need and place any extras in an ignore subdirectory. This will also aid in the bot's performance.
