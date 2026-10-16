# Boot and screen-result safety (0.18.79, owner-approved 2026-10-15 19:23 PDT).
#
# Reproduced cause of the reported boot loop: when the browser cannot give Ren'Py a WebGL
# renderer, Ren'Py raises "Could not set video mode." at the first interaction and leaves
# renpy.display.draw = None. Its default handler cannot show the error screen without a
# renderer, so the exception is only logged and the script carries on with the next
# statement: every later `call screen` fails the same way (core.py interact_core:
# draw.update), `_return` stays None, `r13_choice[0]` fails, and the opening runs on by itself
# into the gate hub, which then loops for ever while each report writes files (FS.syncfs).
#
# What this file does
#   1. Renderer missing: the first exception is kept (console + window.r13BootFailure), the
#      game stops on the spot - no further statements, no autosave, no records or time - and
#      the page shows what happened with a "다시 시도" (reload) button and a log download.
#      Nothing is retried automatically. Desktop builds and a working renderer are untouched:
#      Ren'Py's own error screen still handles every other exception.
#   2. Hub results: a hub/entry screen must return a (kind, value) pair. A bad result shows
#      the same screen again without any game step; three bad results in a row raise a normal
#      Ren'Py error (visible, no silent loop).
init -100 python:
    R13_BOOT_GUARD = {"failures": 0, "first": None, "bad_choice": 0, "bad_seen": []}

    def r13_renderer_ready():
        return renpy.display.draw is not None

    def r13_boot_failure_text(te):
        import io
        out = io.StringIO()
        try:
            te.format(renpy.error.NonColoredExceptionPrintContext(out, filter_private=True, emit_context=False))
        except Exception:
            try:
                out.write(str(te))
            except Exception:
                out.write("unknown error")
        return out.getvalue()[-4000:]

    def r13_boot_halt(te=None):
        import json as _json
        R13_BOOT_GUARD["failures"] += 1
        if R13_BOOT_GUARD["first"] is None:
            R13_BOOT_GUARD["first"] = r13_boot_failure_text(te) if te is not None else "renderer missing"
            renpy.display.log.write("ROOM13 BOOT GUARD: renderer missing; game stopped. First error:\n" + R13_BOOT_GUARD["first"])
        if not renpy.emscripten:
            return False
        import emscripten
        detail = _json.dumps(R13_BOOT_GUARD["first"])
        version = _json.dumps(renpy.config.version)
        emscripten.run_script(r"""(function(){
  var first=%s, version=%s;
  window.r13BootFailure={version:version, first:first, at:new Date().toISOString(),
    userAgent:navigator.userAgent, webgl2:(function(){try{return !!document.createElement('canvas').getContext('webgl2');}catch(e){return false;}})(),
    contextLost:!!window.webglContextLost};
  console.error('ROOM13 BOOT GUARD: renderer missing, game stopped (no autoplay, no saves).', window.r13BootFailure);
  if(document.getElementById('r13-boot-failure'))return;
  var d=document.createElement('div');d.id='r13-boot-failure';
  d.style.cssText='position:fixed;left:50%%;top:50%%;transform:translate(-50%%,-50%%);z-index:1000;max-width:560px;width:86%%;'+
    'background:#211a16f2;border:1px solid #806446;border-radius:8px;padding:18px;color:#f3e7ce;font-family:Galmuri,sans-serif;font-size:15px;line-height:1.6';
  d.innerHTML='<b style="color:#ffdc91;font-size:18px">화면을 그리지 못해 게임을 멈췄습니다</b>'+
    '<p>이 브라우저 탭에서 그래픽(WebGL) 화면을 만들지 못했습니다. 이야기는 진행되지 않았고, 저장도 바뀌지 않았습니다.</p>'+
    '<p>다시 시도해도 같으면 다른 브라우저나 기기에서 열어 주세요. 실행 기록을 받아 두면 원인을 확인할 수 있습니다.</p>';
  var row=document.createElement('div');row.style.cssText='display:flex;gap:10px;margin-top:12px;flex-wrap:wrap';
  function btn(t,f){var b=document.createElement('button');b.textContent=t;b.onclick=f;
    b.style.cssText='font-family:inherit;font-size:15px;padding:8px 14px;background:#30261f;color:#f3e7ce;border:1px solid #806446;border-radius:6px;cursor:pointer';row.appendChild(b);}
  btn('다시 시도',function(){location.reload();});
  btn('실행 기록 받기',function(){try{FSDownload('/log.txt','text/plain');}catch(e){}});
  d.appendChild(row);document.body.appendChild(d);
  var s=document.getElementById('statusDiv');if(s)s.className='hidden';
})();""" % (detail, version))
        # Hold the game thread here: nothing else runs, the page stays responsive (asyncify sleep).
        while True:
            emscripten.sleep(1000)

    def r13_exception_guard(te):
        if renpy.display.draw is None:
            return bool(r13_boot_halt(te))
        return False

    config.exception_handler = r13_exception_guard

    def r13_screen_choice_ok(value, where):
        ok = isinstance(value, (tuple, list)) and len(value) == 2 and isinstance(value[0], str)
        if ok:
            R13_BOOT_GUARD["bad_choice"] = 0
            return True
        R13_BOOT_GUARD["bad_choice"] += 1
        if where not in R13_BOOT_GUARD["bad_seen"]:
            R13_BOOT_GUARD["bad_seen"].append(where)
            renpy.display.log.write("ROOM13 screen %s returned %r (not a choice); showing it again" % (where, value))
        if renpy.display.draw is None:
            r13_boot_halt(None)
        if R13_BOOT_GUARD["bad_choice"] >= 3:
            R13_BOOT_GUARD["bad_choice"] = 0
            raise Exception("Screen %s returned %r three times in a row; stopped instead of looping." % (where, value))
        return False
