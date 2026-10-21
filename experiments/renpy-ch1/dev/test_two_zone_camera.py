"""Behavioural tests for the two-stop camera, using an in-memory UI boundary."""
import copy
from types import SimpleNamespace
import unittest
import test_world_camera


class TwoZoneCamera(unittest.TestCase):
    def setUp(self):
        test_world_camera.WorldCamera.setUp(self)
        self.hub = SimpleNamespace(scope={"world_moving": False})
        self.restarts = []
        self.ns['R13_STAGE_CACHE']={'old-save': ['old geometry']}
        self.ns['persistent'] = SimpleNamespace(room13_motion=True)
        self.ns['renpy'] = SimpleNamespace(
            get_screen=lambda _: self.hub,
            set_screen_variable=lambda k, v, **kw: self.hub.scope.update({k: v}),
            restart_interaction=lambda: self.restarts.append(True),
            retain_after_load=lambda: None, is_skipping=lambda: False,
            display=SimpleNamespace(interface=SimpleNamespace(maximum_framerate=lambda _: None)))
        class Adjustment:
            def __init__(self, range, value, changed, **kw):
                self.range, self.value, self.changed = range, value, changed
                self.animation_target = None
                self.calls = []
            def change(self, value):
                self.value = value
                self.changed(value)
            def animate(self, delta, duration, ease):
                self.calls.append((delta, duration, ease))
                self.animation_target = self.value + delta
            def finish(self):
                self.change(self.animation_target)
                self.animation_target = None
        self.ns['ui'] = SimpleNamespace(adjustment=Adjustment)
        self.adj = self.ns['r13_world_adjustment']('school')
        self.hub.scope['world_adjustment']=self.adj
        self.store.room13.update(location='school', flags=['keep'], evidence=['E1'], checks={})
        self.before = copy.deepcopy(self.store.room13)

    def test_one_press_goes_to_far_endpoint_and_ignores_spam_reverse(self):
        self.ns['r13_pan_camera'](self.adj, 1)
        self.assertEqual(self.adj.animation_target, 520)
        self.assertTrue(self.hub.scope['world_moving'])
        for direction in [1, -1]*20:
            self.ns['r13_pan_camera'](self.adj, direction)
        self.assertEqual(len(self.adj.calls), 1)
        self.adj.change(175)
        self.assertEqual(self.store.r13_world_cameras['school'], 520)
        self.ns['r13_world_pan_finish'](self.adj)
        self.assertTrue(self.hub.scope['world_moving'])
        self.adj.finish()
        self.ns['r13_world_pan_finish'](self.adj)
        self.assertEqual(self.adj.value, 520)
        self.assertFalse(self.hub.scope['world_moving'])
        self.ns['r13_pan_camera'](self.adj, -1)
        self.adj.finish()
        self.ns['r13_world_pan_finish'](self.adj)
        self.assertEqual(self.adj.value, 0)
        self.assertEqual(self.store.room13, self.before)

    def test_motion_off_and_skip_settle_without_animation(self):
        for skip in [False, True]:
            self.ns['persistent'].room13_motion=skip
            self.ns['renpy'].is_skipping=lambda:skip
            self.ns['r13_pan_camera'](self.adj, 1)
            self.assertEqual(self.adj.value, 520)
            self.assertEqual(self.adj.calls, [])
            self.assertFalse(self.hub.scope['world_moving'])
            self.ns['r13_pan_camera'](self.adj, -1)
            self.assertEqual(self.adj.value, 0)
        self.assertEqual(self.store.room13, self.before)

    def test_load_during_motion_restores_destination_and_unlocks(self):
        self.ns['r13_pan_camera'](self.adj, 1)
        self.adj.change(100)
        self.ns['r13_world_restore_zone']()
        restored=self.hub.scope['world_adjustment']
        self.assertIs(restored,self.adj)
        self.assertEqual(restored.value, 520)
        self.assertIsNone(restored.animation_target)
        self.assertFalse(self.hub.scope['world_moving'])
        self.assertFalse(self.ns['R13_STAGE_CACHE'])
        self.assertEqual(self.store.room13, self.before)

    def test_legacy_middle_offset_snaps_only_camera(self):
        for old, expected in [(100,0),(260,0),(300,520),(9999,520),(-8,0)]:
            self.store.r13_world_cameras['school']=old
            self.assertEqual(self.ns['r13_world_adjustment']('school').value,expected)
        self.assertEqual(self.store.room13,self.before)

    def test_legacy_saved_callback_without_destination_attribute(self):
        del self.adj.changed.destination
        self.adj.change(100)
        self.assertEqual(self.store.r13_world_cameras['school'],100)
        self.assertEqual(self.store.room13,self.before)

    def test_ease_is_monotonic_with_stationary_endpoints(self):
        values=[self.ns['r13_pan_ease'](i/100) for i in range(101)]
        self.assertEqual(values,sorted(values))
        self.assertEqual((values[0],values[-1]),(0,1))
