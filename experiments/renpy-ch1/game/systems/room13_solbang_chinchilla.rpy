# Approved chinchilla field activity. All dialogue/profile registration is separate.
init 177 python:
    _r13_solbang_living_pose=r13_living_pose
    def r13_living_pose(person,location,period):
        pose=_r13_solbang_living_pose(person,location,period)
        if person=="resident_solbang" and location=="forest" and period in (0,1) and pose in ("neutral","world","activity","inn_activity"):
            return "work_herb_bundle"
        return pose
