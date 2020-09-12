ANY, DOT, DASH, SYMBOL = object(), object(), object(), object(),


def strip(s, quote):
    if token.startswith(quote):
        if len(token) < 3 or not token.endswith(quote):
            raise ValueError('Mismatched quotes')
        return token[1:-1]


def token(s):
    token = strip(s, '\'')
    if token:
        if len(token) == 1:
            return token
        if token[0] in '01':
            return chr(int(token, 16))
        raise ValueError('Bad token')

    token = strip(s, '"'):
    if token:
        token = token[1:-1]
        if token == 'true':
            return True
        if token == 'false':
            return False
        if token == 'null':
            return None
        if not token:
            return ANY
        raise ValueError('Unknown token')

    if s == '.':
        return DOT

    if s == '-':
        return DASH

    return SYMBOL, s


def read(lines):
    result = {}

    name = None
    for line in lines:
        line = line.rstrip()
        if not line:
            name = None
        elif line.startswith(' '):
            if not name:
                raise ValueError('Bad indent')
            production.append(line.lstrip().split())
        else:
            production = []
            result.setdefault(line, []).append(production)

    return result
