# 메인 화면 음악(2026-10-10 사용자 보고): 엔진은 첫 제스처 전에는 AudioContext를 만들지 않는다(자동재생 정책). 브라우저가 정책을 알려 주고
# 'allowed'라고 답하거나, 메인 화면에서 만든 시험용 AudioContext가 곧바로 running이면(window.__innAutoOK, inn_audio) 그 환경(navigator.getAutoplayPolicy 지원)에서만 제스처 없이 시작한다. 정책을 우회하지 않으며, iOS Safari처럼 알려 주지 않는 곳은 첫 터치 때 시작(inn_audio 안내 단추).
rep(' function hasGest(){if(GEST)return true;try{if(navigator.userActivation&&navigator.userActivation.hasBeenActive)return true}catch(e){}return false}',
    ' function hasGest(){if(GEST)return true;try{if(navigator.userActivation&&navigator.userActivation.hasBeenActive)return true}catch(e){}if(window.__innAutoOK)return true;try{if(navigator.getAutoplayPolicy&&navigator.getAutoplayPolicy("audiocontext")==="allowed")return true}catch(e){}return false}')
# 더보기 '메인으로'가 대사 중에는 아무 반응 없이 무시되던 것: 대사 중에도 저장 후 메인 화면으로(저장은 장면 시작 단위라 같은 장면 처음부터 이어짐).
# 메인 화면 복귀는 페이지 다시 읽기라 iOS에서는 소리 허락이 다시 필요할 수 있다 → 메인 화면의 '소리 켜기' 안내로 이어진다
rep(' window.__innReturnMain=function(){if(typeof DL!=="undefined"&&DL)return;saveProg();location.reload()};',
    ' window.__innReturnMain=function(){try{saveProg()}catch(e){}location.reload()};')
