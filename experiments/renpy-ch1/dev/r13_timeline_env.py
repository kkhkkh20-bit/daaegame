"""Ren'Py에서는 날짜표 상수(R13_CASE_DAY 등, game/systems/room13_timeline.rpy init -200)가 store 전역이다.
단위 테스트는 .rpy 블록을 따로 exec하므로, 같은 값을 builtins에 올려 어느 namespace에서도 보이게 한다."""
import builtins, pathlib, textwrap
_SRC = (pathlib.Path(__file__).resolve().parents[1] / "game/systems/room13_timeline.rpy").read_text()
_ns = {}
exec(textwrap.dedent(_SRC.split("init -200 python:\n")[1].split("\ninit ")[0]), _ns)
for _k, _v in _ns.items():
    if _k.startswith(("R13_", "r13_")):
        setattr(builtins, _k, _v)
