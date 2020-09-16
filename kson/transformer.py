import lark

args = lark.v_args(inline=True)


class JsonTransformer(lark.Transformer):
    @args
    def string(self, s):
        sep = s[0]
        return s[1:-1].replace('\\' + sep, sep)

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


class KsonTransformer(JsonTransformer):
    pass
