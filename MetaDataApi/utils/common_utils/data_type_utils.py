def is_integer(input):
    try_convert_to_type(input, int)


def is_float(input):
    try_convert_to_type(input, float)


def try_convert_to_type(input, method):
    try:
        method(input)
        return True
    except ValueError:
        return False
