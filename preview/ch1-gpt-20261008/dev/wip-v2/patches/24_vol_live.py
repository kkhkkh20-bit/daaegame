# 설정 음량: 배경음·효과음 모두 밀면 바로 들리게(실시간). 저장하면 그대로 유지, 취소/닫기면 저장값으로 되돌림(기존 shut)
rep('if(k==="musicVolume")gains({musicVolume:W.musicVolume,sfxVolume:SET.sfxVolume})});',
    'gains({musicVolume:W.musicVolume,sfxVolume:W.sfxVolume});if(k==="sfxVolume"){var _n=Date.now();if(!r.__lt||_n-r.__lt>160){r.__lt=_n;try{ac();SFX.select()}catch(e){}}}});')
rep('r.addEventListener("change",function(){if(k==="sfxVolume"&&W.sfxVolume>0){try{ac();gains({musicVolume:W.musicVolume,sfxVolume:W.sfxVolume});SFX.select();setTimeout(function(){gains({musicVolume:W.musicVolume,sfxVolume:SET.sfxVolume})},350)}catch(e){}}})});',
    'r.addEventListener("change",function(){try{ac();gains({musicVolume:W.musicVolume,sfxVolume:W.sfxVolume})}catch(e){}})});')
