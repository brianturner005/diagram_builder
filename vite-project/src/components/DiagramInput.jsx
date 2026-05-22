import React from 'react'

const DIAGRAM_TYPES = [
  { value: 'auto', label: 'Auto-detect' },
  { value: 'flowchart', label: 'Flowchart' },
  { value: 'sequence', label: 'Sequence' },
  { value: 'class', label: 'Class diagram' },
  { value: 'er', label: 'ER diagram' },
  { value: 'mindmap', label: 'Mind map' },
]

export default function DiagramInput({ onGenerate, loading }) {
  const [description, setDescription] = React.useState('')
  const [diagramType, setDiagramType] = React.useState('auto')

  function handleSubmit(e) {
    e.preventDefault()
    if (description.trim()) {
      onGenerate(description.trim(), diagramType)
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
        placeholder="e.g. A three-tier web architecture with a load balancer, two app servers, and a PostgreSQL database"
        rows={5}
        disabled={loading}
      />
      <div className="input-controls">
        <select
          className="type-select"
          value={diagramType}
          onChange={(e) => setDiagramType(e.target.value)}
          disabled={loading}
        >
          {DIAGRAM_TYPES.map((t) => (
            <option key={t.value} value={t.value}>
              {t.label}
            </option>
          ))}
        </select>
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
