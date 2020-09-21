from kson.write import quote
import unittest


class QuoteTest(unittest.TestCase):
    def test_empty(self):
        assert quote.single('') == "''"
        assert quote.single_ascii('') == "''"
        assert quote.double('') == '""'
        assert quote.double_ascii('') == '""'

    def test_single(self):
        assert quote.single(' ') == "' '"
        assert quote.single_ascii(' ') == "' '"
        assert quote.double(' ') == '" "'
        assert quote.double_ascii(' ') == '" "'

    def test_quote(self):
        assert quote.single("'") == "'\\''"
        assert quote.single_ascii("'") == "'\\''"
        assert quote.double("'") == '"\'"'
        assert quote.double_ascii("'") == '"\'"'

    def test_quote2(self):
        assert quote.single('"') == "'\"'"
        assert quote.single_ascii('"') == "'\"'"
        assert quote.double('"') == '"\\""'
        assert quote.double_ascii('"') == '"\\""'

    def test_backslashes(self):
        assert quote.single('\n') == "'\\n'"
        assert quote.single_ascii('\n') == "'\\n'"
        assert quote.double('\n') == '"\\n"'
        assert quote.double_ascii('\n') == '"\\n"'

    def test_more_backslashes(self):
        assert quote.single('\\n') == "'\\\\n'"
        assert quote.double('\\n') == '"\\\\n"'
        assert quote.single('\\\n') == "'\\\\\\n'"
        assert quote.double('\\\n') == '"\\\\\\n"'
        assert quote.single('\\\\n') == "'\\\\\\\\n'"
        assert quote.double('\\\\n') == '"\\\\\\\\n"'
        assert quote.single('\\\\\n') == "'\\\\\\\\\\n'"
        assert quote.double('\\\\\n') == '"\\\\\\\\\\n"'
        assert quote.single('\\\\\n') == "'\\\\\\\\\\n'"
        assert quote.double('\\\\\n') == '"\\\\\\\\\\n"'

    def test_extended(self):
        assert quote.single('🔑') == "'🔑'"
        assert quote.single_ascii('🔑') == "'\\ud83d\\udd11'"
        assert quote.double('🔑') == '"🔑"'
        assert quote.double_ascii('🔑') == '"\\ud83d\\udd11"'

    def test_quoter(self):
        assert quote.quoter(False, False)('🔑') == "'🔑'"
        assert quote.quoter(False, True)('🔑') == "'\\ud83d\\udd11'"
        assert quote.quoter(True, False)('🔑') == '"🔑"'
        assert quote.quoter(True, True)('🔑') == '"\\ud83d\\udd11"'
