# A cached vote panel may outlive its original round-table DOM after reopening.
# Keep native verdict/locks; resolve the current native vote button at click time.
rep('''var v=r.querySelector('.rt-mid.vote .vc[data-seat="'+b.dataset.pick+'"]');if(v)v.click()''',
    '''var current=document.querySelector('body>.rt'),v=current&&current.querySelector('.rt-mid.vote .vc[data-seat="'+b.dataset.pick+'"]');if(v)v.click()''', 1)
