# Smithy
# bot.py
#
# Last Date Modified: 05/11/2021
#
# Description:
# The discord bot driver method.

# bot.py
import os
import re
import csv

import discord
from discord.ext import commands
from dotenv import load_dotenv
from queryprocessor import QueryProcessor

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

db = QueryProcessor('../../passfile.txt')


def slot_format(slotsize: int):
    if slotsize == 1:
        return "S"
    elif slotsize == 2:
        return "M"
    elif slotsize == 3:
        return "L"
    else:
        return "-"


def slot_unformat(slotsize: int):
    if slotsize == "S":
        return 1
    elif slotsize == "M":
        return 2
    elif slotsize == "L":
        return 3
    else:
        return 0


@bot.command(name='build', help="Constructs an armor set based on given parameters. \nFormatted as "
                                "'!build [skill 1 name] [skill 1 value], [skill 2 name] [skill 2 value], ...'\n"
                                "Flags:\n"
                                "-csv: Return the results in a CSV file. \n"
                                "-depth [number]: Changes the search depth.  May provide better results, but will run slower.\n"
                                "-many [number]: Changes the number of armor sets returned.")
async def build_armor(ctx, *args):
    uid = ctx.message.author.id
    args = ' '.join(args)
    flags = re.findall(r"-([a-z]+)?( ?[0-9]+)?", args)
    args_no_flags = re.sub(r"-([a-z]+)?( ?[0-9]+)?", '', args)
    skills = re.split(r"[0-9]+", args_no_flags)
    skills = [s.strip(" ,;-") for s in skills if s.strip(" ,;-") != ""]
    skill_vals = re.findall(r"[0-9]+", args_no_flags)

    print_csv = False
    res_len = 1
    search_depth = 4
    try:
        for f in flags:
            if f[0] == "csv":
                print_csv = True
            elif f[0] == "depth":
                search_depth = int(f[1].strip())
            elif f[0] == "many":
                res_len = int(f[1].strip()) if f[1] != "" else 5
    except ValueError as err:
        await ctx.send("There was an error with your flag values.  Be sure to use integer values for flag arguments.")
        return

    if len(skills) != len(skill_vals) or len(skills) == 0:
        response = "You seem to have made an error with the inputs."
        await ctx.send(response)
        return

    skill_set = {skills[i]: int(skill_vals[i]) for i in range(len(skills))}
    results = db.search_armor_set(skill_set, uid, num_results=search_depth, returned_results=res_len)

    if len(results) == 0:
        response = "This query returned no results.  Have you added a charm to the database?"
        await ctx.send(response)
        return

    if print_csv:
        csv_file = "armorsets.csv"
        try:
            with open(csv_file, "w") as pf:
                keys = results[0].keys()
                dict_writer = csv.DictWriter(pf, keys)
                dict_writer.writeheader()
                dict_writer.writerows(results)
            await ctx.send("Here's the {} build results as a CSV file.".format(res_len))
            await ctx.send(file=discord.File(r'armorsets.csv'))
            return
        except IOError as err:
            await ctx.send("An error occurred when writing the csv file.")
            return

    response = ""
    for i in range(len(results)):
        res = results[i]
        base_resp = """**Armor Set {}:**\n------------\n""".format(i+1)
        base_helm = """Helm: {}\n""".format(res["helm"]["name"])
        base_chest = """Chest: {}\n""".format(res["chest"]["name"])
        base_vambraces = """Vambraces: {}\n""".format(res["vambraces"]["name"])
        base_faulds = """Faulds: {}\n""".format(res["faulds"]["name"])
        base_greaves = """Greaves: {}\n""".format(res["greaves"]["name"])
        base_charm = """Charm: {}\n""".format(res["charm"]["name"])
        deco_helm = ""
        deco_chest = ""
        deco_vambraces = ""
        deco_faulds = ""
        deco_greaves = ""
        deco_charms = ""
        for d in res["helm"]["decos"]:
            deco_helm += "- {}\n".format(d)
        for d in res["chest"]["decos"]:
            deco_chest += "- {}\n".format(d)
        for d in res["vambraces"]["decos"]:
            deco_vambraces += "- {}\n".format(d)
        for d in res["faulds"]["decos"]:
            deco_faulds += "- {}\n".format(d)
        for d in res["greaves"]["decos"]:
            deco_greaves += "- {}\n".format(d)
        for d in res["charm"]["decos"]:
            deco_charms += "- {}\n".format(d)
        base_totals = """------------\n**Totals**: """
        for ski, skv in res["totals"].items():
            base_totals += "{}: {}, ".format(ski, skv)

        response += (base_resp + base_helm + deco_helm + base_chest + deco_chest + base_vambraces + deco_vambraces
                    + base_faulds + deco_faulds + base_greaves + deco_greaves + base_charm + deco_charms
                    + base_totals).strip(", ")
        if i < len(results)-1:
            response += "\n \n"

    await ctx.send(response)


@bot.command(name="show", help="Displays values for a specific equipment piece. \n"
                               "Formatted as '!show [helm/chest/vambraces/faulds/greaves/charms]'\n"
                               "Flags:\n"
                               "-count [number]: The number of entries to display.\n"
                               "-skill [skillname]: Display only entries with a specific skill.")
