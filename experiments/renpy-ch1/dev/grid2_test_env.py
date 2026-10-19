"""Load the actual production init-57 helper into isolated source-test globals.
No renderer behavior is stubbed here; displayable mocks remain test-owned.
"""
from pathlib import Path
import textwrap

def load_grid2(env):
    path=Path(__file__).resolve().parents[1]/'game/room13_character_grid2_v1.rpy'
    block=path.read_text().split('init 57 python:\n',1)[1].split('\n# Wrap the final',1)[0]
    exec(compile(textwrap.dedent(block),str(path),'exec'),env)
    assert env['r13_g2_enabled']() is False
    return env
