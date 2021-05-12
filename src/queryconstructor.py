# Smithy
# queryconstructor.py
#
# Last Date Modified: 05/11/2021
#
# Description:
# A set of methods to contruct queries dynamically.

from itertools import chain

def generate_helm(skills, max_deco, num_results):
    skill_totals = ""
    skill_limits = ""
    skill_orders = ""
    skillset = "("
    for i in range(len(skills)):
        skillset += "%s"
        skill_totals += """ (IF(skill1Id = %s, skill1Val, 0)
                        + IF(skill2Id = %s, skill2Val, 0)
                        + IF(skill3Id = %s, skill3Val, 0)
                        + IF(skill4Id = %s, skill4Val, 0)) helmTotal""" + str(i+1)
        skill_limits += """%s IN (h.skill1Id, h.skill2Id, h.skill3Id, h.skill4Id)"""
        skill_orders += "helmTotal" + str(i+1) + " DESC"
        if i < len(skills)-1:
            skill_totals += ",\n"
            skill_limits += "\nOR "
            skillset += ", "
            skill_orders += ", "
    skillset += ")"
    skill_limits += "\nOR h.slot1 > "+str(max_deco)+"\nOR h.slot2 > "+str(max_deco)+"\nOR h.slot3 > "+str(max_deco)
    query = """ (
                SELECT armorName,
                           slot1,
                           slot2,
                           slot3,
            """ + skill_totals + """
                FROM helm h
                WHERE """ + skill_limits + """
            ORDER BY """ + skill_orders + """, slot1+slot2+slot3 DESC LIMIT %s  ) AS helm"""
    query_args = list(chain(*[[skills[i], skills[i], skills[i], skills[i]] for i in range(len(skills))])) + skills + [num_results]

    q_deco = """LEFT JOIN
                (
                    SELECT decoName, slotSize, skillId, skillVal FROM deco
                    WHERE skillId IN """ + skillset + """
                ) hdeco1 ON hdeco1.slotSize <= armor.hslot1
                LEFT JOIN
                (
                    SELECT decoName, slotSize, skillId, skillVal FROM deco
                    WHERE skillId IN """ + skillset + """
                ) hdeco2 ON hdeco2.slotSize <= armor.hslot2
                LEFT JOIN
                (
                    SELECT decoName, slotSize, skillId, skillVal FROM deco
                    WHERE skillId IN """ + skillset + """
                ) hdeco3 ON hdeco3.slotSize <= armor.hslot3"""
    deco_args = skills*3

    return query, q_deco, query_args, deco_args


def generate_chest(skills, max_deco, num_results):
    skill_totals = ""
    skill_limits = ""
    skillset = "("
    skill_orders = ""
    for i in range(len(skills)):
        skillset += "%s"
        skill_totals += """ (IF(skill1Id = %s, skill1Val, 0)
                            + IF(skill2Id = %s, skill2Val, 0)
                            + IF(skill3Id = %s, skill3Val, 0)
                            + IF(skill4Id = %s, skill4Val, 0)) chestTotal""" + str(i+1)
        skill_limits += """%s IN (c.skill1Id, c.skill2Id, c.skill3Id, c.skill4Id)"""
        skill_orders += "chestTotal" + str(i + 1) + " DESC"
        if i < len(skills) - 1:
            skill_totals += ",\n"
            skill_limits += "\nOR "
            skillset += ", "
            skill_orders += ", "
    skillset += ")"
    skill_limits += "\nOR c.slot1 > " + str(max_deco) + "\nOR c.slot2 > " + str(max_deco) + "\nOR c.slot3 > " + str(
        max_deco)
    query = """ (
                    SELECT armorName,
                           slot1,
                           slot2,
                           slot3,
                """ + skill_totals + """
                    FROM chest c
                    WHERE """ + skill_limits + """
                ORDER BY """ + skill_orders + """, slot1+slot2+slot3 DESC LIMIT %s ) AS chest"""
    query_args = list(chain(*[[skills[i], skills[i], skills[i], skills[i]] for i in range(len(skills))])) + skills + [num_results]
    q_deco = """LEFT JOIN
                    (
                        SELECT decoName, slotSize, skillId, skillVal FROM deco
                        WHERE skillId IN """ + skillset + """
                    ) cdeco1 ON cdeco1.slotSize <= armor.cslot1
                    LEFT JOIN
                    (
                        SELECT decoName, slotSize, skillId, skillVal FROM deco
                        WHERE skillId IN """ + skillset + """
                    ) cdeco2 ON cdeco2.slotSize <= armor.cslot2
                    LEFT JOIN
                    (
                        SELECT decoName, slotSize, skillId, skillVal FROM deco
                        WHERE skillId IN """ + skillset + """
                    ) cdeco3 ON cdeco3.slotSize <= armor.cslot3"""
    deco_args = skills * 3

    return query, q_deco, query_args, deco_args


