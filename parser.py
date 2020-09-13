from pathlib import Path
import lark
import sys
import json_parser

from lark import Lark

### Create the JSON parser with Lark, using the Earley algorithm
# json_parser = Lark(json_grammar, parser='earley', lexer='standard')
# def parse(x):
#     return TreeToJson().transform(json_parser.parse(x))

### Create the JSON parser with Lark, using the LALR algorithm
def make_parser(module):
    return lark.Lark(
        module.GRAMMAR,
        transformer=module.Transformer(),
        parser='lalr',
        lexer='standard',
        propagate_positions=False,
        maybe_placeholders=False,
    ).parse


parse = make_parser(json_parser)
TEST = True

def test():
    test_json = '''
        {
            "empty_object" : {},
            "empty_array"  : [],
            "booleans"     : { "YES" : true, "NO" : false },
            "numbers"      : [ 0, 1, -2, 3.3, 4.4e5, 6.6e-7 ],
            "strings"      : [ "This", [ "And" , "That", "And a \\"b" ] ],
            "nothing"      : null
        }
    '''

    j = parse(test_json)
    print(j)
    import json
    assert j == json.loads(test_json)



if __name__ == '__main__':
    if TEST:
        test()

    else:
        with open(sys.argv[1]) as f:
            print(parse(f.read()))
