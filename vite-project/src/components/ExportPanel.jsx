import React from 'react'
import { downloadBlob } from '../api.js'

export default function ExportPanel({ drawioXml }) {
  function downloadDrawio() {
    const blob = new Blob([drawioXml], { type: 'application/xml' })
    downloadBlob(blob, 'diagram.drawio')
  }

  function openInEditor() {
    const encoded = encodeURIComponent(drawioXml)
    window.open(`https://app.diagrams.net/?xml=${encoded}`, '_blank')
  }

  return (
    <div className="export-panel">
      <span className="export-label">Export / Edit:</span>
      <div className="export-buttons">
        <button className="export-btn primary" onClick={downloadDrawio}>
          Download .drawio
        </button>
        <button className="export-btn" onClick={openInEditor}>
          Open in diagrams.net
        </button>
      </div>
      <p className="export-hint">
        .drawio files open in the free <a href="https://app.diagrams.net" target="_blank" rel="noreferrer">diagrams.net</a> app
        and can be imported directly into Microsoft Visio.
      </p>
    </div>
  )
}
