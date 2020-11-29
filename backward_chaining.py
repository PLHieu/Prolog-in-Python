from unify import unify,is_variable,is_compound,is_list
from ClassTheta import Theta
import copy


def fol_bc_ask(facts_of_kb, rules_of_kb, querys, theta, query):

    res=set()
    if len(querys)==0:
        if theta:
            if query.contains_variable() == 0:
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



    for fact in facts_of_kb:
        new_theta = unify(fact, accepted_fact, Theta())
        if new_theta:
            new_theta.mappings.update(theta.mappings)
            res.update(fol_bc_ask(facts_of_kb, rules_of_kb, querys[1:], new_theta,query))


    for rule in rules_of_kb:

        new_rule = copy.deepcopy(rule)
        #doi bien cho accept_fact va rule khac nhau
        #chi doi bien cura accepted_fact



        new_theta = unify(accepted_fact,new_rule.conclusion, Theta())
        if not new_theta:
            continue

        variable_theta = Theta()
        remove_key = []
        add_key={}
        for key, value in new_theta.mappings.items():
            if is_variable(key) and is_variable(value):
                variable_theta.add(value, key)
                remove_key.append(key)
            else:
                if theta.get_key(value):
                    variable_theta.add(key,theta.get_key(value))


        if len(variable_theta.mappings)!=0:
            for condition in new_rule.conditions:
                for idx in range(len(condition.args)):
                    #neu chua trung ten
                    if condition.args[idx] in list(variable_theta.mappings.values()):
                        variable_theta.add(condition.args[idx], new_rule.generate_variable_name())

        for key in remove_key:
            del new_theta.mappings[key]

        new_theta.mappings.update(add_key)


        if len(variable_theta.mappings) != 0:
            for value, key in variable_theta.mappings.items():
                for idx in range(len(rule.conclusion.args)):
                    if (new_rule.conclusion.args[idx] == value):
                        new_rule.conclusion.args[idx] = key

            for i_condition in range(len(new_rule.conditions)):
                for i_arg in range(len(rule.conditions[i_condition].args)):
                    if variable_theta.mappings.get(new_rule.conditions[i_condition].args[i_arg]):
                        new_rule.conditions[i_condition].args[i_arg] = variable_theta.mappings.get(new_rule.conditions[i_condition].args[i_arg])


        new_querys = new_rule.conditions + querys[1:]

        new_theta.mappings.update(theta.mappings)
        res.update(fol_bc_ask(facts_of_kb,rules_of_kb,new_querys, new_theta,query))


    return res



def backward_chaining(kb, query):

    facts_of_kb = copy.deepcopy(kb.facts)
    rules_of_kb = copy.deepcopy(kb.rules)

    theta = Theta()

    res = fol_bc_ask(facts_of_kb,rules_of_kb,copy.deepcopy([query]), theta,query)

    if query.contains_variable():
        final_res = set()
        for subres in res:
            theta0=Theta()
            for arg in query.args:
                if is_variable(arg):
                    theta0.add(arg,subres.mappings.get(arg))
            final_res.add(theta0)

        return final_res

    if res:
        res.add("true")
    else:
        res.add("fase")
    return res

