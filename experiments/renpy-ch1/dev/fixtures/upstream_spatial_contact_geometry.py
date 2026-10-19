# Verbatim upstream assertion/geometry function: game/systems/room13_spatial_contacts.rpy
# PR18C Git blob 8a6f848e29c131a145197e2f9dbb4f0165141386; no display or image execution.
def r13_contact_geometry(actor,pose,anchor,target,height,depth):
    spec=r13_acting_spec(actor["person"],pose) or {}
    w0,h0=r13_actor_geometry(actor["person"],pose)
    point=spec.get(anchor,spec.get("foot",[w0/2.0,h0]))
    scale=float(height)/h0
    x=int(round(target[0]-point[0]*scale));y=int(round(target[1]-point[1]*scale))
    w=int(round(w0*scale));h=int(round(h0*scale))
    changed=dict(actor)
    changed.update(pose=pose,x=x,y=y,width=w,height=h,rect=[x,y,w,h],depth=depth,
        slot=None,occlusion=[],contact=spec.get("contact","standing"))
    return changed
