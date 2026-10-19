# LOCAL default-off prototype. New file only; no renderer/story/schedule replacement.
init 183 python:
    """Pure placement-contract resolver. No renderer, story writes, spawning, or asset generation."""
    import copy as r13_pc_copy
    import math as r13_pc_math


    class R13PlacementContractError(ValueError):
        pass


    def r13_pc_fail(code, detail):
        raise R13PlacementContractError(code + ': ' + detail)


    def r13_pc_point(value, name):
        if not isinstance(value, (list, tuple)) or len(value) != 2 or not all(isinstance(v, (int, float)) and r13_pc_math.isfinite(v) for v in value):
            r13_pc_fail('INVALID_ANCHOR', name)
        return tuple(value)


    def r13_pc_polygons(value, name):
        if not isinstance(value, (list, tuple)):
            r13_pc_fail('INVALID_MASK_POLYGON', name)
        for polygon in value:
            if not isinstance(polygon, (list, tuple)) or len(polygon) < 3:
                r13_pc_fail('INVALID_MASK_POLYGON', name)
            for point in polygon: r13_pc_point(point, name)
        return value


    def r13_pc_number(value, name):
        if not isinstance(value, (int, float)) or not r13_pc_math.isfinite(value):
            r13_pc_fail('INVALID_NUMERIC_GEOMETRY', name)
        return value


    def r13_pc_registry_shape(registry):
        if not isinstance(registry, dict): r13_pc_fail('INVALID_REGISTRY_SHAPE', 'root')
        for name in ('background_variants', 'geometries', 'assets', 'upstream_guards'):
            if not isinstance(registry.get(name), dict) or not all(isinstance(v, dict) for v in registry[name].values()):
                r13_pc_fail('INVALID_REGISTRY_SHAPE', name)
        required_guard = {'pose', 'x', 'y', 'width', 'height', 'rect', 'depth', 'ground_depth', 'elevation', 'contact', 'slot', 'occlusion', 'map27_occlusion', 'map27_keepouts'}
        if any(not required_guard <= set(g) for g in registry['upstream_guards'].values()):
            r13_pc_fail('INCOMPLETE_UPSTREAM_GUARD', 'all placement and mask fields are required')
        if not isinstance(registry.get('bindings'), list) or not all(isinstance(v, dict) for v in registry['bindings']):
            r13_pc_fail('INVALID_REGISTRY_SHAPE', 'bindings')


    def r13_pc_normalized(value):
        if isinstance(value, dict): return {k: r13_pc_normalized(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)): return [r13_pc_normalized(v) for v in value]
        return value


    def r13_pc_overlap(a, b):
        return max(0, min(a[0]+a[2], b[0]+b[2])-max(a[0], b[0])) * max(0, min(a[1]+a[3], b[1]+b[3])-max(a[1], b[1]))


    def r13_pc_viewport_rect(actor, camera, viewport=(1280, 720)):
        """Diagnostic clipping only. Actual picking remains r13_actor_hit_mask, never this box."""
        x, y, w, h = actor['rect']; x -= camera
        left, top = max(0, x), max(0, y)
        right, bottom = min(viewport[0], x+w), min(viewport[1], y+h)
        return None if right <= left or bottom <= top else [left, top, right-left, bottom-top]


    def r13_pc_exact_spec(asset, spec, available, blob_for):
        if asset.get('status') != 'approved':
            r13_pc_fail('UNAPPROVED_ASSET', asset['id'])
        if asset.get('registration') == 'isolated_alias' and asset.get('source_quality', {}).get('status') != 'reference_reviewed':
            r13_pc_fail('UNREVIEWED_NEW_VARIANT', asset['id'])
        if not spec:
            r13_pc_fail('MISSING_EXACT_POSE', asset['person'] + '/' + asset['pose'])
        expected = asset['spec']
        # Exact contract, including authored padding and foreground silhouettes. No neutral fallback.
        if r13_pc_normalized(spec) != r13_pc_normalized(expected):
            r13_pc_fail('STALE_POSE_CONTRACT', asset['id'])
        if not available(expected['file']):
            r13_pc_fail('MISSING_ASSET', expected['file'])
        if blob_for(expected['file']) != asset['git_blob']:
            r13_pc_fail('ASSET_DIGEST_MISMATCH', expected['file'])
        crop = expected['crop']; bounds = asset['alpha_bounds']
        size = asset['source_size']
        if len(size) != 2 or len(crop) != 4 or len(bounds) != 4 or not all(isinstance(v, (int, float)) and r13_pc_math.isfinite(v) for v in list(size)+list(crop)+list(bounds)):
            r13_pc_fail('INVALID_INTRINSIC_BOUNDS', asset['id'])
        if min(size) <= 0 or min(crop[:2]) < 0 or crop[0]+crop[2] > size[0] or crop[1]+crop[3] > size[1] or min(crop[2:]) <= 0 or min(bounds[2:]) <= 0:
            r13_pc_fail('INVALID_INTRINSIC_BOUNDS', asset['id'])
        if bounds[0] < 0 or bounds[1] < 0 or bounds[0]+bounds[2] > crop[2] or bounds[1]+bounds[3] > crop[3]:
            r13_pc_fail('INVALID_INTRINSIC_BOUNDS', asset['id'])
        head = expected.get('head')
        if not isinstance(head, (list, tuple)) or len(head) != 4 or not all(isinstance(v, (int, float)) and r13_pc_math.isfinite(v) for v in head) or min(head[2:]) <= 0:
            r13_pc_fail('INVALID_HEAD_BOUNDS', asset['id'])
        r13_pc_polygons(expected.get('foreground_parts', []), asset['id']+'/foreground_parts')
        return expected


    def r13_pc_anchors(asset):
        spec = asset['spec']
        anchors = dict(spec.get('anchors', {}))
        for name in ('foot', 'hand', 'seat'):
            if name in spec: anchors[name] = spec[name]
        for semantic, source_name in asset['anchor_map'].items():
            if source_name not in anchors:
                r13_pc_fail('MISSING_CONTACT_ANCHOR', asset['id'] + '/' + source_name)
            anchors[semantic] = r13_pc_point(anchors[source_name], source_name)
            if not (0 <= anchors[semantic][0] <= spec['crop'][2] and 0 <= anchors[semantic][1] <= spec['crop'][3]):
                r13_pc_fail('ANCHOR_OUTSIDE_CROP', asset['id']+'/'+semantic)
        return anchors


    def r13_pc_place(actor, asset, slot, world_size):
        spec = asset['spec']; anchors = r13_pc_anchors(asset)
        if min(r13_pc_point(world_size, 'world_size')) <= 0: r13_pc_fail('INVALID_WORLD_SIZE', asset['id'])
        if slot.get('mask_layer') not in ('base', 'map27'): r13_pc_fail('INVALID_MASK_LAYER', asset['id'])
        if spec.get('contact', 'standing') not in slot['contacts']:
            r13_pc_fail('INCOMPATIBLE_CONTACT', asset['id'])
        facing = asset.get('facing', 'authored_unverified')
        if facing not in slot['facing']:
            r13_pc_fail('INCOMPATIBLE_FACING', asset['id'])
        # Swapping never mirrors a source or invents a missing hand/seat point.
        anchor_name = slot['anchor']
        if anchor_name not in anchors:
            r13_pc_fail('MISSING_CONTACT_ANCHOR', asset['id'] + '/' + anchor_name)
        metric = slot['scale']; kind = metric['kind']
        if kind == 'visible_height':
            denominator = asset['alpha_bounds'][3]
        elif kind == 'head_height':
            denominator = spec.get('head', [0, 0, 0, 0])[3]
        elif kind == 'vertical_anchor_span':
            a = anchors.get(metric['from']); b = anchors.get(metric['to'])
            if a is None or b is None:
                r13_pc_fail('MISSING_SCALE_ANCHOR', asset['id'])
            denominator = b[1]-a[1]
        else:
            r13_pc_fail('UNSUPPORTED_SCALE_METRIC', str(kind))
        if denominator <= 0 or not r13_pc_math.isfinite(denominator) or metric['pixels'] <= 0:
            r13_pc_fail('INVALID_SCALE', asset['id'])
        scale = metric['pixels']/float(denominator)
        # Uniform scale only. Slot values already encode perspective/pose stance once.
        cw, ch = spec['crop'][2:]; width0, height0 = cw*scale, ch*scale
        limits = slot['size_limits']
        if not limits[0] <= height0 <= limits[1]:
            r13_pc_fail('SIZE_OUT_OF_RANGE', asset['id'])
        rounding = slot.get('rounding', 'round')
        quantize = (lambda v: int(round(v))) if rounding == 'round' else (lambda v: int(v)) if rounding == 'truncate' else None
        if quantize is None: r13_pc_fail('INVALID_ROUNDING', str(rounding))
        target = r13_pc_point(slot['target'], 'target'); anchor = anchors[anchor_name]
        x = quantize(target[0]-anchor[0]*scale); y = quantize(target[1]-anchor[1]*scale)
        width, height = quantize(width0), quantize(height0)
        if min(width, height) <= 0: r13_pc_fail('INVALID_SCALE', asset['id'])
        for check in slot.get('secondary_contacts', []):
            point = anchors.get(check['anchor'])
            if point is None: r13_pc_fail('MISSING_CONTACT_ANCHOR', check['anchor'])
            actual = (x+point[0]*scale, y+point[1]*scale)
            for axis in check.get('axes', [0, 1]):
                if abs(actual[axis]-check['target'][axis]) > check.get('tolerance', 1):
                    r13_pc_fail('SECONDARY_CONTACT_MISMATCH', check['anchor'])
        left, top = max(0, x), max(0, y)
        right, bottom = min(world_size[0], x+width), min(world_size[1], y+height)
        if right <= left or bottom <= top:
            r13_pc_fail('OUTSIDE_WORLD', asset['id'])
        # World masks stay fixed; source hand/prop keepouts get the very same affine transform.
        masks = r13_pc_copy.deepcopy(r13_pc_polygons(slot.get('occlusion', []), 'occlusion'))
        r13_pc_polygons(spec.get('foreground_parts', []), 'foreground_parts')
        keepouts = [[(x+px*scale, y+py*scale) for px, py in polygon] for polygon in spec.get('foreground_parts', [])]
        depth = slot['depth']
        z = depth['value'] if depth['mode'] == 'fixed' else y+height if depth['mode'] == 'sprite_bottom' else None
        if z is None: r13_pc_fail('INVALID_DEPTH', asset['id'])
        r13_pc_number(z, 'depth')
        for field in ('ground_depth', 'elevation'):
            if field in depth: r13_pc_number(depth[field], field)
        result = dict(actor)
        result.update(pose=asset['pose'], x=x, y=y, width=width, height=height,
            rect=[left, top, right-left, bottom-top], depth=z, contact=spec.get('contact', 'standing'), slot=None,
            occlusion=masks[0] if slot.get('mask_layer') == 'base' and masks else [],
            map27_occlusion=[] if slot.get('mask_layer') == 'base' else masks, map27_keepouts=keepouts)
        if slot.get('mask_layer') == 'base' and len(masks) > 1:
            r13_pc_fail('INVALID_BASE_MASK_COUNT', asset['id'])
        if 'ground_depth' in depth: result['ground_depth'] = depth['ground_depth']
        if 'elevation' in depth: result['elevation'] = depth['elevation']
        # A pose swap reuses its already-authored action label, never inventing a new job.
        if actor['pose'] != asset['pose']:
            label = spec.get('activity_label') or spec.get('action_ko') or spec.get('action')
            if asset.get('caption_policy') != 'authored_pose_on_change' or not label:
                r13_pc_fail('MISSING_APPROVED_POSE_LABEL', asset['id'])
            result['activity'] = label
        return result


    def r13_pc_face(actor, spec):
        cw, ch = spec['crop'][2:]
        x, y, w, h = spec.get('head', [cw*.25, 0, cw*.5, ch*.35])
        scale = actor['height']/float(ch)
        return [actor['x']+x*scale, actor['y']+y*scale, w*scale, h*scale]


    def r13_pc_regression_collision(old, proposed, changed, specs, protected_rects, limit=.08):
        """Conservative head/critical-object regression check, NOT full opaque-pixel collision proof."""
        before = {a['person']: a for a in old}
        for actor in proposed:
            if actor['person'] not in changed: continue
            spec = specs(actor['person'], actor['pose'])
            old_actor = before[actor['person']]
            old_spec = specs(old_actor['person'], old_actor['pose'])
            if not spec or not old_spec: r13_pc_fail('MISSING_COLLISION_SPEC', actor['person'])
            face = r13_pc_face(actor, spec); old_face = r13_pc_face(old_actor, old_spec)
            for other in proposed:
                if other['person'] == actor['person']: continue
                other_spec = specs(other['person'], other['pose'])
                old_other = before[other['person']]; old_other_spec = specs(old_other['person'], old_other['pose'])
                if not other_spec or not old_other_spec: r13_pc_fail('MISSING_COLLISION_SPEC', other['person'])
                other_face = r13_pc_face(other, other_spec); old_other_face = r13_pc_face(old_other, old_other_spec)
                overlap = r13_pc_overlap(face, other_face)/max(1, min(face[2]*face[3], other_face[2]*other_face[3]))
                prior = r13_pc_overlap(old_face, old_other_face)/max(1, min(old_face[2]*old_face[3], old_other_face[2]*old_other_face[3]))
                if overlap > max(limit, prior+.005): r13_pc_fail('FACE_COLLISION', actor['person']+'/'+other['person'])
            for rect in protected_rects:
                # Objects do not get hidden behind a newly moved face. Existing intersections are not approved here.
                if r13_pc_overlap(face, rect) > r13_pc_overlap(old_face, rect)+1:
                    r13_pc_fail('CRITICAL_OBJECT_COLLISION', actor['person'])


    def r13_pc_resolve(actors, state, registry, context, exact_spec, available, blob_for, enabled=False):
        report = dict(applied=[], warnings=[], errors=[], bypass=None)
        if not enabled:
            report['bypass'] = 'disabled'
            return actors, report
        # Existing source roster, event/scene composition, and groups always win.
        if context.get('entry') or context.get('locked_scene') or context.get('offers'):
            report['bypass'] = 'narrative_priority'
            return actors, report
        try:
            r13_pc_registry_shape(registry)
            if registry.get('schema_version') != 1: r13_pc_fail('SCHEMA_VERSION', str(registry.get('schema_version')))
            matches = [v for v in registry['background_variants'].values() if v['location'] == state.get('location') and state.get('period') in v['periods']]
            if not matches:
                report['bypass'] = 'unmigrated_location'
                return actors, report
            if len(matches) != 1: r13_pc_fail('AMBIGUOUS_BACKGROUND', state.get('location', '?'))
            variant = matches[0]; geometry = registry['geometries'][variant['geometry']]
            if context.get('world_size') != geometry['world_size'] or context.get('background') != variant['background']:
                r13_pc_fail('BACKGROUND_VARIANT_MISMATCH', variant['id'])
            if not available(variant['background']['file']) or blob_for(variant['background']['file']) != variant['git_blob']:
                r13_pc_fail('BACKGROUND_DIGEST_MISMATCH', variant['id'])
            flags = set(state.get('flags', [])); by_person = {a['person']: a for a in actors}
            if len(by_person) != len(actors): r13_pc_fail('DUPLICATE_ROSTER_ACTOR', 'upstream roster')
            proposals = {}; selected = {}
            for binding in registry['bindings']:
                if not binding.get('enabled', False) or binding.get('status') != 'approved' or variant['id'] not in binding['variants']: continue
                if state.get('day') not in binding['days'] or state.get('period') not in binding['periods']: continue
                if not set(binding.get('need_flags', [])) <= flags or flags.intersection(binding.get('not_flags', [])): continue
                person = binding['actor']; original = by_person.get(person)
                if original is None: continue  # Never spawn a role because a binding exists.
                if original.get('life_group'): continue
                if original['pose'] not in binding['replace_poses']: continue
                if person in selected: r13_pc_fail('AMBIGUOUS_BINDING', person)
                selected[person] = binding['id']
                guard = registry['upstream_guards'][binding['upstream_guard']]
                for field, expected in guard.items():
                    if r13_pc_normalized(original.get(field)) != r13_pc_normalized(expected):
                        r13_pc_fail('UPSTREAM_PLACEMENT_CHANGED', binding['id']+'/'+field)
                asset = registry['assets'][binding['asset']]
                if asset['person'] != person: r13_pc_fail('IDENTITY_MISMATCH', person)
                slot = geometry['slots'][binding['slot']]
                if binding['role'] not in slot['roles']: r13_pc_fail('INCOMPATIBLE_ROLE_SLOT', binding['role'])
                r13_pc_exact_spec(asset, exact_spec(person, asset['pose']), available, blob_for)
                proposals[person] = r13_pc_place(original, asset, slot, geometry['world_size'])
                quality = asset.get('source_quality', {})
                if quality.get('status') == 'legacy_coarse':
                    report['warnings'].append(dict(code='SOURCE_COARSE_NOT_FIXED_BY_GRID', asset=asset['id']))
                elif quality.get('status') != 'reference_reviewed':
                    report['warnings'].append(dict(code='SOURCE_STYLE_NOT_VERIFIED', asset=asset['id']))
            if not proposals:
                report['bypass'] = 'no_eligible_binding'
                return actors, report
            proposed = [proposals.get(a['person'], a) for a in actors]
            r13_pc_regression_collision(actors, proposed, set(proposals), exact_spec, geometry.get('critical_rects', []))
            report['applied'] = [selected[p] for p in proposals]
            return sorted(proposed, key=lambda a: a['depth']), report
        except (R13PlacementContractError, KeyError, AttributeError, TypeError, ValueError, IndexError, OverflowError, ZeroDivisionError) as error:
            report['errors'].append(str(error)); report['bypass'] = 'transaction_fallback'
            # The old source path is returned untouched, with an explicit diagnostic. No squash/neutral fallback.
            return actors, report

