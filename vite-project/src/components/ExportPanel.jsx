import React from 'react'
import { exportVisio, downloadBlob } from '../api.js'

export default function ExportPanel({ mermaidCode }) {
  const [visioLoading, setVisioLoading] = React.useState(false)
  const [error, setError] = React.useState(null)

  function downloadMermaid() {
    const blob = new Blob([mermaidCode], { type: 'text/plain' })
    downloadBlob(blob, 'diagram.mmd')
  }

  function downloadSVG() {
    const svgEl = document.querySelector('.preview-svg svg')
    if (!svgEl) return
    const serializer = new XMLSerializer()
    const svgStr = serializer.serializeToString(svgEl)
    const blob = new Blob([svgStr], { type: 'image/svg+xml' })
    downloadBlob(blob, 'diagram.svg')
  }

  function downloadPNG() {
    const svgEl = document.querySelector('.preview-svg svg')
    if (!svgEl) return

    const svgStr = new XMLSerializer().serializeToString(svgEl)
    const img = new Image()
    const svgBlob = new Blob([svgStr], { type: 'image/svg+xml;charset=utf-8' })
    const url = URL.createObjectURL(svgBlob)

    img.onload = () => {
      const canvas = document.createElement('canvas')
      canvas.width = img.width || 1200
      canvas.height = img.height || 800
      const ctx = canvas.getContext('2d')
      ctx.fillStyle = 'white'
      ctx.fillRect(0, 0, canvas.width, canvas.height)
      ctx.drawImage(img, 0, 0)
      URL.revokeObjectURL(url)
      canvas.toBlob((pngBlob) => downloadBlob(pngBlob, 'diagram.png'), 'image/png')
    }
    img.src = url
  }

  async function downloadVisio() {
    setVisioLoading(true)
    setError(null)
    try {
      const blob = await exportVisio(mermaidCode)
      downloadBlob(blob, 'diagram.vsdx')
    } catch (err) {
      setError(err.message)
    } finally {
      setVisioLoading(false)
    }
  }

  return (
    <div className="export-panel">
      <span className="export-label">Export as:</span>
      <div className="export-buttons">
        <button className="export-btn" onClick={downloadMermaid}>
          Mermaid (.mmd)
        </button>
        <button className="export-btn" onClick={downloadSVG}>
          SVG
        </button>
        <button className="export-btn" onClick={downloadPNG}>
          PNG
        </button>
        <button className="export-btn" onClick={downloadVisio} disabled={visioLoading}>
          {visioLoading ? 'Exporting…' : 'Visio (.vsdx)'}
        </button>
      </div>
      {error && <p className="export-error">{error}</p>}
    </div>
  )
}
