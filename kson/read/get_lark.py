from pathlib import Path
import lark

GRAMMAR_DIR = Path(__file__).parents[2] / 'grammar'
JSON_GRAMMAR = (GRAMMAR_DIR / 'json.lark').read_text()
KSON_GRAMMAR = (GRAMMAR_DIR / 'kson.lark').read_text()


def get_lark(transformer, use_bytes=False, grammar=KSON_GRAMMAR):
    return lark.Lark(
        grammar,
        transformer=transformer,
        parser='lalr',
        lexer='standard',
        propagate_positions=False,
        maybe_placeholders=False,
        use_bytes=use_bytes,
    )
