import React from 'react'
import mermaid from 'mermaid'

mermaid.initialize({
  startOnLoad: false,
  theme: 'default',
  securityLevel: 'loose',
})

let renderCount = 0

export default function DiagramPreview({ mermaidCode }) {
  const containerRef = React.useRef(null)
  const [showCode, setShowCode] = React.useState(false)
  const [renderError, setRenderError] = React.useState(null)

  React.useEffect(() => {
    if (!mermaidCode || !containerRef.current) return

    setRenderError(null)
    const id = `mermaid-${++renderCount}`

    mermaid.render(id, mermaidCode).then(({ svg }) => {
      if (containerRef.current) {
        containerRef.current.innerHTML = svg
      }
    }).catch((err) => {
      setRenderError(`Mermaid render error: ${err.message}`)
    })
  }, [mermaidCode])

  if (!mermaidCode) {
    return (
      <div className="preview-empty">
        <p>Your diagram will appear here after you generate one.</p>
      </div>
    )
  }

  return (
    <div className="preview-panel">
      <div className="preview-svg" ref={containerRef} />
      {renderError && <p className="preview-error">{renderError}</p>}
      <button
        className="toggle-code-btn"
        onClick={() => setShowCode((s) => !s)}
      >
        {showCode ? 'Hide Mermaid code' : 'Show Mermaid code'}
      </button>
      {showCode && (
        <pre className="mermaid-code">{mermaidCode}</pre>
      )}
    </div>
  )
}
