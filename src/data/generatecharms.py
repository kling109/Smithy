# Smithy
# generatecharms.py
#
# Last Date Modified: 04/16/2021
#
# Description:
# A testing file that allows the user to produce a random set of charms.

import sys
from smithybase import SmithyDB
from faker import Faker

PASSFILE = "../../../gcppassfile.txt"

def gen_charms(n: int):
    """
    Generate a set of n random valid charms.

    :param n: The number of charms to generate.
    :return: A dictionary of charms
    """
    sm = SmithyDB(PASSFILE)
    Faker.seed(0)
    fake = Faker()
    charms = {}
    for i in range(n):
        name = "test" + fake.pystr(min_chars=5, max_chars=10)
        uid = fake.pyint(min_value=pow(10, 17), max_value=pow(10, 18)) # Discord user Id's are 17 or 18 digits long
        sslots = fake.pyint(min_value=0, max_value=3)
        mslots = fake.pyint(min_value=0, max_value=3)
        lslots = fake.pyint(min_value=0, max_value=3)
        num_skills = fake.pyint(min_value=1, max_value=4)
        skills = []
        for _ in range(num_skills):
            skillnu = fake.pyint(min_value=1, max_value=104)
            skillva = fake.pyint(min_value=1, max_value=sm.get_skill(skillnu)[0][2])
            skills.append((skillnu, skillva))

        charms["Charm " + str(i)] = {}
        charms["Charm " + str(i)]["name"] = name
        charms["Charm " + str(i)]["uid"] = uid
        charms["Charm " + str(i)]["sslots"] = sslots
        charms["Charm " + str(i)]["mslots"] = mslots
        charms["Charm " + str(i)]["lslots"] = lslots
        for j in range(num_skills):
            charms["Charm " + str(i)]["skillnum" + str(j+1)] = skills[j][0]
            charms["Charm " + str(i)]["skillval" + str(j+1)] = skills[j][1]
        for k in range(num_skills, 4):
            charms["Charm " + str(i)]["skillnum" + str(k+1)] = None
            charms["Charm " + str(i)]["skillval" + str(k+1)] = 0

    return charms


def write_charms(charms: dict, filename: str):
    """
    Write a dictionary describing charms to a tsv file.

    :param charms: A dictionary specifying the charms
    :param filename: The name of the file to write to
    :return: None
    """
    sm = SmithyDB(PASSFILE)
    with open(filename, 'w') as testcharms:
        cols = "Name\tUserId\tSlots\tSkill1\tSkill2\tSkill3\tSkill4\n"
        testcharms.write(cols)
        for ch in charms.values():
            name = ch["name"]
            usr = ch["uid"]
            slots = (str(ch["sslots"])+str(ch["mslots"])+str(ch["lslots"])).replace("0", "-")
            skills = []
            for i in range(1, 5):
                if ch["skillnum"+str(i)] != None:
                    skilldet = sm.get_skill(ch["skillnum"+str(i)])[0]
                    skills.append(skilldet[1] + " Lv. " + str(ch["skillval"+str(i)]))
                else:
                    skills.append("")
            line = "{}\t{}\t{}\t{}\t{}\t{}\n".format(name, usr, slots, skills[0], skills[1], skills[2], skills[3]).strip()
            testcharms.write(line + "\n")


if __name__ == "__main__":
    path = sys.argv[1]
    x = sys.argv[2]
    try:
        numcharms = int(x)
        if path[-4:] != ".tsv":
            print("Warning: The values will be output as a tab-separated value file.")
            print("It is recommended to name your file 'filename.tsv' to avoid confusion.")
        ch = gen_charms(numcharms)
        write_charms(ch, path)
        print("Program exited successfully.")
    except ValueError as verr:
        print("Error: The second input is not a valid number of charms.")
        print("The input should be formatted as 'python gencharms.py [path] [numcharms]")