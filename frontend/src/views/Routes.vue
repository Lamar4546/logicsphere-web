<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import Layout from '../components/Layout.vue'
import api from '../api'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const origin = ref('Port of Rotterdam')
const destination = ref('Munich Hub')
const selectedRoute = ref(null)
const routes = ref([])
const optimizing = ref(false)
const applying = ref(false)
const mapContainer = ref(null)
const errorMsg = ref('')
const toast = ref('')
const shipmentForm = ref({
  tracking_number: `LS-${Date.now().toString().slice(-6)}`,
  carrier: '',
  mode: 'Ocean',
})

let map = null
let routeLayer = null

function showToast(message) {
  toast.value = message
  setTimeout(() => toast.value = '', 3000)
}

function resetTrackingNumber() {
  shipmentForm.value.tracking_number = `LS-${Date.now().toString().slice(-6)}`
}

function clearRouteLayers() {
  if (!map) return
  if (routeLayer) {
    map.removeLayer(routeLayer)
    routeLayer = null
  }
  map.eachLayer(layer => {
    if (layer instanceof L.Marker || layer instanceof L.Polyline) {
      map.removeLayer(layer)
    }
  })
}

function drawRoute(route) {
  if (!map || !route?.coordinates?.length) return

  clearRouteLayers()
  const coordinates = route.coordinates.map(point => [point[0], point[1]])
  const originCoords = coordinates[0]
  const destinationCoords = coordinates[coordinates.length - 1]

  const originIcon = L.divIcon({
    className: '',
    html: '<div style="background:#3B82F6;width:12px;height:12px;border-radius:50%;border:2px solid #fff;"></div>',
  })

  const destIcon = L.divIcon({
    className: '',
    html: '<div style="background:#10B981;width:12px;height:12px;border-radius:50%;border:2px solid #fff;"></div>',
  })

  L.marker(originCoords, { icon: originIcon }).addTo(map).bindPopup(route.origin)
  L.marker(destinationCoords, { icon: destIcon }).addTo(map).bindPopup(route.destination)

  routeLayer = L.polyline(coordinates, {
    color: route.color || '#3B82F6',
    weight: 4,
    dashArray: route.type === 'lowest_cost' ? '8 6' : null,
  }).addTo(map)

  map.fitBounds(L.latLngBounds(coordinates), { padding: [44, 44] })
}

function selectRoute(route) {
  selectedRoute.value = route
  drawRoute(route)
}

async function optimize() {
  if (!origin.value.trim() || !destination.value.trim()) {
    errorMsg.value = 'Enter an origin and destination'
    return
  }

  optimizing.value = true
  errorMsg.value = ''

  try {
    const { data } = await api.post('/routes/optimize', {
      origin: origin.value,
      destination: destination.value,
    })
    routes.value = data.routes || []
    selectRoute(data.recommended || routes.value[0])
  } catch (e) {
    errorMsg.value = e.response?.data?.error || 'Could not optimize that route'
  } finally {
    optimizing.value = false
  }
}

async function applyShipment() {
  if (!selectedRoute.value) {
    errorMsg.value = 'Optimize and select a route first'
    return
  }
  if (!shipmentForm.value.tracking_number.trim()) {
    errorMsg.value = 'Tracking number is required'
    return
  }

  applying.value = true
  errorMsg.value = ''

  try {
    await api.post('/shipments/', {
      tracking_number: shipmentForm.value.tracking_number,
      origin: selectedRoute.value.origin,
      destination: selectedRoute.value.destination,
      carrier: shipmentForm.value.carrier || `LogiSphere ${selectedRoute.value.label}`,
      mode: shipmentForm.value.mode,
      status: 'In Transit',
    })
    showToast(`Shipment ${shipmentForm.value.tracking_number} added`)
    resetTrackingNumber()
  } catch (e) {
    errorMsg.value = e.response?.data?.error || 'Could not add optimized shipment'
  } finally {
    applying.value = false
  }
}

onMounted(async () => {
  await nextTick()

  if (!mapContainer.value) return

  map = L.map(mapContainer.value, { zoomControl: true }).setView([20, 0], 2)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap',
    maxZoom: 19,
  }).addTo(map)

  await optimize()
})

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
  }
})
</script>

