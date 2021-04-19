# Smithy
# loaddata.py
#
# Last Date Modified: 04/16/2021
#
# Description:
# A basic loader file that moves armor and skill data from a .csv file
# into the database.

from os import path
import sys
from smithybase import SmithyDB
import re

PASSFILE = "../../../gcppassfile.txt"

HELM_NAMES = ['Helm', 'Vertex', 'Vizor', 'Mask', 'Hat', 'Scarf', 'Hood', 'Visage', 'Headgear',
              'Hair-tie', 'Brain', 'Lobos', 'Chaoshroom', 'Archbun', 'Headdress', 'Feather']
CHEST_NAMES = ['Mail', 'Thorax', 'Ribplate', 'Vest', 'Garb', 'Cover', 'Jacket',
               'Cloak', 'Robe', 'Muscle', 'Breastplate', 'Suit', 'Plate', 'Archplate', 'Haori', 'Torso']
VAMBRACE_NAMES = ['Braces', 'Brachia', 'Creeper', 'Gloves', 'Sleeves', 'Branch',
                  'Hope', 'Grip', 'Pauldrons', 'Vambraces', 'Gauntlets', 'Prayer', 'Kote', 'Armguards']
FAULD_NAMES = ['Coil', 'Elytra', 'Folia', 'Obi', 'Sash', 'Tassets', 'Bowels', 'Fauld', 'Belt']
GREAVE_NAMES = ['Greaves', 'Crura', 'Roots', 'Shinguards', 'Boots', 'Leggings',
                'Pants', 'Sandals', 'Hakama', 'Heel', 'Ibushi', 'Feet', 'Narwa']

def load_skills(sm: SmithyDB, filepath: str):
    """
    Loads skill information from a properly-formatted tsv file, then adds it to the
    database.

    :param sm: The database object to operate on.
    :param filepath: The path to the desired .csv file.
    :return:
    """
    if path.exists(filepath):
        with open(filepath) as skilltsv:
            columns = skilltsv.readline()
            data = skilltsv.readlines()

        skills = []
        skilldesc = []
        for entry in data:
            entry = entry.strip().split('\t')
            name = entry[0]
            skilllv = entry[2][0]
            skills.append((name, skilllv))

        sm.add_skills(skills)

        for entry in data:
            entry = entry.strip().split('\t')
            name = entry[0]
            skillnu = sm.get_skill_by_name(name)
            desc = entry[3]
            skilldesc.append((skillnu[0][0], desc))

        sm.add_skill_desc(skilldesc)

    else:
        print("The path to the .tsv file does not exist.")

def load_armor(sm: SmithyDB, filepath: str):
    """
    Loads in armor data from a tsv file.  Sorts loaded armors by type, then
    adds each to their repective tables.

    :param sm: The database object to operate on.
    :param filepath: a path to the armor tsv file
    :return: None
    """
    if path.exists(filepath):
        with open(filepath) as armortsv:
            columns = armortsv.readline()
            data = armortsv.readlines()

        helms = []
        chests = []
        vambraces = []
        faulds = []
        greaves = []
        for entry in data:
            entry = entry.strip().split('\t')
            name = entry[0]
            slots = {i : entry[1].count(i) for i in set(entry[1])}
            sslots = slots.get('1', 0)
            mslots = slots.get('2', 0)
            lslots = slots.get('3', 0)
            skills = []

            if len(entry) > 2:
                for i in range(2, len(entry)):
                    skni = entry[i].split('Lv.')[0].strip()
                    skidi = sm.get_skill_by_name(skni)
                    skvi = entry[i].split('Lv.')[1].strip()
                    skills.append((skidi[0][0], skvi))
            for i in range(6 - len(entry)):
                skills.append((None, 0))

            armtype = re.sub(r" \bS\b", "", name).strip().split(' ')[-1]
            if armtype in HELM_NAMES:
                helms.append((name, sslots, mslots, lslots, skills[0][0],
                              skills[0][1], skills[1][0], skills[1][1],
                              skills[2][0], skills[2][1], skills[3][0], skills[3][1]))
            elif armtype in CHEST_NAMES:
                chests.append((name, sslots, mslots, lslots, skills[0][0],
                              skills[0][1], skills[1][0], skills[1][1],
                              skills[2][0], skills[2][1], skills[3][0], skills[3][1]))
            elif armtype in VAMBRACE_NAMES:
                vambraces.append((name, sslots, mslots, lslots, skills[0][0],
                               skills[0][1], skills[1][0], skills[1][1],
                               skills[2][0], skills[2][1], skills[3][0], skills[3][1]))
            elif armtype in FAULD_NAMES:
                faulds.append((name, sslots, mslots, lslots, skills[0][0],
                               skills[0][1], skills[1][0], skills[1][1],
                               skills[2][0], skills[2][1], skills[3][0], skills[3][1]))
            elif armtype in GREAVE_NAMES:
                greaves.append((name, sslots, mslots, lslots, skills[0][0],
                               skills[0][1], skills[1][0], skills[1][1],
                               skills[2][0], skills[2][1], skills[3][0], skills[3][1]))
            else:
                print("This armor type is not yet handled: {}".format(armtype))
                return

        sm.add_armors('helm', helms)
        sm.add_armors('chest', chests)
        sm.add_armors('vambraces', vambraces)
        sm.add_armors('faulds', faulds)
        sm.add_armors('greaves', greaves)

    else:
        print("The path to the .tsv file does not exist.")

