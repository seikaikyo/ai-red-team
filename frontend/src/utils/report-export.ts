import type { TestRun } from '../composables/useTestRunner'

export function generateReport(results: TestRun[]): string {
  if (!results.length) return ''

  const now = new Date().toISOString().slice(0, 10)
  const models = [...new Set(results.map(r => r.model))]
  const total = results.length
  const pass = results.filter(r => r.success === true).length
  const fail = results.filter(r => r.success === false).length
  const pending = results.filter(r => r.success === null).length
  const rate = total > 0 ? ((pass / total) * 100).toFixed(1) : '0.0'

  const categoryGroups: Record<string, TestRun[]> = {}
  for (const r of results) {
    if (!categoryGroups[r.category]) categoryGroups[r.category] = []
    categoryGroups[r.category].push(r)
  }

  let md = `# AI Red Team Report\n\n`
  md += `**Date:** ${now}\n`
  md += `**Target Model(s):** ${models.join(', ')}\n`
  md += `**Total Tests:** ${total}\n\n`

  md += `## Summary\n\n`
  md += `| Metric | Count |\n`
  md += `|--------|-------|\n`
  md += `| Attack Success (Exploited) | ${pass} |\n`
  md += `| Blocked by Model | ${fail} |\n`
  md += `| Pending Review | ${pending} |\n`
  md += `| **Success Rate** | **${rate}%** |\n\n`

  for (const [cat, items] of Object.entries(categoryGroups)) {
    const catPass = items.filter(r => r.success === true).length
    md += `## ${cat} (${catPass}/${items.length} exploited)\n\n`

    for (const item of items) {
      const verdict = item.success === true ? 'PASS' : item.success === false ? 'FAIL' : 'PENDING'
      md += `### ${item.template_name} [${verdict}]\n\n`
      md += `- **Model:** ${item.model}\n`
      md += `- **Duration:** ${item.duration_ms}ms\n`
      md += `- **Severity:** ${item.severity}\n\n`
      md += `**Prompt:**\n\`\`\`\n${item.prompt_sent}\n\`\`\`\n\n`
      md += `**Response:**\n\`\`\`\n${item.response}\n\`\`\`\n\n`
      md += `---\n\n`
    }
  }

  md += `## Recommendations\n\n`
  if (pass > 0) {
    md += `- ${pass} attack(s) successfully bypassed model safety measures\n`
    md += `- Review exploited categories and strengthen corresponding guardrails\n`
  }
  if (fail > 0) {
    md += `- ${fail} attack(s) were properly blocked\n`
  }
  if (pending > 0) {
    md += `- ${pending} result(s) still need manual review\n`
  }

  return md
}

export function downloadMarkdown(content: string, filename: string) {
  const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}
