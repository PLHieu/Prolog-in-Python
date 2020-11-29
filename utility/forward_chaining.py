from utility.unify import unify
from object.ClassTheta import *
from itertools import permutations


def unify_of_rule(facts_1, facts_2):  # Generalized Modus Ponens
    if len(facts_1) != len(facts_2):
        return False

    for f1, f2 in zip(facts_1, facts_2):
        if f1.get_op() != f2.get_op():
            return False

    return unify(facts_1, facts_2, Theta())

def forward_chaining(kb, query):
    facts_of_kb = set(kb.facts)
    rules_of_kb = list(kb.rules)
    result = set()
    for fact in facts_of_kb:
        theta= unify(fact, query, Theta())
        #if face contain query
        if (theta):
            if len(theta.mappings)==0:
            #add true
                result.add("true")
                return result
            result.add(theta)

    neareast_facts = facts_of_kb

    while True:
        new_facts=[]
        for  rule in rules_of_kb:
            #if neareast facts do not support this rule then continute
            if not rule.is_potential_with(neareast_facts):
                continue

            #get facts have operator on rule
            appropcitate_facts = rule.get_appropciate_fact(facts_of_kb)


            set_of_generated_conditions = permutations(appropcitate_facts, len(rule.conditions))

            for generated_conditions in set_of_generated_conditions:
                #convert set to list of conditions
                generated_conditions = list(generated_conditions)
                generated_conditions.sort()

                theta = unify_of_rule(rule.conditions,generated_conditions);

                if not theta:
                    continue
                accepted_fact = rule.conclusion.copy()
                #set constant for rule
                for i in range(len(accepted_fact.args)):
                    const = theta.get_const(accepted_fact.args[i])
                    if (const):
                        accepted_fact.args[i] = const
                if accepted_fact not in new_facts and accepted_fact not in facts_of_kb:
                    new_facts.append(accepted_fact)


                    theta = unify(accepted_fact, query, Theta())
                    # if face contain query
                    if theta:
                        if len(theta.mappings)==0:
                            # add true
                            result.add("true")
                            return result
                        result.add(theta)
            #no new fact was infered
        if not new_facts:
            if not result:
                result.add("false")
            return result

        neareast_facts = new_facts
        facts_of_kb.update(new_facts)