def load_charms(sm: SmithyDB, filepath: str):
    """
    A method to add a set of charms given by a tsv file to the charm database.

    :param sm: The database object to operate on.
    :param filepath: a path to the charm tsv file
    :return:
    """
    if path.exists(filepath):
        with open(filepath) as charmtsv:
            columns = charmtsv.readline()
            data = charmtsv.readlines()

    charms = []
    for entry in data:
        entry = entry.strip().split('\t')
        name = entry[0]
        usrid = entry[1]
        slots = {i: entry[2].count(i) for i in set(entry[1])}
        sslots = slots.get('1', 0)
        mslots = slots.get('2', 0)
        lslots = slots.get('3', 0)
        skills = []
        if len(entry) > 3:
            for i in range(3, len(entry)):
                skni = entry[i].split('Lv.')[0].strip()
                skidi = sm.get_skill_by_name(skni)
                skvi = entry[i].split('Lv.')[1].strip()
                skills.append((skidi[0][0], skvi))
        for i in range(7 - len(entry)):
            skills.append((None, 0))

        sm.add_charm(name, usrid, sslots, mslots, lslots, skills[0][0],
                       skills[0][1], skills[1][0], skills[1][1], skills[2][0],
                       skills[2][1], skills[3][0], skills[3][1])

def load_decos(sm: SmithyDB, filepath: str):
    """
    A method to add a list of decorations from a given file into the deco table

    :param sm: The database object to operate on.
    :param filepath: a path to the file to use.
    :return: None
    """
    if path.exists(filepath):
        with open(filepath) as decotsv:
            columns = decotsv.readline()
            data = decotsv.readlines()

    decos = []
    for entry in data:
        entry = entry.strip().split('\t')
        name = entry[0]
        slotSize = entry[1]
        skni = entry[2].split('Lv.')[0].strip()
        skidi = sm.get_skill_by_name(skni)[0][0]
        skvi = entry[2].split('Lv.')[1].strip()
        decos.append((name, slotSize, skidi, skvi))

    sm.add_deco(decos)

if __name__ == "__main__":
    loadtype = sys.argv[1]
    loadpath = sys.argv[2]
    sm = SmithyDB(PASSFILE)
    if loadtype == "skill":
        load_skills(sm, loadpath)
    elif loadtype == "armor":
        load_armor(sm, loadpath)
    elif loadtype == "charm":
        load_charms(sm, loadpath)
    elif loadtype == "deco":
        load_decos(sm, loadpath)
    else:
        print("The given type of element cannot be loaded.")
        print("Input should be of the form, 'python loaddata.py [type] [path]")
        print("Available types: 'armor', 'skill', 'charm'")
    print("Program exited correctly.")