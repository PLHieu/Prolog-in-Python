from unify import unify,is_variable,is_compound,is_list
from ClassTheta import Theta
import copy


def fol_bc_ask(facts_of_kb, rules_of_kb, querys, theta, root_query):

    res=set()
    #if querys is empty then add result
    if len(querys)==0:
        if theta:
            if root_query.contains_variable() == 0:
                # add true
                res.add("true")
                return res
            res.add(theta)
        return res

    #get the first of query
    accepted_conclusion = querys[0]

    #replace variable by constant in theta
    for i in range(len(accepted_conclusion.args)):
        const = theta.get_const(accepted_conclusion.args[i])
        if (const):
            accepted_conclusion.args[i] = const

    #loop fact in kb
    for fact in facts_of_kb:
        #new theta for accepted conclusion and this fact
        new_theta = unify(fact, accepted_conclusion, Theta())
        if new_theta:
            # new theta is exist then use this fact to calculate next query
            new_theta.mappings.update(theta.mappings)
            res.update(fol_bc_ask(facts_of_kb, rules_of_kb, querys[1:], new_theta,root_query))
    #loop rule in kb
    for rule in rules_of_kb:
        #deepcopy the rule because then new rule is replaced variable by theta
        new_rule = copy.deepcopy(rule)
        #find theta for accepted conclusion and this rule to determine choose it or not
        new_theta = unify(accepted_conclusion,new_rule.conclusion, Theta())
        #continue other rule
        if not new_theta:
            continue


        variable_theta = Theta()#virtal theta have key is variable and value is variable
        remove_key = []#saving key need to delete
        for key, value in new_theta.mappings.items():
            #if new theta have 2 variable
            if is_variable(key) and is_variable(value):
                #add value, key to variable theta
                variable_theta.add(value, key)
                #add key need to remove
                remove_key.append(key)
            else:
                #if old theta had value of this key and replace key by its value in old theta
                if theta.get_key(value):
                    variable_theta.add(key,theta.get_key(value))

        if len(variable_theta.mappings)!=0:
            for condition in new_rule.conditions:
                for idx in range(len(condition.args)):
                    #in new rule have some variable name, which need a variable change to
                    if condition.args[idx] in list(variable_theta.mappings.values()):
                        #change the variable to new name, which not in new rule
                        variable_theta.add(condition.args[idx], new_rule.generate_variable_name())
        #remove key and value in new_theta some saved key in remobe_key
        for key in remove_key:
            del new_theta.mappings[key]
        if len(variable_theta.mappings) != 0:
            #change arg in conclusion of new rule
            for value, key in variable_theta.mappings.items():
                for idx in range(len(rule.conclusion.args)):
                    if (new_rule.conclusion.args[idx] == value):
                        new_rule.conclusion.args[idx] = key
            # change arg in condition of new rule
            for i_condition in range(len(new_rule.conditions)):
                for i_arg in range(len(rule.conditions[i_condition].args)):
                    if variable_theta.mappings.get(new_rule.conditions[i_condition].args[i_arg]):
                        new_rule.conditions[i_condition].args[i_arg] = variable_theta.mappings.get(new_rule.conditions[i_condition].args[i_arg])

        #new query is replaced conditions and remain query
        new_querys = new_rule.conditions + querys[1:]
        #new thate add old theta
        new_theta.mappings.update(theta.mappings)
        res.update(fol_bc_ask(facts_of_kb,rules_of_kb,new_querys, new_theta, root_query))
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

