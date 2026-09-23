from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    DateTime,
    ForeignKey,
    func,
    JSON,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# รองรับ: FR-BKG-01, FR-BKG-06, CON-TECH-01
class Slot(Base):
    __tablename__ = "slots"

    id = Column(Integer, primary_key=True)
    slot_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    package_code = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False, default=0)
    remaining = Column(Integer, nullable=False, default=0)


# รองรับ: FR-BKG-04, FR-BKG-02, IF-HIS-01
# หมายเหตุ: เก็บเฉพาะ `hn` ตาม IF-HIS-01 ห้ามเก็บเลขบัตรประชาชน
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    hn = Column(String(64), nullable=False, index=True)
    slot_id = Column(Integer, ForeignKey("slots.id"), nullable=False)
    booking_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    queue_no = Column(String(50), nullable=True)  # Q-02 ยังรอคำตอบ รูปแบบไม่กำหนด
    status = Column(String(20), nullable=False, default="confirmed")

    slot = relationship("Slot", backref="bookings")


# รองรับ: DOM-PDPA-01
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    actor_id = Column(String(128), nullable=False)
    action = Column(String(128), nullable=False)
    hn = Column(String(64), nullable=True)
    accessed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
