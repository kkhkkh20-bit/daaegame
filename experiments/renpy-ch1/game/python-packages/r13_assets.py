"""에셋 등록·태그 매칭. RenPy/HTTP/게임 상태에 의존하지 않는 공통 모듈."""
from copy import deepcopy
from pathlib import PurePosixPath


class AssetError(ValueError):
    pass


def safe_asset_path(path):
    if not isinstance(path, str) or '\\' in path:
        raise AssetError("올바른 에셋 경로가 아닙니다.")
    p = PurePosixPath(path)
    if p.is_absolute() or '..' in p.parts or not path.startswith('assets/'):
        raise AssetError("assets 안의 상대 경로만 사용할 수 있습니다.")
    return path


class Registry:
    def __init__(self, catalog, bindings):
        self.catalog, self.bindings = catalog, bindings
        if catalog.get('version') != 1 or bindings.get('version') != 1:
            raise AssetError("지원하지 않는 도구함 버전입니다.")
        self._index()

    def _index(self):
        self.by_tag = {}
        self.cache = {}
        self._resolving = set()
        for key, asset in self.catalog.get('assets', {}).items():
            safe_asset_path(asset.get('path'))
            asset['id'] = key
            tags = set(asset.get('tags', [])) | {'asset:' + key}
            if not any(t.startswith('state:') for t in tags):
                tags.add('state:basic')
            asset['tags'] = sorted(tags)
            for tag in tags:
                if not isinstance(tag, str) or not tag or len(tag) > 180:
                    raise AssetError("태그는 1~180자 문자열이어야 합니다.")
                self.by_tag.setdefault(tag, set()).add(key)

    def candidates(self, tags):
        if not tags:
            return set(self.catalog['assets'])
        found = None
        for tag in tags:
            ids = self.by_tag.get(tag, set())
            found = set(ids) if found is None else found & ids
        return found or set()

    def resolve(self, role, state='basic'):
        key=(role,state)
        if key in self._resolving:
            raise AssetError("연결이 순환합니다: "+role)
        self._resolving.add(key)
        try:
            return self._resolve(role,state)
        finally:
            self._resolving.remove(key)

    def _resolve(self, role, state='basic'):
        cached = self.cache.get((role, state))
        if cached is not None:
            return deepcopy(cached)
        rule = self.bindings.get('bindings', {}).get(role)
        if rule is None:
            raise AssetError("등록하지 않은 역할: " + role)
        states = rule.get('states', ['basic'])
        fallback = rule.get('fallback', {})
        requested = state
        seen = set()
        while True:
            if state in seen:
                raise AssetError("상태 대체가 순환합니다: " + role)
            seen.add(state)
            ids = self.candidates(rule.get('match', []) + rule.get('requires', []))
            # 한 파일을 직접 지정한 연결은 그 그림 자체를 선택한다.
            direct = any(t.startswith('asset:') for t in rule.get('match', [])) and len(states) == 1
            if not direct:
                ids &= self.by_tag.get('state:' + state, set())
            if len(ids) > 1:
                raise AssetError("매칭이 여러 개입니다: %s / %s" % (role, state))
            if ids:
                asset = deepcopy(self.catalog['assets'][next(iter(ids))])
                if rule.get('media') and asset.get('media') != rule['media']:
                    raise AssetError("에셋 종류가 다릅니다: " + role)
                if rule.get('canvas_size') and asset.get('size') != rule['canvas_size']:
                    raise AssetError("캔버스 크기가 다릅니다: %s / 필요 %s" % (role, rule['canvas_size']))
                asset['render'] = dict(rule.get('render', {})) if role.startswith('file:') else dict(asset.get('render', {}), **rule.get('render', {}))
                if any(not asset['render'].get(k) for k in rule.get('requires_render', [])):
                    raise AssetError("이 역할에 필요한 렌더 정보가 없습니다: " + role)
                if any(asset['render'].get(k) for k in rule.get('forbid_render', [])):
                    raise AssetError("이 역할에서 허용하지 않는 분할/변형입니다: " + role)
                self._check_render(asset)
                # 원래 파일 이름을 참조하는 옛 화면도 같은 최종 파일을 사용한다.
                alias='file:'+asset['path']
                if alias!=role and alias in self.bindings['bindings']:
                    asset['path']=self.resolve(alias)['path']
                asset['role'], asset['state'], asset['requested_state'] = role, state, requested
                self.cache[(role, requested)] = asset
                return deepcopy(asset)
            next_state = fallback.get(state)
            if next_state is None and state not in states:
                next_state = 'basic'
            if next_state is None:
                raise AssetError("매칭할 에셋이 없습니다: %s / %s" % (role, state))
            state = next_state

    @staticmethod
    def _check_render(asset):
        render = asset.get('render', {})
        size = asset.get('size')
        crop = render.get('crop')
        if crop:
            if (len(crop) != 4 or any(not isinstance(n, (int, float)) for n in crop)
                    or min(crop[:2]) < 0 or min(crop[2:]) <= 0 or not size
                    or crop[0] + crop[2] > size[0] or crop[1] + crop[3] > size[1]):
                raise AssetError("잘라내기 범위가 원본 밖입니다: " + asset['id'])
        safe = render.get('safe_size')
        if 'safe_size' in render:
            area = crop[2:] if crop else size
            if (not isinstance(safe, (list, tuple)) or len(safe) != 2 or not area
                    or any(isinstance(n, bool) or not isinstance(n, (int, float))
                           or not 0 < n <= area[i] for i, n in enumerate(safe))):
                raise AssetError("내용 안전영역이 잘라낸 그림 안의 양수 크기가 아닙니다: " + asset['id'])
        gap = render.get('icon_gap', 8)
        if (isinstance(gap, bool) or not isinstance(gap, (int, float))
                or not 0 <= gap < float('inf')):
            raise AssetError("아이콘 간격은 유한한 0 이상의 수여야 합니다: " + asset['id'])
        zoom = render.get('zoom', 1.0)
        if not isinstance(zoom, (int, float)) or not 0 < zoom <= 16:
            raise AssetError("균일 배율이 올바르지 않습니다: " + asset['id'])
        if render.get('frame'):
            if not render.get('allow_frame'):
                raise AssetError("분할 확대를 허용하지 않은 에셋입니다: " + asset['id'])
            if len(render['frame']) not in (2, 4) or min(render['frame']) < 0:
                raise AssetError("프레임 여백이 올바르지 않습니다: " + asset['id'])
            borders=render['frame'] if len(render['frame'])==4 else render['frame']*2
            area=crop[2:] if crop else size
            if not area or borders[0]+borders[2]>area[0]*zoom or borders[1]+borders[3]>area[1]*zoom:
                raise AssetError("프레임 여백이 축소한 그림보다 큽니다: " + asset['id'])
        if any(k in render for k in ('xzoom', 'yzoom', 'xscale', 'yscale')):
            raise AssetError("가로·세로 개별 늘림은 허용하지 않습니다.")

    def validate(self):
        errors = []
        for role, rule in self.bindings.get('bindings', {}).items():
            geometry = None
            for state in rule.get('states', ['basic']):
                try:
                    item = self.resolve(role, state)
                    render = item.get('render', {})
                    current = (item.get('size'), render.get('crop'), render.get('zoom', 1), render.get('frame'),
                               render.get('safe_size'), render.get('icon_gap', 8))
                    if geometry is not None and current != geometry:
                        raise AssetError("상태별 캔버스·잘라내기·배율·내용 배치가 다릅니다: " + role)
                    geometry = current
                except (AssetError, TypeError, KeyError) as exc:
                    errors.append(str(exc))
        return errors

    def assign(self, role, asset_id):
        if role not in self.bindings['bindings'] or asset_id not in self.catalog['assets']:
            raise AssetError("역할 또는 에셋을 찾을 수 없습니다.")
        rule = self.bindings['bindings'][role]
        group = rule.get('group', role)
        changed = [k for k, v in self.bindings['bindings'].items() if v.get('group', k) == group]
        asset = self.catalog['assets'][asset_id]
        packs = [t for t in asset['tags'] if t.startswith('pack:')]
        before = deepcopy(self.bindings)
        try:
            for key in changed:
                target = self.bindings['bindings'][key]
                if len(target.get('states', ['basic'])) > 1 or (packs and target.get('states', ['basic']) != ['basic']):
                    if len(packs) != 1:
                        raise AssetError("이 역할은 기본·누름·선택·비활성 상태 세트가 필요합니다.")
                    target['match'] = packs
                else:
                    target['match'] = ['asset:' + asset_id]
            self.cache.clear()
            errors = self.validate()
            if errors:
                raise AssetError(errors[0])
        except Exception:
            self.bindings.clear(); self.bindings.update(before); self.cache.clear()
            raise
        return changed

    def set_tags(self, asset_id, tags):
        if asset_id not in self.catalog['assets'] or not isinstance(tags, list):
            raise AssetError("올바른 에셋과 태그 목록이 필요합니다.")
        before = deepcopy(self.catalog['assets'][asset_id]['tags'])
        try:
            self.catalog['assets'][asset_id]['tags'] = list(tags)
            self._index()
            errors = self.validate()
            if errors:
                raise AssetError(errors[0])
        except Exception:
            self.catalog['assets'][asset_id]['tags'] = before; self._index()
            raise


class RuntimeSession:
    """테마의 제작 세션 메모리. 게임의 저장·롤백 변수와 분리한다."""
    def __init__(self):
        self.registry = None
        self.revision = 0
        self.slots = None
        self.mtimes = None
        self.file_map = {}
        self.file_guard = None
        self.prior_open = None


runtime = RuntimeSession()
