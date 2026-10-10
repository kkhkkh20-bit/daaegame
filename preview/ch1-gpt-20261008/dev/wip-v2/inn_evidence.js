/* Keep the extra snow observation in the authored witness card. UI changes
   must not turn an unasked observation into a fact or erase it on a reload. */
(function(){
 function snow(){var b=G&&G.beats||{};return !!(b.inn_show_geokkuri_C08||b.inn_snowWitness||b.inn_c13fix)}
 var x=window.EP1INN&&window.EP1INN.EV.C13;if(!x)return;
 ['desc','card','detail','desc2','card2','detail2'].forEach(function(k){var base=x[k];if(!base)return;Object.defineProperty(x,k,{enumerable:true,configurable:true,get:function(){return base+(snow()?' 추가 관찰: 그 사람이 지나갈 때 창밖에 올해 첫눈이 막 내리기 시작했다.':'')}})});
})();
