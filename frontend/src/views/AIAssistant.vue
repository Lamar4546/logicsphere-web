<template>
  <Layout>
    <div style="padding:32px; background:var(--bg-primary); height:100vh; display:flex; flex-direction:column; box-sizing:border-box;">
      <div style="margin-bottom:20px; flex-shrink:0;">
        <p style="color:var(--text-muted); font-size:11px; text-transform:uppercase; letter-spacing:0.1em; margin:0 0 4px;">AI Module</p>
        <h1 style="color:var(--text-primary); font-size:24px; font-weight:700; margin:0;">LogiSphere AI Assistant</h1>
        <p style="color:var(--text-secondary); font-size:13px; margin:6px 0 0;">Ask anything about your supply chain</p>
      </div>
      <div v-if="messages.length === 0" style="display:flex; flex-wrap:wrap; gap:8px; margin-bottom:20px; flex-shrink:0;">
        <button v-for="prompt in suggestions" :key="prompt" @click="sendMessage(prompt)"
          style="background:var(--bg-secondary); border:1px solid var(--border); color:var(--text-secondary); font-size:13px; padding:8px 16px; border-radius:20px; cursor:pointer;">
          {{ prompt }}
        </button>
      </div>
      <div ref="chatBox" style="flex:1; overflow-y:auto; margin-bottom:16px; display:flex; flex-direction:column; gap:12px;">
        <div v-for="msg in messages" :key="msg.id" style="display:flex;" :style="msg.role === 'user' ? 'justify-content:flex-end;' : 'justify-content:flex-start;'">
          <div :style="msg.role === 'user'
            ? 'background:var(--accent-blue); color:white; padding:12px 16px; border-radius:16px 16px 4px 16px; max-width:70%; font-size:14px; line-height:1.5;'
            : 'background:var(--bg-secondary); border:1px solid var(--border); color:var(--text-secondary); padding:12px 16px; border-radius:16px 16px 16px 4px; max-width:70%; font-size:14px; line-height:1.5;'">
            <p v-if="msg.role === 'assistant'" style="color:#10B981; font-size:11px; font-weight:600; margin:0 0 6px;">🤖 LogiSphere AI</p>
            <p style="margin:0; white-space:pre-wrap;">{{ msg.content }}</p>
          </div>
        </div>
        <div v-if="loading" style="display:flex; justify-content:flex-start;">
          <div style="background:var(--bg-secondary); border:1px solid var(--border); padding:14px 18px; border-radius:16px 16px 16px 4px; display:flex; gap:6px; align-items:center;">
            <span v-for="i in 3" :key="i" style="width:8px; height:8px; background:var(--text-muted); border-radius:50%; display:inline-block; animation:bounce 1s infinite;"
              :style="`animation-delay:${(i-1)*0.15}s`"></span>
          </div>
        </div>
      </div>
      <div style="display:flex; gap:12px; flex-shrink:0;">
        <input v-model="input" @keydown.enter="sendMessage()"
          placeholder="Ask about shipments, costs, delays, routes..."
          style="flex:1; background:var(--bg-secondary); border:1px solid var(--border); border-radius:10px; padding:14px 18px; color:var(--text-primary); font-size:14px; outline:none; box-sizing:border-box;" />
        <button @click="sendMessage()" :disabled="loading || !input.trim()"
          style="background:var(--accent-blue); color:white; border:none; padding:14px 24px; border-radius:10px; font-size:14px; font-weight:600; cursor:pointer;"
          :style="{ opacity: (loading || !input.trim()) ? 0.5 : 1 }">
          Send
        </button>
      </div>
    </div>
  </Layout>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import Layout from '../components/Layout.vue'
import api from '../api'

const input = ref('')
const messages = ref([])
const loading = ref(false)
const chatBox = ref(null)

const suggestions = [
  'How can I reduce freight costs by 15%?',
  'Which shipments are at risk of delay?',
  'Summarize my current inventory health',
  'Best route from Rotterdam to Munich?',
]

async function sendMessage(text) {
  const content = text || input.value.trim()
  if (!content) return
  messages.value.push({ id: Date.now(), role: 'user', content })
  input.value = ''
  loading.value = true
  await scrollToBottom()
  try {
    const { data } = await api.post('/ai/chat', { message: content })
    messages.value.push({ id: Date.now() + 1, role: 'assistant', content: data.reply })
  } catch (e) {
    const error = e.response?.data?.error || 'Connection error. Please try again.'
    messages.value.push({ id: Date.now() + 1, role: 'assistant', content: error })
  } finally {
    loading.value = false
    await scrollToBottom()
  }
}

async function scrollToBottom() {
  await nextTick()
  if (chatBox.value) chatBox.value.scrollTop = chatBox.value.scrollHeight
}
</script>

<style scoped>
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}
</style>
