import React from 'react'
import DiagramInput from './components/DiagramInput.jsx'
import DiagramPreview from './components/DiagramPreview.jsx'
import ExportPanel from './components/ExportPanel.jsx'
import { generateDiagram } from './api.js'

export default function App() {
  const [drawioXml, setDrawioXml] = React.useState('')
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState(null)

  async function handleGenerate(description) {
    setLoading(true)
    setError(null)
    try {
      const result = await generateDiagram(description)
      setDrawioXml(result.drawio_xml)
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
        <p className="app-subtitle">
          Describe your network or infrastructure in plain English and get a diagram instantly
        </p>
      </header>

      <main className="app-main">
        <DiagramInput onGenerate={handleGenerate} loading={loading} />

        {error && (
          <div className="error-banner" role="alert">
            <strong>Error:</strong> {error}
            <button className="error-dismiss" onClick={() => setError(null)}>×</button>
          </div>
        )}

        <DiagramPreview drawioXml={drawioXml} />

        {drawioXml && <ExportPanel drawioXml={drawioXml} />}
      </main>
    </div>
  )
}
