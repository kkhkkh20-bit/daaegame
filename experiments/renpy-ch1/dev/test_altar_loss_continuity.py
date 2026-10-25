"""제단 패배 지문은 가설 회의에서 실제로 불을 껐는지 반영한다."""
import unittest
from test_newworld_text import Layer

class AltarLossContinuity(Layer):
 def test_hypothesis_loss_keeps_current_stone_fires(self):
  env=self.load()
  env['r13_v111_set']('meeting:hypothesis','lose')
  texts=[row[1] for row in env['r13_nw_block']('altar_lost14')]
  self.assertTrue(any('오늘도 푸른 불이 오른다' in text for text in texts))
  self.assertFalse(any('다음 겨울에는 다시 돌' in text for text in texts))
 def test_win_and_partial_keep_original_future_warning(self):
  for outcome in ('win','partial'):
   with self.subTest(outcome=outcome):
    env=self.load()
    env['r13_v111_set']('meeting:hypothesis',outcome)
    texts=[row[1] for row in env['r13_nw_block']('altar_lost14')]
    self.assertTrue(any('다음 겨울에는 다시 돌' in text for text in texts))
    self.assertFalse(any('오늘도 푸른 불이 오른다' in text for text in texts))

if __name__=='__main__':unittest.main()
