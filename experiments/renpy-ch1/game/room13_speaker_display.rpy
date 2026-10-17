# Presentation only: do not rename character objects, IDs, save keys or authored speech.
init 150 python:
    R13_DISPLAY_NAMES = {
        "resident_nubi": "누비", "resident_momo": "모모",
        "resident_musoe": "무쇠", "resident_seori": "서리",
        "resident_ppul": "뿔이", "resident_eunho": "은호",
    }
    R13_DISPLAY_ALIASES = {R13_NAMES[key]: name for key, name in R13_DISPLAY_NAMES.items()}
    R13_DISPLAY_ALIASES.update({"모모 관장": "모모"})

    def r13_display_name(person):
        # Call only where this person was already named by the existing discovery UI.
        return R13_DISPLAY_NAMES.get(person, R13_NAMES.get(person, person or ""))

    def r13_speaker_label(who):
        # Resolve the visible label, never infer an identity from the current actor/packet.
        # Unknown, masked, narrator and unresolved role-only names remain untouched.
        return R13_DISPLAY_ALIASES.get(who, who)

    def r13_display_role(person):
        return R13_PUBLIC_ROLES.get(person, "")
