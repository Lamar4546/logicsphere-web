<template>
  <div style="min-height:100vh; background:var(--bg-primary); display:flex; align-items:center; justify-content:center; font-family:sans-serif;">
    <div style="width:100%; max-width:420px; padding:0 20px;">
      <div style="text-align:center; margin-bottom:32px;">
        <img src="@/assets/logo.png" alt="LogiSphere AI" style="height:80px; object-fit:contain;" />
      </div>
      <div style="background:var(--bg-secondary); border:1px solid var(--border); border-radius:16px; padding:32px;">
        <h2 style="color:var(--text-primary); font-size:20px; font-weight:600; margin:0 0 4px;">Welcome back</h2>
        <p style="color:var(--text-secondary); font-size:14px; margin:0 0 24px;">Sign in to your LogiSphere dashboard</p>
        <div v-if="error" style="background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3); color:#F87171; font-size:13px; border-radius:8px; padding:10px 14px; margin-bottom:16px;">
          {{ error }}
        </div>
        <div style="margin-bottom:16px;">
          <label style="color:var(--text-muted); font-size:12px; display:block; margin-bottom:6px; text-transform:uppercase; letter-spacing:0.05em;">Email</label>
          <input v-model="email" type="email" placeholder="you@company.com"
            style="width:100%; background:var(--bg-primary); border:1px solid var(--border); border-radius:10px; padding:12px 16px; color:var(--text-primary); font-size:14px; outline:none; box-sizing:border-box;" />
        </div>
        <div style="margin-bottom:24px;">
          <label style="color:var(--text-muted); font-size:12px; display:block; margin-bottom:6px; text-transform:uppercase; letter-spacing:0.05em;">Password</label>
          <input v-model="password" type="password" placeholder="••••••••" @keydown.enter="handleLogin"
            style="width:100%; background:var(--bg-primary); border:1px solid var(--border); border-radius:10px; padding:12px 16px; color:var(--text-primary); font-size:14px; outline:none; box-sizing:border-box;" />
        </div>
        <button @click="handleLogin" :disabled="loading"
          style="width:100%; background:var(--accent-blue); color:white; font-size:15px; font-weight:600; padding:13px; border:none; border-radius:10px; cursor:pointer;"
          :style="{ opacity: loading ? 0.6 : 1 }">
          {{ loading ? 'Signing in...' : 'Sign In' }}
        </button>
        <div style="display:flex; align-items:center; gap:12px; margin:20px 0;">
          <div style="flex:1; height:1px; background:var(--border);"></div>
          <span style="color:var(--text-muted); font-size:12px;">or</span>
          <div style="flex:1; height:1px; background:var(--border);"></div>
        </div>
        <button @click="handleRegister" :disabled="loading"
          style="width:100%; background:transparent; color:var(--text-secondary); font-size:14px; font-weight:500; padding:12px; border:1px solid var(--border); border-radius:10px; cursor:pointer;">
          Create an account
        </button>
      </div>
      <p style="text-align:center; color:var(--text-muted); font-size:12px; margin-top:24px;">
        © 2025 LogiSphere AI. Intelligent Global Logistics.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  if (!email.value || !password.value) { error.value = 'Please enter your email and password'; return }
  loading.value = true; error.value = ''
  try {
    await auth.login(email.value, password.value)
    router.push('/dashboard')
  } catch (e) {
    error.value = e.message || 'Invalid email or password'
  } finally { loading.value = false }
}

async function handleRegister() {
  if (!email.value || !password.value) { error.value = 'Please enter an email and password'; return }
  if (password.value.length < 6) { error.value = 'Password must be at least 6 characters'; return }
  loading.value = true; error.value = ''
  try {
    await auth.register(email.value, password.value)
    await auth.login(email.value, password.value)
    router.push('/dashboard')
  } catch (e) {
    error.value = e.message || 'Registration failed'
  } finally { loading.value = false }
}
</script>