# Smithy
A discord bot for displaying armor builds for Monster Hunter Rise via a Discord bot.

# Running Instructions (Assignment 4):
Move to the `src/data` folder, then run the command `python generatecharms.py [path to output file] [number of charms]`.  This will generate a tab-separated value file at the path given with the desired number of charms.  Then, running `python loaddata.py charm [path to input file]` with the path of the input file being the previously generated charms will load those charms into the database.
