from collections import OrderedDict

# Ordered by precedence where a lower index indicates a higher index
OPERATORS = OrderedDict({
    '*': {'operands': 1, 'function': ...},
    '.': {'operands': 2, 'function': ...},
    '|': {'operands': 2, 'function': ...},

})


def infix_to_postfix(expression: str) -> str:
    stack = []
    output = []

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


tests = [  # abc.a|
    # Simple non grouped expressions
    ('a.b|c.a', 'ab.ca.|'), ('a.b.c*', 'ab.c*.'), ('a.b|d.c*', 'ab.dc*.|'), ('a.bd*', 'abd*.'),
    ('a.b.b*.c*', 'ab.b*.c*.'), ('a.b.c*', 'ab.c*.'),

    # Simple expressions with grouping
    ('a.(b|d).c*', 'abd|.c*.'), ('(a.(b|d))*', 'abd|.*'), ('a.(b.b)*.c*', 'abb.*.c*.'),
]

for expression, expected_result in tests:
    result = infix_to_postfix(expression)
    print()
    print('Expression:', expression)
    print('Expected Result:', expected_result)
    print('Result:', result)
    print('Test:', expected_result == result)
    print()
