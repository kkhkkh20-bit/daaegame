"""Source-backed Sling branches, not a Ren'Py renderer or a gameplay pass.

Loads production helpers and interprets only the Ren'Py statements used by these
labels. Menus, conditions, Python actions, and nested label calls come from the
actual .rpy files; expected flag/cash changes are not a second implementation.
The fixture does not start Ren'Py, render a scene, or emulate save/rollback UI.
"""
import ast
import copy
import io
import json
import re
import textwrap
import tokenize
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = "systems/room13_week1_cases.rpy"
MEMORY = "systems/room13_memory.rpy"
CONFIDENCE = "systems/room13_sling_confidence.rpy"


def source(relative):
    return (ROOT / "game" / relative).read_text(encoding="utf-8")


def load_function(namespace, relative, name):
    lines = source(relative).splitlines(True)
    start = next(i for i, line in enumerate(lines)
                 if line.startswith("    def " + name + "("))
    end = start + 1
    while end < len(lines):
        if lines[end].strip() and not lines[end].startswith("        "):
            break
        end += 1
    exec(compile(textwrap.dedent("".join(lines[start:end])), relative, "exec"), namespace)


class LabelReturn(Exception):
    pass


class SourceBranches:
    """Intentionally bounded reader: unknown Ren'Py syntax fails, never skips."""
    def __init__(self, namespace, files, menu):
        self.ns, self.menu, self.labels = namespace, menu, {}
        for relative in files:
            text = source(relative)
            headers = list(re.finditer(r"^label (\w+)(?:\((.*?)\))?:\s*$", text, re.M))
            for i, header in enumerate(headers):
                end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
                self.labels[header[1]] = (header[2] or "", self.logical(text[header.end():end]))

    @staticmethod
    def logical(text):
        result, pending, indent = [], "", 0
        for line in text.splitlines():
            if not pending:
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                indent = len(line) - len(line.lstrip())
            pending += ("\n" if pending else "") + line.strip()
            balance = 0
            try:
                for token in tokenize.generate_tokens(io.StringIO(pending).readline):
                    if token.type == tokenize.OP:
                        if token.string in "([{": balance += 1
                        elif token.string in ")]}": balance -= 1
            except tokenize.TokenError:
                pass
            if balance == 0:
                result.append((indent, pending))
                pending = ""
        if pending:
            raise AssertionError("Unclosed statement: " + pending)
        return result

    def evaluate(self, expression, frame):
        return eval(expression, self.ns, dict(frame, room13=self.ns["store"].room13))

    @staticmethod
    def suite_end(lines, start, indent):
        end = start
        while end < len(lines) and lines[end][0] > indent:
            end += 1
        return end

    def run(self, label, *args, **kwargs):
        parameters, lines = self.labels[label]
        # Bind production label defaults and restore them on nested calls.
        signature = ast.parse("def label(" + parameters + "): pass").body[0].args
        names = [arg.arg for arg in signature.args]
        frame = dict(zip(names[-len(signature.defaults):],
                         [self.evaluate(ast.unparse(d), {}) for d in signature.defaults])) if signature.defaults else {}
        frame.update(zip(names, args))
        frame.update(kwargs)
        try:
            self.block(lines, frame)
        except LabelReturn:
            pass

    def block(self, lines, frame):
        index = 0
        while index < len(lines):
            indent, text = lines[index]
            if text.startswith("if "):
                clauses, end = [], index
                while end < len(lines) and lines[end][0] == indent:
                    head = lines[end][1]
                    if not (head.startswith("if ") or head.startswith("elif ") or head == "else:"):
                        break
                    stop = self.suite_end(lines, end + 1, indent)
                    condition = "True" if head == "else:" else head.split(" ", 1)[1][:-1]
                    clauses.append((condition, lines[end + 1:stop]))
                    end = stop
                    if end >= len(lines) or not (lines[end][1].startswith("elif ") or lines[end][1] == "else:"):
                        break
                for condition, body in clauses:
                    if self.evaluate(condition, frame):
                        self.block(body, frame)
                        break
                index = end
                continue
            if text == "menu:":
                end = self.suite_end(lines, index + 1, indent)
                choices, cursor = [], index + 1
                while cursor < end:
                    level, choice = lines[cursor]
                    match = re.fullmatch(r'("(?:[^"\\]|\\.)*")(?: if (.*))?:', choice)
                    if not match:
                        raise AssertionError("Unsupported menu: " + choice)
                    stop = self.suite_end(lines, cursor + 1, level)
                    if match[2] is None or self.evaluate(match[2], frame):
                        choices.append((ast.literal_eval(match[1]), lines[cursor + 1:stop]))
                    cursor = stop
                selected = self.menu([title for title, _ in choices])
                self.block(dict(choices)[selected], frame)
                index = end
                continue
            if text.startswith("$ "):
                frame["room13"] = self.ns["store"].room13
                exec(text[2:], self.ns, frame)
            elif text.startswith("call "):
                expression = text[5:]
                if "(" not in expression:
                    expression += "()"
                call = ast.parse(expression, mode="eval").body
                name = call.func.id
                args = [self.evaluate(ast.unparse(a), frame) for a in call.args]
                kwargs = {k.arg: self.evaluate(ast.unparse(k.value), frame) for k in call.keywords}
                if name in self.ns:
                    self.ns[name](*args, **kwargs)
                else:
                    self.run(name, *args, **kwargs)
            elif text == "return" or text.startswith("return "):
                raise LabelReturn()
            elif text != "pass":
                raise AssertionError("Unsupported statement: " + text)
            index += 1


