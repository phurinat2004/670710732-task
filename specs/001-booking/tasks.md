Feature: จองคิวตรวจสุขภาพ (Booking)
Spec ID: SPEC-BKG-001
อ้างอิง: plan.md
วันที่: 2569-09-23

สรุป: แยกงานเป็น 15 tasks; มี 2 task ที่รอคำตอบใน Open Questions

### T-01 สร้างตารางและ migration
- รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-02
- ไฟล์ที่แตะ: backend/app/db/models.py, backend/app/db/migrations/001_init.py
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: ฟังก์ชัน migration `upgrade(engine)` สร้างตาราง `slots`, `bookings`, `audit_logs` ได้สำเร็จ
- สถานะ: พร้อมทำ
- สถานะ: เสร็จ รอทีมตรวจ

### T-02 พัฒนา GET /slots และการคำนวณช่วงว่าง
- รองรับ: FR-BKG-01, FR-BKG-06, NFR-PERF-01
- ตรวจด้วย: AC-BKG-05
- ไฟล์ที่แตะ: backend/app/slots/router.py, backend/app/slots/service.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: `test_AC_BKG_05` (โหลด /slots และวัด p95 แบบย่อส่วน) รันได้
- สถานะ: พร้อมทำ

### T-03 พัฒนา POST /bookings พื้นฐาน (บันทึกการจองและตัดที่นั่ง)
- รองรับ: FR-BKG-04
- ตรวจด้วย: AC-BKG-01
- ไฟล์ที่แตะ: backend/app/booking/router.py, backend/app/booking/service.py, backend/app/db/session.py
- ต้องทำหลัง: T-01, T-02
- เสร็จเมื่อ: `test_AC_BKG_01` ผ่าน (บันทึกการจองและลด remaining เป็น 0)
- สถานะ: พร้อมทำ

### T-04 ป้องกันการจองซ้ำในวันเดียวกัน
- รองรับ: FR-BKG-02
- ตรวจด้วย: AC-BKG-02
- ไฟล์ที่แตะ: backend/app/booking/service.py, backend/app/booking/router.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: `test_AC_BKG_02` ผ่าน (ขอจองซ้ำได้รับ 409 หรือปฏิเสธพร้อมหมายเลขคิวเดิม)
- สถานะ: พร้อมทำ

### T-05 เสนอช่วงใกล้เคียงเมื่อช่วงที่เลือกเต็ม (หา 3 ตัวเลือก)
- รองรับ: FR-BKG-03
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: backend/app/booking/service.py, backend/app/slots/service.py
- ต้องทำหลัง: T-02, T-03
- เสร็จเมื่อ: `test_AC_BKG_03` ผ่าน (POST /bookings ส่งคืน 409 พร้อม 3 ช่วงที่ใกล้ที่สุด)
- สถานะ: พร้อมทำ

### T-06 วางงานส่งข้อความลงคิวและการส่งซ้ำ (retry ตาม ASM-03)
- รองรับ: FR-BKG-05, IF-NOT-01, NFR-REL-02, ASM-03
- ตรวจด้วย: AC-BKG-04
- ไฟล์ที่แตะ: backend/app/notify/queue.py, backend/app/booking/service.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: `test_AC_BKG_04` ผ่าน (การจองถูกบันทึกแม้ sender ไม่ตอบ และมีงานในคิวกำหนดส่งซ้ำภายใน 5 นาที)
- สถานะ: พร้อมทำ

### T-07 ติดตั้ง audit log middleware และบันทึกการเข้าถึง
- รองรับ: DOM-PDPA-01
- ตรวจด้วย: AC-BKG-06
- ไฟล์ที่แตะ: backend/app/audit/middleware.py, backend/app/db/models.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: `test_AC_BKG_06` ผ่าน (การเข้าถึงการจองสร้าง `audit_logs` ที่ระบุ actor_id, accessed_at, hn)
- สถานะ: พร้อมทำ

### T-08 พัฒนา client สำหรับค้น HN จาก HIS (ไม่เก็บ national_id)
- รองรับ: IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-03
- ไฟล์ที่แตะ: backend/app/his/client.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: ฟังก์ชัน `lookup_by_national_id()` คืนค่า `hn` และ unit test ครอบคลุม
- สถานะ: พร้อมทำ

### T-09 เขียน test จำลองการส่งข้อความไม่สำเร็จและ retry
- รองรับ: NFR-REL-02, FR-BKG-05
- ตรวจด้วย: AC-BKG-04
- ไฟล์ที่แตะ: backend/tests/test_notify_retry.py, backend/app/notify/queue.py
- ต้องทำหลัง: T-06
- เสร็จเมื่อ: test_notify_retry ที่ตรวจเวลาส่งซ้ำภายใน 5 นาทีผ่าน
- สถานะ: พร้อมทำ