def generate_vamb(skills, max_deco, num_results):
    skill_totals = ""
    skill_limits = ""
    skill_orders = ""
    skillset = "("
    for i in range(len(skills)):
        skillset += "%s"
        skill_totals += """ (IF(skill1Id = %s, skill1Val, 0)
                                + IF(skill2Id = %s, skill2Val, 0)
                                + IF(skill3Id = %s, skill3Val, 0)
                                + IF(skill4Id = %s, skill4Val, 0)) vambraceTotal""" + str(i+1)
        skill_limits += """%s IN (v.skill1Id, v.skill2Id, v.skill3Id, v.skill4Id)"""
        skill_orders += "vambraceTotal" + str(i + 1) + " DESC"
        if i < len(skills) - 1:
            skill_totals += ",\n"
            skill_limits += "\nOR "
            skillset += ", "
            skill_orders += ", "
    skillset += ")"
    skill_limits += "\nOR v.slot1 > " + str(max_deco) + "\nOR v.slot2 > " + str(max_deco) + "\nOR v.slot3 > " + str(
        max_deco)
    query = """ (
                    SELECT armorName,
                           slot1,
                           slot2,
                           slot3,
                """ + skill_totals + """
                    FROM vambraces v
                    WHERE """ + skill_limits + """
                ORDER BY """ + skill_orders + """, slot1+slot2+slot3 DESC LIMIT %s ) AS vambraces"""
    query_args = list(chain(*[[skills[i], skills[i], skills[i], skills[i]] for i in range(len(skills))])) + skills + [num_results]
    q_deco = """LEFT JOIN
                    (
                        SELECT decoName, slotSize, skillId, skillVal FROM deco
                        WHERE skillId IN """ + skillset + """
                    ) vdeco1 ON vdeco1.slotSize <= armor.vslot1
                    LEFT JOIN
                    (
                        SELECT decoName, slotSize, skillId, skillVal FROM deco
                        WHERE skillId IN """ + skillset + """
                    ) vdeco2 ON vdeco2.slotSize <= armor.vslot2
                    LEFT JOIN
                    (
                        SELECT decoName, slotSize, skillId, skillVal FROM deco
                        WHERE skillId IN """ + skillset + """
                    ) vdeco3 ON vdeco3.slotSize <= armor.vslot3"""
    deco_args = skills * 3

    return query, q_deco, query_args, deco_args


def generate_fauld(skills, max_deco, num_results):
    skill_totals = ""
    skill_limits = ""
    skill_orders = ""
    skillset = "("
    for i in range(len(skills)):
        skillset += "%s"
        skill_totals += """ (IF(skill1Id = %s, skill1Val, 0)
                                    + IF(skill2Id = %s, skill2Val, 0)
                                    + IF(skill3Id = %s, skill3Val, 0)
                                    + IF(skill4Id = %s, skill4Val, 0)) fauldTotal""" + str(i+1)
        skill_limits += """%s IN (f.skill1Id, f.skill2Id, f.skill3Id, f.skill4Id)"""
        skill_orders += "fauldTotal" + str(i + 1) + " DESC"
        if i < len(skills) - 1:
            skill_totals += ",\n"
            skill_limits += "\nOR "
            skillset += ", "
            skill_orders += ", "
    skillset += ")"
    skill_limits += "\nOR f.slot1 > " + str(max_deco) + "\nOR f.slot2 > " + str(max_deco) + "\nOR f.slot3 > " + str(
        max_deco)
    query = """ (
                    SELECT armorName,
                           slot1,
                           slot2,
                           slot3,
                """ + skill_totals + """
                    FROM faulds f
                    WHERE """ + skill_limits + """
                ORDER BY """ + skill_orders + """, slot1+slot2+slot3 DESC LIMIT %s ) AS faulds"""
    query_args = list(chain(*[[skills[i], skills[i], skills[i], skills[i]] for i in range(len(skills))])) + skills + [num_results]
    q_deco = """LEFT JOIN
                    (
                        SELECT decoName, slotSize, skillId, skillVal FROM deco
                        WHERE skillId IN """ + skillset + """
                    ) fdeco1 ON fdeco1.slotSize <= armor.fslot1
                    LEFT JOIN
                    (
                        SELECT decoName, slotSize, skillId, skillVal FROM deco
                        WHERE skillId IN """ + skillset + """
                    ) fdeco2 ON fdeco2.slotSize <= armor.fslot2
                    LEFT JOIN
                    (
                        SELECT decoName, slotSize, skillId, skillVal FROM deco
                        WHERE skillId IN """ + skillset + """
                    ) fdeco3 ON fdeco3.slotSize <= armor.fslot3"""
    deco_args = skills * 3

    return query, q_deco, query_args, deco_args


