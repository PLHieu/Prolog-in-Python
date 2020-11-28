from unify import unify,is_variable,is_compound,is_list
from ClassTheta import Theta
from itertools import permutations


def unify_of_rule(facts_1, facts_2):  # Generalized Modus Ponens
    if len(facts_1) != len(facts_2):
        return False

    for f1, f2 in zip(facts_1, facts_2):
        if f1.op != f2.op:
            return False

    return unify(facts_1, facts_2, Theta())

def fol_bc_ask(facts_of_kb, rules_of_kb, querys, theta):

    res=set()
    if len(querys)==0:
        if theta:

            if len(theta.mappings) == 0:
                # add true

                res.add("true")
                return res
            res.add(theta)
        return res

    accepted_fact = querys[0]

    for i in range(len(accepted_fact.args)):
        const = theta.get_const(accepted_fact.args[i])
        if (const):
            accepted_fact.args[i] = const

    if not accepted_fact.contains_variable():
        res.update(fol_bc_ask(facts_of_kb, rules_of_kb, querys[1:], theta))
        return res

    for fact in facts_of_kb:
        new_theta = Theta()

        theta1 = unify(fact, accepted_fact, Theta())
        if theta1:
            new_theta.mappings.update(theta.mappings)
            if len(theta1.mappings) != 0:
                new_theta.mappings.update(theta1.mappings)
            res.update(fol_bc_ask(facts_of_kb, rules_of_kb, querys[1:], new_theta))


    for rule in rules_of_kb:

        new_rule = rule.copy()
        #doi bien cho accept_fact va rule khac nhau
        #chi doi bien cura accepted_fact

        # for idx in range(len(accepted_fact.args)):
        #     if is_variable(accepted_fact.args[idx]):
        #         init_name = accepted_fact.args[idx]
        #         while accepted_fact.contains_in_args(init_name) and rule.contains_arg(init_name):
        #             init_name = rule.generate_variable_name()
        #         accepted_fact.args[idx] = init_name

        new_theta = unify(accepted_fact,rule.conclusion, Theta())
        if not new_theta:
            continue


        variable_theta = Theta()
        remove_key = []
        for key, value in new_theta.mappings.items():
            if is_variable(key) and is_variable(value):
                variable_theta.add(value, key)
                remove_key.append(key)

        for key in remove_key:
            del new_theta.mappings[key]
        if len(variable_theta.mappings) != 0:
            for value, key in variable_theta.mappings.items():
                for idx in range(len(rule.conclusion.args)):
                    if (new_rule.conclusion.args[idx] == value):
                        new_rule.conclusion.args[idx] = key

            for i_condition in range(len(new_rule.conditions)):
                for i_arg in range(len(rule.conditions[i_condition].args)):
                    if variable_theta.mappings.get(new_rule.conditions[i_condition].args[i_arg]):
                        new_rule.conditions[i_condition].args[i_arg] = variable_theta.mappings.get(new_rule.conditions[i_condition].args[i_arg])
                    else:
                        key = 0
                        while rule.conditions[i_condition].args[i_arg] in list(variable_theta.mappings.values()):
                            key = key + 1
                            rule.conditions[i_condition].args[i_arg] = rule.generate_variable_name(str(key) + rule.conditions[i_condition].op)


        new_querys = new_rule.conditions + querys[1:]

        new_theta.mappings.update(theta.mappings)

        res.update(fol_bc_ask(facts_of_kb,rules_of_kb,new_querys, new_theta))


    return res


def backward_chaining(kb, query):
    facts_of_kb = set(kb.facts)
    rules_of_kb = list(kb.rules)
    theta = Theta()

    res = fol_bc_ask(facts_of_kb,rules_of_kb, [query], theta)



    if query.contains_variable():
        final_res = set()
        for subres in res:
            theta0=Theta()
            for arg in query.args:
                if is_variable(arg):
                    theta0.add(arg,subres.mappings.get(arg))
            final_res.add(theta0)
        return final_res
    # if face contain query
    return res

