"""Reviewed adult stature at two kitchen depths, independent from prop-support anchors."""
# Head bounds include ears. Same-depth actions use equal head heights, not equal full canvases.
HEAD_HEIGHT={'KI-1':120,'KI-2':94,'KI-3':120,'KI-4':120,'KI-5':120}
def apply_kitchen_stature(registry):
 for row in registry['rows']:
  key=row['request_id']
  if key not in HEAD_HEIGHT:continue
  spec=row['spec'];variant=row['variants']['morning']
  variant['render_height']=round(HEAD_HEIGHT[key]*spec['crop'][3]/spec['head'][3])
  variant['review_head_height']=HEAD_HEIGHT[key]
  variant['review_ground_depth']=500 if key=='KI-2' else 690
  # Keep the approved support point and occlusion: scaling occurs about the prop, not feet.
 return registry
