from collections import OrderedDict

# Ordered by precedence where a lower index indicates a higher index
from dataclasses import dataclass
from typing import Optional

OPERATORS = OrderedDict({
    '*': {'operands': 1, 'function': ...},
    '.': {'operands': 2, 'function': ...},
    '|': {'operands': 2, 'function': ...},

})


class State:
    label = None
    edges = tuple()


@dataclass
class NFA:
    initial: Optional[State] = None
    accept: Optional[State] = None


def infix_to_postfix(expression: str) -> str:
    stack, output = [], []

    for token in expression:

        # Each operator is evaluated prior to being appended to the output
        if token in OPERATORS:
            while stack and list(OPERATORS).index(token) >= (len(OPERATORS) if stack[-1] is '(' else list(OPERATORS).index(stack[-1])):
                output.append(stack.pop())
            stack.append(token)

        elif token == '(':
            stack.append(token)

        elif token == ')':
            while stack and stack[-1] is not '(':
                output.append(stack.pop())
            stack.pop()
        else:
            if token != '(':
                output.append(token)

    # Add all remaining operators to the output
    for operator in stack[::-1]:
        output.append(operator)

    return ''.join(output)


def compile(expression: str):
    nfs_stack = []

    for token in expression:

        if token == '.':
            nfa2, nfa1 = (nfs_stack.pop() for _ in range(2))

            nfa1.accept.edges = (nfa2.initial,)
            nfs_stack.append(NFA(nfa1.initial, nfa2.accept))

        elif token == '|':
            nfa2, nfa1 = (nfs_stack.pop() for _ in range(2))

            initial = State()
            initial.edges = (nfa1.initial, nfa2.initial)

            accept = State()
            nfa1.accept.edges = (accept,)
            nfa2.accept.edges = (accept,)

            nfs_stack.append(NFA(initial, accept))

        elif token == '*':
            nfa1 = nfs_stack.pop()
            initial = State()
            accept = State()
            initial.edges = (nfa1.initial, accept)
            nfa1.accept.edges = (nfa1.initial, accept)
            nfs_stack.append(NFA(initial, accept))

        else:
            accept = State()
            initial = State()
            initial.label = token
            initial.edges = (accept,)
            nfs_stack.append(NFA(initial, accept))

    return nfs_stack.pop()


def match(expression: str, test_string: str) -> bool:
    nfa = compile(infix_to_postfix(expression))
    current_states, next_states = set(), set()

    # Add the initial state to the curenent set
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
    """ Returns the set of states forllowing E arrows """

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

infixes = ["a.b.c*", "a.(b|d).c*", "(a.(b|d))*", "a.(b.b)*.c"]
strings = ["", "abc", "abbc", "abcc", "abad", "abbbc"]

for i in infixes:
    for s in strings:
        print(match(i, s), i, s)
