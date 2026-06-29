<template>
  <Layout>
    <div style="padding:32px; background:var(--bg-primary); min-height:100vh;">
      <div style="margin-bottom:28px;">
        <p style="color:var(--text-muted); font-size:11px; text-transform:uppercase; letter-spacing:0.1em; margin:0 0 4px;">Module 4</p>
        <h1 style="color:var(--text-primary); font-size:24px; font-weight:700; margin:0;">Customs Compliance AI</h1>
      </div>
      <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:24px;">
        <div v-for="kpi in kpis" :key="kpi.label" style="background:var(--bg-secondary); border:1px solid var(--border); border-radius:12px; padding:20px;">
          <p style="color:var(--text-secondary); font-size:11px; text-transform:uppercase; letter-spacing:0.08em; margin:0 0 8px;">{{ kpi.label }}</p>
          <p style="font-size:26px; font-weight:700; margin:0;" :style="`color:${kpi.color};`">{{ kpi.value }}</p>
        </div>
      </div>
      <div style="background:var(--bg-secondary); border:1px solid var(--border); border-radius:12px; overflow:hidden;">
        <table style="width:100%; border-collapse:collapse;">
          <thead>
            <tr style="border-bottom:1px solid var(--border);">
              <th v-for="h in ['Shipment','HS Code','Country','Duty Est.','AI Status']" :key="h"
                style="text-align:left; padding:14px 24px; color:var(--text-muted); font-size:11px; text-transform:uppercase; font-weight:500;">{{ h }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in customs" :key="item.shipment" style="border-bottom:1px solid var(--border);">
              <td style="padding:16px 24px; color:#60A5FA; font-family:monospace; font-size:13px;">{{ item.shipment }}</td>
              <td style="padding:16px 24px; color:var(--text-secondary); font-family:monospace; font-size:13px;">{{ item.hs_code }}</td>
              <td style="padding:16px 24px; color:var(--text-secondary); font-size:13px;">{{ item.country }}</td>
              <td style="padding:16px 24px; color:var(--text-primary); font-weight:500; font-size:13px;">{{ item.duty }}</td>
              <td style="padding:16px 24px;">
                <span style="font-size:12px; padding:4px 12px; border-radius:20px; font-weight:500;" :style="item.statusStyle">{{ item.status }}</span>
              </td>
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

const kpis = ref([
  { label: 'Pending Clearance', value: '—', color: '#F59E0B' },
  { label: 'Cleared Today', value: '—', color: '#10B981' },
  { label: 'Exceptions', value: '—', color: '#EF4444' },
  { label: 'Avg Clearance Time', value: '18h', color: 'var(--text-primary)' },
])

const customs = ref([])

function statusStyle(status) {
  return {
    'Cleared': 'background:rgba(16,185,129,0.15); color:#10B981;',
    'Under Review': 'background:rgba(245,158,11,0.15); color:#FCD34D;',
    'Exception': 'background:rgba(239,68,68,0.15); color:#F87171;',
    'Pending': 'background:rgba(100,116,139,0.15); color:var(--text-secondary);',
  }[status] || ''
}

onMounted(async () => {
  const { data: shipments } = await supabase.from('shipments').select('*').limit(10)
  customs.value = (shipments || []).map(s => ({
    shipment: s.tracking_number,
    hs_code: '8483.40.90',
    country: s.destination?.split(' ').pop() || 'Unknown',
    duty: `$${(Math.random() * 1500 + 200).toFixed(2)}`,
    status: s.status === 'At Customs' ? 'Under Review' : s.status === 'Delivered' ? 'Cleared' : 'Pending',
    statusStyle: statusStyle(s.status === 'At Customs' ? 'Under Review' : s.status === 'Delivered' ? 'Cleared' : 'Pending')
  }))
  kpis.value[0].value = customs.value.filter(c => c.status === 'Under Review').length.toString()
  kpis.value[1].value = customs.value.filter(c => c.status === 'Cleared').length.toString()
  kpis.value[2].value = customs.value.filter(c => c.status === 'Exception').length.toString()
})
</script>