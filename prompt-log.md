# Prompt log

บันทึกทุกครั้งที่ใช้ AI กับ repo นี้ เขียนต่อท้ายเรื่อย ๆ ไม่ลบของเก่า

---

## 2569-09-23 13.40 คำสั่ง: /tasks specs/001-booking/spec.md

- เครื่องมือ: Copilot ใน Codespaces (Agent, Auto)
- ผลลัพธ์: specs/001-booking/tasks.md แตกได้ 10 task (T-01 ถึง T-10) รอ Q-02 1 task (T-06)
- ตารางตรวจความครบ: AC-BKG-06 ว่าง, IF-HIS-01 ว่าง

### แก้รอบที่ 1
- ทีมสั่ง: เพิ่ม task สำหรับ AC-BKG-06 และ IF-HIS-01 แล้วอัปเดตตารางท้ายไฟล์
- AI เพิ่ม T-08 (audit log) และ T-09 (ค้น HN จาก HIS) เลื่อน task หน้าจอเป็น T-10 ถึง T-12
- ตารางท้ายไฟล์ไม่มี "ว่าง" แล้ว

---

## 2569-09-23 14.20 คำสั่ง: /implement T-01 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/config.py, backend/app/db/models.py, backend/app/db/session.py, backend/app/db/migrations/001_init.py, backend/tests/test_T01_schema.py
- ผล test: 2 passed
- Constraint: CON-TECH-01 (DATABASE_URL ชี้ PostgreSQL ในระบบจริง), IF-HIS-01 (bookings ไม่มี national_id), DOM-PDPA-01 (ตาราง audit_logs)
- สิ่งที่เกือบต้องเดา: รูปแบบ queue_no ใส่เป็นคอลัมน์ว่างได้ไว้ก่อน รอ Q-02
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-27 19.05 คำสั่ง: /implement T-02 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/slots/router.py, backend/app/slots/service.py, backend/app/main.py, backend/tests/conftest.py, backend/tests/test_AC_BKG_05.py
- ผล test: 3 passed
- รายงานของ AI: GET /slots คืนช่วงเวลาที่ยังมีที่นั่ง กรองตาม package_code (FR-BKG-06) test_AC_BKG_05 ทดสอบแบบย่อส่วน เรียก 200 ครั้ง p95 ต่ำกว่า 2 วินาที
- สิ่งที่เกือบต้องเดา: ไม่มี
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-28 20.30 คำสั่ง: /implement T-03 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/booking/router.py, backend/app/booking/service.py, backend/app/auth/idp.py และแก้ backend/app/main.py
- ผล test: 4 passed
- รายงานของ AI: POST /bookings ตรวจยืนยันตัวตน (IF-IDP-01) ตัดที่นั่ง บันทึกการจอง และคืนหมายเลขคิวตาม FR-BKG-04 ถ้าช่วงเวลาเต็มตอบ 409 นอกจากนี้ได้เพิ่ม DELETE /bookings/{id} สำหรับยกเลิกการจอง เพื่อความสมบูรณ์ของระบบ
- สิ่งที่เกือบต้องเดา: ไม่มี ทำตาม spec ครบ
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2026-10-07 00.00 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/

- โหมด: ร่าง (AC ยังไม่มีแถวสถานะ "ใช้ได้" ใน test-cases.md)
- TC ID ที่เสนอ: TC-BKG-01-1, TC-BKG-01-2, TC-BKG-01-3
- ผล: หยุดที่ชั้นเสนอ test case ร่าง ไม่เขียนโค้ด test ตามคำสั่งของ prompt เพราะยังไม่มีแถว "ใช้ได้" สำหรับ AC นี้
- หมายเหตุ: spec บอกให้มีหมายเลขคิวตาม Q-02 ยังไม่มีคำตอบ จึงติด (รอ Q-xx) ใน Then ของทุกแถว

---

## 2026-10-07 00.45 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/

- โหมด: เขียน test (มีแถวสถานะ "ใช้ได้" ใน test-cases.md แล้ว)
- TC ID ที่เขียน test: TC-BKG-01-1, TC-BKG-01-2, TC-BKG-01-3
- ไฟล์ที่แก้: backend/tests/test_AC_BKG_01.py
- ผลการรัน: `cd backend && pytest -v tests/test_AC_BKG_01.py`
  - test_AC_BKG_01: ผ่าน
  - test_TC_BKG_01_1_successful_booking: ผ่าน
  - test_TC_BKG_01_2_last_seat_booking: ผ่าน
  - test_TC_BKG_01_3_rejects_unverified_or_full_slot: ไม่ผ่าน
- กรณีที่ไม่ผ่าน: โค้ดทำไม่ตรง AC (เจอบั๊ก)
  - สาเหตุ: [backend/app/booking/service.py](backend/app/booking/service.py#L21-L36) ตรวจว่า `slot.remaining < 0` แทนที่จะป้องกัน `slot.remaining <= 0`
  - ผล: การจองเมื่อ slot.remaining = 0 ยังได้ status 201 แทนที่จะต้อง 409 ตาม AC-BKG-01 และ FR-BKG-03
- ข้อสรุป: หยุดที่จุดนี้ตามข้อบังคับของ prompt ว่าเมื่อ test ใหม่ไม่ผ่านเพราะโค้ดผิด ต้องระบุว่าเป็นกรณีโค้ดทำไม่ตรง AC แล้วหยุด

---

## 2026-10-07 08:35 คำสั่ง: /verify specs/001-booking/

- โหมด: ตรวจ requirement / RTM
- ผล test: `cd backend && pytest -v` -> 6 ผ่าน 1 ไม่ผ่าน; `cd frontend && npm test -- --run` -> 1 ผ่าน 0 ไม่ผ่าน
- กรณีที่ไม่ผ่าน: โค้ดทำไม่ตรง AC (เจอบั๊ก) จาก [backend/app/booking/service.py](backend/app/booking/service.py#L21-L36) ให้จองได้ที่ `remaining == 0`
- ข้อค้นพบใหม่: F-001 ถึง F-004
- RTM ที่สร้าง: [specs/001-booking/rtm.md](specs/001-booking/rtm.md)
- สรุป: สถานะตามรอยไปข้างหน้า: ครบ 4 รายการ, ยังไม่ถึง 8 รายการ, ช่องโหว่ 4 รายการ, รอ Q-xx 0 รายการ
