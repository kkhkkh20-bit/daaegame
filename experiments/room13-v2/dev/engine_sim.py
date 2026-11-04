"""화면을 만들지 않고 실제 엔진 함수와 현재 이야기 데이터를 실행하는 시험 도우미."""
import copy
import textwrap
import types
from pathlib import Path

from v2data import GAME


def 무동작(*args, **kwargs):
    return None


class RenpyStub:
    def __init__(self):
        self.music = types.SimpleNamespace(play=무동작, stop=무동작)
        self.tags = {}

    def open_file(self, path, **kwargs):
        return (Path(GAME) / path).open(**kwargs)

    def show(self, tag, **kwargs):
        self.tags[tag] = kwargs.get("what")

    def hide(self, tag):
        self.tags.pop(tag, None)

    def scene(self):
        self.tags.clear()

    with_statement = staticmethod(무동작)
    notify = staticmethod(무동작)
    say = staticmethod(무동작)
    choice_for_skipping = staticmethod(무동작)
    retain_after_load = staticmethod(무동작)
    restart_interaction = staticmethod(무동작)


class EngineSim:
    def __init__(self):
        self.store = types.SimpleNamespace(v2_pick=[], v2_pick_for=None, v2_pair=False, v2_stage=None)
        self.persistent = types.SimpleNamespace(v2_text_size="normal", v2_last_end=None)
        self.ns = dict(store=self.store, persistent=self.persistent, renpy=RenpyStub(),
                       Character=무동작, Transform=무동작, Fixed=무동작, Solid=무동작,
                       Dissolve=무동작, SnowBlossom=무동작, AlphaMask=무동작, Fade=무동작,
                       vpunch=None, v2_jolt=None)
        source = (Path(GAME) / "engine/engine.rpy").read_text(encoding="utf-8")
        source = source.split("init python:\n", 1)[1].split("\ntransform ", 1)[0]
        exec(compile(textwrap.dedent(source), "engine.rpy", "exec"), self.ns)
        self.call("v2_new_game")
        self.lines = []

    def call(self, name, *args, **kwargs):
        return self.ns[name](*args, **kwargs)

    def drain(self):
        for _ in range(2000):
            kind = self.call("v2_advance")
            if kind == "line":
                frame, step = self.call("v2_current")
                if frame[2] == 0:
                    self.lines.append(copy.deepcopy(step))
                # 대사 쪽 넘김·자료 그림·읽음 ID도 엔진의 실제 함수를 거친다.
                self.call("v2_do_line")
            elif kind == "wait":
                self.call("v2_wait_enter")
                return kind
            else:
                return kind
        raise AssertionError("대화 실행이 2000단계 안에 멈추지 않았다.")

    def expect(self, kind):
        actual = self.drain()
        return self.require(actual, kind)

    def require(self, actual, kind):
        if actual != kind:
            raise AssertionError("기대한 대기 %r, 실제 %r" % (kind, actual))
        return actual

    def option(self, gate, index):
        available = dict(self.call("v2_gate_options", gate))
        if index not in available:
            raise AssertionError("현재 조건에서 열리지 않은 선택지: %s/%d" % (gate, index))
        self.call("v2_run_option", gate, index)
        return self.drain()

    def investigate(self, rules=False):
        self.expect("wait")
        self.require(self.store.v2_gate, "gate_request")
        self.require(self.option("gate_request", 1), "wait")
        self.require(self.option("gate_choice", 1), "menu")
        self.call("v2_menu_choose", 1)
        self.expect("wait")
        self.require(self.option("gate_investigate", 0), "wait")
        if rules:
            self.require(self.option("gate_investigate", 1), "wait")

    def submit_gate(self, evidence):
        self.require(self.option("gate_investigate", 4), "proof")
        self.call("v2_proof_prepare", "gate")
        self.call("v2_proof_result", ("submit", list(evidence)))
        return self.drain()

    def dismiss_topics(self):
        if self.store.v2_ui:
            self.call("v2_ui_result", ("back",))

    def line_ids(self):
        return [line.get("id") for line in self.lines if line.get("id")]
