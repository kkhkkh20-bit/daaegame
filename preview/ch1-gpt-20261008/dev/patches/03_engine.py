# 콜드 오픈 → 마차 전환: 첫 줄이 아빠 속마음(인물 없음)이어도 배경이 준비되면 암전을 걷는다
rep('if(!bgReady||!im||!im.complete||!im.naturalWidth||!scene||scene.key!=="carriage"){revealFrame=requestAnimationFrame(reveal);return}','if(!bgReady||!scene||scene.key!=="carriage"){revealFrame=requestAnimationFrame(reveal);return}')
