<template>
  <Layout>
    <div style="padding:32px; background:var(--bg-primary); min-height:100vh;">
      <div style="margin-bottom:28px;">
        <p style="color:var(--text-muted); font-size:11px; text-transform:uppercase; letter-spacing:0.1em; margin:0 0 4px;">Module 5</p>
        <h1 style="color:var(--text-primary); font-size:24px; font-weight:700; margin:0;">Inventory Intelligence</h1>
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
              <th v-for="h in ['SKU','Product','Quantity','Reorder Point','Location','Health']" :key="h"
                style="text-align:left; padding:14px 24px; color:var(--text-muted); font-size:11px; text-transform:uppercase; font-weight:500;">{{ h }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in inventory" :key="item.sku" style="border-bottom:1px solid var(--border);">
              <td style="padding:16px 24px; color:#60A5FA; font-family:monospace; font-size:13px;">{{ item.sku }}</td>
              <td style="padding:16px 24px; color:var(--text-primary); font-size:13px;">{{ item.product_name }}</td>
              <td style="padding:16px 24px; color:var(--text-secondary); font-size:13px;">{{ item.quantity?.toLocaleString() }}</td>
              <td style="padding:16px 24px; color:var(--text-muted); font-size:13px;">{{ item.reorder_point }}</td>
              <td style="padding:16px 24px; color:var(--text-muted); font-size:13px;">{{ item.warehouse_location }}</td>
              <td style="padding:16px 24px;">
                <span style="font-size:12px; padding:4px 12px; border-radius:20px; font-weight:500;" :style="healthStyle(item)">{{ healthLabel(item) }}</span>
              </td>
            </tr>
            <tr v-if="inventory.length === 0">
              <td colspan="6" style="padding:40px; text-align:center; color:var(--text-muted);">Loading inventory...</td>
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

const inventory = ref([])
const kpis = ref([
  { label: 'Total SKUs', value: '—', color: 'var(--text-primary)' },
  { label: 'Low Stock Items', value: '—', color: '#F59E0B' },
  { label: 'Stockouts', value: '—', color: '#EF4444' },
  { label: 'Inventory Value', value: '$2.4M', color: '#10B981' },
])

function healthLabel(item) {
  if (item.quantity === 0) return 'Stockout'
  if (item.quantity < item.reorder_point) return 'Low Stock'
  return 'Healthy'
}

function healthStyle(item) {
  if (item.quantity === 0) return 'background:rgba(239,68,68,0.15); color:#F87171;'
  if (item.quantity < item.reorder_point) return 'background:rgba(245,158,11,0.15); color:#FCD34D;'
  return 'background:rgba(16,185,129,0.15); color:#10B981;'
}

onMounted(async () => {
  const { data } = await supabase.from('inventory').select('*').order('product_name')
  inventory.value = data || []
  kpis.value[0].value = data?.length.toLocaleString() || '0'
  kpis.value[1].value = data?.filter(i => i.quantity < i.reorder_point && i.quantity > 0).length.toString() || '0'
  kpis.value[2].value = data?.filter(i => i.quantity === 0).length.toString() || '0'
})
</script>