# Boot and authored scenes acquire their background synchronously. The runner
# waits for its decoded primary picture before starting the first dialogue.
rep('render();if(EPK==="inn"&&window.__innStart)setTimeout(window.__innStart,300);',
    'render();if(EPK==="inn"&&window.__innStart)window.__innStart();')
rep('var go=function(){if(!proAlive())return;play(s.items,function(){',
    'var go=function(){if(!proAlive())return;Promise.resolve(window.__innPresentationWait?window.__innPresentationWait():true).then(function(ready){if(ready&&proAlive())play(s.items,function(){')
rep('else runPro(i+1)})};', 'else runPro(i+1)})})};')
rep('setTimeout(step,it.dir.ms!=null?it.dir.ms:420);return}',
    'setTimeout(function(){Promise.resolve(window.__innPresentationWait?window.__innPresentationWait():true).then(function(ready){if(ready)step()})},it.dir.ms!=null?it.dir.ms:420);return}')
# A failed primary picture must be recoverable even while its place card is
# active or a previous banner's tap tail is being swallowed. Exempt only this
# recovery control, leaving investigation/dialogue protections unchanged.
rep('window.addEventListener(t,function(e){if(!e.isTrusted)return;var o=blocker();',
    'window.addEventListener(t,function(e){if(!e.isTrusted)return;if(e.target&&e.target.closest&&e.target.closest("#inn-story-cg .cinema-retry"))return;var o=blocker();')
