# Replace the very first loader, before engine skins exist, with the same
# source used by the v2 wrapper. Keep the native readiness/removal contract.
a=s.index('<div id="bootld" ')
b=s.index('</div></div>',a)+len('</div></div>')
boot_css=(SOURCE/'boot_theme.css').read_text(encoding='utf-8')
boot_markup=(SOURCE/'boot_theme.html').read_text(encoding='utf-8')
s=s[:a]+'<style id="inn-boot-theme">'+boot_css+'</style><div id="bootld">'+boot_markup+'</div><script>try{if(parent!==window)parent.postMessage({type:"inn-v2-boot-ready"},location.origin)}catch(e){}</script>'+s[b:]
# Galmuri is already embedded in this payload. External font services should
# not hold its load event or introduce another font during a cold start.
rep('<link rel="preconnect" href="https://fonts.googleapis.com">\n','')
rep('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n','')
rep('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jua&family=Gowun+Dodum&family=Gaegu:wght@400;700&display=swap">\n','')
