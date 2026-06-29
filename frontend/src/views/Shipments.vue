<template>
  <Layout>
    <div style="padding:32px; background:var(--bg-primary); min-height:100vh;">

      <!-- Toast -->
      <div v-if="toast" style="position:fixed; top:24px; right:24px; background:var(--accent-green); color:white; padding:12px 20px; border-radius:10px; font-size:13px; font-weight:600; z-index:999;">
        ✓ {{ toast }}
      </div>
      <div v-if="error" style="position:fixed; top:24px; right:24px; background:#EF4444; color:white; padding:12px 20px; border-radius:10px; font-size:13px; font-weight:600; z-index:999;">
        {{ error }}
      </div>

      <!-- Modal -->
      <div v-if="showModal" style="position:fixed; inset:0; background:rgba(0,0,0,0.7); z-index:998; display:flex; align-items:center; justify-content:center;">
        <div style="background:var(--bg-secondary); border:1px solid var(--border); border-radius:16px; padding:32px; width:480px;">
          <h2 style="color:var(--text-primary); font-size:18px; font-weight:700; margin:0 0 20px;">Add Shipment</h2>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:20px;">
            <div v-for="field in modalFields" :key="field.key">
              <label style="color:var(--text-muted); font-size:11px; text-transform:uppercase; display:block; margin-bottom:6px;">{{ field.label }}</label>
              <select v-if="field.options" v-model="form[field.key]"
                style="width:100%; background:var(--bg-primary); border:1px solid var(--border); border-radius:8px; padding:10px 14px; color:var(--text-primary); font-size:13px; outline:none; box-sizing:border-box;">
                <option v-for="o in field.options" :key="o">{{ o }}</option>
              </select>
              <input v-else v-model="form[field.key]" :placeholder="field.placeholder"
                style="width:100%; background:var(--bg-primary); border:1px solid var(--border); border-radius:8px; padding:10px 14px; color:var(--text-primary); font-size:13px; outline:none; box-sizing:border-box;" />
            </div>
          </div>
          <div style="display:flex; gap:12px; justify-content:flex-end;">
            <button @click="showModal = false" style="background:transparent; color:var(--text-secondary); border:1px solid var(--border); padding:10px 20px; border-radius:8px; font-size:13px; cursor:pointer;">Cancel</button>
            <button @click="submitShipment" style="background:var(--accent-blue); color:white; border:none; padding:10px 20px; border-radius:8px; font-size:13px; font-weight:600; cursor:pointer;">Add Shipment</button>
          </div>
        </div>
      </div>

      <!-- Header -->
      <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:28px;">
        <div>
          <p style="color:var(--text-muted); font-size:11px; text-transform:uppercase; letter-spacing:0.1em; margin:0 0 4px;">Module 1</p>
          <h1 style="color:var(--text-primary); font-size:24px; font-weight:700; margin:0;">Shipment Visibility</h1>
        </div>
        <button @click="showModal = true" style="background:var(--accent-blue); color:white; border:none; padding:10px 18px; border-radius:8px; font-size:13px; font-weight:600; cursor:pointer;">+ Add Shipment</button>
      </div>

      <!-- Filters -->
      <div style="display:flex; gap:8px; margin-bottom:20px;">
        <button v-for="f in filters" :key="f" @click="setFilter(f)"
          :style="activeFilter === f
            ? 'background:var(--accent-blue); color:white; border:1px solid var(--accent-blue); padding:6px 16px; border-radius:20px; font-size:12px; font-weight:500; cursor:pointer;'
            : 'background:transparent; color:var(--text-muted); border:1px solid var(--border); padding:6px 16px; border-radius:20px; font-size:12px; cursor:pointer;'">
          {{ f }}
          <span v-if="f !== 'All'" style="margin-left:4px; opacity:0.7;">({{ countByStatus(f) }})</span>
        </button>
      </div>

      <!-- Table -->
      <div style="background:var(--bg-secondary); border:1px solid var(--border); border-radius:12px; overflow:hidden;">
        <table style="width:100%; border-collapse:collapse;">
          <thead>
            <tr style="border-bottom:1px solid var(--border);">
              <th v-for="h in ['Tracking #','Route','Mode','Carrier','ETA','Status','Actions']" :key="h"
                style="text-align:left; padding:14px 24px; color:var(--text-muted); font-size:11px; text-transform:uppercase; font-weight:500;">{{ h }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in filteredShipments" :key="s.id" style="border-bottom:1px solid var(--border);">
              <td style="padding:16px 24px; color:#60A5FA; font-family:monospace; font-size:13px;">{{ s.tracking_number }}</td>
              <td style="padding:16px 24px; color:var(--text-secondary); font-size:13px;">{{ s.origin }} → {{ s.destination }}</td>
              <td style="padding:16px 24px; color:var(--text-secondary); font-size:13px;">{{ modeIcon(s.mode) }} {{ s.mode }}</td>
              <td style="padding:16px 24px; color:var(--text-secondary); font-size:13px;">{{ s.carrier }}</td>
              <td style="padding:16px 24px; color:var(--text-muted); font-size:13px;">{{ formatEta(s.eta) }}</td>
              <td style="padding:16px 24px;">
                <span style="font-size:12px; padding:4px 12px; border-radius:20px; font-weight:500;" :style="statusStyle(s.status)">{{ s.status }}</span>
              </td>
              <td style="padding:16px 24px;">
                <button @click="markDelivered(s)" style="background:transparent; color:#60A5FA; border:1px solid rgba(59,130,246,0.2); padding:5px 12px; border-radius:6px; font-size:11px; cursor:pointer; margin-right:6px;">Mark Delivered</button>
                <button v-if="s.status === 'Delivered'" @click="archiveShipment(s)" style="background:transparent; color:#F59E0B; border:1px solid rgba(245,158,11,0.25); padding:5px 12px; border-radius:6px; font-size:11px; cursor:pointer; margin-right:6px;">Archive</button>
                <button @click="deleteShipment(s)" style="background:transparent; color:#F87171; border:1px solid rgba(239,68,68,0.2); padding:5px 12px; border-radius:6px; font-size:11px; cursor:pointer;">Remove</button>
              </td>
            </tr>
            <tr v-if="filteredShipments.length === 0">
              <td colspan="7" style="padding:40px; text-align:center; color:var(--text-muted); font-size:14px;">No shipments found</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </Layout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Layout from '../components/Layout.vue'
import api from '../api'

const showModal = ref(false)
const toast = ref('')
const error = ref('')
const activeFilter = ref('All')
const filters = ['All', 'In Transit', 'Delayed', 'At Customs', 'Delivered', 'Archived']
const shipments = ref([])

const form = ref({ tracking_number: '', origin: '', destination: '', carrier: '', mode: 'Ocean', status: 'In Transit' })

const modalFields = [
  { key: 'tracking_number', label: 'Tracking #', placeholder: 'LS-2024-005' },
  { key: 'mode', label: 'Mode', options: ['Ocean', 'Air', 'Road', 'Rail'] },
  { key: 'origin', label: 'Origin', placeholder: 'Port of Rotterdam' },
  { key: 'destination', label: 'Destination', placeholder: 'Munich Hub' },
  { key: 'carrier', label: 'Carrier', placeholder: 'Maersk' },
  { key: 'status', label: 'Status', options: ['In Transit', 'Delayed', 'At Customs', 'Delivered'] },
]

const filteredShipments = computed(() =>
  activeFilter.value === 'All' ? shipments.value : shipments.value.filter(s => s.status === activeFilter.value)
)

function countByStatus(status) { return shipments.value.filter(s => s.status === status).length }
function modeIcon(mode) { return { Ocean: '🚢', Air: '✈️', Road: '🚛', Rail: '🚂' }[mode] || '📦' }
function formatEta(eta) { if (!eta) return '—'; return new Date(eta).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) }

