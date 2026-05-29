import React from 'react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import DiagramInput from './DiagramInput.jsx'
import TEMPLATES from '../templates.js'

function setup(props = {}) {
  const onGenerate = vi.fn()
  const user = userEvent.setup()
  const utils = render(<DiagramInput onGenerate={onGenerate} loading={false} {...props} />)
  return { onGenerate, user, ...utils }
}

describe('DiagramInput — template cards', () => {
  it('renders all 8 template cards by default', () => {
    setup()
    TEMPLATES.forEach((t) => {
      expect(screen.getByText(t.name)).toBeInTheDocument()
    })
  })

  it('hides template grid when toggle is clicked', async () => {
    const { user } = setup()
    await user.click(screen.getByText(/hide templates/i))
    TEMPLATES.forEach((t) => {
      expect(screen.queryByText(t.name)).not.toBeInTheDocument()
    })
  })

  it('shows template grid again after a second toggle', async () => {
    const { user } = setup()
    await user.click(screen.getByText(/hide templates/i))
    await user.click(screen.getByText(/show templates/i))
    expect(screen.getByText(TEMPLATES[0].name)).toBeInTheDocument()
  })

  describe.each(TEMPLATES)('card "$name"', (template) => {
    it('clicking calls onGenerate with the template description', async () => {
      const { onGenerate, user } = setup()
      await user.click(screen.getByText(template.name))
      expect(onGenerate).toHaveBeenCalledOnce()
      expect(onGenerate).toHaveBeenCalledWith(template.description)
    })

    it('clicking fills the textarea with the template description', async () => {
      const { user } = setup()
      await user.click(screen.getByText(template.name))
      const textarea = screen.getByLabelText(/describe your diagram/i)
      expect(textarea).toHaveValue(template.description)
    })

    it('clicking hides the template grid', async () => {
      const { user } = setup()
      await user.click(screen.getByText(template.name))
      expect(screen.queryByText(template.name)).not.toBeInTheDocument()
    })

    it('is disabled while loading', () => {
      setup({ loading: true })
      const btn = screen.getByText(template.name).closest('button')
      expect(btn).toBeDisabled()
    })
  })
})

describe('DiagramInput — manual entry', () => {
  it('Generate button is disabled when textarea is empty', () => {
    setup()
    expect(screen.getByRole('button', { name: /generate diagram/i })).toBeDisabled()
  })

  it('Generate button is enabled after typing', async () => {
    const { user } = setup()
    await user.type(screen.getByLabelText(/describe your diagram/i), 'a simple network')
    expect(screen.getByRole('button', { name: /generate diagram/i })).toBeEnabled()
  })

  it('submitting the form calls onGenerate with the trimmed description', async () => {
    const { onGenerate, user } = setup()
    await user.type(screen.getByLabelText(/describe your diagram/i), '  my diagram  ')
    await user.click(screen.getByRole('button', { name: /generate diagram/i }))
    expect(onGenerate).toHaveBeenCalledWith('my diagram')
  })

  it('shows "Generating…" label while loading', () => {
    setup({ loading: true })
    expect(screen.getByRole('button', { name: /generating/i })).toBeInTheDocument()
  })
})
