# Official-engine fixture prepared only. Not run locally, no gameplay-progression claim.
testcase recommended_canonical_cloth_and_contact:
    pause 2.0
    run Call("r13_recommended_art_admin")
    assert screen "r13_rec_cloth_comparison"
    screenshot "recommended-cloth-separated-alpha.png"
    click "조각을 옮긴다"
    click "조각을 옮긴다"
    screenshot "recommended-cloth-matched-alpha.png"
    click "두 줄과 가장자리가 이어진다"
    assert screen "r13_rec_piko_contact_sequence"
    screenshot "recommended-lamp-open.png"
    click "다음 장면"
    screenshot "recommended-lamp-grip.png"
    click "다음 장면"
    screenshot "recommended-lamp-contact.png"
    click pos (760,288)
    click "다음 장면"
    screenshot "recommended-lamp-lifted.png"
    click "다음 장면"
    screenshot "recommended-lamp-container.png"
    click "다음 장면"
    screenshot "recommended-lamp-covered-fitting.png"
    click "구조 확인을 마친다"
    assert eval (not r13_rec_piko_contact_art_verified)
    assert eval (not r13_rec_e3_geometry_art_verified)
    $ r13_qa_note("Actual screen-only alpha/contact inspection. Neither native approval nor gameplay fact is awarded by this fixture.")

testcase recommended_isolated_native_gate_entry:
    pause 2.0
    run Call("r13_recommended_native_qa_start")
    click "돌아가기"
    click "QA 전용 상태로 새로 시작한다"
    pause 1.0
    assert eval (r13_recommended.get("qa_fixture")=="native_geometry_probe_v1")
    assert eval (r13_rec_piko_geometry_ready(r13_recommended) and r13_rec_e3_geometry_ready(r13_recommended))
    assert eval (not r13_rec_piko_contact_art_verified and not r13_rec_e3_geometry_art_verified)
    screenshot "recommended-isolated-qa-entry.png"
