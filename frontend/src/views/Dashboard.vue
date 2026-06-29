<template>
  <Layout>
    <div style="padding:32px; background:var(--bg-primary); min-height:100vh;">

      <!-- Toast -->
      <div v-if="toast" style="position:fixed; top:24px; right:24px; background:var(--accent-green); color:white; padding:12px 20px; border-radius:10px; font-size:13px; font-weight:600; z-index:999; box-shadow:var(--card-shadow);">
        ✓ {{ toast }}
      </div>

      <!-- New Shipment Modal -->
      <div v-if="showModal" style="position:fixed; inset:0; background:rgba(0,0,0,0.7); z-index:998; display:flex; align-items:center; justify-content:center;">
        <div style="background:var(--bg-secondary); border:1px solid var(--border); border-radius:16px; padding:32px; width:480px;">
          <h2 style="color:var(--text-primary); font-size:18px; font-weight:700; margin:0 0 20px;">New Shipment</h2>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:16px;">
            <div v-for="field in modalFields" :key="field.key">
              <label style="color:var(--text-muted); font-size:11px; text-transform:uppercase; display:block; margin-bottom:6px;">{{ field.label }}</label>
              <select v-if="field.options" v-model="newShipment[field.key]"
                style="width:100%; background:var(--bg-primary); border:1px solid var(--border); border-radius:8px; padding:10px 14px; color:var(--text-primary); font-size:13px; outline:none; box-sizing:border-box;">
                <option v-for="o in field.options" :key="o">{{ o }}</option>
              </select>
              <input v-else v-model="newShipment[field.key]" :placeholder="field.placeholder"
                style="width:100%; background:var(--bg-primary); border:1px solid var(--border); border-radius:8px; padding:10px 14px; color:var(--text-primary); font-size:13px; outline:none; box-sizing:border-box;" />
            </div>
          </div>
          <div style="display:flex; gap:12px; justify-content:flex-end;">
            <button @click="showModal = false" style="background:transparent; color:var(--text-secondary); border:1px solid var(--border); padding:10px 20px; border-radius:8px; font-size:13px; cursor:pointer;">Cancel</button>
            <button @click="addShipment" style="background:var(--accent-blue); color:white; border:none; padding:10px 20px; border-radius:8px; font-size:13px; font-weight:600; cursor:pointer;">Add Shipment</button>
          </div>
        </div>
      </div>

      <!-- Header -->
      <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:28px;">
        <div>
          <p style="color:var(--text-muted); font-size:11px; text-transform:uppercase; letter-spacing:0.1em; margin:0 0 4px;">Operational Control</p>
          <h1 style="color:var(--text-primary); font-size:24px; font-weight:700; margin:0;">Control Tower</h1>
        </div>
        <div style="display:flex; align-items:center; gap:12px;">
          <span style="color:var(--text-muted); font-size:11px;">ML MODEL V4.2.1 · EURO-CENTRAL-1 · 24MS</span>
          <button @click="showModal = true" style="background:var(--accent-blue); color:white; border:none; padding:10px 18px; border-radius:8px; font-size:13px; font-weight:600; cursor:pointer;">+ New Shipment</button>
        </div>
      </div>

      <!-- KPI Cards -->
      <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:24px;">
        <div v-for="kpi in kpis" :key="kpi.label" style="background:var(--bg-secondary); border:1px solid var(--border); border-radius:12px; padding:20px;">
          <p style="color:var(--text-secondary); font-size:11px; text-transform:uppercase; letter-spacing:0.08em; margin:0 0 8px;">{{ kpi.label }}</p>
          <p style="color:var(--text-primary); font-size:26px; font-weight:700; margin:0 0 4px;">{{ kpi.value }}</p>
          <p style="font-size:12px; margin:0;" :style="{ color: kpi.changeColor }">{{ kpi.change }}</p>
        </div>
      </div>

      <!-- Main Grid -->
      <div style="display:grid; grid-template-columns:2fr 1fr; gap:20px; margin-bottom:20px;">
        <div style="background:var(--bg-secondary); border:1px solid var(--border); border-radius:12px; padding:24px;">
          <p style="color:var(--text-muted); font-size:11px; text-transform:uppercase; letter-spacing:0.08em; margin:0 0 12px;">Active Route Planner</p>
          <div style="display:flex; align-items:center; gap:24px; margin-bottom:16px;">
            <div>
              <p style="color:var(--text-muted); font-size:11px; margin:0 0 2px;">Origin</p>
              <p style="color:var(--text-primary); font-weight:600; font-size:15px; margin:0;">Port of Rotterdam</p>
            </div>
            <span style="color:var(--text-muted); font-size:20px;">→</span>
            <div>
              <p style="color:var(--text-muted); font-size:11px; margin:0 0 2px;">Target</p>
              <p style="color:var(--text-primary); font-weight:600; font-size:15px; margin:0;">Munich Hub</p>
            </div>
          </div>
          <div ref="mapContainer" style="height:200px; border-radius:10px; margin-bottom:16px; overflow:hidden; border:1px solid var(--border);"></div>
          <div style="background:var(--bg-primary); border:1px solid rgba(59,130,246,0.2); border-radius:10px; padding:14px 16px; display:flex; align-items:center; justify-content:space-between;">
            <div style="display:flex; align-items:center; gap:10px;">
              <span>🤖</span>
              <p style="color:var(--text-secondary); font-size:13px; margin:0;">ML Suggestion: Reroute via A62 to avoid 42min delay in Antwerp</p>
            </div>
            <button @click="applyOptimization" style="background:var(--accent-blue); color:white; border:none; padding:8px 14px; border-radius:8px; font-size:12px; font-weight:600; cursor:pointer; white-space:nowrap; margin-left:12px;">Apply Optimization</button>
          </div>
        </div>

        <div style="background:var(--bg-secondary); border:1px solid var(--border); border-radius:12px; padding:24px;">
          <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:16px;">
            <p style="color:var(--text-primary); font-weight:600; font-size:14px; margin:0;">ML Predictive Delay Alerts</p>
            <span style="background:rgba(59,130,246,0.15); color:#60A5FA; border:1px solid rgba(59,130,246,0.2); padding:3px 10px; border-radius:20px; font-size:11px;">Real-time</span>
          </div>
          <div v-for="alert in alerts" :key="alert.title"
            :style="`background:${alert.type === 'severe' ? 'rgba(239,68,68,0.08)' : 'rgba(245,158,11,0.08)'}; border:1px solid ${alert.type === 'severe' ? 'rgba(239,68,68,0.25)' : 'rgba(245,158,11,0.25)'}; border-radius:10px; padding:14px; margin-bottom:10px;`">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
              <span>{{ alert.type === 'severe' ? '⚠️' : '⚡' }}</span>
              <p :style="`color:${alert.type === 'severe' ? '#F87171' : '#FCD34D'}; font-size:12px; font-weight:700; margin:0;`">{{ alert.title }}</p>
            </div>
            <p style="color:var(--text-secondary); font-size:12px; margin:0;">{{ alert.message }}</p>
          </div>
          <div style="background:var(--bg-primary); border:1px solid var(--border); border-radius:10px; padding:16px; margin-top:8px;">
            <p style="color:var(--text-muted); font-size:11px; text-transform:uppercase; letter-spacing:0.08em; margin:0 0 8px;">Fuel Savings Projection</p>
            <p style="color:var(--text-primary); font-size:28px; font-weight:700; margin:0 0 4px;">-14.2%</p>
            <p style="color:var(--text-muted); font-size:12px; margin:0;">Estimated $12,400 saved this month based on optimized logistics routes.</p>
          </div>
        </div>
      </div>

      <!-- Invoice Table -->
      <div style="background:var(--bg-secondary); border:1px solid var(--border); border-radius:12px; overflow:hidden;">
        <div style="padding:20px 24px; border-bottom:1px solid var(--border);">
          <p style="color:var(--text-primary); font-weight:600; font-size:14px; margin:0;">Automated Invoice Processing</p>
        </div>
        <table style="width:100%; border-collapse:collapse;">
          <thead>
            <tr style="border-bottom:1px solid var(--border);">
              <th style="text-align:left; padding:12px 24px; color:var(--text-muted); font-size:11px; text-transform:uppercase; font-weight:500;">Invoice</th>
              <th style="text-align:left; padding:12px 24px; color:var(--text-muted); font-size:11px; text-transform:uppercase; font-weight:500;">Amount</th>
              <th style="text-align:left; padding:12px 24px; color:var(--text-muted); font-size:11px; text-transform:uppercase; font-weight:500;">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="inv in invoices" :key="inv.id" style="border-bottom:1px solid var(--border);">
              <td style="padding:14px 24px; color:var(--text-secondary); font-family:monospace; font-size:13px;">{{ inv.id }}</td>
              <td style="padding:14px 24px; color:var(--text-primary); font-weight:500;">{{ inv.amount }}</td>
              <td style="padding:14px 24px;">
                <span style="font-size:12px; padding:4px 10px; border-radius:20px; font-weight:500;" :style="statusStyle(inv.status)">{{ inv.status }}</span>
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
import api from '../api'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const mapContainer = ref(null)
const showModal = ref(false)
const toast = ref('')
const alerts = ref([])
const invoices = ref([])
const kpis = ref([
  { label: 'On-Time Rate', value: '98.4%', change: '+2.1% from ML predictive tuning', changeColor: '#10B981' },
  { label: 'Active Routes', value: '1,242', change: 'Global operational network', changeColor: 'var(--text-muted)' },
  { label: 'Inventory Health', value: 'Optimal', change: 'View 3 stock warnings', changeColor: '#F59E0B' },
  { label: 'Pending Invoices', value: '48', change: 'Automated processing active', changeColor: '#60A5FA' },
])

