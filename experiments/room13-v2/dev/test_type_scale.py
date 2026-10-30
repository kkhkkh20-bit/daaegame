# 글자 크기는 v2_type 단계로만(숫자 크기 하드코딩 금지).
import re
import unittest

from v2data import rpy_files

LITERAL = re.compile(r"\b(?:text_)?size\s+\(?\s*\d")
STYLE_SIZE = re.compile(r"^\s+size\s+\d")


class TypeScale(unittest.TestCase):
    def test_no_literal_sizes(self):
        bad = []
        for path in rpy_files(include_qa=True):
            with open(path, encoding="utf-8") as f:
                for n, line in enumerate(f, 1):
                    code = line.split("#", 1)[0]
                    if LITERAL.search(code) or STYLE_SIZE.match(code):
                        bad.append("%s:%d %s" % (path, n, line.strip()))
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main()