class SlingChoiceFlow(unittest.TestCase):
    IGNORE = "“못 본 것으로 하겠습니다.”"
    CATCH = "“편지에서 뭘 보려는 겁니까?”"
    WHO = "“직접 보려는 겁니까?”"
    REPORT = "편지 개봉을 경비에게 알린다"
    PROCEED = "그래도 경비에게 알린다"
    LISTEN = "“먼저 사정을 듣겠습니다.”"
    PORTRAIT = "전에 보인 아내 초상을 꺼낸다"
    STOP = "“남의 편지는 열지 마세요.”"
    PAY = "슬링의 오늘 몫 지원 (내 돈 3냥)"
    SEND = "“이 편지는 그대로 보내 주세요.”"
    FAKE = "가짜 약속 쪽지를 맡긴다"

    def setUp(self):
        self.store = types.SimpleNamespace(room13=dict(
            day=2, period=0, location="post", flags=[], evidence=[], records={},
            encounters=[], read_topics=[], case_state="pending", victim_state="alive",
            daram_state="with_dad", livelihood={"cash":3}), r13_topic_shown=None)
        self.lines, self.menus, self.choices = [], [], []
        self.n = dict(store=self.store, winter_copy=copy,
            persistent=types.SimpleNamespace(room13_knowledge=[]),
            R13_NAMES={"resident_sling":"슬링", "neoul":"너울"},
            R13_TRIAL_DAY=10, R13_CASE_DAY=7, R13_WEEK2_DAY=11,
            R13_TL_MAP={4:7, 5:8, 6:9, 7:10, 8:11},
            ROOM13={"evidence":{k:{"name":k} for k in ("H9","E17")},
                    "topics":{"somi_after_hostile":{}, "siluk_cold":{}}},
            R13_TOPIC_LABELS={}, R13_CONTACT_RECORDS={}, r13_topics=lambda p:[],
            r13_remember_line=lambda key:None, source_fx=lambda *a:None,
            r13_evidence_acquired=lambda *a:None,
            r13_calendar_key=lambda p:"test:"+p,
            r13_topic_current_context=lambda k:None,
            r13_conversation_topic_lines=lambda k:[], r13_present=lambda *a:[],
            r13_w2e_unflag=lambda *a:None, r13_ev_here=lambda *a:None,
            r13_scene=lambda *a:None, r13_owl_events=lambda:None,
            r13_offer=lambda *a:None, r13_lines=self.show)
        for name in ("r13_edit","r13_flag","r13_has","r13_grant","r13_available","r13_finish_topic"):
            load_function(self.n, "room13_rules.rpy", name)
        for relative, name in (
            ("systems/room13_livelihood_model.rpy","r13_wallet"),
            ("systems/room13_town_events.rpy","r13_cash"),
            ("systems/room13_town_events.rpy","r13_cash_now"),
            ("systems/room13_timeline.rpy","r13_tl"),
            ("room13_life.rpy","r13_note_encounter"),
            ("room13_notebook.rpy","r13_met_people"),
            (CASES,"r13_sling_note_confession"),
            (CASES,"r13_sling_can_support_day"),
            (CASES,"r13_sling_support_day")):
            load_function(self.n, relative, name)
        block = source(MEMORY).split("init 114 python:\n", 1)[1].split("\nlabel ", 1)[0]
        exec(compile(textwrap.dedent(block), MEMORY, "exec"), self.n)
        block = source(CONFIDENCE).split("init 206 python:\n", 1)[1].split("\nlabel ", 1)[0]
        exec(compile(textwrap.dedent(block), CONFIDENCE, "exec"), self.n)
        self.runner = SourceBranches(self.n, (CASES, MEMORY, CONFIDENCE), self.choose)

    @property
    def s(self):
        return self.store.room13

    def show(self, rows, identity, **kwargs):
        self.lines.append((identity, copy.deepcopy(rows), copy.deepcopy(self.s)))

    def choose(self, choices):
        self.menus.append((choices, copy.deepcopy(self.s), copy.deepcopy(self.lines)))
        self.assertTrue(self.choices, "Unexpected menu: " + repr(choices))
        selected = self.choices.pop(0)
        self.assertIn(selected, choices)
        return selected

    def run_letters(self, *choices):
        self.choices = list(choices)
        self.runner.run("r13_w1c_letters")
        self.assertEqual([], self.choices)

    def has(self, key):
        return self.n["r13_has"](key)

    def money(self):
        return self.n["r13_cash_now"]()

    def available(self, key):
        return self.n["r13_available"](self.n["ROOM13"]["topics"][key])

    def test_first_encounter_has_visible_seam_and_permission_before_choice(self):
        self.run_letters(self.IGNORE)
        choices, state, rows = self.menus[0]
        self.assertNotIn(self.PAY, choices)
        self.assertEqual(["w1c:letters:intro","w1c:letters:open"], [r[0] for r in rows])
        text = str(rows)
        self.assertIn("풀 붙인 귀퉁이가 조금씩 들렸다", text)
        self.assertIn("받는 분이 열어 달라고", text)
        self.assertIn("……아니요.", text)
        self.assertEqual(1, len(state["encounters"]))
        self.assertTrue(self.has("warning_exposed"))
        self.assertFalse(self.has("H9"))
        self.assertFalse(self.has("know_granny_reads"))
        self.assertEqual(3, self.money())
        self.assertIn("resident_sling", self.n["r13_met_people"]())

    def test_already_met_does_not_repeat_intro_or_event(self):
        self.n["r13_note_encounter"]("resident_sling")
        self.run_letters(self.IGNORE)
        self.assertNotIn("w1c:letters:intro", [r[0] for r in self.lines])
        before = copy.deepcopy(self.s)
        count = len(self.lines)
        self.run_letters()
        self.assertEqual(before, self.s)
        self.assertEqual(count, len(self.lines))

    def test_question_and_free_stop_do_not_charge(self):
        for question in (self.CATCH, self.WHO):
            with self.subTest(question=question):
                self.setUp()
                self.run_letters(question, self.STOP)
                options, at_menu, rows = self.menus[1]
                self.assertIn(self.PAY, options)
                self.assertIn("sling_job_pressure_heard", at_menu["flags"])
                self.assertIn("sling_day_wage_known", at_menu["flags"])
                self.assertIn("세 냥이요.", str(rows))
                confession = next(row for row in self.lines if row[0] in ("w1c:letters:catch","w1c:letters:who"))
                self.assertNotIn("H9", confession[2]["evidence"])
                self.assertEqual(3, self.money())
                self.assertEqual([], self.n["r13_wallet"](self.s)["ledger"])
                self.assertFalse(self.has("H9"))
                self.assertTrue(self.has("letters_safe"))
                self.assertTrue(self.has("sling_ally"))

    def test_two_coins_hide_only_paid_choice(self):
        self.s["livelihood"]["cash"] = 2
        self.run_letters(self.CATCH, self.STOP)
        self.assertNotIn(self.PAY, self.menus[1][0])
        self.assertIn(self.STOP, self.menus[1][0])
        self.assertNotIn(self.FAKE, self.menus[1][0])
        self.assertEqual(2, self.money())

    def test_paid_choice_charges_once_and_keeps_followup(self):
        self.run_letters(self.CATCH, self.PAY, self.SEND)
        self.assertEqual(0, self.money())
        ledger = self.n["r13_wallet"](self.s)["ledger"]
        self.assertEqual([-3], [entry["amount"] for entry in ledger])
        self.assertNotIn(self.PAY, self.menus[2][0])
        self.assertNotIn(self.FAKE, self.menus[2][0])
        self.assertEqual(0, self.s["evidence"].count("H9"))
        self.assertFalse(self.n["r13_sling_nonpaid_trust"]())
        before = copy.deepcopy(self.s)
        self.store.room13 = json.loads(json.dumps(self.s))
        self.assertFalse(self.n["r13_sling_support_day"]())
        self.n["r13_sling_note_confession"]()
        self.assertEqual(before, self.s)

    def test_support_gate_preview_and_invalid_actions_do_not_mutate(self):
        before = copy.deepcopy(self.s)
        for _ in range(3):
            self.assertFalse(self.n["r13_sling_can_support_day"]())
            self.assertFalse(self.n["r13_sling_support_day"]())
        self.assertEqual(before, self.s)
        self.n["r13_flag"]("sling_confession_heard")
        before = copy.deepcopy(self.s)
        self.assertFalse(self.n["r13_sling_support_day"]())
        self.assertEqual(before, self.s)

    def test_report_warning_is_not_report_or_confession(self):
        self.run_letters(self.REPORT, self.PROCEED)
        warning_state = self.menus[1][1]
        self.assertNotIn("sling_hostile", warning_state["flags"])
        self.assertNotIn("H9", warning_state["evidence"])
        self.assertIn("우체국에서 일 못 해요", str(self.menus[1][2]))
        self.assertTrue(self.has("sling_hostile"))
        for key in ("H9","know_granny_reads","sling_confession_heard","letters_safe","warning_exposed"):
            self.assertFalse(self.has(key), key)

    def test_report_then_listen_does_not_create_hostility(self):
        self.run_letters(self.REPORT, self.LISTEN, self.STOP)
        self.assertFalse(self.has("sling_hostile"))
        self.assertTrue(self.has("sling_job_pressure_heard"))
        self.assertFalse(self.has("sling_confession_heard"))
        self.assertTrue(self.has("letters_safe"))
        self.assertEqual(3, self.money())

    def test_portrait_needs_owned_and_already_shown_then_never_charges(self):
        for owned, shown in ((False,False),(True,False),(False,True),(True,True)):
            with self.subTest(owned=owned, shown=shown):
                self.setUp()
                if owned: self.s["evidence"].append("P01")
                if shown: self.n["r13_flag"]("portrait_known")
                self.run_letters(*((self.PORTRAIT,self.SEND) if owned and shown else (self.IGNORE,)))
                self.assertEqual(owned and shown, self.PORTRAIT in self.menus[0][0])
                if owned and shown:
                    self.assertNotIn(self.PAY, self.menus[1][0])
                    self.assertFalse(self.has("H9"))
                    self.assertTrue(self.has("letters_safe"))
                    self.assertFalse(self.has("sling_day_wage_known"))
                    self.assertEqual(3, self.money())

    def test_free_reconciliation_needs_no_h9_and_does_not_identify_requester(self):
        self.run_letters(self.REPORT, self.PROCEED)
        self.assertTrue(self.available("grudge_reason:sling"))
        self.assertTrue(self.available("grudge_fix:sling"))
        self.runner.run("r13_sling_grudge_reason")
        self.assertFalse(self.has("H9"))
        self.assertFalse(self.has("know_granny_reads"))
        self.assertNotIn("할머니", str(self.lines))
        self.assertFalse(self.available("grudge_reason:sling"))
        for key in ("sling_reconciled","letters_safe","sling_ally","fake_letter_planted"):
            self.assertFalse(self.has(key), key)
        self.n["r13_topic"] = "grudge_fix:sling"
        self.runner.run("r13_grudge_fix")
        self.assertTrue(self.has("sling_reconciled"))
        self.assertTrue(self.has("neoul_annoyed"))
        self.assertFalse(self.has("letters_safe"))
        self.assertFalse(self.has("H9"))
        self.assertTrue(self.n["r13_sling_nonpaid_trust"]())
        self.assertEqual(3, self.money())
        before = copy.deepcopy(self.s)
        self.runner.run("r13_grudge_fix")
        self.runner.run("r13_sling_grudge_reason")
        self.assertEqual(before, self.s)

    def test_old_h9_preserved_and_reconciliation_not_confession_gated(self):
        self.n["r13_flag"]("sling_hostile","rumor:fair","know_granny_reads")
        self.s["evidence"].append("H9")
        self.assertTrue(self.available("grudge_reason:sling"))
        self.assertTrue(self.available("grudge_fix:sling"))
        self.runner.run("r13_sling_grudge_reason")
        self.assertEqual(1, self.s["evidence"].count("H9"))
        self.assertIn("할머니가 베껴 오라고", str(self.lines))
        self.assertNotIn("누구 부탁인지는 말 못", str(self.lines))

    def test_fake_success_failure_and_existing_payoff_date(self):
        for found_out in (False,True):
            with self.subTest(found_out=found_out):
                self.setUp()
                self.s["evidence"].append("H9") # Preserve already-earned/legacy fake route.
                if found_out: self.n["r13_flag"]("granny_knows_found_out")
                self.run_letters(self.WHO, self.FAKE)
                self.assertEqual(not found_out, self.has("fake_letter_planted"))
                self.assertEqual(not found_out, self.has("letters_safe"))
                self.assertFalse(self.has("E17"))
                self.assertEqual(3, self.money())
                self.s.update(day=6, period=2)
                self.runner.run("r13_w1c_events")
                self.assertFalse(self.has("E17"))
                self.s.update(day=7, period=2)
                self.choices = [] if found_out else ["할머니를 따라간다"]
                self.runner.run("r13_w1c_events")
                self.assertEqual(not found_out, self.has("E17"))
                self.assertEqual(not found_out, self.has("granny_lure_seen"))
                self.assertEqual(not found_out, self.has("prevention_witness"))
                self.assertEqual("pending" if found_out else "prevented", self.s["case_state"])

    def test_paid_fake_failure_does_not_undo_original_letter_protection(self):
        self.s["evidence"].append("H9")
        self.n["r13_flag"]("granny_knows_found_out")
        self.run_letters(self.CATCH, self.PAY, self.FAKE)
        self.assertTrue(self.has("letters_safe"))
        self.assertTrue(self.has("sling_ally"))
        self.assertFalse(self.has("fake_letter_planted"))
        self.assertEqual(0, self.money())

    def test_fake_night_staying_with_child_keeps_prevention_not_witness(self):
        self.s["evidence"].append("H9")
        self.run_letters(self.CATCH, self.FAKE)
        self.s.update(day=7, period=2)
        self.choices = ["다람이와 방에 남는다"]
        self.runner.run("r13_w1c_events")
        self.assertEqual("prevented", self.s["case_state"])
        self.assertTrue(self.has("E17"))
        self.assertTrue(self.has("victim_protected"))
        self.assertFalse(self.has("granny_lure_seen"))
        self.assertFalse(self.has("prevention_witness"))

    def test_week_two_protection_payoff_preserves_existing_gate(self):
        for protected in (False,True):
            with self.subTest(protected=protected):
                self.setUp()
                self.s.update(day=11, period=0)
                self.n["r13_flag"]("pursuit_active")
                if protected: self.n["r13_flag"]("letters_safe")
                self.runner.run("r13_w1c_events")
                self.assertEqual(protected, self.has("pursuit_managed"))
                count = len(self.lines)
                self.runner.run("r13_w1c_events")
                self.assertEqual(count, len(self.lines))


if __name__ == "__main__":
    unittest.main()
