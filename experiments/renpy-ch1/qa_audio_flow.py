"""Run native chapter QA and verify authored dramatic audio through the ending.

Uses the same real clicks as qa_source; never injects game progress or audio state.
"""
import argparse
import asyncio
import json

import qa_source


ROOT = qa_source.ROOT
PACKAGE = json.loads((ROOT / "game/chapter-source.json").read_text())
PATHS = json.loads((ROOT / "game/assets/source-map.json").read_text())
EPISODE = dict(PACKAGE["episode"])
EPISODE.update(qa_source.DIALOGUE["sections"])


def authored_cues():
    cues = {}
    for group, section in (("meet", "MEET"), ("final", "FINAL")):
        for phase, spec in enumerate(EPISODE[section]["phases"]):
            lists = [(f"{group}{phase}", spec.get("lines", []))]
            lists += [(f"{group}{phase}/ok", claim.get("ok", []))
                      for claim in spec.get("stms", [])]
            for origin, packets in lists:
                for index, packet in enumerate(packets):
                    if isinstance(packet, dict) and packet.get("audio"):
                        cues[(f"{origin}:{index}", packet.get("t"))] = (
                            group, packet["audio"])
    return cues


CUES = authored_cues()
BASE_STATE = qa_source.SourceTrial.state


def music_path(key):
    return PATHS[PACKAGE["music"][key]["media"]]


async def settled_audio(self, state, expected_music, expected_pulse=None,
                        silent_typing=False):
    """Observe the current line after real channel fades, without advancing it.

    get_playing() retains the outgoing file during a .15-second music fade.
    A bounded wait distinguishes that transition from a persistent wrong cue.
    """
    line = (state.get("line"), state.get("text"))
    for attempt in range(13):
        matches = (state["music"] == expected_music
                   and (expected_pulse is None or bool(state["pulse"]) == expected_pulse)
                   and (not silent_typing or state["typing"] is None))
        if matches:
            return state
        if attempt == 12:
            break
        await self.page.wait_for_timeout(100)
        state = await BASE_STATE(self)
        assert (state.get("line"), state.get("text")) == line, (
            "Dialogue advanced while checking its audio cue", line,
            (state.get("line"), state.get("text")))
    assert state["music"] == expected_music, (
        "Incorrect dramatic music after channel fade", line,
        state["music"], expected_music)
    if expected_pulse is not None:
        assert bool(state["pulse"]) == expected_pulse, (
            "Incorrect heartbeat state after channel fade", line, state["pulse"])
    if silent_typing:
        assert state["typing"] is None, (
            "Typing leaked into dramatic silence after channel fade", line)
    return state


async def audio_state(self):
    state = await BASE_STATE(self)
    if not hasattr(self, "audio_flow"):
        self.audio_flow = {"cues": [], "seen": set(), "pulse_count": None}
    flow = self.audio_flow
    cue_id = (state.get("line"), state.get("text"))
    cue = CUES.get(cue_id)
    # A line remains in source_state during the next location transition.
    # Only inspect while its actual dialogue interaction is on screen.
    if (cue and state["stage"] == "meeting" and state["group"] == cue[0]
        and str(state["line"]).startswith(f"{state['group']}{state['phase']}")
        and not (
        state["debate"] or state["evidence"] or state["choice"]
        or state["saving"] or state["loading"] or state["menu"]
    )):
        group, kind = cue
        calm_key = ("inn_after" if "inn_case_cleared" in state["flags"] else
                    "inn_meet" if group == "meet" else "inn_climax")
        expected = (music_path(calm_key)
                    if kind == "calm" else
                    music_path("inn_meet_press" if group == "meet" else "inn_climax_press")
                    if kind in ("press", "impact") else None)
        state = await settled_audio(
            self, state, expected,
            expected_pulse=kind == "pulse" if kind in ("pulse", "silence") else None,
            silent_typing=kind in ("pulse", "silence"))
        if kind in ("pulse", "silence"):
            assert state["typing"] is None, ("Typing leaked into dramatic silence", cue_id)
            assert bool(state["pulse"]) == (kind == "pulse"), (
                "Incorrect heartbeat state", cue_id, state["pulse"])
        if kind == "pulse":
            starts = state["effects"].count("heartbeat")
            if flow["pulse_count"] is not None:
                assert starts == flow["pulse_count"], (
                    "Consecutive pulse cues restarted the heartbeat", cue_id,
                    starts, flow["pulse_count"])
            flow["pulse_count"] = starts
        else:
            flow["pulse_count"] = None
        if cue_id not in flow["seen"]:
            flow["seen"].add(cue_id)
            flow["cues"].append(dict(line=cue_id[0], group=group, cue=kind,
                                     music=state["music"], pulse=state["pulse"]))
    if (state["stage"] == "ending" and not state["complete_screen"]
        and str(state["line"]).startswith(f"{state['scene']}:") ):
        event = "ending_" + state["scene"]
        assert event in state["time_events"], ("After-story time event missing", event)
        assert state["minutes"] >= qa_source.TIMELINE["events"][event]["at"], (
            "After-story clock did not advance", state["scene"], state["minutes"])
        expected = music_path("inn_serious" if state["scene"] == "E4" else "inn_after")
        state = await settled_audio(self, state, expected, expected_pulse=False)
        assert state["pulse"] is None, "Heartbeat leaked into after-story"
    return state


BASE_RUN = qa_source.run


async def audio_run(*args, **kwargs):
    # Collect each instance's records without changing the original QA route.
    sessions = []
    async def capture(self):
        if self not in sessions:
            sessions.append(self)
        return await audio_state(self)
    qa_source.SourceTrial.state = capture
    result = await BASE_RUN(*args, **kwargs)
    cues = [cue for session in sessions for cue in session.audio_flow["cues"]]
    if not kwargs.get("discovery_only") and not (len(args) > 4 and args[4]):
        assert any(c["group"] == "final" and c["cue"] == "calm" for c in cues), (
            "Full route never verified a final-round calm cue")
        assert any(c["cue"] == "pulse" for c in cues), (
            "Full route never verified heartbeat cues")
    result["dramatic_audio_cues"] = cues
    result["checks"].extend(["meeting_and_final_music_follow_authored_cues",
                              "consecutive_heartbeat_cues_keep_continuous_playback",
                              "dramatic_silence_has_no_typing",
                              "after_story_music_and_heartbeat_do_not_leak",
                              "after_story_clock_advances_from_noon_to_night"])
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="/tmp/daram-audio-flow-qa")
    parser.add_argument("--desktop-only", action="store_true")
    parser.add_argument("--mobile-only", action="store_true")
    parser.add_argument("--discovery-only", action="store_true")
    qa_source.run = audio_run
    asyncio.run(qa_source.main(parser.parse_args()))
