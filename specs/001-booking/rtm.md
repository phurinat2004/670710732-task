# RTM: จองคิวตรวจสุขภาพ (Booking)
อ้างอิง: spec.md Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2569-10-07 08:35 | test: 6 ผ่าน 1 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | AC-BKG-05 | T-02 | backend/app/slots/service.py: list_available_slots; backend/app/slots/router.py: get_slots | backend/tests/test_AC_BKG_05.py: PASS | ช่องโหว่ |
| FR-BKG-02 | AC-BKG-02 | T-04 | ไม่พบโค้ดจริงที่ปฏิเสธการจองซ้ำวันเดียวกัน | ไม่มี test ในโค้ด | ยังไม่ถึง |
| FR-BKG-03 | AC-BKG-03 | T-05, T-11, T-12 | ไม่พบโค้ดที่แสดง 3 ตัวเลือกเมื่อช่วงเต็ม | ไม่มี test ในโค้ด | ยังไม่ถึง |
| FR-BKG-04 | AC-BKG-01 | T-03, T-06 | backend/app/booking/service.py: create_booking; backend/app/booking/router.py: create_booking | backend/tests/test_AC_BKG_01.py: 3 ผ่าน, 1 ไม่ผ่าน | ช่องโหว่ |
| FR-BKG-05 | AC-BKG-04 | T-07 | ไม่พบโค้ดคิวส่งข้อความและส่งซ้ำ | ไม่มี test ในโค้ด | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC | T-10 | backend/app/slots/service.py: list_available_slots; backend/app/slots/router.py: get_slots | ไม่มี test ในโค้ด | ช่องโหว่ |
| NFR-PERF-01 | AC-BKG-05 | T-02 | backend/app/slots/service.py: list_available_slots | backend/tests/test_AC_BKG_05.py: PASS | ครบ |
| NFR-SEC-01 | ไม่มี AC | ไม่มี task | ไม่มีโค้ดที่บังคับ TLS 1.2 และการเข้ารหัสข้อมูลรับส่ง | ไม่มี test | ยังไม่ถึง |
| NFR-REL-02 | AC-BKG-04 | T-07 | ไม่มีโค้ดคิวส่งซ้ำตาม 5 นาที | ไม่มี test ในโค้ด | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC | ไม่มี task | ไม่มีโค้ดและไม่มี test สำหรับผู้ใช้ใหม่ 8/10 คนใน 3 นาที | ไม่มี test | ยังไม่ถึง |
| CON-TECH-01 | ไม่มี AC | T-01 | backend/app/config.py: DATABASE_URL; backend/app/db/session.py: engine; backend/app/db/migrations/001_init.py: upgrade | backend/tests/test_T01_schema.py: PASS | ครบ |
| DOM-PDPA-01 | AC-BKG-06 | T-08 | backend/app/db/models.py: AuditLog; ไม่มี middleware หรือ endpoint ที่บันทึก audit log จริง | ไม่มี test ในโค้ด | ยังไม่ถึง |
| IF-IDP-01 | AC-BKG-01 | T-03 | backend/app/auth/idp.py: get_verified_hn | backend/tests/test_AC_BKG_01.py: PASS (verified flow) | ครบ |
| IF-HIS-01 | ไม่มี AC | T-09 | backend/app/db/models.py: Booking เก็บเฉพาะ hn; ไม่มี client HIS จริง | backend/tests/test_T01_schema.py: PASS (ไม่เก็บ national_id) | ยังไม่ถึง |
| IF-NOT-01 | AC-BKG-04 | T-07 | ไม่มีคิวส่งข้อความ asynchronous จริง | ไม่มี test ในโค้ด | ยังไม่ถึง |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| backend/app/slots/service.py: list_available_slots | FR-BKG-01, FR-BKG-06 | ไม่ตรง | แสดงเฉพาะ 14 วัน (`DAYS_AHEAD = 14`) ไม่ตรงกับ FR-BKG-01 ที่กำหนดเป็น 30 วันข้างหน้า |
| backend/app/booking/service.py: create_booking | FR-BKG-04, FR-BKG-03 | ไม่ตรง | ตรวจ `slot.remaining < 0` เท่านั้น จึงยอมจองเมื่อ `remaining == 0` ทำให้ช่องเต็มยังผ่านได้ |
| backend/app/booking/router.py: BookingRequest | IF-HIS-01, DOM-PDPA-01 | ไม่ตรง | มี field `national_id` และ log `national_id` ใน request แม้ spec ระบุไม่เก็บเลขบัตรประชาชนในตารางการจองและต้องปกป้องข้อมูลสุขภาพ |
| backend/app/auth/idp.py: get_verified_hn | IF-IDP-01 | ตรง | ตรวจ Header `Authorization` แบบ `Bearer verified:<HN>` ก่อนให้เข้าถึงข้อมูลผู้รับบริการ |
| backend/app/db/models.py: Slot, Booking, AuditLog | CON-TECH-01, DOM-PDPA-01, IF-HIS-01 | ส่วนหนึ่งตรง | ตารางมี `hn` แต่ไม่มี `national_id`; อย่างไรก็ตาม ไม่มี middleware จริงที่บันทึก audit log ทุกการเข้าถึง |
| backend/app/config.py: DATABASE_URL | CON-TECH-01 | ตรง | อ่าน `DATABASE_URL` และให้ค่าเริ่มต้น SQLite สำหรับ Codespace แต่ spec บังคับ PostgreSQL ในระบบจริง |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-001 | ตัวเลขไม่ตรง spec / ช่องโหว่ | backend/app/booking/service.py: create_booking | FR-BKG-04, FR-BKG-03 | โค้ดตรวจ `slot.remaining < 0` แต่ต้องปฏิเสธเมื่อว่างเหลือ 0 แล้ว จากการรัน `pytest -v` test_TC_BKG_01_3_rejects_unverified_or_full_slot ไม่ผ่านเพราะ status กลับเป็น 201 แทน 409 |  |
| F-002 | ตัวเลขไม่ตรง spec | backend/app/slots/service.py: list_available_slots | FR-BKG-01 | ตัวเลข `DAYS_AHEAD = 14` ทำให้ระบบแสดงได้เฉพาะ 14 วัน ขณะที่ spec ระบุภายใน 30 วันข้างหน้า |  |
| F-003 | ละเมิด Constraint | backend/app/booking/router.py: BookingRequest; backend/app/booking/router.py: create_booking | IF-HIS-01, DOM-PDPA-01 | มี field `national_id` และ log `national_id` ใน request แม้ spec ระบุให้ไม่เก็บเลขบัตรประชาชนในตารางการจองและไม่ควรส่ง/บันทึกต่อข้อมูลที่ห้ามเก็บ |  |
| F-004 | FR ไม่มี AC | specs/001-booking/spec.md | FR-BKG-06 | FR-BKG-06 มีใน requirement แต่ไม่มี AC ที่ตรวจสิ่งนี้ใน spec หรือ test-cases.md จึงเป็นช่องโหว่ของ requirement ที่ต้องทีมตัดสินใจเพิ่ม AC ก่อนใช้เป็นเกณฑ์ยอมรับ |  |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
| - | - | ยังไม่มีข้อค้นพบที่ทีมแก้แล้วในรอบนี้ |
