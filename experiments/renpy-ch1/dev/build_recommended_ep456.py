from pathlib import Path
root=Path(__file__).resolve().parents[1]
model=(root/'dev/recommended_ep456_model.py').read_text()
labels=(root/'dev/recommended_ep456_labels.rpy').read_text()
(root/'game/systems/room13_recommended_ep456.rpy').write_text('# Isolated recommended route plugin. Generated from dev/recommended_ep456_model.py and labels.\ninit 910 python:\n'+''.join('    '+x+'\n' for x in model.splitlines())+'\n'+labels)
