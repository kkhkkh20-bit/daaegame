# 머리판을 건너뛰고 상자를 누른 경우에도 허락을 받은 뒤 잠금 입력을 연다.
rep('function lockPad(){var K=EP.LOCK;',
    '''function lockPad(){var K=EP.LOCK;
  if(K.permission&&!bt("inn_ledger_permission")){say(K.permission.map(function(x){return x.slice()}),function(){setb("inn_ledger_permission");lockPad()});return}''')
