#!/usr/bin/env python3
"""Portable source-only regression for the morning staff override. Not a native render test."""
import copy
import json
from pathlib import Path
from types import SimpleNamespace
import textwrap

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / 'game'
acting = json.loads((GAME / 'assets/room13-pixel-acting.json').read_text())
layouts = json.loads((GAME / 'assets/room13-world-layout.json').read_text())
state = SimpleNamespace(room13={'location': 'post', 'period': 0, 'day': 2})
actors = [dict(person='seryeon', pose='action_1', x=4, y=469, width=171, height=205,
               rect=[4, 469, 171, 205], depth=674, slot=[90, 675, 220, 'waiting'],
               contact='clipboard', occlusion=[], activity='original'),
          dict(person='resident_sling', pose='map27_po_1', x=1298, y=383, width=187,
               height=280, rect=[1298, 383, 187, 280], depth=663, slot=None,
               contact='behind_counter', occlusion=[], activity='parcel')]
offers = set()
width = [2160]
ns = dict(store=state, r13_stage_people=lambda entry=False: copy.deepcopy(actors),
          r13_offer_for_person=lambda p: p in offers,
          r13_world_width=lambda: width[0], r13_layout=lambda where: layouts[where],
          r13_acting_spec=lambda p, pose: acting[p][pose],
          r13_actor_geometry=lambda p, pose: acting[p][pose]['crop'][2:])
# Use the actual production geometry function, not a duplicate in the test.
import ast
spatial = (GAME / 'systems/room13_spatial_contacts.rpy').read_text().split('init 179 python:\n', 1)[1]
module = ast.parse(textwrap.dedent(spatial))
node = next(n for n in module.body if isinstance(n, ast.FunctionDef) and n.name == 'r13_contact_geometry')
exec(compile(ast.Module(body=[node], type_ignores=[]), 'production-contact-geometry', 'exec'), ns)
source = (GAME / 'systems/room13_post_staff_contact.rpy').read_text().split('init 182 python:\n', 1)[1]
exec(compile(textwrap.dedent(source), 'post-staff-contact', 'exec'), ns)
before = copy.deepcopy(actors)
for day in range(2, 15):
    state.room13['day'] = day
    out = ns['r13_stage_people']()
    s = next(a for a in out if a['person'] == 'seryeon')
    assert s['rect'] == [1403, 340, 195, 234] and s['depth'] == 560
    assert s['pose'] == 'action_1' and s['slot'] is None
    assert s['map27_occlusion'] == [list(ns['R13_POST_STAFF_CONTACT']['foreground'])]
    assert not s['map27_keepouts'] and not s['occlusion']
    spec = acting['seryeon']['action_1']; scale = s['height'] / spec['crop'][3]
    hand = [s['x'] + spec['hand'][0] * scale, s['y'] + spec['hand'][1] * scale]
    assert max(abs(a - b) for a, b in zip(hand, (1566, 432))) < .51
    assert abs(s['width'] - spec['crop'][2] * scale) <= .5
    assert next(a for a in out if a['person'] == 'resident_sling') == before[1]
assert actors == before, 'Cached input actor dictionaries mutated'
for person in ('seryeon', 'resident_sling'):
    offers.add(person); assert ns['r13_post_staff_contact'](actors) == actors; offers.clear()
for location, period, w in [('inn', 0, 2160), ('post', 1, 1280), ('post', 2, 1280), ('post', 0, 1280), ('post', 0, 1920)]:
    state.room13.update(location=location, period=period); width[0] = w
    assert ns['r13_post_staff_contact'](actors) == actors
state.room13.update(location='post', period=0); width[0] = 2160
layout = layouts['post']; file = layout['files']['morning']
layout['files']['morning'] = 'another-background.webp'; assert ns['r13_post_staff_contact'](actors) == actors; layout['files']['morning'] = file
crop = layout['crops']['morning']; layout['crops']['morning'] = [0, 0, 1920, 720]
assert ns['r13_post_staff_contact'](actors) == actors; layout['crops']['morning'] = crop
spec = acting['seryeon']['action_1']; hand = spec['hand']; spec['hand'] = [320, 180]
assert ns['r13_post_staff_contact'](actors) == sorted(actors, key=lambda a: a['depth']); spec['hand'] = hand
for pose in ('neutral', 'chair_read'):
    actors[0]['pose'] = pose; assert ns['r13_post_staff_contact'](actors) == sorted(actors, key=lambda a: a['depth'])
actors[:] = before[1:]; assert ns['r13_post_staff_contact'](actors) == actors
actors.clear(); assert ns['r13_post_staff_contact'](actors) == []
print('PASS: hand geometry, uniform scale, all other actors, source input immutability, offer/scene/pose/absence guards. Native renderer/picker NOT RUN.')