def generate_greave(skills, max_deco, num_results):
    skill_totals = ""
    skill_limits = ""
    skill_orders = ""
    skillset = "("
    for i in range(len(skills)):
        skillset += "%s"
        skill_totals += """ (IF(skill1Id = %s, skill1Val, 0)
                                    + IF(skill2Id = %s, skill2Val, 0)
                                    + IF(skill3Id = %s, skill3Val, 0)
                                    + IF(skill4Id = %s, skill4Val, 0)) greaveTotal""" + str(i+1)
        skill_limits += """%s IN (g.skill1Id, g.skill2Id, g.skill3Id, g.skill4Id)"""
        skill_orders += "greaveTotal" + str(i + 1) + " DESC"
        if i < len(skills) - 1:
            skill_totals += ",\n"
            skill_limits += "\nOR "
            skillset += ", "
            skill_orders += ", "
    skillset += ")"
    skill_limits += "\nOR g.slot1 > " + str(max_deco) + "\nOR g.slot2 > " + str(max_deco) + "\nOR g.slot3 > " + str(
        max_deco)
    query = """ (
                    SELECT armorName,
                            slot1,
                            slot2,
                            slot3,
                        """ + skill_totals + """
                            FROM greaves g
                            WHERE """ + skill_limits + """
                        ORDER BY """ + skill_orders + """, slot1+slot2+slot3 DESC LIMIT %s ) AS greaves"""
    query_args = list(chain(*[[skills[i], skills[i], skills[i], skills[i]] for i in range(len(skills))])) + skills + [num_results]
    q_deco = """LEFT JOIN
                    (
                        SELECT decoName, slotSize, skillId, skillVal FROM deco
                        WHERE skillId IN """ + skillset + """
                    ) gdeco1 ON gdeco1.slotSize <= armor.gslot1
                    LEFT JOIN
                    (
                        SELECT decoName, slotSize, skillId, skillVal FROM deco
                        WHERE skillId IN """ + skillset + """
                    ) gdeco2 ON gdeco2.slotSize <= armor.gslot2
                    LEFT JOIN
                    (
                        SELECT decoName, slotSize, skillId, skillVal FROM deco
                        WHERE skillId IN """ + skillset + """
                    ) gdeco3 ON gdeco3.slotSize <= armor.gslot3"""
    deco_args = skills * 3

    return query, q_deco, query_args, deco_args


def generate_skill_limits(skills, skill_maxlv, num_results):
    skill_limits = ""
    skill_order = ""
    for i in range(len(skills)):
        skill_limits += "Skill" + str(i+1) + "Total <= %s"
        skill_order += "Skill" + str(i+1) + "Total DESC"
        if i < len(skills) - 1:
            skill_limits += " AND "
            skill_order += ", "
    sk_lims = """HAVING """ + skill_limits +  """\nORDER BY """ \
              + skill_order + """, Slot1Total DESC, Slot2Total DESC, Slot3Total DESC"""
    sk_lims_args = [skill_maxlv[i] for i in range(len(skills))]
    return sk_lims, sk_lims_args