async def display(ctx, *args):
    args = ' '.join(args)
    flags = re.findall(r"-([a-z]+)?( ?[0-9a-zA-Z ]+)?", args)
    args_no_flags = re.sub(r"-([a-z]+)?( ?[0-9a-zA-Z ]+)?", '', args)
    armor_type = args_no_flags.split(',')[0].strip()

    display_number = 3
    skill_to_show = None

    try:
        for f in flags:
            if f[0] == "count":
                display_number = int(f[1].strip())
            elif f[0] == "skill":
                skill_to_show = f[1].strip()
    except ValueError as err:
        await ctx.send("There was an error with your flag values.  Be sure to use integer values for numerical flag arguments.")
        return

    results = db.display(ctx.message.author.id, armor_type, skill_to_show)

    response = ""
    if len(results) == 0:
        if armor_type == "charms" and skill_to_show is None:
            response = "You haven't added any charms to the database.  Try using '!addcharm [name], [slot1], [slot2], [slot3]," \
                       " [skill 1 name] [skill 1 value], [skill 2 name] [skill 2 value] ....' to add a charm."
        elif skill_to_show is not None:
            response = "There are no results for {} with the skill {}.".format(armor_type, skill_to_show)
        else:
            response = "There seems to be an error with the paramteters you gave.  Use '!help show' to get more " \
                       "information about the available parameters."
        await ctx.send(response)
        return

    i = 1
    for piece in results[0:min(display_number, len(results))]:
        base_piece = """**{} {}: {}** \n------------\nSlots: {} {} {}""".format(armor_type.capitalize(), i, piece["name"],
                                                                 slot_format(piece["slot1"]), slot_format(piece["slot2"]),
                                                                 slot_format(piece["slot3"]))
        for key, val in piece["skills"].items():
            base_piece += """\n- {} {}""".format(key, val)

        response += base_piece + "\n \n"
        i += 1
    await ctx.send(response)
    return


@bot.command(name="addcharm", help="Add a new charm given its specifications. \nFormatted as '!addcharm [name], [slot1],"
                                   " [slot2], [slot3], [skill 1 name] [skill 1 value], [skill 2 name] [skill 2 value], ....'")
async def add_charms(ctx, *args):
    uid = ctx.message.author.id
    args = (' '.join(args)).split(',')
    if len(args) < 5:
        response = "The command was given an insufficient number of arguments.  Use '!help' to find a list of commands."
    else:
        slot1 = slot_unformat(args[1]) if slot_unformat(args[1]) in (1, 2, 3) else 0
        slot2 = slot_unformat(args[2]) if slot_unformat(args[2]) in (1, 2, 3) else 0
        slot3 = slot_unformat(args[3]) if slot_unformat(args[3]) in (1, 2, 3) else 0
        skills = []
        skillvals = []
        for i in range(4, len(args)):
            skill = re.split("[0-9]+", args[i])
            skill = [s.strip(" ,;-") for s in skill if s.strip(" ,;-") != ""]
            skillval = re.findall("[0-9]+", args[i])
            skills.append(skill[0])
            skillvals.append(int(skillval[0]))
        for i in range(len(args), 8):
            skills.append(None)
            skillvals.append(0)

        new_charm = {"name": args[0], "slot1": slot1, "slot2": slot2, "slot3": slot3, "skill1Name": skills[0],
                     "skill1Val": skillvals[0], "skill2Name": skills[1], "skill2Val": skillvals[1],
                     "skill3Name": skills[2], "skill3Val": skillvals[2], "skill4Name": skills[3], "skill4Val": skillvals[3]}
        db.add_user_charm(new_charm, uid)
        response = "Added the charm '{}' to the database.".format(args[0])

    await ctx.send(response)


@bot.command(name="deletecharm", help="Remove a charm you've previously added to the database. \nFormatted as '!deletecharm"
                                      " [name]'")
async def delete_charm(ctx, *args):
    uid = ctx.message.author.id
    args = (' '.join(args)).split(',')
    db.remove_user_charm(args[0], uid)
    await ctx.send("Removed charm {} from the database.".format(args[0]))


@bot.command(name="modifycharm", help="Modify a value of a charm in the database. \nFormatted as '!modifycharm"
                                      " [name], [slots/skill 1/skill 2/skill 3/skill 4], [new value 1], [new value 2], ...'")
async def modify_charm(ctx, *args):
    uid = ctx.message.author.id
    args = (' '.join(args)).split(',')
    name = args[0].strip()
    response = "An error has occurred."
    if args[1].strip() == 'slots':
        if len(args) != 5:
            response = "An improper set of arguments was given. To modify slots, use the schema '!modifycharm " \
                       "[name], slots, [slot 1 value], [slot 2 value], [slot 3 value]'"
        else:
            slot_vals = [slot_unformat(args[2].strip()), slot_unformat(args[3].strip()), slot_unformat(args[4].strip())]
            db.modify_user_charm(name, uid, 'slots', slot_vals)
            response = "Successfully modified the number of slots on charm {}.".format(name)
    elif args[1].strip()[0:5] == 'skill':
        if len(args) != 4:
            response = "An improper set of arguments was given.  To modify a skill, use the schema '!modifycharm " \
                       "[name], [skill 1/skill 2/skill 3/skill 4], [new skill name], [new skill value]"
        else:
            col_num = args[-1]
            db.modify_user_charm(name, uid, 'skill', [col_num, args[3], args[4]])
            response = "Successfully modified skill {} of charm {}.".format(col_num, name)

    await ctx.send(response)


bot.run(TOKEN)
