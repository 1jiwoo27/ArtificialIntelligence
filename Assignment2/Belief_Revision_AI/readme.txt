# BeliefBase

## Overview
This directory contains two Python scripts: one for beliefbase and another for implementing function of entilment. 

## Scripts:
1. AI_Project2.py: This script provides the implementation of the BeliefBase and an interface for the user.
2. entailment.py: This script implements some functions for the entailment.

## Requirements
- Python 3.8

## Usage
1. Ensure you have Python installed on your system.
2. Open a terminal or command prompt.
3. Navigate to the directory containing both scripts.
4. Run the 'AI_Project2.py' script using the following command:
	python AI_Project2.py
5. Follow the on-screen instructions to add, display, empty beliefs or to quit.

## AI_Project2
- When run, if asks if the user wants to add, display, empty beliefs or quit.
- When adding new beliefs, they are compared to other beliefs already in the base, if they are.
- If there is direct contradiction, the belief with higher plausability is kept, and the other disregarded.
- The base will be expanded if a new belief is added and fills the requirements for that action.
- Implications are resolved and consistency is checked.

## Entailment
- PL-resolution algorithm from the book is implemented. 

## Credits
- Developed by Group 43 - F24 02180 Introdcution to AI at The Technical University of Denmark.