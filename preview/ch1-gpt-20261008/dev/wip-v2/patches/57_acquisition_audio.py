# The acquisition card owns its sound for dialogue, grant and discovery paths.
# Native scene cards and grants without a card keep their original sound.
rep('function gotCard(id,done){var e=EVO[id],m=EP.MEMO[id];if(!e){done&&done();return}',
    'function gotCard(id,done){var e=EVO[id],m=EP.MEMO[id];if(!e){done&&done();return}try{SFX.found()}catch(e){}')
rep('if(it.grant){if(G.found.indexOf(it.grant)<0)G.found.push(it.grant);try{SFX.found()}catch(e){}',
    'if(it.grant){if(G.found.indexOf(it.grant)<0)G.found.push(it.grant);if(!it.card)try{SFX.found()}catch(e){}')
