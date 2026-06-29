<template>
  <div style="display:flex; min-height:100vh; background:#0F172A;">
    <Sidebar />
    <main style="flex:1; overflow:auto;">
      <slot />
    </main>

    <div v-if="showTutorial" style="position:fixed; inset:0; background:rgba(2,6,23,0.78); z-index:1200; display:flex; align-items:center; justify-content:center; padding:24px;">
      <div style="width:100%; max-width:520px; background:#1E293B; border:1px solid rgba(255,255,255,0.1); border-radius:16px; padding:28px; box-shadow:0 24px 80px rgba(0,0,0,0.45);">
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:16px;">
          <span style="color:#60A5FA; font-size:11px; text-transform:uppercase; letter-spacing:0.1em; font-weight:700;">Step {{ tutorialIndex + 1 }} of {{ tutorialSteps.length }}</span>
          <button @click="finishTutorial" style="background:transparent; color:#64748B; border:none; cursor:pointer; font-size:13px;">Skip</button>
        </div>
        <h2 style="color:white; font-size:22px; font-weight:700; margin:0 0 10px;">{{ currentStep.title }}</h2>
        <p style="color:#CBD5E1; font-size:14px; line-height:1.6; margin:0 0 22px;">{{ currentStep.body }}</p>
        <div style="display:flex; gap:8px; margin-bottom:22px;">
          <span v-for="(_, index) in tutorialSteps" :key="index" :style="`height:4px; flex:1; border-radius:999px; background:${index <= tutorialIndex ? '#3B82F6' : 'rgba(255,255,255,0.12)'};`"></span>
        </div>
        <div style="display:flex; justify-content:space-between; gap:12px;">
          <button @click="previousStep" :disabled="tutorialIndex === 0" style="background:transparent; color:#94A3B8; border:1px solid rgba(255,255,255,0.1); padding:10px 16px; border-radius:8px; font-size:13px; cursor:pointer;" :style="{ opacity: tutorialIndex === 0 ? 0.45 : 1 }">Back</button>
          <button @click="nextStep" style="background:#2563EB; color:white; border:none; padding:10px 18px; border-radius:8px; font-size:13px; font-weight:700; cursor:pointer;">{{ tutorialIndex === tutorialSteps.length - 1 ? 'Start Working' : 'Next' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import Sidebar from './Sidebar.vue'

const tutorialIndex = ref(0)
const showTutorial = ref(false)

const tutorialSteps = [
  {
    title: 'Welcome to LogiSphere',
    body: 'Start in the control tower for a quick view of shipments, route risks, cost signals, and operational alerts.',
  },
  {
    title: 'Create and Track Shipments',
    body: 'Use Shipment Visibility to add a shipment, then watch it appear at the top of the list with its current status and ETA.',
  },
  {
    title: 'Optimize Routes',
    body: 'Open Route Optimization, enter an origin and destination, then compare the fastest, lowest-cost, and lowest-carbon routes on the map.',
  },
  {
    title: 'Ask the Assistant',
    body: 'Use the AI Assistant for logistics questions, shipment summaries, route ideas, and operational recommendations.',
  },
]

const currentStep = computed(() => tutorialSteps[tutorialIndex.value])

function finishTutorial() {
  showTutorial.value = false
  localStorage.removeItem('ls_show_tutorial')
  localStorage.setItem('ls_tutorial_done', 'true')
}

function nextStep() {
  if (tutorialIndex.value === tutorialSteps.length - 1) {
    finishTutorial()
    return
  }
  tutorialIndex.value += 1
}

function previousStep() {
  if (tutorialIndex.value > 0) tutorialIndex.value -= 1
}

onMounted(() => {
  showTutorial.value = localStorage.getItem('ls_show_tutorial') === 'true' && localStorage.getItem('ls_tutorial_done') !== 'true'
})
</script>