const newShipment = ref({ tracking_number: '', origin: '', destination: '', carrier: '', mode: 'Ocean', status: 'In Transit' })

const modalFields = [
  { key: 'tracking_number', label: 'Tracking #', placeholder: 'LS-2024-005' },
  { key: 'mode', label: 'Mode', options: ['Ocean', 'Air', 'Road', 'Rail'] },
  { key: 'origin', label: 'Origin', placeholder: 'Port of Rotterdam' },
  { key: 'destination', label: 'Destination', placeholder: 'Munich Hub' },
  { key: 'carrier', label: 'Carrier', placeholder: 'Maersk' },
  { key: 'status', label: 'Status', options: ['In Transit', 'Delayed', 'At Customs', 'Delivered'] },
]

function statusStyle(status) {
  return {
    'Processed': 'background:rgba(16,185,129,0.15); color:#10B981;',
    'OCR Reading': 'background:rgba(59,130,246,0.15); color:#60A5FA;',
    'Pending Sync': 'background:rgba(100,116,139,0.15); color:var(--text-secondary);',
    'Flagged': 'background:rgba(239,68,68,0.15); color:#F87171;',
  }[status] || ''
}

function showToast(msg) {
  toast.value = msg
  setTimeout(() => toast.value = '', 3000)
}

