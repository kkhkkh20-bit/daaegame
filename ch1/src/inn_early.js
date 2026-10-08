/* v210 가로 시험본(wide.html) 전용 · 게임 코드보다 먼저 실행
   1) 저장 격리: 이 페이지의 localStorage 읽기/쓰기는 모두 "daae-wide209:" 접두어 키로만 간다.
      기본 게임 저장(daae-detective-v3 등)은 읽지도 쓰지도 않는다. 예외: 도트 그림 캐시(dc1:)는 진행과 무관해 같은 키를 쓴다.
   2) 클라우드 동기화 끔: window.claude를 비워 동기화 모듈이 연결하지 않게 한다.
   격리에 실패하면 window.__W209SAFE=false가 되고, 뒤 모듈이 저장 함수를 막고 시험을 멈춘다. */
(function(){
 window.__W209=true;window.__W209SAFE=false;
 var P="daae-inn1:";window.__EP1INN=true;
 try{
  var R=window.localStorage;
  function k(x){x=String(x);return x.indexOf("dc1:")===0?x:P+x}
  function mine(){var a=[];for(var i=0;i<R.length;i++){var x=R.key(i);if(x&&x.indexOf(P)===0)a.push(x.slice(P.length))}return a}
  var shim={
   getItem:function(x){return R.getItem(k(x))},
   setItem:function(x,v){R.setItem(k(x),String(v))},
   removeItem:function(x){R.removeItem(k(x))},
   key:function(i){return mine()[i]||null},
   clear:function(){mine().forEach(function(x){R.removeItem(P+x)})}
  };
  Object.defineProperty(shim,"length",{get:function(){return mine().length}});
  Object.defineProperty(window,"localStorage",{value:shim,configurable:true,writable:false});
  window.__W209SAFE=(window.localStorage===shim);
  window.__W209REAL=R;window.__W209P=P;
 }catch(e){window.__W209SAFE=false}
 try{Object.defineProperty(window,"claude",{value:null,configurable:true,writable:false})}catch(e){}
})();
