import React from 'react'

export default function UpdatePanel({ onUpdate, loading }) {
  const [change, setChange] = React.useState('')

  function handleSubmit(e) {
    e.preventDefault()
    if (change.trim()) {
      onUpdate(change.trim())
      setChange('')
    }
  }

  return (
    <div className="update-panel">
      <h2 className="update-title">✏️ Update diagram</h2>
      <p className="update-subtitle">
        Describe a change and the diagram will be updated in place
      </p>
      <form onSubmit={handleSubmit} className="update-form">
        <textarea
          className="description-textarea"
          value={change}
          onChange={(e) => setChange(e.target.value)}
          placeholder='e.g. "Add a Redis cache between the app servers and database" or "Replace the single web server with a load balancer and two web servers"'
          rows={3}
          disabled={loading}
        />
        <div className="input-controls">
          <button
            type="submit"
            className="generate-btn update-btn"
            disabled={loading || !change.trim()}
          >
            {loading ? 'Updating…' : 'Update Diagram'}
          </button>
        </div>
      </form>
    </div>
  )
}
