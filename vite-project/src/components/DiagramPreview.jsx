import React from 'react'

let graphCount = 0

export default function DiagramPreview({ drawioXml }) {
  const containerRef = React.useRef(null)
  const [showXml, setShowXml] = React.useState(false)

  React.useEffect(() => {
    if (!drawioXml || !containerRef.current) return

    // Clear previous diagram
    containerRef.current.innerHTML = ''

    const div = document.createElement('div')
    div.className = 'mxgraph'
    div.style.maxWidth = '100%'
    div.style.border = 'none'
    div.setAttribute(
      'data-mxgraph',
      JSON.stringify({
        highlight: '#4A90D9',
        nav: true,
        resize: true,
        toolbar: 'zoom layers lightbox',
        edit: '_blank',
        xml: drawioXml,
        'auto-fit': true,
      })
    )
    containerRef.current.appendChild(div)

    // Render: use existing GraphViewer if already loaded, otherwise wait
    const render = () => {
      if (window.GraphViewer) {
        window.GraphViewer.processElements()
      }
    }
    render()
    // Belt-and-suspenders retry in case the script hadn't finished loading
    const timer = setTimeout(render, 300)
    return () => clearTimeout(timer)
  }, [drawioXml])

  if (!drawioXml) {
    return (
      <div className="preview-empty">
        <p>Your diagram will appear here after you generate one.</p>
      </div>
    )
  }

  return (
    <div className="preview-panel">
      <div ref={containerRef} className="drawio-container" />
      <div className="preview-footer">
        <button className="toggle-code-btn" onClick={() => setShowXml((s) => !s)}>
          {showXml ? 'Hide XML' : 'Show XML'}
        </button>
        <span className="preview-hint">
          Use the toolbar above the diagram to zoom and pan
        </span>
      </div>
      {showXml && <pre className="mermaid-code">{drawioXml}</pre>}
    </div>
  )
}
