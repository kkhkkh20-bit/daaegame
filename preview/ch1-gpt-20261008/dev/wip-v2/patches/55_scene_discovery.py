# Keep the native click/input guards, route this deliberate observation through
# one transaction so rescue and its evidence card cannot split into two clicks.
rep('  var id=b.dataset.spot||b.dataset.obs;\n  if(id==="o_inn_lock")',
    '  var id=b.dataset.spot||b.dataset.obs;\n  if(id==="o_under"&&window.__innDiscover){e.stopImmediatePropagation();e.preventDefault();window.__innDiscover();return}\n  if(id==="o_inn_lock")')
