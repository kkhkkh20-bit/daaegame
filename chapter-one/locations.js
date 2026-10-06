/* Each entry is a separate room; panorama offsets are local to that room. */
const ROOMS=[
 {id:'reception',name:'산장 접수대',asset:'reception-pixel',purpose:'봉투가 전달된 자리',people:['karo'],spots:[{id:'receipt',x:.15,y:.53,w:.14,h:.11},{id:'tray',x:.565,y:.558,w:.15,h:.105}],observations:[{id:'window',x:.28,y:.25,w:.15,h:.3,title:'눈 덮인 창밖',text:'발자국도 눈 속에 파묻혔다. 밖의 흔적만으로 누가 왔는지 정하긴 어렵다.',memo:'눈은 발자국을 지우고 나는 메모를 한다. 오늘은 내가 이길 예정.'}]},
 {id:'lounge',name:'손님 휴게실',asset:'room-lounge',purpose:'까로가 기다리던 곳',people:['karo'],spots:[{id:'clock',x:.52,y:.23,w:.16,h:.23}],observations:[{id:'fireplace',x:.2,y:.48,w:.22,h:.3,title:'따뜻한 벽난로',text:'장작불이 타고 있다. 까로는 이곳에서 젖은 날개를 말렸다고 했다.',memo:'깃털 말리기에는 딱이다. 내 간식 굽기에도… 사건 끝나고.'}]},
 {id:'cabinet',name:'접수 담당자 관리실',asset:'room-office',purpose:'예비 열쇠와 잠긴 보관함',people:['mungchi'],spots:[{id:'cabinet',x:.73,y:.42,w:.24,h:.49}],observations:[{id:'ledger',x:.215,y:.5,w:.2,h:.12,title:'업무 책상',text:'접수 담당자가 쓰는 책상이다. 장부는 있지만 주민에게 돈을 지급했다는 확인은 찾을 수 없다.',memo:'정리된 책상은 수상하지 않다. 내 책상이랑 너무 달라서 부러울 뿐.'}]},
 {id:'archive',name:'문서 보관실',asset:'room-archive',purpose:'회수한 봉투와 두 문서 대조',people:[],spots:[{id:'envelope',x:.275,y:.68,w:.17,h:.16},{id:'roster',x:.49,y:.66,w:.17,h:.19},{id:'report',x:.755,y:.67,w:.29,h:.18}],observations:[]}
];
