# Pilot: carriage entry, camera cuts, and the receiving village location.
# Plain store data and script calls are rollback/save aware. No async timers.
default scene_execution = None
default scene_execution_log = []

init 30 python:
    def scene_direction_spec(direction):
        spec = dict(store.scene_execution)
        spec.update(camera=direction.get("camera", "stage"), night=direction.get("night"), who=None)
        if "music" in direction:
            spec["music"] = direction["music"]
        return spec

    def scene_prepare(spec):
        store.scene_execution = dict(spec)
        store.source_scene = spec["sid"]
        store.place, store.clock_text = spec["title"], spec["sub"]
        store.source_camera = spec.get("camera", "stage")
        store.source_background = spec.get("bg", spec.get("loc", "carriage"))
        store.source_night = spec.get("night")
        store.source_stage_person = SOURCE_ALIAS.get(spec.get("who"), spec.get("who"))
        store.dialogue_speaker, store.dialogue_expression = None, "neutral"
        store.source_proof_show = []
        source_pulse(False)
        renpy.music.stop(channel="scene_fx")
        store.scene_execution_log.append(dict(scene=spec["sid"], camera=store.source_camera))

label scene_present(spec):
    window hide
    hide visitor
    hide screen source_proof
    $ scene_prepare(spec)
    scene black with Dissolve(.15)
    $ source_score(spec.get("music"))
    $ renpy.pause(.3,hard=True)
    scene expression source_picture() with Dissolve(.22)
    return
