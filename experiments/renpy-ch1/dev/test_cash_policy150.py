"""현재 본편의 돈 변경 금지와 구 사건 정답 처리 보존을 검증한다."""
import ast
import copy
from pathlib import Path
from types import SimpleNamespace
import textwrap
import unittest

from dev.test_exploration149 import environment as model_environment, own


ROOT = Path(__file__).resolve().parents[1]


def environment():
    env, state = model_environment()
    state.active = True
    state.proved = []
    state.notices = []
    state.proof_result = object()
    def prove(claim):
        state.proved.append(claim)
        return state.proof_result
    def flag(*keys):
        room = copy.deepcopy(state.room13)
        room['flags'].extend(key for key in keys if key not in room['flags'])
        state.room13 = room
    env.update(r13_v111_active=lambda: state.active, r13_prove=prove,
               r13_has=lambda key: key in state.room13['flags'], r13_flag=flag,
               renpy=SimpleNamespace(notify=lambda text: state.notices.append(text)))
    town = ROOT / 'game/systems/room13_town_events.rpy'
    tree = ast.parse(textwrap.dedent(town.read_text().split('init 102 python:\n', 1)[1].split('\nlabel ', 1)[0]))
    cash = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'r13_cash')
    exec(compile(ast.Module(body=[cash], type_ignores=[]), str(town), 'exec'), env)
    legacy = ROOT / 'game/systems/room13_no_livelihood.rpy'
    tree = ast.parse(textwrap.dedent(legacy.read_text().split('init 168 python:\n', 1)[1]))
    selected = [node for node in tree.body if (
        isinstance(node, ast.FunctionDef) and node.name == 'r13_prove') or (
        isinstance(node, ast.Assign) and any(isinstance(target, ast.Name)
            and target.id in ('R13_EP_REWARD', '_r13_nolive_prove') for target in node.targets))]
    exec(compile(ast.Module(body=selected, type_ignores=[]), str(legacy), 'exec'), env)
    policy = ROOT / 'game/systems/room13_cash_policy150.rpy'
    exec(textwrap.dedent(policy.read_text().split('init 392 python:\n', 1)[1]), env)
    return env, state


class CashPolicy150(unittest.TestCase):
    def test_current_campaign_cash_calls_never_change_saves_for_any_direction_or_reason(self):
        for cash in (None, 0, 71):
            for delta, reason in ((20, '집에서 가져온 노잣돈'), (8, '사례 · 톡'),
                                  (18, '은호에게 약초를 넘김'), (-3, '생활 물품'),
                                  (5, '보증금 돌려받음'), (0, '물건 정산')):
                env, state = environment()
                if cash is not None: own(state, cash=cash)
                before = copy.deepcopy(state.room13)
                self.assertFalse(env['r13_cash'](delta, reason))
                self.assertEqual(state.room13, before, (delta, reason))

    def test_old_reward_claims_keep_original_result_and_never_pay_or_mark_rewards(self):
        env, state = environment()
        self.assertEqual(env['R13_EP_REWARD'], {})
        before = copy.deepcopy(state.room13)
        claims = ('Q1', 'Q3', 'C1', 'C2', 'C3', 'C4', 'Q5')
        for claim in claims:
            self.assertIs(env['r13_prove'](claim), state.proof_result)
        self.assertEqual(state.proved, list(claims))
        self.assertEqual(state.room13, before)
        self.assertEqual(state.notices, [])

    def test_unselected_legacy_campaign_retains_cash_helper_behavior(self):
        env, state = environment();state.active = False;own(state, cash=10)
        env['r13_cash'](18, '은호에게 약초를 넘김')
        env['r13_cash'](-5, '물건 정산')
        self.assertEqual(state.room13['livelihood']['cash'], 23)
        self.assertEqual([row['amount'] for row in state.room13['livelihood']['ledger']], [18, -5])

    def test_legacy_shop_cannot_spend_current_campaign_saved_cash(self):
        env, state = environment();own(state, cash=50)
        state.room13['flags'].append('livelihood_open')
        before = copy.deepcopy(state.room13)
        result, success = env['r13_purchase'](state.room13, 'cord')
        self.assertFalse(success)
        self.assertIs(result, state.room13)
        self.assertEqual(state.room13, before)
        state.active = False
        result, success = env['r13_purchase'](state.room13, 'cord')
        self.assertTrue(success)
        self.assertEqual(result['livelihood']['cash'], 47)


if __name__ == '__main__':
    unittest.main()
