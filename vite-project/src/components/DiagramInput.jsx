import React from 'react'

export default function DiagramInput({ onGenerate, loading }) {
  const [description, setDescription] = React.useState('')

  function handleSubmit(e) {
    e.preventDefault()
    if (description.trim()) {
      onGenerate(description.trim())
    }
  }

  return (
    <form className="input-panel" onSubmit={handleSubmit}>
      <label className="input-label" htmlFor="description">
        Describe your diagram
      </label>
      <textarea
        id="description"
        className="description-textarea"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="e.g. A corporate network with an internet connection through a firewall, a core router, two switches serving an office floor and a server room, three app servers, a database cluster, and laptops for 20 users"
        rows={5}
        disabled={loading}
      />
      <div className="input-controls">
        <button
          type="submit"
          className="generate-btn"
          disabled={loading || !description.trim()}
        >
          {loading ? 'Generating…' : 'Generate Diagram'}
        </button>
      </div>
    </form>
  )
}
