import React from 'react'
import { exportVisio, downloadBlob } from '../api.js'

export default function ExportPanel({ drawioXml }) {
  const [exporting, setExporting] = React.useState(false)
  const [exportError, setExportError] = React.useState(null)

  function downloadDrawio() {
    const blob = new Blob([drawioXml], { type: 'application/xml' })
    downloadBlob(blob, 'diagram.drawio')
  }

  function openInEditor() {
    const encoded = encodeURIComponent(drawioXml)
    window.open(`https://app.diagrams.net/?xml=${encoded}`, '_blank')
  }

  async function downloadVisio() {
    setExporting(true)
    setExportError(null)
    try {
      const blob = await exportVisio(drawioXml)
      downloadBlob(blob, 'diagram.vsdx')
    } catch (err) {
      setExportError(err.message)
    } finally {
      setExporting(false)
    }
  }

  return (
    <div className="export-panel">
      <span className="export-label">Export / Edit:</span>
      <div className="export-buttons">
        <button className="export-btn primary" onClick={downloadDrawio}>
          Download .drawio
        </button>
        <button
          className="export-btn primary"
          onClick={downloadVisio}
          disabled={exporting}
        >
          {exporting ? 'Generating…' : 'Download .vsdx'}
        </button>
        <button className="export-btn" onClick={openInEditor}>
          Open in diagrams.net
        </button>
      </div>
      {exportError && (
        <p className="export-hint" style={{ color: '#b85450' }}>
          Visio export failed: {exportError}
        </p>
      )}
    </div>
  )
}
