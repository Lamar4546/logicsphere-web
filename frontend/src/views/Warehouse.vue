<template>
  <Layout>
    <div style="padding:32px; background:var(--bg-primary); min-height:100vh;">
      <div style="margin-bottom:28px;">
        <p style="color:var(--text-muted); font-size:11px; text-transform:uppercase; letter-spacing:0.1em; margin:0 0 4px;">Module 6</p>
        <h1 style="color:var(--text-primary); font-size:24px; font-weight:700; margin:0;">Warehouse Management</h1>
      </div>
      <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-bottom:24px;">
        <div v-for="kpi in kpis" :key="kpi.label" style="background:var(--bg-secondary); border:1px solid var(--border); border-radius:12px; padding:20px;">
          <p style="color:var(--text-secondary); font-size:11px; text-transform:uppercase; letter-spacing:0.08em; margin:0 0 8px;">{{ kpi.label }}</p>
          <p style="color:var(--text-primary); font-size:26px; font-weight:700; margin:0 0 4px;">{{ kpi.value }}</p>
          <p style="font-size:12px; margin:0;" :style="`color:${kpi.subColor};`">{{ kpi.sub }}</p>
        </div>
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px;">
        <div style="background:var(--bg-secondary); border:1px solid var(--border); border-radius:12px; padding:24px;">
          <p style="color:var(--text-primary); font-weight:600; font-size:14px; margin:0 0 20px;">Space Utilization</p>
          <div v-for="zone in zones" :key="zone.name" style="margin-bottom:20px;">
            <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:6px;">
              <span style="color:var(--text-secondary);">{{ zone.name }}</span>
              <span style="color:var(--text-primary); font-weight:500;">{{ zone.used }}%</span>
            </div>
            <div style="height:8px; background:var(--bg-primary); border-radius:4px; overflow:hidden;">
              <div :style="`height:100%; border-radius:4px; background:${zone.color}; width:${zone.used}%;`"></div>
            </div>
          </div>
        </div>
        <div style="background:var(--bg-secondary); border:1px solid var(--border); border-radius:12px; padding:24px;">
          <p style="color:var(--text-primary); font-weight:600; font-size:14px; margin:0 0 16px;">AI Recommendations</p>
          <div v-for="rec in recommendations" :key="rec" style="background:var(--bg-primary); border:1px solid var(--border); border-radius:10px; padding:14px 16px; margin-bottom:10px; display:flex; gap:10px;">
            <span style="color:#60A5FA; margin-top:1px;">🤖</span>
            <p style="color:var(--text-secondary); font-size:13px; margin:0; line-height:1.5;">{{ rec }}</p>
          </div>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script setup>
import Layout from '../components/Layout.vue'

const kpis = [
  { label: 'Total Capacity', value: '48,000 m²', sub: 'Across 3 facilities', subColor: 'var(--text-muted)' },
  { label: 'Utilization', value: '73%', sub: 'Optimal range: 70–85%', subColor: '#10B981' },
  { label: 'Pending Picks', value: '284', sub: '12 urgent orders', subColor: '#F59E0B' },
]
const zones = [
  { name: 'Zone A — Receiving', used: 88, color: '#EF4444' },
  { name: 'Zone B — Storage', used: 65, color: '#10B981' },
  { name: 'Zone C — Picking', used: 72, color: '#3B82F6' },
  { name: 'Zone D — Dispatch', used: 45, color: '#10B981' },
]
const recommendations = [
  'Redistribute Zone A overflow to Zone B — capacity available.',
  'Schedule additional labor shift for Friday based on order forecast.',
  'Reorganize SKU-002 to Zone C for faster picking efficiency.',
]
</script>