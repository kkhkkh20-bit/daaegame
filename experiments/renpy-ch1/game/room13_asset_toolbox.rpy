# 등록/매칭 모델과 RenPy 표시 어댑터를 분리한다. 게임 진행 상태에는 접근하지 않는다.
init -200 python:
    import json as r13_assets_json
    import weakref as r13_assets_weakref
    import os as r13_assets_os
    import threading as r13_assets_threading
    from r13_assets import Registry as R13AssetRegistry, AssetError as R13AssetError

    from r13_assets import runtime as _r13_asset_runtime
    _r13_asset_runtime.revision=0
    _r13_asset_runtime.slots=r13_assets_weakref.WeakSet()
    _r13_asset_files=("asset-toolbox/catalog.json","asset-toolbox/bindings.json")
    _r13_asset_runtime.mtimes=None

    def _r13_asset_load():
        data=[]
        for path in _r13_asset_files:
            with renpy.file(path) as handle:data.append(r13_assets_json.load(handle))
        registry=R13AssetRegistry(*data)
        errors=registry.validate()
        if errors:raise R13AssetError(errors[0])
        return registry

    _r13_asset_runtime.registry=_r13_asset_load()

    def _r13_asset_file_map(registry):
        extensions=(".png",".webp",".jpg",".jpeg",".svg",".mp3",".ogg",".wav",".opus",".ttf",".otf",".woff2")
        mapping={}
        for role in registry.bindings["bindings"]:
            if not role.startswith("file:assets/") or not role.lower().endswith(extensions):continue
            path=registry.resolve(role)["path"]
            if path!=role[5:]:mapping[role[5:]]=path
        return mapping

    _r13_asset_runtime.file_map=_r13_asset_file_map(_r13_asset_runtime.registry)
    _r13_asset_runtime.file_guard=r13_assets_threading.local()
    _r13_asset_runtime.prior_open=(getattr(config.file_open_callback,"r13_asset_previous",None) if getattr(config.file_open_callback,"r13_asset_hook",False) else config.file_open_callback)

    def _r13_asset_file_open(name):
        previous=_r13_asset_runtime.prior_open
        if getattr(_r13_asset_runtime.file_guard,"active",False):
            return previous(name) if previous else None
        target=_r13_asset_runtime.file_map.get(name)
        if target:
            _r13_asset_runtime.file_guard.active=True
            try:return renpy.file(target)
            finally:_r13_asset_runtime.file_guard.active=False
        return previous(name) if previous else None

    _r13_asset_file_open.r13_asset_hook=True
    _r13_asset_file_open.r13_asset_previous=_r13_asset_runtime.prior_open
    config.file_open_callback=_r13_asset_file_open

    def r13_asset_revision():
        return _r13_asset_runtime.revision

    def r13_asset_spec(role,state="basic"):
        if role.startswith("file:") and role not in _r13_asset_runtime.registry.bindings["bindings"]:
            # 새 파일은 scan 전에도 기존 로딩 의미를 유지한다.
            from r13_assets import safe_asset_path
            return dict(id=role,path=safe_asset_path(role[5:]),render={},tags=[],size=None,media="image")
        return _r13_asset_runtime.registry.resolve(role,state)

    def r13_asset_path(role,state="basic"):
        return r13_asset_spec(role,state)["path"]

    class R13AssetSlot(renpy.Displayable):
        def __init__(self,role,state="basic",**kwargs):
            super(R13AssetSlot,self).__init__(**kwargs)
            self.role,self.state=role,state
            self.revision=-1
            self.child=None
            _r13_asset_runtime.slots.add(self)
        def resolve(self):
            if self.child is None or self.revision!=_r13_asset_runtime.revision:
                spec=r13_asset_spec(self.role,self.state)
                if spec.get("media")!="image":raise R13AssetError("표시용 이미지가 아닙니다: "+self.role)
                render=spec.get("render",{})
                child=Image(spec["path"])
                if render.get("crop"):child=Crop(tuple(render["crop"]),child)
                if render.get("zoom",1)!=1:child=Transform(child,zoom=render["zoom"])
                if render.get("frame"):child=Frame(child,*render["frame"])
                if render.get("alpha",1)!=1:child=Transform(child,alpha=render["alpha"])
                self.child,self.revision=child,_r13_asset_runtime.revision
            return self.child
        def visit(self):
            return [self.resolve()]
        def render(self,width,height,st,at):
            return renpy.render(self.resolve(),width,height,st,at)

    def r13_asset(role,state="basic"):
        return R13AssetSlot(role,state)

    def _r13_assets_changed(flush_files=False):
        _r13_asset_runtime.revision+=1
        if flush_files:
            for path in {item["path"] for item in _r13_asset_runtime.registry.catalog["assets"].values()}:
                renpy.flush_cache_file(path)
            renpy.free_memory()
        for slot in list(_r13_asset_runtime.slots):renpy.redraw(slot,0)
        if "_r13_evidence_art_cache" in globals():_r13_evidence_art_cache.clear()
        if "R13_FULLBODY_ART_CACHE" in globals():R13_FULLBODY_ART_CACHE.clear()
        renpy.restart_interaction()

    def r13_assets_reload():
        replacement=_r13_asset_load()
        mapping=_r13_asset_file_map(replacement)
        _r13_asset_runtime.registry=replacement
        _r13_asset_runtime.file_map=mapping
        _r13_assets_changed(True)
        return _r13_asset_runtime.revision

    def r13_assets_assign(role,asset_id):
        # 개발 도구·검수용 메모리 변경. 진행/저장/소지 자료는 변경하지 않는다.
        changed=_r13_asset_runtime.registry.assign(role,asset_id)
        mapping=_r13_asset_file_map(_r13_asset_runtime.registry)
        changed_files=mapping!=_r13_asset_runtime.file_map
        _r13_asset_runtime.file_map=mapping
        _r13_assets_changed(changed_files)
        return changed

    def r13_assets_poll():
        current=tuple(r13_assets_os.stat(r13_assets_os.path.join(config.gamedir,path)).st_mtime_ns for path in _r13_asset_files)
        if _r13_asset_runtime.mtimes is None:_r13_asset_runtime.mtimes=current
        elif current!=_r13_asset_runtime.mtimes:
            try:r13_assets_reload()
            except Exception as exc:renpy.notify("에셋 연결을 적용하지 못했습니다: "+str(exc))
            _r13_asset_runtime.mtimes=current

    # 로컬 제작 환경에서만 자동 새로고침. 일반 게임 화면에는 도구 UI를 넣지 않는다.
    if r13_assets_os.environ.get("R13_ASSET_TOOLBOX")=="1":
        config.overlay_screens.append("r13_asset_toolbox_watch")

screen r13_asset_toolbox_watch():
    timer .5 repeat True action Function(r13_assets_poll)
