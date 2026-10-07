import { render, screen, waitFor } from '@testing-library/react'
import SlotPicker from '../pages/SlotPicker.jsx'
import { api } from '../api/client.js'

vi.mock('../api/client.js', () => ({
  api: { getSlots: vi.fn() },
}))

test('T-10 โหลดช่วงเวลาว่างจาก API จำลองได้', async () => {
  api.getSlots.mockResolvedValue([
    { slot_date: '2026-09-23', start_time: '09:00', remaining: 4 },
    { slot_date: '2026-09-23', start_time: '10:30', remaining: 2 },
  ])

  render(<SlotPicker dateFrom="2026-09-23" packageCode="general" client={api} />)

  expect(screen.getByText('เลือกช่วงเวลา')).toBeTruthy()
  await waitFor(() => {
    expect(screen.getByText('09:00')).toBeTruthy()
    expect(screen.getByText('4 ที่')).toBeTruthy()
  })

  expect(api.getSlots).toHaveBeenCalledWith({
    dateFrom: '2026-09-23',
    packageCode: 'general',
  })
})
