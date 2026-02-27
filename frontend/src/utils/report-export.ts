import type { TestRun } from '../composables/useTestRunner'

type TranslateFn = (key: string, params?: Record<string, string | number>) => string

export function generateReport(results: TestRun[], t: TranslateFn): string {
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
    categoryGroups[r.category]!.push(r)
  }

  let md = `# ${t('export.title')}\n\n`
  md += `**${t('export.date')}:** ${now}\n`
  md += `**${t('export.targetModels')}:** ${models.join(', ')}\n`
  md += `**${t('export.totalTests')}:** ${total}\n\n`

  md += `## ${t('export.summary')}\n\n`
  md += `| ${t('export.metric')} | ${t('export.count')} |\n`
  md += `|--------|-------|\n`
  md += `| ${t('export.attackSuccess')} | ${pass} |\n`
  md += `| ${t('export.blockedByModel')} | ${fail} |\n`
  md += `| ${t('export.pendingReview')} | ${pending} |\n`
  md += `| **${t('export.successRate')}** | **${rate}%** |\n\n`

  for (const [cat, items] of Object.entries(categoryGroups)) {
    const catPass = items.filter(r => r.success === true).length
    md += `## ${cat} (${catPass}/${items.length} ${t('export.exploited')})\n\n`

    for (const item of items) {
      const verdict = item.success === true ? t('export.pass') : item.success === false ? t('export.fail') : t('export.pending')
      md += `### ${item.template_name} [${verdict}]\n\n`
      md += `- **${t('export.model')}:** ${item.model}\n`
      md += `- **${t('export.duration')}:** ${item.duration_ms}ms\n`
      md += `- **${t('export.severity')}:** ${item.severity}\n\n`
      md += `**${t('export.prompt')}:**\n\`\`\`\n${item.prompt_sent}\n\`\`\`\n\n`
      md += `**${t('export.response')}:**\n\`\`\`\n${item.response}\n\`\`\`\n\n`
      md += `---\n\n`
    }
  }

  md += `## ${t('export.recommendations')}\n\n`
  if (pass > 0) {
    md += `- ${t('export.recBypassed', { count: pass })}\n`
    md += `- ${t('export.recReview')}\n`
  }
  if (fail > 0) {
    md += `- ${t('export.recBlocked', { count: fail })}\n`
  }
  if (pending > 0) {
    md += `- ${t('export.recPending', { count: pending })}\n`
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
