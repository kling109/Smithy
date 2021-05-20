# Smithy
A discord bot for displaying armor builds for Monster Hunter Rise via a Discord bot.

## Running Instructions
The bot requires 2 files to be made; `passfile.txt` and `.env`.  The `.env` file must contain the bot Discord Token and Guild Name for the bot's connection, and should be addedto the `src` folder.  Meanwhile, the passfile should contain the details of the MySQL database connection and should be placed one folder above the `smithy` folder.  This folder should contain 3 values; the IP address of the database, the database username, and the database user password.

After these files are added, start the bot by running `python bot.py`.  You should see the bot connect to your server specified in the `.env` file.

This project is still very much in alpha, and this should all be streamlined in the near future.  Ideally, I would like to allow users to invite the bot to their servers directly, but would need to get a dedicated database server set up for this.