function statusStyle(status) {
  return {
    'In Transit': 'background:rgba(59,130,246,0.15); color:#60A5FA;',
    'Delayed': 'background:rgba(239,68,68,0.15); color:#F87171;',
    'At Customs': 'background:rgba(245,158,11,0.15); color:#FCD34D;',
    'Delivered': 'background:rgba(16,185,129,0.15); color:#10B981;',
    'Archived': 'background:rgba(100,116,139,0.15); color:var(--text-secondary);',
  }[status] || ''
}

function showToast(msg) { toast.value = msg; setTimeout(() => toast.value = '', 3000) }
function showError(msg) { error.value = msg; setTimeout(() => error.value = '', 4500) }
async function setFilter(filter) {
  activeFilter.value = filter
  await loadShipments()
}

async function loadShipments() {
  try {
    const { data } = await api.get('/shipments/', { params: { include_archived: activeFilter.value === 'Archived' ? 'true' : undefined } })
    shipments.value = data || []
  } catch (e) {
    showError(e.response?.data?.error || 'Could not load shipments')
  }
}

async function submitShipment() {
  if (!form.value.tracking_number || !form.value.origin || !form.value.destination) {
    showError('Tracking number, origin, and destination are required')
    return
  }

  try {
    await api.post('/shipments/', form.value)
    showToast(`Shipment ${form.value.tracking_number} added`)
    showModal.value = false
    form.value = { tracking_number: '', origin: '', destination: '', carrier: '', mode: 'Ocean', status: 'In Transit' }
    await loadShipments()
  } catch (e) {
    showError(e.response?.data?.error || 'Could not add shipment')
  }
}

async function markDelivered(s) {
  try {
    const { data } = await api.patch(`/shipments/${s.id}`, { status: 'Delivered' })
    Object.assign(s, data)
    showToast(`${s.tracking_number} marked as Delivered`)
  } catch (e) {
    showError(e.response?.data?.error || 'Could not update shipment')
  }
}

async function archiveShipment(s) {
  try {
    await api.post(`/shipments/${s.id}/archive`)
    shipments.value = shipments.value.filter(x => x.id !== s.id)
    showToast(`${s.tracking_number} archived`)
  } catch (e) {
    showError(e.response?.data?.error || 'Could not archive shipment')
  }
}

async function deleteShipment(s) {
  try {
    await api.delete(`/shipments/${s.id}`)
    shipments.value = shipments.value.filter(x => x.id !== s.id)
    showToast(`${s.tracking_number} removed`)
  } catch (e) {
    showError(e.response?.data?.error || 'Could not remove shipment')
  }
}

onMounted(loadShipments)
</script>
