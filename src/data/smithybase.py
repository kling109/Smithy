# Smithy
# smithybase.py
#
# Last Date Modified: 04/16/2021
#
# Description:
# A MySQL wrapper class that allows the user to create a database object
# and perform various actions on that database.

import mysql.connector
from os import path


class SmithyDB:
    db = None
    cursor = None

    def __init__(self, info: str):
        if path.exists(info):
            with open(info) as passfile:
                host_name = passfile.readline()
                usr_name = passfile.readline()
                pw = passfile.readline()

            self.db = mysql.connector.connect(
                host=host_name,
                user=usr_name,
                passwd=pw,
                database="armorSkills"
            )
            cn = self.db
            self.cursor = cn.cursor()
        else:
            print("Error: The given path to a password file does not exist.")

    def __del__(self):
        # There appears to be some issue with "weakly reference objects" and the __del__ function.
        pass

    def add_charm(self, name: str, uid: int, sslot: int, mslot: int, lslot: int,
                  skill1id: str, skill1val: int, skill2id: str, skill2val: int,
                  skill3id: str, skill3val: int, skill4id: str, skill4val: int):
        """
        Inserts a charm into the charm database based on function input.

        :param name: Name of the charm
        :param uid: Discord ID of the user adding the charm
        :param sslot: number of small slots on the charm
        :param mslot: number of medium slots on the charm
        :param lslot: number of large slots on the charm
        :param skill1id: id of the first skill
        :param skill1val: number of points of the first skill
        :param skill2id: id of the second skill
        :param skill2val: number of points of the second skill
        :param skill3id: id of the third skill
        :param skill3val: number of points of the third skill
        :param skill4id: id of the fourth skill
        :param skill4val: number of points of the fourth skill
        :return: None
        """
        try:
            self.cursor.execute('INSERT INTO charm(charmName, userId, sslot, mslot, lslot, '
                                'skill1Id, skill1Val, skill2Id, skill2Val, '
                                'skill3Id, skill3Val, skill4Id, skill4Val) '
                                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',
                                (name, uid, sslot, mslot, lslot, skill1id, skill1val,
                                 skill2id, skill2val, skill3id, skill3val, skill4id, skill4val))
            self.db.commit()
        except mysql.connector.Error as err:
            print("Error: {}".format(err))

    def add_armors(self, table: str, armor_list: list):
        """
        A method that allows the user to add a set of armors
        :param table: A string indicating which table to add the elements to.
        :param armor_list: A list of armor elements to add.
        :return: None
        """
        try:
            self.cursor.executemany('INSERT INTO ' + table + '(armorName, sslot, mslot, lslot, '
                                                             'skill1Id, skill1Val, skill2Id, skill2Val, '
                                                             'skill3Id, skill3Val, skill4Id, skill4Val) '
                                                             'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',
                                    armor_list)
            self.db.commit()
        except mysql.connector.Error as err:
            print("Error: {}".format(err))

    def add_skills(self, skill_list: list):
        """
        A method that allows the user to add a set of skills

        :param skill_list: A list of skill elements to add.
        :return: process code; 0 on success, error code on fail.
        """
        try:
            self.cursor.executemany('INSERT INTO skills(skillName, maxLv) '
                                    'VALUES (%s, %s);', skill_list)
            self.db.commit()
        except mysql.connector.Error as err:
            print("Error: {}".format(err))

    def add_skill_desc(self, skill_desc_list: list):
        """
        A method that allows the user to add text descriptions for skills.

        :param skill_desc_list: a list of items to add
        :return: None
        """
        try:
            self.cursor.executemany('INSERT INTO skillDesc(skillId, descText) VALUES (%s, %s);', skill_desc_list)
            self.db.commit()
        except mysql.connector.Error as err:
            print("Error: {}".format(err))

    def add_deco(self, deco_list):
        """
        A method that allows the user to add a list of decorations
        :param deco_list: The list of decorations to add.
        :return: None
        """
        try:
            self.cursor.executemany('INSERT INTO deco(decoName, slotSize, skillId, skillVal) '
                                    'VALUES (%s, %s, %s, %s);', deco_list)
            self.db.commit()
        except mysql.connector.Error as err:
            print("Error: {}".format(err))

    def get_skill_by_name(self, name: str):
        """
        A method that allows the user to search for a skill by name.

        :param name: the name of the skill to search for
        :return: list of query results
        """
        try:
            self.cursor.execute('SELECT * FROM skills WHERE skillName = %s;', (name,))
            records = self.cursor.fetchall()
            return list(records)
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            return []

    def get_skill(self, skId: int):
        """
        A method that allows the user to query a skill by its id.

        :param skId: The id of the skill to search for.
        :return: list of query results
        """
        try:
            self.cursor.execute('SELECT * FROM skills WHERE skillId = %s;', (skId,))
            records = self.cursor.fetchall()
            return list(records)
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            return []
