# Prompt log

บันทึกทุกครั้งที่ใช้ AI กับ repo นี้ เขียนต่อท้ายเรื่อย ๆ ไม่ต้องลบของเก่า

---

## [วันที่] [เวลา] คำสั่ง: /clarify

- เครื่องมือ: (Copilot ใน Codespaces / Claude Code / Cursor / แชตทั่วไป)
- ไฟล์: specs/001-xxx/spec.md (v1)

### คำถามที่ AI ถาม (ทั้งหมด)

1. ...
2. ...

### คำตอบของทีมและเหตุผล

1. ...
2. ตอบไม่ได้ ย้ายไป Open Questions (ต้องถาม...)

### สิ่งที่แก้ใน spec.md (v1 เป็น v2)

- ...

---

## [วันที่] [เวลา] คำสั่ง: /plan

- เครื่องมือ:
- ผลลัพธ์: specs/001-xxx/plan.md
- Constraint ที่ AI ยังไม่ได้ใช้:
- สิ่งที่ AI บอกว่าอยากเดาแต่ไม่ได้เดา:

---

## 2569-09-23 10:00 คำสั่ง: /tasks (สร้าง tasks.md)

- เครื่องมือ: GitHub Copilot (ใน Codespaces)
- ไฟล์: specs/001-booking/tasks.md
- ผลลัพธ์: สร้าง `tasks.md` ซึ่งแยกงานเป็น 15 tasks ครอบคลุม AC และ Constraints ตาม spec v2
- Open Questions ที่ยังรอ: Q-02 (รูปแบบหมายเลขคิว) — ส่งผลให้ T-12 และ T-13 รอสถานะ

---

## 2569-09-23 10:30 คำสั่ง: /implement T-01

- เครื่องมือ: GitHub Copilot (ใน Codespaces)
- ไฟล์ที่สร้าง/แก้: backend/app/db/models.py, backend/app/db/migrations/001_init.py, backend/tests/test_migration_create_tables.py, specs/001-booking/tasks.md
- ผลการรัน test: `pytest` ในโฟลเดอร์ `backend` ผ่าน 1 test (migration สร้างตาราง `slots`, `bookings`, `audit_logs`)
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี — งานอิง spec/plan ชัดเจน


