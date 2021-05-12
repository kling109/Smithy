# Smithy
# queryprocessor.py
#
# Last Date Modified: 05/12/2021
#
# Description:
# A class which allows for the formatting and execution of queries

from smithybase import SmithyDB


class QueryProcessor:
    armordb = None

    def __init__(self, info: str):
        self.armordb = SmithyDB(info)

    def __del__(self):
        pass

    def add_user_charm(self, charminfo: dict, uid: int):
        """
        Adds a charm to the database from the user's given skills and other info.
        :param charminfo: a dictionary of charm parameters
        :param uid: the user's Discord Id
        :return: None
        """
        try:
            skill_names = [charminfo["skill1Name"], charminfo["skill2Name"], charminfo["skill3Name"], charminfo["skill4Name"]]
            skill_data = self.armordb.get_skills_by_name(skill_names)
            skill_ids = [s[0] for s in skill_data] + [None for i in range(len(skill_data), 4)]
            self.armordb.add_charm(charminfo["name"], uid, charminfo["slot1"], charminfo["slot2"], charminfo["slot3"],
                                   skill_ids[0], charminfo["skill1Val"], skill_ids[1],
                                   charminfo["skill2Val"], skill_ids[2], charminfo["skill3Val"],
                                   skill_ids[3], charminfo["skill4Val"])
        except ValueError as err:
            print("Charm was unable to be added to the database.")

    def remove_user_charm(self, charm_name: str, uid: int):
        """
        Removes a given charm from the database of a user.

        :param charm_name: The name of the charm to remove
        :param uid: the user's Discord Id
        :return: None
        """
        try:
            self.armordb.delete_charm(charm_name, uid)
        except ValueError as err:
            print("The given charm was not removed from the database.")

    def modify_user_charm(self, charm_name: str, uid : int, value_to_modify: str, new_val):
        """
        Modifies an existing user charm.
        
        :param charm_name: The name of the charm to modify
        :param uid: The Discord User Id
        :param value_to_modify: the name of the column to modify
        :param new_val: the new value to place in the column
        :return: None.
        """
        try:
            if value_to_modify == 'slots':
                self.armordb.update_charm(charm_name, uid, 'slot1', new_val[0])
                self.armordb.update_charm(charm_name, uid, 'slot2', new_val[1])
                self.armordb.update_charm(charm_name, uid, 'slot3', new_val[2])
            elif value_to_modify == 'skill':
                skill_index = new_val[0]
                new_skill = new_val[1]
                new_skill_val = new_val[2]
                self.armordb.update_charm(charm_name, uid, 'skill'+str(skill_index)+'Id', new_skill)
                self.armordb.update_charm(charm_name, uid, 'skill'+str(skill_index)+'Val', new_skill_val)
        except ValueError as err:
            print("Charm was unable to be modified.")

    def search_armor_set(self, skills: dict, uid: int, num_results: int = 4, returned_results: int = 1):
        """
        Generates an optimized armor set for the given set of skills

        :param skills: a dictionary of skills to search for
        :param uid: the Discord user's Id.
        :param num_results: the number of elements to include in the search.  Default value is 4
        :param returned_results: the number of results to return.  default is 1.
        :return: armor_sets: A list of dictionaries specifying the armor set and its decorations.
        """
        try:
            skill_names = [k for k in skills.keys()]
            skill_data = self.armordb.get_skills_by_name(skill_names)
            skill_ids = [s[0] for s in skill_data]
            skill_max_vals = [v for v in skills.values()]
            results = self.armordb.get_armor_by_skills(skill_ids, skill_max_vals, uid, num_results)
            armor_sets = []
            for i in range(min(returned_results, len(results))):
                set_dict = {"helm": {}, "chest": {}, "vambraces": {}, "faulds": {}, "greaves": {}, "charm": {},
                            "totals": {}}
                set_res = results[i]
                set_dict["helm"]["name"] = set_res[0]
                set_dict["chest"]["name"] = set_res[1]
                set_dict["vambraces"]["name"] = set_res[2]
                set_dict["faulds"]["name"] = set_res[3]
                set_dict["greaves"]["name"] = set_res[4]
                set_dict["charm"]["name"] = set_res[5]
                set_dict["helm"]["decos"] = [x for x in set_res[6:9] if x is not None]
                set_dict["chest"]["decos"] = [x for x in set_res[9:12] if x is not None]
                set_dict["vambraces"]["decos"] = [x for x in set_res[12:15] if x is not None]
                set_dict["faulds"]["decos"] = [x for x in set_res[15:18] if x is not None]
                set_dict["greaves"]["decos"] = [x for x in set_res[18:21] if x is not None]
                set_dict["charm"]["decos"] = [x for x in set_res[21:24] if x is not None]
                for n in range(len(skill_names)):
                    set_dict["totals"][skill_names[n]] = int(set_res[24 + n])

                armor_sets.append(set_dict)

            return armor_sets
        except ValueError as err:
            print("Search could not be performed")
            return []

    def format_sets(self, unformatted_set: list):
        """
        Formats a set of objects from a query result.

        :param unformatted_set: The set of objects to format.
        :return: formatted_set: The set of proper dictionaries.
        """
        formatted_set = []
        for c in unformatted_set:
            item = {"name": c[0], "slot1": c[1], "slot2": c[2], "slot3": c[3], "skills": {}}
            if c[4] is not None:
                item["skills"][self.armordb.get_skill(c[4])[0][1]] = int(c[5])
            if c[6] is not None:
                item["skills"][self.armordb.get_skill(c[6])[0][1]] = int(c[7])
            if c[8] is not None:
                item["skills"][self.armordb.get_skill(c[8])[0][1]] = int(c[9])
            if c[10] is not None:
                item["skills"][self.armordb.get_skill(c[10])[0][1]] = int(c[11])
            formatted_set.append(item)

        return formatted_set

    def display(self, uid: int, armor_type: str, skill_name: str = None):
        """
        Returns and formats all charms for a given user.

        :param uid: the user's Discord Id
        :param armor_type: the type of armor to return.
        :param skill_name: The name of a skill to search for.
        :return: charm_set: list of dictionaries of the charms.
        """
        try:
            skillId = None
            if skill_name is not None:
                skillId = self.armordb.get_skills_by_name([skill_name])[0][0]

            if armor_type == "helms":
                unformatted_set = self.armordb.get_helms(skillId)
            elif armor_type == "chests":
                unformatted_set = self.armordb.get_chests(skillId)
            elif armor_type == "vambraces":
                unformatted_set = self.armordb.get_vambraces(skillId)
            elif armor_type == "faulds":
                unformatted_set = self.armordb.get_faulds(skillId)
            elif armor_type == "greaves":
                unformatted_set = self.armordb.get_greaves(skillId)
            elif armor_type == "charms":
                unformatted_set = self.armordb.get_charms(uid, skillId)
            else:
                raise ValueError

            return self.format_sets(unformatted_set)
        except ValueError as err:
            print("Unable to query the set.")
            return []


if __name__ == "__main__":
    # Need to reformat the main search query a bit; move the left joins to be part of another subquery.
    sm = QueryProcessor("../../passfile.txt")
    res = sm.search_armor_set({'Weakness Exploit': 3, 'Critical Boost': 3, 'Attack Boost': 7}, 999999999999999999, returned_results=3)
    for r in res:
        print(r)