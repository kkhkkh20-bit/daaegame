"""Source-context metadata provenance; not a native or visual approval."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / 'docs/reviews/dialogue-beats'


class RecommendedDialogueReview(unittest.TestCase):
    def test_existing_runtime_ordinal_refs_keep_exact_context(self):
        rows = list(json.loads((REVIEWS / 'dynamic-context-review.json').read_text())['rows'].values())
        bindings = json.loads((ROOT / 'game/assets/room13-dialogue-bindings.json').read_text())
        supplemental = json.loads((REVIEWS / 'supplemental-context-review.json').read_text())['rows']
        refusal = [r for r in supplemental if r.get('person') == 'buri'
                   and r.get('source') == 'game/room13_dialogue_openings_20261013.rpy'
                   and r.get('line') == 127]
        self.assertEqual(len(refusal), 1)
        checked = 0
        for cue in bindings['cues'].values():
            reference = cue.get('review_ref', '')
            if not reference.startswith('dynamic-context-review:'):
                continue
            ordinal, separator, suffix = reference.split(':', 1)[1].partition('+')
            row = rows[int(ordinal)]
            for field in ('person', 'source'):
                self.assertEqual(cue[field], row[field], (reference, field))
            # The pre-existing composed refusal names the same base ordinal
            # plus its separately reviewed literal suffix, not a new base row.
            if separator:
                self.assertEqual(suffix, 'refused', reference)
                self.assertEqual(cue['text'], row['text'] + refusal[0]['text'], reference)
            else:
                self.assertEqual(cue['text'], row['text'], reference)
            self.assertEqual(cue['source_line'], row['line'], reference)
            self.assertNotEqual(row.get('batch'), 'recommended-context-20261019', reference)
            checked += 1
        self.assertGreater(checked, 0)

    def test_recommended_decisions_are_exact_source_only_records(self):
        review = json.loads((REVIEWS / 'dynamic-context-review.json').read_text())
        rows = [r for r in review['rows'].values() if r.get('batch') == 'recommended-context-20261019']
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row['review_scope'], 'manual_source_context_only_not_native_visual_or_runtime_binding_approval')
            self.assertEqual(row['application_status'], 'awaiting_approved_runtime_assets')
            self.assertFalse(row['reaction'])
            self.assertTrue(row['reason'])
            self.assertEqual(row['text_sha256'], hashlib.sha256(row['text'].encode()).hexdigest())

    def test_receipt_matches_reviewed_source_and_does_not_promote_art(self):
        receipt = json.loads((REVIEWS / 'recommended-context-review-20261019.json').read_text())
        for source, expected in receipt['source_sha256'].items():
            self.assertEqual(hashlib.sha256((ROOT / source).read_bytes()).hexdigest(), expected, source)
        self.assertFalse(receipt['native_validation'])
        self.assertFalse(receipt['runtime_bindings_changed'])
        self.assertFalse(receipt['art_approvals_changed'])

    def test_source_review_scope_cannot_authorize_runtime_binding(self):
        from build_dialogue_bindings import review_allows_runtime_binding
        held = dict(reviewed=True, emotion='surprise', reaction=True,
                    application_status='approved_art_when_available',
                    review_scope='manual_source_context_only_not_native_visual_or_runtime_binding_approval')
        self.assertFalse(review_allows_runtime_binding(held))
        # Preserve the existing reviewed runtime path. Asset availability is
        # still decided by the runtime art gate, not bypassed by this helper.
        self.assertTrue(review_allows_runtime_binding(dict(reviewed=True)))
        self.assertTrue(review_allows_runtime_binding(dict(reviewed=True,
                        application_status='awaiting_approved_runtime_assets')))

    def test_compiler_does_not_cross_bind_recommended_reviews_into_legacy_topics(self):
        from build_dialogue_bindings import compile_registry
        compiled = compile_registry()
        reviews = json.loads((REVIEWS / 'dynamic-context-review.json').read_text())['rows']
        held = {(r['source'], r['person'], r['text']) for r in reviews.values()
                if r.get('review_scope') == 'manual_source_context_only_not_native_visual_or_runtime_binding_approval'}
        self.assertTrue(held)
        self.assertTrue(compiled['cues'])
        for cue in compiled['cues'].values():
            self.assertNotIn((cue['source'], cue['person'], cue['text']), held)


if __name__ == '__main__':
    unittest.main()
