# User requested the new Drive Neoul and ceiling-hanging Bami on every surface.
# Shared runtime crops keep dialogue, record faces and council emotions aligned.
rep('function figHtml(k,m){if(G&&CASES[G.ci]&&CASES[G.ci].id==="inn"&&k==="innma"',
    '''function figHtml(k,m){if(G&&CASES[G.ci]&&CASES[G.ci].id==="inn"){var crop=window.__innCropSvg&&window.__innCropSvg(k,m,"sf innpixel");if(crop)return crop;if(k==="geokkuri")return '<img alt="" class="sf innpixel hanging-bami" draggable="false" src="art/ch1/action-poses/bami/dialogue.png">'}if(G&&CASES[G.ci]&&CASES[G.ci].id==="inn"&&k==="innma"''')
# An SVG crop also needs to change when the actual council line's mood changes.
# Replace only the actor child, keeping the native seat and input nodes intact.
rep('''var want=figHtml(k,m),im=s.querySelector("img"),src=(want.match(/src="([^"]+)"/)||[])[1];if(im&&src&&im.getAttribute("src")!==src)im.setAttribute("src",src);''',
    '''var want=figHtml(k,m);if(s.__artHtml!==want){var holder=document.createElement("div");holder.innerHTML=want;var art=s.firstElementChild;if(art&&holder.firstElementChild)art.replaceWith(holder.firstElementChild);s.__artHtml=want;}''')