### T-10 สร้างหน้า SlotPicker (frontend) ใช้ API จำลอง
- รองรับ: FR-BKG-01, FR-BKG-06
- ตรวจด้วย: ไม่มี AC ตรง ๆ (เป็นหน้าจอพื้นฐาน)
- ไฟล์ที่แตะ: frontend/src/pages/SlotPicker.jsx, frontend/src/api/client.js
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: หน้าจอโหลดรายการช่วงเวลาโดยใช้ API จำลอง (Vitest) ได้
- สถานะ: พร้อมทำ

### T-11 สร้างหน้า ConfirmBooking (frontend) แสดงสถานะ "ช่วงเวลาเต็ม" และ 3 ตัวเลือก
- รองรับ: FR-BKG-03, FR-BKG-04
- ตรวจด้วย: AC-BKG-03 (ไฟล์ทดสอบ: frontend/__tests__/AC-BKG-03.test.jsx)
- ไฟล์ที่แตะ: frontend/src/pages/ConfirmBooking.jsx, frontend/__tests__/AC-BKG-03.test.jsx
- ต้องทำหลัง: T-10
- เสร็จเมื่อ: หน้าจอแสดงข้อความ "ช่วงเวลาเต็ม" และปุ่ม 3 ตัวเลือก เมื่อ API จำลองคืน 409
- สถานะ: พร้อมทำ

### T-12 สร้างหน้า BookingResult (frontend) แสดงหมายเลขคิว แม้ส่งข้อความไม่สำเร็จ
- รองรับ: FR-BKG-04, FR-BKG-05
- ตรวจด้วย: AC-BKG-01, AC-BKG-04
- ไฟล์ที่แตะ: frontend/src/pages/BookingResult.jsx, frontend/__tests__/AC-BKG-01.test.jsx, frontend/__tests__/AC-BKG-04.test.jsx
- ต้องทำหลัง: T-11, T-06
- เสร็จเมื่อ: หน้าจอแสดงหมายเลขคิวจาก API แม้ระบบแจ้งเตือนไม่ตอบ
- สถานะ: รอ Q-02

### T-13 ต่อหน้าจอกับ API จริง (frontend ↔ backend integration)
- รองรับ: FR-BKG-01, FR-BKG-03, FR-BKG-04
- ตรวจด้วย: ไม่มี AC ตรง ๆ (เป็นงานรวมระบบเพื่อสาธิตและตรวจความถูกต้อง)
- ไฟล์ที่แตะ: frontend/src/*, backend/app/*
- ต้องทำหลัง: T-02, T-03, T-11
- เสร็จเมื่อ: หน้า SlotPicker → ConfirmBooking → BookingResult ทำงาน end-to-end ใน dev environment
- สถานะ: รอ Q-02

### T-14 เขียน backend unit tests สำหรับทุก AC (1 ไฟล์ต่อ 1 AC)
- รองรับ: AC-BKG-01, AC-BKG-02, AC-BKG-03, AC-BKG-04, AC-BKG-05, AC-BKG-06
- ตรวจด้วย: ทุก AC ถูกครอบคลุมโดย test ที่ชื่อ `test_AC_BKG_*.py`
- ไฟล์ที่แตะ: backend/tests/test_AC_BKG_01.py ... test_AC_BKG_06.py
- ต้องทำหลัง: งานที่เกี่ยวข้องแต่ละ AC (T-02..T-09, T-07)
- เสร็จเมื่อ: pytest รันผ่านสำหรับ test ทั้งหมดที่ตรวจ AC เหล่านี้ (บน SQLite in-memory)
- สถานะ: พร้อมทำ

### T-15 ปรับปรุงเอกสารและตาราง traceability
- รองรับ: Traceability ใน spec
- ตรวจด้วย: ไม่มี AC ตรง ๆ
- ไฟล์ที่แตะ: specs/001-booking/tasks.md (ไฟล์นี้), specs/001-booking/plan.md, specs/001-booking/spec.md
- ต้องทำหลัง: T-01..T-14
- เสร็จเมื่อ: ตารางตรวจ AC/Constraint ครบถ้วนในไฟล์นี้
- สถานะ: พร้อมทำ


## ตารางตรวจความครบ

1) ตาราง AC → task

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-BKG-01 | T-03, T-12 |
| AC-BKG-02 | T-04 |
| AC-BKG-03 | T-05, T-11 |
| AC-BKG-04 | T-06, T-09, T-12 |
| AC-BKG-05 | T-02 |
| AC-BKG-06 | T-07 |

2) ตาราง Constraint → task

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| CON-TECH-01 | T-01, T-15 |
| DOM-PDPA-01 | T-01, T-07 |
| IF-IDP-01 | (ตรวจที่ทุก endpoint) - หมายเหตุ: จำเป็นต้องมี task integration | T-03, T-13 |
| IF-HIS-01 | T-01, T-08 |
| IF-NOT-01 | T-06, T-09 |


## สิ่งที่ยังไม่ทำ (Open Questions)
- Q-02: รูปแบบหมายเลขคิว (รีเซ็ตรายวัน หรือ นับต่อเนื่อง และรูปแบบเช่น A001 หรือไม่)
  - แสดงผล: งานที่รอ Q-02 — T-12 (แสดงหมายเลขคิว) และ T-13 (integration ที่แสดง queue_no)
