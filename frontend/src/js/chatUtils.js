export async function sendMessage({ query, props, tab }) {
  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      base_url: props.base_url,
      lm_name: props.lm_name,
      agent_type: tab,
      system_message: props.system_message,
      query
    })
  })
  const data = await res.json()
  return data.response || 'Error.'
}
