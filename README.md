# Swords and Potions 2 Bot

This was a small personal project I started to automate the (sometimes) mundane task of playing [SNP2](http://www.edgebee.com/games?id=5).

I initially wrote it for Python 2.7, but you can easily run it in Python 3.x by converting it with the [2to3](https://docs.python.org/2/library/2to3.html) tool first.

There is a dependency on (Automa)[http://www.getautoma.com/download], which unfortunately is not free software. I assume you install Automa to `C:\automa`, but you can easily change that path in the script.

The bot requires that a browser tab with `Edgebee` in the title be open. You should already be logged into the game before starting the bot. If you would like to play the game from Kongregate, simply change the name of the window in the `switch_to()` call.

## How it Works

