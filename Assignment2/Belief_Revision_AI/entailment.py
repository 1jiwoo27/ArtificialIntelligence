def negate(literal):
    if isinstance(literal, tuple) and literal[0] == 'not':
        return literal[1]  # Return the positive literal
    return ('not', literal)  # Return the negated literal

def pl_resolve(ci, cj):
    """Resolve two clauses ci, cj."""
    resolvents = []
    for di in ci:
        for dj in cj:
            if negate(di) == dj or di == negate(dj):
                # Create a new resolvent clause without di and dj
                new_ci = [x for x in ci if x != di]
                new_cj = [x for x in cj if x != dj]
                resolvent = list(set(new_ci + new_cj))  # Remove duplicates
                if len(resolvent) == 0:
                    return [False]  # Represent contradiction with [False]
                resolvents.append(resolvent)
    return resolvents  # Return the list of resolvents (empty if none are found)

def PL_resolution(belief_base, query):
    """Determine if the belief base entails the query using the resolution algorithm."""
    # negate query
    negated_query = [negate(q) for q in query]  # Assuming query is a single clause
    
    # Add the negated query to the belief base
    clauses = belief_base + [negated_query]
    new = set()

    while True:
        n = len(clauses)
        pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i + 1, n)]
        new_this_round = set()

        for (ci, cj) in pairs:
            resolvents = pl_resolve(ci, cj)
            for resolvent in resolvents:
                if resolvent == [False]:  # Empty clause found, indicating a contradiction
                    return True
                # Convert the list to a tuple to make it hashable for the set
                new_this_round.add(tuple(resolvent))

        if new_this_round.issubset(new):  # If no new resolvents, belief base does not entail the query
            return False

        # Update the set of new clauses with the new resolvents found in this round
        new.update(new_this_round)

        # Update the clauses with the new resolvents, converting them back to lists
        clauses.extend(list(resolvent) for resolvent in new_this_round if list(resolvent) not in clauses)