export async function sendMessage({ text }) {
  const res = await fetch('/api/log-unit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        text: text
    })
  })
  const data = await res.json()
  return data.response || 'Error.'
}