init 184 python:
    # Integration adapter, intentionally default-off. Existing upstream stages remain authoritative.
    import json as r13_pc_json
    R13_PLACEMENT_CONTRACTS_ENABLED = False
    R13_PC_BLOB_CACHE = {}
    R13_PC_LAST_DIAGNOSTIC = None
    try:
        R13_PLACEMENT_CONTRACTS = r13_pc_json.load(renpy.file('assets/room13-placement-contracts.json'))
    except (IOError, OSError, ValueError, TypeError) as r13_pc_load_error:
        R13_PLACEMENT_CONTRACTS = {}
        R13_PLACEMENT_CONTRACTS_ENABLED = False
        renpy.log('PLACEMENT_CONTRACTS REGISTRY_UNAVAILABLE '+str(r13_pc_load_error))


    def r13_pc_blob(path):
        import hashlib
        key = (R13_PLACEMENT_CONTRACTS.get('revision'), path)
        if key not in R13_PC_BLOB_CACHE:
            try:
                with renpy.file(path) as source:
                    data = source.read()
                R13_PC_BLOB_CACHE[key] = hashlib.sha1(('blob %d\0' % len(data)).encode('ascii')+data).hexdigest()
            except (IOError, OSError):
                R13_PC_BLOB_CACHE[key] = None
        return R13_PC_BLOB_CACHE[key]


    def r13_pc_register_aliases_at_init():
        """Init only. No live renpy.image calls and no overwrite of a shared original pose."""
        r13_pc_registry_shape(R13_PLACEMENT_CONTRACTS)
        pending = []
        for asset in R13_PLACEMENT_CONTRACTS.get('assets', {}).values():
            if asset.get('registration') != 'isolated_alias' or asset.get('status') != 'approved':
                continue
            person, pose, spec = asset['person'], asset['pose'], asset['spec']
            if not pose.startswith('pc_') or person not in CAST:
                r13_pc_fail('INVALID_ALIAS', asset['id'])
            if pose in R13_ACTING.get(person, {}) or pose in CAST[person] or renpy.has_image(person+' '+pose, exact=True):
                r13_pc_fail('ALIAS_ALREADY_REGISTERED', asset['id'])
            r13_pc_exact_spec(asset, spec, renpy.loadable, r13_pc_blob)
            r13_pc_anchors(asset)
            pending.append((person, pose, spec, Transform(Crop(tuple(spec['crop']), spec['file']), nearest=True)))
        # Validate the complete list before registration. Image calls only happen in init 184.
        if len({(p, n) for p, n, _, _ in pending}) != len(pending):
            r13_pc_fail('DUPLICATE_ALIAS', 'registry')
        for person, pose, spec, displayable in pending:
            renpy.image(person+' '+pose, displayable)
        for person, pose, spec, displayable in pending:
            runtime_spec = r13_pc_copy.deepcopy(spec)
            R13_ACTING.setdefault(person, {})[pose] = runtime_spec
            CAST[person][pose] = runtime_spec


    if R13_PLACEMENT_CONTRACTS_ENABLED:
        try:
            r13_pc_register_aliases_at_init()
        except (R13PlacementContractError, KeyError, AttributeError, TypeError, ValueError, IndexError, IOError, OSError) as r13_pc_alias_error:
            R13_PLACEMENT_CONTRACTS_ENABLED = False
            renpy.log('PLACEMENT_CONTRACTS ALIAS_INIT_REJECTED '+str(r13_pc_alias_error))


    def r13_pc_runtime_context(entry=False):
        state = store.room13 or {}; location = state.get('location'); daylight = r13_daylight()
        layout = r13_layout(location)
        background = None
        if layout:
            background = dict(file=r13_world_file(location, daylight), crop=list(layout.get('crops', {}).get(daylight, [])))
        elif location == 'post':
            file = r13_art_path('village', daylight)
            atlas = R13_PIXEL_LAYOUTS.get(file.rsplit('/', 1)[-1], {})
            rects = atlas.get('rects', [])
            if len(rects) > 1: background = dict(file=file, crop=list(rects[1]))
        locked = not getattr(store, 'r13_life_field_active', False)
        locked = locked or any(getattr(store, key, False) for key in ('r13_cg_active', 'r13_meeting_active', 'r13_meeting_live_active', 'r13_aftermath_active', 'r13_ending_story_active'))
        locked = locked or bool(set(renpy.get_showing_tags()).intersection(('r13_ep_cut', 'r13_ep_book')))
        return dict(entry=entry, locked_scene=locked, offers=bool(r13_offers_here()),
            world_size=[r13_world_width(location), 720], background=background)


    _r13_pc_upstream_stage = r13_stage_people

    def r13_stage_people(entry=False):
        global R13_PC_LAST_DIAGNOSTIC
        actors = _r13_pc_upstream_stage(entry)
        if not R13_PLACEMENT_CONTRACTS_ENABLED:
            return actors
        try:
            context = r13_pc_runtime_context(entry)
            result, report = r13_pc_resolve(actors, store.room13 or {}, R13_PLACEMENT_CONTRACTS, context,
                lambda person, pose: R13_ACTING.get(person, {}).get(pose), renpy.loadable, r13_pc_blob, enabled=True)
        except (KeyError, AttributeError, TypeError, ValueError, IndexError, IOError, OSError) as error:
            result, report = actors, dict(bypass='adapter_fallback', errors=[str(error)])
        diagnostic = repr(report)
        if diagnostic != R13_PC_LAST_DIAGNOSTIC:
            renpy.log('PLACEMENT_CONTRACTS '+diagnostic)
            R13_PC_LAST_DIAGNOSTIC = diagnostic
        return result