def generate_charm(skills, max_deco, user_id, num_results):
    skill_totals = ""
    skill_limits = ""
    skill_orders = ""
    skillset = "("
    for i in range(len(skills)):
        skillset += "%s"
        skill_totals += """ (IF(skill1Id = %s, skill1Val, 0)
                                        + IF(skill2Id = %s, skill2Val, 0)
                                        + IF(skill3Id = %s, skill3Val, 0)
                                        + IF(skill4Id = %s, skill4Val, 0)) charmTotal""" + str(i+1)
        skill_limits += """%s IN (ch.skill1Id, ch.skill2Id, ch.skill3Id, ch.skill4Id)"""
        skill_orders += "charmTotal" + str(i + 1) + " DESC"
        if i < len(skills) - 1:
            skill_totals += ",\n"
            skill_limits += "\nOR "
            skillset += ", "
            skill_orders += ", "
    skillset += ")"
    skill_limits += "\nOR ch.slot1 > " + str(max_deco) + "\nOR ch.slot2 > " + str(max_deco) + "\nOR ch.slot3 > " + str(
        max_deco)
    query = """ (
                    SELECT charmName,
                           slot1,
                           slot2,
                           slot3,
                """ + skill_totals + """
                    FROM charm ch
                    WHERE userId = %s AND isDeleted = 0 AND (""" + skill_limits + """)
                ORDER BY """ + skill_orders + """, slot1+slot2+slot3 DESC LIMIT %s ) AS charm"""
    query_args = list(chain(*[[skills[i], skills[i], skills[i], skills[i]] for i in range(len(skills))])) + [user_id] + skills + [num_results]
    q_deco = """LEFT JOIN
                        (
                            SELECT decoName, slotSize, skillId, skillVal FROM deco
                            WHERE skillId IN """ + skillset + """
                        ) chdeco1 ON chdeco1.slotSize <= armor.chslot1
                        LEFT JOIN
                        (
                            SELECT decoName, slotSize, skillId, skillVal FROM deco
                            WHERE skillId IN """ + skillset + """
                        ) chdeco2 ON chdeco2.slotSize <= armor.chslot2
                        LEFT JOIN
                        (
                            SELECT decoName, slotSize, skillId, skillVal FROM deco
                            WHERE skillId IN """ + skillset + """
                        ) chdeco3 ON chdeco3.slotSize <= armor.chslot3"""
    deco_args = skills * 3

    return query, q_deco, query_args, deco_args
    return query, query_args


def assemble(skills, helm_subq, chest_subq, vamb_subq, fauld_subq, greave_subq, charm_subq, skill_limits, helm_dec,
             chest_dec, vamb_dec, fauld_dec, greave_dec, charm_dec):
    skill_totals = ""
    skill_totals_label = ""
    for i in range(len(skills)):
        deco_sums = """ + IF(hdeco1.skillId = %s, hdeco1.skillVal, 0)
                                  + IF(hdeco2.skillId = %s, hdeco2.skillVal, 0)
                                  + IF(hdeco3.skillId = %s, hdeco1.skillVal, 0)
                                  + IF(cdeco1.skillId = %s, cdeco1.skillVal, 0)
                                  + IF(cdeco2.skillId = %s, cdeco2.skillVal, 0)
                                  + IF(cdeco3.skillId = %s, cdeco1.skillVal, 0)
                                  + IF(vdeco1.skillId = %s, vdeco1.skillVal, 0)
                                  + IF(vdeco2.skillId = %s, vdeco2.skillVal, 0)
                                  + IF(vdeco3.skillId = %s, vdeco1.skillVal, 0)
                                  + IF(fdeco1.skillId = %s, fdeco1.skillVal, 0)
                                  + IF(fdeco2.skillId = %s, fdeco2.skillVal, 0)
                                  + IF(fdeco3.skillId = %s, fdeco1.skillVal, 0)
                                  + IF(gdeco1.skillId = %s, gdeco1.skillVal, 0)
                                  + IF(gdeco2.skillId = %s, gdeco2.skillVal, 0)
                                  + IF(gdeco3.skillId = %s, gdeco1.skillVal, 0)
                                  + IF(chdeco1.skillId = %s, chdeco1.skillVal, 0)
                                  + IF(chdeco2.skillId = %s, chdeco2.skillVal, 0)
                                  + IF(chdeco3.skillId = %s, chdeco1.skillVal, 0)"""
        skill_totals += """(helmTotal""" + str(i+1) + """ + chestTotal""" + str(i+1) + """ + vambraceTotal""" + str(i+1) \
                        + """ + fauldTotal""" + str(i+1) + """ + greaveTotal""" + str(i+1) + """
                        + charmTotal""" + str(i+1) + """) Skill""" + str(i+1) + """Total,"""
        skill_totals_label += """(armor.Skill""" + str(i+1) + """Total""" + deco_sums + """) Skill""" + str(i+1) + """Total"""
        if i < len(skills)-1:
            skill_totals += "\n"
            skill_totals_label += ",\n"
    query = """ SELECT armor.HelmName,
           armor.ChestName,
           armor.VambraceName,
           armor.FauldName,
           armor.GreaveName,
           armor.CharmName,
           hdeco1.decoName HelmDeco1,
           hdeco2.decoName HelmDeco2,
           hdeco3.decoName HelmDeco3,
           cdeco1.decoName ChestDeco1,
           cdeco2.decoName ChestDeco2,
           cdeco3.decoName ChestDeco3,
           vdeco1.decoName VambracesDeco1,
           vdeco2.decoName VambracesDeco2,
           vdeco3.decoName VambracesDeco3,
           fdeco1.decoName FauldsDeco1,
           fdeco2.decoName FauldsDeco2,
           fdeco3.decoName FauldsDeco3,
           gdeco1.decoName GreavesDeco1,
           gdeco2.decoName GreavesDeco2,
           gdeco3.decoName GreavesDeco3,
           chdeco1.decoName CharmDeco1,
           chdeco2.decoName CharmDeco2,
           chdeco3.decoName CharmDeco3,
           """+ skill_totals_label + """
           FROM
           (
           SELECT helm.armorName HelmName,
           helm.slot1 hslot1,
           helm.slot2 hslot2,
           helm.slot3 hslot3,
           chest.armorName ChestName,
           chest.slot1 cslot1,
           chest.slot2 cslot2,
           chest.slot3 cslot3,
           vambraces.armorName VambraceName,
           vambraces.slot1 vslot1,
           vambraces.slot2 vslot2,
           vambraces.slot3 vslot3,
           faulds.armorName FauldName,
           faulds.slot1 fslot1,
           faulds.slot2 fslot2,
           faulds.slot3 fslot3,
           greaves.armorName GreaveName,
           greaves.slot1 gslot1,
           greaves.slot2 gslot2,
           greaves.slot3 gslot3,
           charm.charmName CharmName,
           charm.slot1 chslot1,
           charm.slot2 chslot2,
           charm.slot3 chslot3,
           """ + skill_totals + """
           (helm.slot1 + chest.slot1 + vambraces.slot1
               + faulds.slot1 + greaves.slot1) Slot1Total,
           (helm.slot2 + chest.slot2 + vambraces.slot2
               + faulds.slot2 + greaves.slot2) Slot2Total,
           (helm.slot3 + chest.slot3 + vambraces.slot3
               + faulds.slot3 + greaves.slot3) Slot3Total
           FROM\n""" + helm_subq + ",\n" + chest_subq + ",\n"+vamb_subq + ",\n" + fauld_subq + ",\n" + greave_subq + \
           ",\n" + charm_subq + "\n" + skill_limits + ") AS armor \n" \
           + helm_dec + "\n" + chest_dec + "\n" + vamb_dec + "\n" + fauld_dec + "\n" + greave_dec + "\n" + charm_dec + \
            "\n" + skill_limits + ";"
    return query


