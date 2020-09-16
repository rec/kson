import lark

args = lark.v_args(inline=True)


class Transformer(lark.Transformer):
    @args
    def string(self, s):
        return s[1:-1].replace('\\' + s[0], s[0])

    array = list
    pair = tuple
    object = dict
    number = args(float)

    def null(self, _):
        return None

    def false(self, _):
        return False

    def true(self, _):
        return True
