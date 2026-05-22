import React from 'react'
import DiagramInput from './components/DiagramInput.jsx'
import DiagramPreview from './components/DiagramPreview.jsx'
import ExportPanel from './components/ExportPanel.jsx'
import { generateDiagram } from './api.js'

export default function App() {
  const [mermaidCode, setMermaidCode] = React.useState('')
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState(null)

  async function handleGenerate(description, diagramType) {
    setLoading(true)
    setError(null)
    try {
      const result = await generateDiagram(description, diagramType)
      setMermaidCode(result.mermaid_code)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1 className="app-title">Diagram Builder</h1>
        <p className="app-subtitle">Describe a diagram in plain English and get it instantly</p>
      </header>

      <main className="app-main">
        <DiagramInput onGenerate={handleGenerate} loading={loading} />

        {error && (
          <div className="error-banner" role="alert">
            <strong>Error:</strong> {error}
            <button className="error-dismiss" onClick={() => setError(null)}>×</button>
          </div>
        )}

        <DiagramPreview mermaidCode={mermaidCode} />

        {mermaidCode && <ExportPanel mermaidCode={mermaidCode} />}
      </main>
    </div>
  )
}
