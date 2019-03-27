from dataclasses import dataclass
from typing import Optional, List, Tuple

# Order of precedence for operators is derived from it's index e.g. index of '0' would indicate highest precedence.
OPERATORS = ['*', '+', '?', '.', '|']


class State:
    label: Optional[str] = None
    edges: Tuple = tuple()


@dataclass
class NFA:
    initial: Optional[State] = None
    accept: Optional[State] = None


def infix_to_postfix(infix_expression: str) -> str:
    stack, output = [], []

    for token in infix_expression:

        # Pop stack until a lower priority operator is found. A '(' will be considered to have the highest priority.
        if token in OPERATORS:
            while stack and OPERATORS.index(token) >= (len(OPERATORS) if stack[-1] is '(' else OPERATORS.index(stack[-1])):
                output.append(stack.pop())
            stack.append(token)

        # A '(' will be considered to have the highest priority and therefore will be always be added to top of stack
        elif token == '(':
            stack.append(token)

        # A ')' will pop the stack until a '(' is found.
        elif token == ')':
            while stack and stack[-1] is not '(':
                output.append(stack.pop())
            stack.pop()

        # Non-parentheses and non-operators are immediately added to the output
        else:
            output.append(token)

    # Add all remaining operators to the output
    for operator in stack[::-1]:
        output.append(operator)

    return ''.join(output)


def build_nfa(postfix_expression: str) -> NFA:
    nfs_stack: List[NFA] = []

    for token in postfix_expression:

        if token is '.':
            nfa_2, nfa_1 = (nfs_stack.pop() for _ in range(2))

            # Connect nfa_1 to nfa_2
            nfa_1.accept.edges = (nfa_2.initial,)

            nfs_stack.append(NFA(nfa_1.initial, nfa_2.accept))

        elif token is '|':
            nfa_2, nfa_1 = (nfs_stack.pop() for _ in range(2))

            # Create a new state and connect both NFA's initial state to the new state
            initial = State()
            initial.edges = (nfa_1.initial, nfa_2.initial)

            # Create a new accept state and set both NFA's edges to the new accept state
            accept = State()
            nfa_1.accept.edges = (accept,)
            nfa_2.accept.edges = (accept,)

            nfs_stack.append(NFA(initial, accept))

        elif token is '*':
            nfa = nfs_stack.pop()
            initial, accept = State(), State()

            # In the newly created initial state set it's edges to the NFA's initial state and the newly created accept
            initial.edges = (nfa.initial, accept)

            # Connect the NFA to its initial state and the new accept state
            nfa.accept.edges = (nfa.initial, accept)
            nfs_stack.append(NFA(initial, accept))

        elif token is '+':
            nfa = nfs_stack.pop()

            initial, accept = State(), State()
            # Connect the new initial state to the NFA's initial state
            initial.edges = (nfa.initial,)

            # Connect the NFA to the newly created initial state and accept state
            nfa.accept.edges = (initial, accept,)
            nfs_stack.append(NFA(initial, accept))

        elif token is '?':
            nfa = nfs_stack.pop()
            initial, accept = State(), State()

            # In the newly created initial state set it's edges to the NFA's initial state and the newly created accept
            initial.edges = (nfa.initial, accept)

            # Connect the NFA to the new accept state
            nfa.accept.edges = (accept,)
            nfs_stack.append(NFA(initial, accept))
        else:
            accept = State()
            initial = State()
            initial.label = token
            initial.edges = (accept,)
            nfs_stack.append(NFA(initial, accept))

    return nfs_stack.pop()


def match(infix_expression: str, test_string: str) -> bool:
    # Convert infix expression to postfix and build a NFA from said expression
    nfa = build_nfa(infix_to_postfix(infix_expression))

    current_states, next_states = set(), set()

    # Add the initial state to the current set
    current_states = current_states.union(follow_es(nfa.initial))

    for token in test_string:
        # Loop through the set of states
        for c in current_states:
            if c.label == token:
                # Add the edge1 state to the next set
                next_states = next_states.union(follow_es(c.edges[0]))

        # Set current to next, and clear out next
        current_states = next_states.copy()
        next_states.clear()

    # Check if the accept state is in the set oc current states
    return nfa.accept in current_states


def follow_es(state: State):
    # Create a new set, with state as it's only member
    states = {state}

    if state.label is None:
        for s in state.edges:
            states = states.union(follow_es(s))

    return states


tests = [
    # Simple non grouped expressions
    ('a.b|c.a', 'ab.ca.|'), ('a.b.c*', 'ab.c*.'), ('a.b|d.c*', 'ab.dc*.|'), ('a.bd*', 'abd*.'),
    ('a.b.b*.c*', 'ab.b*.c*.'), ('a.b.c*', 'ab.c*.'),

    # Simple expressions with grouping
    ('a.(b|d).c*', 'abd|.c*.'), ('(a.(b|d))*', 'abd|.*'), ('a.(b.b)*.c*', 'abb.*.c*.'),
]

# for expression, expected_result in tests:
#     result = infix_to_postfix(expression)
#     print()
#     print('Expression:', expression)
#     print('Expected Result:', expected_result)
#     print('Result:', result)
#     print('Test:', expected_result == result)
#     print()

infixes = ["a.b.c*", "a.(b|d).c*", "(a.(b|d))*", "a.(b.b)*.c", 'a+', '(a|b)+', 'a?', '(a|b)?']
strings = ["", "abc", "abbc", "abcc", "abad", "abbbc", 'a', 'aaa', 'ab', 'abab', 'ababa', 'a', 'aa', 'b']

for i in infixes:
    for s in strings:
        print(match(i, s), i, s)
