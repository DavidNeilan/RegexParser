from collections import OrderedDict

# Ordered by precedence where a lower index indicates a higher index
OPERATORS = OrderedDict({
    '*': lambda x, y: x * y,
    '.': str.__add__,
    '|': str,
})


def infix_to_postfix(expression: str) -> str:
    stack = []
    output = []

    for token in expression:

        # Each operator is evaluated prior to being appended to the output
        if token in OPERATORS:

            if stack:
                # Checks if current operator has a lower precedence of the last operator on the stack
                if list(OPERATORS).index(token) < list(OPERATORS).index(stack[-1]):
                    stack.append(token)
                else:
                    while list(OPERATORS).index(token) >= list(OPERATORS).index(stack[-1]):
                        output.append(stack.pop())
                        if not stack:
                            break
                    stack.append(token)

            else:
                stack.append(token)

        # All letters are appended to the output
        else:
            output.append(token)

    # Add all remaining operators to the output
    for operator in stack[::-1]:
        output.append(operator)

    return ''.join(output)


tests = [  # abc.a|
    ('a.b|c.a', 'ab.ca.|'),
    ('a.b.c*', 'ab.c*.'),
    ('a.b|d.c*', 'ab.dc*.|'),
    ('a.bd*', 'abd*.'),
    ('a.b.b*.c*', 'ab.b*.c*.'),
    ('a.b.c*', 'ab.c*.'),
    ('a.(b|d).c*', 'abd|.c*.'),
    ('(a.(b|d))*', 'abd|.*'),
    ('a.(b.b)*.c*', 'abb.*.c*.'),
]

for exp, res in tests:
    print((exp, res), infix_to_postfix(exp) == res)

