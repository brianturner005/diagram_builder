import { describe, it, expect } from 'vitest'
import TEMPLATES from './templates.js'

const EXPECTED_IDS = [
  'home-network',
  '3-tier-web',
  'aws-vpc',
  'corporate-office',
  'dmz',
  'kubernetes',
  'azure-app',
  'gcp-data',
]

describe('TEMPLATES', () => {
  it('exports exactly 8 templates', () => {
    expect(TEMPLATES).toHaveLength(8)
  })

  it('all template IDs are unique', () => {
    const ids = TEMPLATES.map((t) => t.id)
    expect(new Set(ids).size).toBe(ids.length)
  })

  it('contains all expected template IDs', () => {
    const ids = TEMPLATES.map((t) => t.id)
    expect(ids).toEqual(EXPECTED_IDS)
  })
})

describe.each(TEMPLATES)('template "$name"', (template) => {
  it('has a non-empty id', () => {
    expect(template.id).toBeTruthy()
  })

  it('has a non-empty name', () => {
    expect(template.name).toBeTruthy()
  })

  it('has a non-empty icon', () => {
    expect(template.icon).toBeTruthy()
  })

  it('has a description that is a non-empty string', () => {
    expect(typeof template.description).toBe('string')
    expect(template.description.trim().length).toBeGreaterThan(0)
  })

  it('description is at least 50 characters (long enough to generate a useful diagram)', () => {
    expect(template.description.length).toBeGreaterThanOrEqual(50)
  })

  it('id contains only lowercase letters, numbers, and hyphens', () => {
    expect(template.id).toMatch(/^[a-z0-9-]+$/)
  })
})
