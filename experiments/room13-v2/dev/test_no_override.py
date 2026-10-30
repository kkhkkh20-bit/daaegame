# 같은 함수 덮어쓰기 금지(지금 판의 `_old=f; def f():` 층 쌓기를 막는다), init 우선순위 꼼수 금지,
# 같은 이름의 화면 두 번 정의 금지.
import re
import unittest

from v2data import rpy_files

DEF = re.compile(r"^\s*def\s+(\w+)\s*\(")
ALIAS = re.compile(r"^\s*(\w+)\s*=\s*([A-Za-z_]\w*)\s*$")
INIT = re.compile(r"^\s*init\b(.*):\s*$")
SCREEN = re.compile(r"^screen\s+(\w+)")


class NoOverride(unittest.TestCase):
    def read(self):
        for path in rpy_files(include_qa=True):
            with open(path, encoding="utf-8") as f:
                yield path, f.read().splitlines()

    def test_each_function_defined_once(self):
        where = {}
        dup = []
        for path, lines in self.read():
            for n, line in enumerate(lines, 1):
                m = DEF.match(line)
                if m and not line.startswith(" " * 8 + " "):
                    name = m.group(1)
                    if name in where:
                        dup.append("%s: %s 와 %s:%d" % (name, where[name], path, n))
                    where[name] = "%s:%d" % (path, n)
        self.assertEqual(dup, [], "같은 함수를 두 번 정의했다(덮어쓰기)")

    def test_no_alias_then_redefine(self):
        defined = set()
        aliases = []
        for path, lines in self.read():
            for line in lines:
                m = DEF.match(line)
                if m:
                    defined.add(m.group(1))
        for path, lines in self.read():
            for n, line in enumerate(lines, 1):
                m = ALIAS.match(line)
                if m and m.group(2) in defined:
                    aliases.append("%s:%d %s" % (path, n, line.strip()))
        self.assertEqual(aliases, [], "함수를 다른 이름에 붙잡아 두는 줄(덮어쓰기 준비)")

    def test_no_init_priority(self):
        bad = []
        for path, lines in self.read():
            for n, line in enumerate(lines, 1):
                m = INIT.match(line)
                if m and re.search(r"-?\d", m.group(1)):
                    bad.append("%s:%d %s" % (path, n, line.strip()))
        self.assertEqual(bad, [], "init 우선순위 숫자 금지")

    def test_screens_defined_once(self):
        seen = {}
        dup = []
        for path, lines in self.read():
            for line in lines:
                m = SCREEN.match(line)
                if m:
                    if m.group(1) in seen:
                        dup.append(m.group(1))
                    seen[m.group(1)] = path
        self.assertEqual(dup, [])


if __name__ == "__main__":
    unittest.main()
