from unify import unify
from ClassTheta import  Theta
from itertools import permutations

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

    while True:
        new_facts=[]
        for rule in rules_of_kb:

            appropcitate_facts = rule.get_appropciate_fact(facts_of_kb)

            set_of_generated_conditions = permutations(appropcitate_facts, len(rule.conditions))

            for generated_conditions in set_of_generated_conditions:
                #convert tuple to list of conditions
                generated_conditions = list(generated_conditions)
                generated_conditions.sort()

                if len(generated_conditions)!=len(rule.conditions):
                    continue
                theta = unify(rule.conditions,generated_conditions, Theta());
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

                    #remove rule when rule was infered
                    rules_of_kb.remove(rule)
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
        facts_of_kb.update(new_facts)