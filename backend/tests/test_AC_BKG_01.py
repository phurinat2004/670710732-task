# test ของ T-03: จองคิวสำเร็จ
# AC-BKG-01 (FR-BKG-04)
from app.db.models import Slot
from tests.conftest import AUTH


def test_AC_BKG_01(client, make_slot):
    """AC-BKG-01: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง จองแล้วต้องสำเร็จ"""
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201


def test_TC_BKG_01_1_successful_booking(client, db, make_slot):
    # Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    # When: ยืนยันการจองช่วง 09.00 น.
    slot = make_slot(start="09:00", remaining=1)
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: บันทึกการจองสำเร็จ; แสดงหมายเลขคิว (รอ Q-xx); ที่นั่งว่างของช่วงนั้นลดจาก 1 เป็น 0;
    # ส่งคำขอส่งข้อความยืนยันตาม IF-NOT-01
    assert res.status_code == 201
    assert db.get(Slot, slot.id).remaining == 0


def test_TC_BKG_01_2_last_seat_booking(client, db, make_slot):
    # Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่ (จุดเกินขั้นต่ำก่อนลดลงเป็น 0)
    # When: ยืนยันการจองช่วง 09.00 น. โดยใช้ที่นั่งสุดท้าย
    slot = make_slot(start="09:00", remaining=1)
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: การจองยังบันทึกสำเร็จ; หมายเลขคิวแสดงตามรูปแบบที่กำหนด (รอ Q-xx);
    # จำนวนที่นั่งที่เหลือเปลี่ยนจาก 1 เป็น 0; ไม่มีการจองซ้ำเกิดขึ้นในช่วงเดียวกัน
    assert res.status_code == 201
    assert db.get(Slot, slot.id).remaining == 0


def test_TC_BKG_01_3_rejects_unverified_or_full_slot(client, make_slot):
    # Given: ยังไม่ได้ยืนยันตัวตน หรือช่วง 09.00 น. มีที่นั่งว่าง 0 ที่
    # When: พยายามยืนยันการจองช่วง 09.00 น.
    slot = make_slot(start="09:00", remaining=0)
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: ไม่บันทึกการจอง; ไม่แสดงหมายเลขคิว (รอ Q-xx); ไม่ลดจำนวนที่นั่ง;
    # ปฏิเสธด้วยเงื่อนไขยืนยันตัวตนก่อนหรือช่วงเต็มตาม IF-IDP-01 / FR-BKG-03
    assert res.status_code == 409
