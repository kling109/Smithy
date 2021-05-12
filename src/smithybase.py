# Smithy
# smithybase.py
#
# Last Date Modified: 05/11/2021
#
# Description:
# A MySQL wrapper class that allows the user to create a database object
# and perform various actions on that database.

import queryconstructor
import mysql.connector
import time
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

    def add_charm(self, name: str, uid: int, slot1: int, slot2: int, slot3: int,
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
            self.cursor.execute('INSERT INTO charm(charmName, userId, slot1, slot2, slot3, '
                                'skill1Id, skill1Val, skill2Id, skill2Val, '
                                'skill3Id, skill3Val, skill4Id, skill4Val, isDeleted) '
                                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',
                                (name, uid, slot1, slot2, slot3, skill1id, skill1val,
                                 skill2id, skill2val, skill3id, skill3val, skill4id, skill4val, 0))
            self.db.commit()
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            self.db.rollback()
            raise ValueError

    def delete_charm(self, name : str, uid : int):
        """
        Soft-deletes a charm for a given user.

        :param name: The name of the charm to delete.
        :param uid: The user attempting to delete the charm.
        :return: None
        """
        try:
            self.cursor.execute('UPDATE charm SET isDeleted = 1 WHERE charmName = %s AND userId = %s;', (name, uid))
            self.db.commit()
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            self.db.rollback()
            raise ValueError

    def update_charm(self, name: str, uid: int, column_name : str, new_value):
        """
        Allows users to update the skill values on a given charm.

        :param name: Name of the charm
        :param uid: Discord ID of the user adding the charm
        :param column_name: The column to modify
        :param new_value: the new value to add in
        :return: None
        """
        try:
            self.cursor.execute('UPDATE charm SET '
                                + column_name + '= %s '
                                'WHERE charmName = %s AND userId = %s AND isDeleted = 0;',
                                (new_value, name, uid))
            self.db.commit()
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            self.db.rollback()

    def add_armors(self, table: str, armor_list: list):
        """
        A method that allows the user to add a set of armors
        :param table: A string indicating which table to add the elements to.
        :param armor_list: A list of armor elements to add.
        :return: None
        """
        try:
            self.cursor.executemany('INSERT INTO ' + table + '(armorName, slot1, slot2, slot3, '
                                                             'skill1Id, skill1Val, skill2Id, skill2Val, '
                                                             'skill3Id, skill3Val, skill4Id, skill4Val) '
                                                             'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',
                                    armor_list)
            self.db.commit()
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            self.db.rollback()

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
            self.db.rollback()

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
            self.db.rollback()

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
            self.db.rollback()

    def get_skills_by_name(self, namelist: list):
        """
        A method that allows the user to search for a skill by name.

        :param namelist: the names of the skills to search for
        :return: list of query results
        """
        try:
            if len(namelist) > 1:
                inputs = [(n,) for n in namelist]
                records = []
                for n in inputs:
                    self.cursor.execute('SELECT * FROM skills WHERE skillName = %s;', n)
                    records += self.cursor.fetchall()
                return records
            elif len(namelist) == 1:
                self.cursor.execute('SELECT * FROM skills WHERE skillName = %s;', (namelist[0],))
                records = self.cursor.fetchall()
                return list(records)
            else:
                print("Error: No values were provided in the namelist.")
                return []
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

    def get_decos(self, sklist: list):
        """
        Returns a list of decorations based on a desired set of skills.

        :param sklist: a list of skill ID's to search
        :return: a list of decoration results
        """
        try:
            result = []
            for skill in sklist:
                self.cursor.execute('SELECT * FROM deco WHERE skillId = %s;', (skill,))
                result = result + self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            return []

    def get_charms(self, uid: int, skill_id: int = None):
        """
        Get a list of all the charms for a specific user.

        :param uid: the user's id
        :param skill_id: The id of a skill to search for.
        :return: list of charms
        """
        try:
            if skill_id is None:
                self.cursor.execute('SELECT charmName, slot1, slot2, slot3, skill1Id, skill1Val, '
                                    'skill2Id, skill2Val, skill3Id, skill3Val, skill4Id, skill4Val'
                                    ' FROM charm WHERE userId = %s AND isDeleted = 0;', (uid,))
            else:
                self.cursor.execute('SELECT charmName, slot1, slot2, slot3, skill1Id, skill1Val, '
                                    'skill2Id, skill2Val, skill3Id, skill3Val, skill4Id, skill4Val'
                                    ' FROM charm WHERE userId = %s AND isDeleted = 0 '
                                    'AND %s IN (skill1Id, skill2Id, skill3Id, skill4Id);', (uid, skill_id))
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            return []

    def get_helms(self, skill_id: int = None):
        """
        Gets a list of all helms.

        :return: list of helms
        """
        try:
            if skill_id is None:
                self.cursor.execute('SELECT armorName, slot1, slot2, slot3, skill1Id, skill1Val,'
                                    'skill2Id, skill2Val, skill3Id, skill3Val, skill4Id, skill4Val FROM helm;')
            else:
                self.cursor.execute('SELECT armorName, slot1, slot2, slot3, skill1Id, skill1Val,'
                                    'skill2Id, skill2Val, skill3Id, skill3Val, skill4Id, skill4Val FROM helm '
                                    'WHERE %s IN (skill1Id, skill2Id, skill3Id, skill4Id);', (skill_id,))
            results = self.cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            return []

    def get_chests(self, skill_id: int = None):
        """
        Gets a list of all chestplates.

        :return: list of chestplates
        """
        try:
            if skill_id is None:
                self.cursor.execute('SELECT armorName, slot1, slot2, slot3, skill1Id, skill1Val,'
                                    'skill2Id, skill2Val, skill3Id, skill3Val, skill4Id, skill4Val FROM chest;')
            else:
                self.cursor.execute('SELECT armorName, slot1, slot2, slot3, skill1Id, skill1Val,'
                                    'skill2Id, skill2Val, skill3Id, skill3Val, skill4Id, skill4Val FROM chest '
                                    'WHERE %s IN (skill1Id, skill2Id, skill3Id, skill4Id);', (skill_id,))
            results = self.cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            return []

    def get_vambraces(self, skill_id: int = None):
        """
        Gets a list of all vambraces.

        :return: list of vambraces
        """
        try:
            if skill_id is None:
                self.cursor.execute('SELECT armorName, slot1, slot2, slot3, skill1Id, skill1Val,'
                                    'skill2Id, skill2Val, skill3Id, skill3Val, skill4Id, skill4Val FROM vambraces;')
            else:
                self.cursor.execute('SELECT armorName, slot1, slot2, slot3, skill1Id, skill1Val,'
                                    'skill2Id, skill2Val, skill3Id, skill3Val, skill4Id, skill4Val FROM vambraces '
                                    'WHERE %s IN (skill1Id, skill2Id, skill3Id, skill4Id);', (skill_id,))
            results = self.cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            return []

    def get_faulds(self, skill_id: int = None):
        """
        Gets a list of all faulds.

        :return: list of faulds
        """
        try:
            if skill_id is None:
                self.cursor.execute('SELECT armorName, slot1, slot2, slot3, skill1Id, skill1Val,'
                                    'skill2Id, skill2Val, skill3Id, skill3Val, skill4Id, skill4Val FROM faulds;')
            else:
                self.cursor.execute('SELECT armorName, slot1, slot2, slot3, skill1Id, skill1Val,'
                                    'skill2Id, skill2Val, skill3Id, skill3Val, skill4Id, skill4Val FROM faulds '
                                    'WHERE %s IN (skill1Id, skill2Id, skill3Id, skill4Id);', (skill_id,))
            results = self.cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            return []

    def get_greaves(self, skill_id: int = None):
        """
        Gets a list of all greaves.

        :return: list of greaves
        """
        try:
            if skill_id is None:
                self.cursor.execute('SELECT armorName, slot1, slot2, slot3, skill1Id, skill1Val,'
                                    'skill2Id, skill2Val, skill3Id, skill3Val, skill4Id, skill4Val FROM greaves;')
            else:
                self.cursor.execute('SELECT armorName, slot1, slot2, slot3, skill1Id, skill1Val,'
                                    'skill2Id, skill2Val, skill3Id, skill3Val, skill4Id, skill4Val FROM greaves '
                                    'WHERE %s IN (skill1Id, skill2Id, skill3Id, skill4Id);', (skill_id,))
            results = self.cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            return []

    def get_armor_by_skills(self, sklist: list, max_lvs : list, user_id : int, num_results : int):
        """
        Returns a list of armor sets based on a set of desired skills.

        :param sklist: A list of skills to search for.
        :param max_lvs: A user-defined set of maximum skill levels
        :param user_id: The ID of the user in question, used to find specific charms.
        :return: list of helms
        """
        try:
            decodata = self.get_decos(sklist)
            sslots = 1 if len([s for s in decodata if s[2] == 1]) > 0 else 0
            mslots = 2 if len([s for s in decodata if s[2] == 2]) > 0 else 0
            lslots = 3 if len([s for s in decodata if s[2] == 3]) > 0 else 0
            max_slot = max(lslots, mslots, sslots)
            sk_max = []

            for s in range(len(sklist)):
                skill = self.get_skill(sklist[s])[0]
                sk_max.append(skill[2] if skill[2] < max_lvs[s] else max_lvs[s])

            query, args = queryconstructor.construct_query(sklist, sk_max, user_id, max_slot, num_results)
            self.cursor.execute(query, tuple(args))
            results = self.cursor.fetchall()
            return results

        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            return []


if __name__ == "__main__":
    db = SmithyDB("../../passfile.txt")
    # for i in range(1, 7):
    #     start_time = time.time()
    #     res = db.get_armor_by_skills([89, 90, 91], [3, 3, 6], 351847321245586963, i)
    #     print(str(i) + ": --- %s seconds ---" % (time.time() - start_time))
    res = db.get_armor_by_skills([89, 90, 91], [3, 3, 6], 999999999999999999, 2)
    print(res)
    # for r in res:
    #     print(r)
    # db.delete_charm('testNvnAvOpy', 351847321245586963)
    # print(db.get_greaves())
    # print(db.get_charms(999999999999999999))
    # print(db.get_skill(90))

