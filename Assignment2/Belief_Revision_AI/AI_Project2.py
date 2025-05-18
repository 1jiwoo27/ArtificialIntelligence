from entailment import *
from sympy import And, Not, Or, Implies, symbols, to_cnf

# Define the belief base
belief_base = []

from sympy import symbols, Implies, Not, Or, And, simplify, S
from sympy.logic.boolalg import is_literal

def has_direct_contradiction(belief_base, new_belief, new_priority):
    # Simplify the new belief for standard comparison
    new_belief = simplify(new_belief)
    
    # Determine the contrary belief to identify contradictions
    contrary_belief = Not(new_belief) if is_literal(new_belief) else simplify(Not(new_belief))

    # Iterate over the belief base to find and resolve contradictions
    for i, (belief, priority) in enumerate(belief_base):
        # Simplify the belief for comparison
        belief = simplify(belief)

        # Check if there is a direct contradiction
        if simplify(belief) == contrary_belief:
            if new_priority > priority:
                belief_base[i] = (new_belief, new_priority)
                return True
            else:
                return False

        # Handle contradictions involving implications
        if isinstance(belief, Implies):
            # Decompose implication
            premise, consequence = belief.args
            # Check if the new belief contradicts either part of the implication
            if simplify(consequence) == contrary_belief or simplify(premise) == contrary_belief:
                if new_priority > priority:
                    belief_base[i] = (new_belief, new_priority)
                    return True
                else:
                    return False
                
    # If no contradiction is found, add the new belief to the base
    belief_base.append((new_belief, new_priority))
    return True




# Function to handle implications and check consistency
def resolve_implications(belief_base, new_belief):
    """Resolves implications and checks for consistency."""
    implications_to_resolve = []

    # Check if the new belief is an implication
    if "->" in str(new_belief):  # Convert to string
        antecedent, consequent = str(new_belief).split("->")
        antecedent = antecedent.strip()  # Remove leading/trailing spaces
        consequent = consequent.strip()  # Remove leading/trailing spaces

        # Check if there are direct contradictions with the antecedent and consequent
        if has_direct_contradiction(belief_base, antecedent, 0):  # Assuming default priority 0 for implications
            return f"Contradiction: '{antecedent}' cannot coexist with existing beliefs."
        if has_direct_contradiction(belief_base, consequent, 0):  # Assuming default priority 0 for implications
            return f"Contradiction: '{consequent}' cannot coexist with existing beliefs."

        # Add the implication to the belief base
        implications_to_resolve.append(new_belief)

        # Add the consequent as a standalone belief if it's not already there
        if consequent not in [belief for belief, _ in belief_base] and antecedent in [belief for belief, _ in belief_base]:
            belief_base.append((consequent, 0))  # Add consequent with priority 0

    return implications_to_resolve



# Function to add or update beliefs in the belief base
def update_belief(belief_base, new_belief, priority):
    for i, (b, p) in enumerate(belief_base):
        if b == new_belief:
            if priority > p:
                belief_base[i] = (new_belief, priority)  # Update priority
                print(f"Updated priority for '{new_belief}' to {priority}.")
            return True
    return False

def expand(belief_base, new_belief, priority):
    belief_base.append((new_belief, priority))
    return f"Belief added successfully: {new_belief} with plausibility {priority}"

# Main function to interact with the belief base
def main(belief_base):
    while True:
        print("\n______\nHey! \nPress [q] to quit \nPress [a] to add a belief")
        print("Press [e] to empty the belief base \nPress [d] to display the belief base")
        to_do = input("> ").lower()

        if to_do == "q":
            break
        elif to_do == "a":
            to_add = input("What do you believe? ")
            print(to_cnf(to_add))
            try:
                priority = float(input("What is the priority of this belief? (0 to 1) "))
                if priority < 0 or priority > 1:
                    print("Invalid priority. Priority must be between 0 and 1.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a numeric value for priority.")
                continue

            if len(belief_base) == 0: 
                expand(belief_base, to_add, priority)


            # Check if belief already in belief set
            if to_add in [belief for belief, _ in belief_base]:
                update_belief(belief_base, to_add, priority)
                continue # Skip

            else: 
                if PL_resolution(to_cnf(belief_base), [to_cnf(to_add)]):
                    print("The belief base entails the new belief and will not be added to keep the belief base simple")
                else: 
                    if has_direct_contradiction(belief_base, to_add, priority):
                        print("Contradiction detected, belief with highest priority added.")
                        continue  # Skip adding this belief
           
            # Resolve implications and check for consistency
            implications = resolve_implications(belief_base, to_add)
            if isinstance(implications, str):  # If it's a contradiction message
                print(implications)
                continue  # Skip adding this belief

        elif to_do == "e":
            belief_base.clear()
            print("Belief base has been emptied.")
        elif to_do == "d":
            if not belief_base:
                print("Belief base is currently empty.")
            else:
                print("Current Belief Base:")
                for belief, priority in sorted(set(belief_base), key=lambda x: x[1], reverse=True):
                    print(f"Belief: {to_cnf(belief)}, Priority: {priority}")
        else:
            print("Invalid input. Please try again.")

    # Display the final belief base when the program ends
    print("Final belief base:", belief_base)


if __name__ == "__main__":
        
    main(belief_base)

