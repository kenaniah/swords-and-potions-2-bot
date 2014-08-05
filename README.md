# Swords and Potions 2 Bot

This was a small personal project I started to automate the (sometimes) mundane task of playing [SNP2](http://www.edgebee.com/games?id=5).

## Environment

I initially wrote it for Python 2.7, but you can easily run it in Python 3.x by converting it with the [2to3](https://docs.python.org/2/library/2to3.html) tool first.

There is a dependency on [Automa](http://www.getautoma.com/download), which unfortunately is not free software (currently they offer a 30-day trial). I assume you install Automa to `C:\automa`, but you can easily change that path in the script.

The bot requires that a browser tab with `Edgebee` in the title be open. You should already be logged into the game before starting the bot. If you would like to play the game from Kongregate, simply change the name of the window in the `switch_to()` call.

The bot is designed to be run from the command line, so a simple `python snp2-bot.py` will suffice. 

All relevant images are loaded at startup, so swapping out images requires a restart of the bot.

## How it Works

------

Due to Automa's speed, all of your customers will end up mad after a few minutes when you hit the midgame. But it's a small price to pay for waking up to millions after a single night. 

## Tips

The bot essentially uses Automa's image recognition features to click on stuff. Most of the images provided were taken at a zoom of 125%, so if you play the game at the normal 100% zoom instead, some of the images may need to be retaken or scaled to match. 

To get the best performance out of the bot, your browser window should be sized down to show only the contents of the flash game. A smaller window size means faster scans when attempting image searches.

Make sure you only include the images you need and place any extras in an ignore subdirectory. This will also aid in the bot's performance.