function applyOptimization() {
  showToast('Route optimization applied — rerouting via A62')
}

async function addShipment() {
  if (!newShipment.value.tracking_number || !newShipment.value.origin || !newShipment.value.destination) return
  try {
    await api.post('/shipments/', newShipment.value)
    showToast(`Shipment ${newShipment.value.tracking_number} added`)
    showModal.value = false
    newShipment.value = { tracking_number: '', origin: '', destination: '', carrier: '', mode: 'Ocean', status: 'In Transit' }
    await loadData()
  } catch (e) {
    showToast(e.response?.data?.error || 'Could not add shipment')
  }
}

async function loadData() {
  const { data: alertData } = await supabase.from('alerts').select('*').eq('resolved', false).limit(3)
  alerts.value = alertData || [
    { type: 'severe', title: 'SEVERE DELAY HAZARD', message: "Vessel 'Ever-Cloud' arriving 8h late due to weather anomaly." },
    { type: 'warning', title: 'FUEL OPPORTUNITY', message: 'Lower speed for Fleet-34 will reduce consumption.' },
  ]

  const { data: invData } = await supabase.from('freight_invoices').select('*').limit(3)
  invoices.value = invData?.map(i => ({ id: i.invoice_number, amount: `€${i.amount.toLocaleString()}`, status: i.status })) || [
    { id: 'INV-9902', amount: '€4,240.00', status: 'Processed' },
    { id: 'INV-9903', amount: '€1,822.10', status: 'OCR Reading' },
    { id: 'INV-9904', amount: '€12,500.00', status: 'Pending Sync' },
  ]

  const { data: shipmentData } = await api.get('/shipments/')
  if (shipmentData?.length) kpis.value[0].value = shipmentData.length.toLocaleString()
}

onMounted(async () => {
  await loadData()

  const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  const tileUrl = isDark
    ? 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
    : 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png'

  const map = L.map(mapContainer.value, { zoomControl: true }).setView([50.5, 7.5], 5)
  L.tileLayer(tileUrl, { attribution: '© OpenStreetMap © CARTO', subdomains: 'abcd', maxZoom: 19 }).addTo(map)

  const blueIcon = L.divIcon({ className: '', html: '<div style="background:#3B82F6;width:12px;height:12px;border-radius:50%;border:2px solid white;"></div>' })
  const greenIcon = L.divIcon({ className: '', html: '<div style="background:#10B981;width:12px;height:12px;border-radius:50%;border:2px solid white;"></div>' })

  L.marker([51.9225, 4.4792], { icon: blueIcon }).addTo(map).bindPopup('Port of Rotterdam')
  L.marker([48.1351, 11.5820], { icon: greenIcon }).addTo(map).bindPopup('Munich Hub')
  L.polyline([[51.9225, 4.4792],[51.2, 5.5],[50.8, 7.0],[49.5, 9.0],[48.1351, 11.5820]],
    { color: '#3B82F6', weight: 3, dashArray: '6 4' }).addTo(map)

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    map.eachLayer(l => { if (l instanceof L.TileLayer) map.removeLayer(l) })
    L.tileLayer(
      e.matches ? 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png' : 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
      { attribution: '© OpenStreetMap © CARTO', subdomains: 'abcd', maxZoom: 19 }
    ).addTo(map)
  })
})
</script>