<template>
  <Layout>
    <div style="padding:32px; background:var(--bg-primary); min-height:100vh;">
      <div v-if="toast" style="position:fixed; top:24px; right:24px; background:var(--accent-green); color:white; padding:12px 20px; border-radius:10px; font-size:13px; font-weight:600; z-index:999;">
        {{ toast }}
      </div>

      <div style="margin-bottom:24px;">
        <p style="color:var(--text-muted); font-size:11px; text-transform:uppercase; letter-spacing:0.1em; margin:0 0 4px;">Module 2</p>
        <h1 style="color:var(--text-primary); font-size:24px; font-weight:700; margin:0;">Route Optimization</h1>
      </div>

      <div style="display:grid; grid-template-columns:360px 1fr; gap:20px; align-items:start;">
        <div style="display:flex; flex-direction:column; gap:16px;">
          <div style="background:var(--bg-secondary); border:1px solid var(--border); border-radius:12px; padding:20px;">
            <label style="color:var(--text-muted); font-size:11px; text-transform:uppercase; display:block; margin-bottom:6px;">Origin</label>
            <input v-model="origin" placeholder="Kingston, Jamaica" style="width:100%; background:var(--bg-primary); border:1px solid var(--border); border-radius:8px; padding:11px 14px; color:var(--text-primary); font-size:13px; outline:none; margin-bottom:12px;" />

            <label style="color:var(--text-muted); font-size:11px; text-transform:uppercase; display:block; margin-bottom:6px;">Destination</label>
            <input v-model="destination" placeholder="Tokyo, Japan" style="width:100%; background:var(--bg-primary); border:1px solid var(--border); border-radius:8px; padding:11px 14px; color:var(--text-primary); font-size:13px; outline:none; margin-bottom:14px;" />

            <button @click="optimize" :disabled="optimizing" style="width:100%; background:var(--accent-blue); color:white; border:none; padding:12px 18px; border-radius:8px; font-size:13px; font-weight:600; cursor:pointer;" :style="{ opacity: optimizing ? 0.65 : 1 }">
              {{ optimizing ? 'Optimizing...' : 'Optimize Route' }}
            </button>

            <p v-if="errorMsg" style="color:#F87171; font-size:13px; line-height:1.5; margin:12px 0 0;">{{ errorMsg }}</p>
          </div>

          <div v-if="selectedRoute" style="background:var(--bg-secondary); border:1px solid var(--border); border-radius:12px; padding:20px;">
            <p style="color:var(--text-primary); font-weight:600; font-size:14px; margin:0 0 14px;">Apply Optimized Shipment</p>

            <label style="color:var(--text-muted); font-size:11px; text-transform:uppercase; display:block; margin-bottom:6px;">Tracking #</label>
            <input v-model="shipmentForm.tracking_number" style="width:100%; background:var(--bg-primary); border:1px solid var(--border); border-radius:8px; padding:10px 12px; color:var(--text-primary); font-size:13px; outline:none; margin-bottom:12px;" />

            <label style="color:var(--text-muted); font-size:11px; text-transform:uppercase; display:block; margin-bottom:6px;">Carrier</label>
            <input v-model="shipmentForm.carrier" placeholder="Auto assign" style="width:100%; background:var(--bg-primary); border:1px solid var(--border); border-radius:8px; padding:10px 12px; color:var(--text-primary); font-size:13px; outline:none; margin-bottom:12px;" />

            <label style="color:var(--text-muted); font-size:11px; text-transform:uppercase; display:block; margin-bottom:6px;">Mode</label>
            <select v-model="shipmentForm.mode" style="width:100%; background:var(--bg-primary); border:1px solid var(--border); border-radius:8px; padding:10px 12px; color:var(--text-primary); font-size:13px; outline:none; margin-bottom:14px;">
              <option>Ocean</option>
              <option>Air</option>
              <option>Road</option>
              <option>Rail</option>
            </select>

            <button @click="applyShipment" :disabled="applying" style="width:100%; background:var(--accent-green); color:white; border:none; padding:12px 18px; border-radius:8px; font-size:13px; font-weight:600; cursor:pointer;" :style="{ opacity: applying ? 0.65 : 1 }">
              {{ applying ? 'Adding...' : 'Apply as Shipment' }}
            </button>
          </div>

          <div v-if="routes.length" style="display:flex; flex-direction:column; gap:10px;">
            <button v-for="route in routes" :key="route.id" @click="selectRoute(route)"
              style="text-align:left; background:var(--bg-secondary); border:1px solid var(--border); border-radius:12px; padding:16px; cursor:pointer;"
              :style="selectedRoute?.id === route.id ? `border-color:${route.color}; box-shadow:0 0 0 1px ${route.color};` : ''">
              <div style="display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:10px;">
                <span style="color:var(--text-primary); font-size:14px; font-weight:700;">{{ route.icon }} {{ route.label }}</span>
                <span style="color:var(--text-muted); font-size:12px;">{{ route.eta }}</span>
              </div>
              <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:10px;">
                <span style="color:var(--text-secondary); font-size:12px;">Cost: ${{ route.cost?.toLocaleString() }}</span>
                <span style="color:var(--text-secondary); font-size:12px;">CO2: {{ route.carbon_kg?.toLocaleString() }} kg</span>
              </div>
              <p style="color:var(--text-muted); font-size:12px; line-height:1.45; margin:0;">{{ route.ai_suggestion }}</p>
            </button>
          </div>
        </div>

        <div ref="mapContainer" style="height:calc(100vh - 128px); min-height:520px; border:1px solid var(--border); border-radius:12px; overflow:hidden; background:var(--bg-secondary);"></div>
      </div>
    </div>
  </Layout>
</template>
