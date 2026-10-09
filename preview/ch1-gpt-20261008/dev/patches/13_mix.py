# 음량(2026-10-09 "효과음·배경음이 너무 작다"): 오프라인 측정으로 대화 중 여행곡 RMS가 약 -34dBFS(음량 70%·대화 덕킹 포함)였다.
# 음악 버스 +3.9dB(MBASE .16→.25), 효과음 버스 +3.1dB(.42→.6). 마스터 컴프레서(-16dB 문턱)는 그대로 두어 클리핑을 막는다.
rep('MBASE=.16','MBASE=.25')
rep('SFXG=AC.createGain();SFXG.gain.value=.42;','SFXG=AC.createGain();SFXG.gain.value=.6;')
rep('SFXG.gain.setTargetAtTime(.42*SFXV,AC.currentTime,.05)','SFXG.gain.setTargetAtTime(.6*SFXV,AC.currentTime,.05)')
rep('SFXG.gain.value=.42*o.sfxVolume/100','SFXG.gain.value=.6*o.sfxVolume/100')
rep('try{SFXG.gain.value=.42*SFXV}catch(e){}}','try{SFXG.gain.value=.6*SFXV}catch(e){}}')
