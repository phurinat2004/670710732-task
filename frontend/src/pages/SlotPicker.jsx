import { useEffect, useState } from 'react'
import { api } from '../api/client.js'

// รองรับ FR-BKG-01, FR-BKG-06
export default function SlotPicker({
  dateFrom = '2026-09-23',
  packageCode = 'general',
  client = api,
}) {
  const [slots, setSlots] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let isMounted = true

    client
      .getSlots({ dateFrom, packageCode })
      .then((data) => {
        if (!isMounted) return
        const nextSlots = Array.isArray(data) ? data : data?.slots ?? []
        setSlots(nextSlots)
        setError('')
      })
      .catch(() => {
        if (!isMounted) return
        setSlots([])
        setError('ไม่สามารถโหลดช่วงเวลาว่างได้')
      })
      .finally(() => {
        if (isMounted) setLoading(false)
      })

    return () => {
      isMounted = false
    }
  }, [client, dateFrom, packageCode])

  return (
    <section className="mx-auto max-w-2xl rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-sm font-medium uppercase tracking-wide text-teal-700">เลือกวันที่</p>
          <h2 className="mt-1 text-2xl font-bold text-slate-800">เลือกช่วงเวลา</h2>
        </div>
        <span className="rounded-full bg-teal-50 px-3 py-1 text-sm font-medium text-teal-800">
          {packageCode}
        </span>
      </div>

      {loading && <p className="mt-4 text-slate-600">กำลังโหลดช่วงเวลาว่าง...</p>}
      {error && <p className="mt-4 text-red-600">{error}</p>}

      {!loading && !error && (
        <ul className="mt-5 space-y-3">
          {slots.length === 0 ? (
            <li className="rounded-lg border border-dashed border-slate-300 p-4 text-slate-500">
              ไม่มีช่วงเวลาว่างในช่วงวันที่นี้
            </li>
          ) : (
            slots.map((slot) => {
              const time = slot.start_time ?? slot.startTime ?? slot.time ?? 'เวลา'
              const remaining = Number(slot.remaining ?? slot.available ?? slot.capacity ?? 0)
              const slotKey = `${slot.slot_date ?? dateFrom}-${time}`

              return (
                <li key={slotKey} className="flex items-center justify-between rounded-lg border border-slate-200 p-4">
                  <div>
                    <p className="text-base font-semibold text-slate-800">{time}</p>
                    <p className="text-sm text-slate-500">{slot.slot_date ?? dateFrom}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-slate-600">คงเหลือ</p>
                    <p className="text-lg font-bold text-teal-700">{remaining} ที่</p>
                  </div>
                </li>
              )
            })
          )}
        </ul>
      )}
    </section>
  )
}
