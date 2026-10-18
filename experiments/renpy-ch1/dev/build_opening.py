from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'dev/recommended_opening_model.py').read_text()
(R/'game/systems/room13_recommended_opening.rpy').write_text('# Independent day-one entry; no legacy automatic campaign events.\ninit 906 python:\n'+''.join('    '+line+'\n' for line in s.splitlines())+'\n'+(R/'dev/recommended_opening_ui.rpy').read_text())
