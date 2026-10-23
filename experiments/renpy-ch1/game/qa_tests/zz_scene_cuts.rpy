# 0.20.7: picture cuts (record pictures held up, the reunion two-shot) inside a real line.
label qa_cut_demo:
    call r13_scene(R13_PLACES["greenhouse"][1],R13_PLACES["greenhouse"][0],"calm")
    call r13_lines([(None,"다람은 입구에서 멈춘다. 아빠가 옆으로 비켜도 움직이지 않는다.",dict(cut="v111_reunion_far"))],"qa:cut1")
    call r13_lines([(None,"다람이 두 손으로 엄마의 외투를 잡는다.",dict(cut="v111_reunion_close"))],"qa:cut2")
    call r13_lines([("daram","이 그림 가져왔네! 이것 봐, 나 팔 세 개 그린 거.",dict(cut="ev:D01_FAMILY_DRAWING",expression="joy",pose="joy"))],"qa:cut3")
    call r13_lines([(None,"끝.",dict(cut=""))],"qa:cut4")
    return
testcase scene_cuts:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Call("qa_cut_demo")
    pause 1.5
    screenshot "cut-01-reunion-far.png"
    click pos (640,600)
    pause 1.5
    screenshot "cut-02-reunion-close.png"
    click pos (640,600)
    pause 1.5
    screenshot "cut-03-family-drawing.png"
