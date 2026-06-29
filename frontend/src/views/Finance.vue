<template>
  <Layout>
    <div style="padding:32px; background:var(--bg-primary); min-height:100vh;">
      <div style="margin-bottom:28px;">
        <p style="color:var(--text-muted); font-size:11px; text-transform:uppercase; letter-spacing:0.1em; margin:0 0 4px;">Module 8</p>
        <h1 style="color:var(--text-primary); font-size:24px; font-weight:700; margin:0;">Logistics Finance Hub</h1>
      </div>
      <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:24px;">
        <div v-for="kpi in kpis" :key="kpi.label" style="background:var(--bg-secondary); border:1px solid var(--border); border-radius:12px; padding:20px;">
          <p style="color:var(--text-secondary); font-size:11px; text-transform:uppercase; letter-spacing:0.08em; margin:0 0 8px;">{{ kpi.label }}</p>
          <p style="font-size:26px; font-weight:700; margin:0 0 4px;" :style="`color:${kpi.color};`">{{ kpi.value }}</p>
          <p style="color:var(--text-muted); font-size:12px; margin:0;">{{ kpi.sub }}</p>
        </div>
      </div>
      <div style="background:var(--bg-secondary); border:1px solid var(--border); border-radius:12px; overflow:hidden;">
        <div style="padding:20px 24px; border-bottom:1px solid var(--border); display:flex; align-items:center; justify-content:space-between;">
          <p style="color:var(--text-primary); font-weight:600; font-size:14px; margin:0;">Invoice Audit Log</p>
          <span style="background:rgba(16,185,129,0.1); color:#10B981; border:1px solid rgba(16,185,129,0.2); padding:4px 12px; border-radius:20px; font-size:11px;">AI Auditing Active</span>
        </div>
        <table style="width:100%; border-collapse:collapse;">
          <thead>
            <tr style="border-bottom:1px solid var(--border);">
              <th v-for="h in ['Invoice','Carrier','Amount','Currency','Status']" :key="h"
                style="text-align:left; padding:14px 24px; color:var(--text-muted); font-size:11px; text-transform:uppercase; font-weight:500;">{{ h }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="inv in invoices" :key="inv.invoice_number" style="border-bottom:1px solid var(--border);">
              <td style="padding:16px 24px; color:#60A5FA; font-family:monospace; font-size:13px;">{{ inv.invoice_number }}</td>
              <td style="padding:16px 24px; color:var(--text-secondary); font-size:13px;">{{ inv.carrier }}</td>
              <td style="padding:16px 24px; color:var(--text-primary); font-weight:500; font-size:13px;">{{ inv.amount?.toLocaleString() }}</td>
              <td style="padding:16px 24px; color:var(--text-muted); font-size:13px;">{{ inv.currency }}</td>
              <td style="padding:16px 24px;">
                <span style="font-size:12px; padding:4px 12px; border-radius:20px; font-weight:500;" :style="statusStyle(inv.status)">{{ inv.status }}</span>
              </td>
            </tr>
            <tr v-if="invoices.length === 0">
              <td colspan="5" style="padding:40px; text-align:center; color:var(--text-muted);">No invoices found</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Layout from '../components/Layout.vue'
import { supabase } from '../lib/supabase'

const invoices = ref([])
const kpis = ref([
  { label: 'Total Freight Spend', value: '$842K', color: 'var(--text-primary)', sub: 'This quarter' },
  { label: 'AI Cost Savings', value: '$42,150', color: '#10B981', sub: 'Via route optimization' },
  { label: 'Invoices Flagged', value: '—', color: '#EF4444', sub: 'Billing errors detected' },
  { label: 'Pending Approvals', value: '—', color: '#F59E0B', sub: 'Awaiting review' },
])

function statusStyle(status) {
  return {
    'Processed': 'background:rgba(16,185,129,0.15); color:#10B981;',
    'OCR Reading': 'background:rgba(59,130,246,0.15); color:#60A5FA;',
    'Pending': 'background:rgba(100,116,139,0.15); color:var(--text-secondary);',
    'Flagged': 'background:rgba(239,68,68,0.15); color:#F87171;',
  }[status] || ''
}

onMounted(async () => {
  const { data } = await supabase.from('freight_invoices').select('*').order('created_at', { ascending: false })
  invoices.value = data || []
  kpis.value[2].value = data?.filter(i => i.status === 'Flagged').length.toString() || '0'
  kpis.value[3].value = data?.filter(i => i.status === 'Pending').length.toString() || '0'
})
</script>