def is_valid_bracket_sequence(sequence: str) -> bool:
    stack = []

    for bracket in sequence:
        if bracket == '(':
            stack.append('(')
        elif bracket == ')':
            if not stack:
                return False
            stack.pop()

    return not stack


user_input = input("Введите скобочную последовательность: ")
if is_valid_bracket_sequence(user_input):
    print("Правильная последовательность скобок")
else:
    print("Неправильная последовательность скобок")
