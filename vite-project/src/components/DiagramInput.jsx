import React from 'react'
import TEMPLATES from '../templates.js'

export default function DiagramInput({ onGenerate, loading }) {
  const [description, setDescription] = React.useState('')
  const [showTemplates, setShowTemplates] = React.useState(true)

  function handleSubmit(e) {
    e.preventDefault()
    if (description.trim()) onGenerate(description.trim())
  }

  function handleTemplate(template) {
    setDescription(template.description)
    setShowTemplates(false)
    onGenerate(template.description)
  }

  return (
    <div className="input-panel">
      <button
        className="templates-toggle"
        onClick={() => setShowTemplates((s) => !s)}
        type="button"
      >
        {showTemplates ? '▾ Hide templates' : '▸ Show templates'}
      </button>

      {showTemplates && (
        <div className="templates-grid">
          {TEMPLATES.map((t) => (
            <button
              key={t.id}
              className="template-card"
              onClick={() => handleTemplate(t)}
              disabled={loading}
              type="button"
            >
              <span className="template-icon">{t.icon}</span>
              <span className="template-name">{t.name}</span>
            </button>
          ))}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <label className="input-label" htmlFor="description">
          Describe your diagram
        </label>
        <textarea
          id="description"
          className="description-textarea"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="e.g. A corporate network with a firewall, core router, two switches, three app servers, and a database cluster"
          rows={4}
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
    </div>
  )
}
