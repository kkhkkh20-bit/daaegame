import renpy,time
s=renpy.store
s._review_trace=[]
def wrap_render(cls,kind):
 old=cls.render
 def traced(self,w,h,st,at):
  began=time.perf_counter();t=renpy.display.core.get_time()
  value=old(self,w,h,st,at)
  row=dict(kind=kind,t=t,st=st,at=at,id=id(self),ms=(time.perf_counter()-began)*1000)
  if kind=='layer':row.update(view=self.review_view_override,components=list(self.review_components),actors=list(self.review_actor_ids),lag=self.lag)
  if kind=='transition':row.update(arrival=self.arrival)
  s._review_trace.append(row)
  return value
 cls.render=traced
for cls,kind in [(s.R13EffectReview,'root'),(s.R13DirectionalTrailReview,'transition'),(s.R13ReviewOrbitLayer,'layer')]:wrap_render(cls,kind)
old_init=s.R13EffectReview.__init__
def traced_init(self,*args,**kwargs):
 old_init(self,*args,**kwargs)
 s._review_trace.append(dict(kind='construct',t=renpy.display.core.get_time(),id=id(self)))
s.R13EffectReview.__init__=traced_init
result=True
