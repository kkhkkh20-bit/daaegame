from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def build():
    model=(ROOT/'dev/recommended_meeting_staging_model.py').read_text()
    runtime=(ROOT/'dev/recommended_meeting_staging_runtime.rpy').read_text()
    header='''# Recommended-only six-hearing presentation. Source-wired, native validation pending.
# Default-off: no release activation without the native matrix in the handoff document.
default r13_rec_staging_enabled = False
default r13_rec_staging_active = False
default r13_rec_staging_snapshot = None
default r13_rec_stage_session = None
default r13_rec_stage_memory = {}
default r13_rec_stage_preview_mode = False

init 925 python:
'''
    dest=ROOT/'game/systems/room13_recommended_meeting_adapter.rpy'
    dest.write_text(header+'\n'.join('    '+line if line else '' for line in model.splitlines())+'\n\n'+runtime)
    return dest
if __name__=='__main__': print(build())
