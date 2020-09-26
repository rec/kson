from pathlib import Path
import lark

GRAMMAR_DIR = Path(__file__).parents[2] / 'grammar'


def grammar(name):
    return (GRAMMAR_DIR / (name + '.lark')).read_text()


def get_lark(transformer, use_bytes=False, grammar=None):
    return lark.Lark(
        grammar or KSON_GRAMMAR,
        transformer=transformer,
        parser='lalr',
        lexer='standard',
        propagate_positions=False,
        maybe_placeholders=False,
        use_bytes=use_bytes,
    )


def parser(transformer, use_bytes=False, grammar=None):
    return get_lark(transformer, use_bytes, grammar).parser.parse


KSON_GRAMMAR = grammar('kson')