def construct_query(skills : list, skill_maxlv : list, user_id : str, max_deco : int, num_results : int):
    """
    Produces a string query to be used with the MySQL engine.

    :param skills: A list containing all the desirable skills and their levels.
    :return: String
    """
    helm_subq, helm_dec, helm_args, helm_dec_args = generate_helm(skills, max_deco, num_results)
    chest_subq, chest_dec, chest_args, chest_dec_args = generate_chest(skills, max_deco, num_results)
    vamb_subq, vamb_dec, vamb_args, vamb_dec_args = generate_vamb(skills, max_deco, num_results)
    fauld_subq, fauld_dec, fauld_args, fauld_dec_args = generate_fauld(skills, max_deco, num_results)
    greave_subq, greave_dec, greaves_args, greave_dec_args = generate_greave(skills, max_deco, num_results)
    charm_subq, charm_dec, charms_args, charm_dec_args = generate_charm(skills, max_deco, user_id, num_results)
    skill_limits, skill_limits_args = generate_skill_limits(skills, skill_maxlv, num_results)
    total_query = assemble(skills, helm_subq, chest_subq, vamb_subq, fauld_subq, greave_subq, charm_subq, skill_limits,
                           helm_dec, chest_dec, vamb_dec, fauld_dec, greave_dec, charm_dec)
    deco_args = list(chain(*[[skills[i]]*18 for i in range(len(skills))]))
    full_args = (deco_args + helm_args + chest_args + vamb_args + fauld_args + greaves_args + charms_args + skill_limits_args
                + helm_dec_args + chest_dec_args + vamb_dec_args + fauld_dec_args + greave_dec_args + charm_dec_args
                + skill_limits_args)
    return total_query, full_args


if __name__ == "__main__":
    skills = [89, 90, 91]
    skill_max = [3, 3, 3]
    max_deco = 1
    user_id = 351847321245586963
    query, args = construct_query(skills, skill_max, user_id, max_deco, 10)
    print(query)
    print(len(args))