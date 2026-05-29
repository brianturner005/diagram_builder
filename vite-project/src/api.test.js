import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { generateDiagram, updateDiagram, downloadBlob } from './api.js'

const MOCK_XML = '<mxGraphModel><root><mxCell id="0"/></root></mxGraphModel>'

function mockFetch(body, ok = true, status = 200) {
  global.fetch = vi.fn().mockResolvedValue({
    ok,
    status,
    json: () => Promise.resolve(body),
    statusText: 'Error',
  })
}

afterEach(() => {
  vi.restoreAllMocks()
})

describe('generateDiagram', () => {
  it('POSTs to /api/generate with the description', async () => {
    mockFetch({ drawio_xml: MOCK_XML })
    await generateDiagram('a simple network')
    expect(fetch).toHaveBeenCalledWith('/api/generate', expect.objectContaining({
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description: 'a simple network' }),
    }))
  })

  it('returns the parsed JSON on success', async () => {
    mockFetch({ drawio_xml: MOCK_XML })
    const result = await generateDiagram('a simple network')
    expect(result).toEqual({ drawio_xml: MOCK_XML })
  })

  it('throws with the detail message on a non-OK response', async () => {
    mockFetch({ detail: 'AI generation failed' }, false, 500)
    await expect(generateDiagram('test')).rejects.toThrow('AI generation failed')
  })

  it('throws a fallback message when error body is not JSON', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
      statusText: 'Bad Gateway',
      json: () => Promise.reject(new Error('not json')),
    })
    await expect(generateDiagram('test')).rejects.toThrow('Bad Gateway')
  })
})

describe('updateDiagram', () => {
  it('POSTs to /api/update with existing_xml and change_description', async () => {
    mockFetch({ drawio_xml: MOCK_XML })
    await updateDiagram(MOCK_XML, 'add a firewall')
    expect(fetch).toHaveBeenCalledWith('/api/update', expect.objectContaining({
      method: 'POST',
      body: JSON.stringify({ existing_xml: MOCK_XML, change_description: 'add a firewall' }),
    }))
  })

  it('returns the updated diagram XML on success', async () => {
    const updatedXml = MOCK_XML + '<!-- updated -->'
    mockFetch({ drawio_xml: updatedXml })
    const result = await updateDiagram(MOCK_XML, 'add a firewall')
    expect(result.drawio_xml).toBe(updatedXml)
  })

  it('throws with the detail message on a non-OK response', async () => {
    mockFetch({ detail: 'Update failed: quota exceeded' }, false, 429)
    await expect(updateDiagram(MOCK_XML, 'add a server')).rejects.toThrow('Update failed: quota exceeded')
  })
})

describe('downloadBlob', () => {
  it('creates an anchor with the correct filename and clicks it', () => {
    const clickSpy = vi.fn()
    const revokeSpy = vi.fn()
    vi.stubGlobal('URL', {
      createObjectURL: vi.fn(() => 'blob:fake-url'),
      revokeObjectURL: revokeSpy,
    })
    const anchor = { href: '', download: '', click: clickSpy }
    vi.spyOn(document, 'createElement').mockReturnValue(anchor)

    const blob = new Blob(['<xml/>'], { type: 'application/xml' })
    downloadBlob(blob, 'diagram.drawio')

    expect(anchor.download).toBe('diagram.drawio')
    expect(anchor.href).toBe('blob:fake-url')
    expect(clickSpy).toHaveBeenCalledOnce()
    expect(revokeSpy).toHaveBeenCalledWith('blob:fake-url')
  })
})
