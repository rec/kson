from pathlib import Path
from tatsu import parse
from tatsu.util import asjson
import json
import pprint
import sys

GRAMMAR = Path('grammar.tat')
TEST = '3 + 5 * ( 10 - 20 )'

if __name__ == '__main__':
    text = ''.join(sys.argv[1:]) or TEST
    ast = parse(GRAMMAR.read_text(), text)
    print('# JSON')
    print(json.dumps(asjson(ast), indent=2))
    print()
