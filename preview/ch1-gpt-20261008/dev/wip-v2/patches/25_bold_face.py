# 증언 글씨가 번져 보이던 문제: Galmuri11B(이미 굵은 글꼴)를 font-weight:700으로 부르면 브라우저가 한 번 더 가짜 굵게(합성)를 입혀 획이 뭉개진다. 글꼴 선언에 굵기 범위를 주어 합성을 막는다
rep('font-family:"Galmuri11B";src:','font-family:"Galmuri11B";font-weight:100 900;src:')
