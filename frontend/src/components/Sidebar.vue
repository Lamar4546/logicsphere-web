<template>
  <aside style="width:220px; min-height:100vh; background:var(--bg-secondary); border-right:1px solid var(--border); display:flex; flex-direction:column; flex-shrink:0;">
    <div style="padding:20px; border-bottom:1px solid var(--border);">
      <img src="@/assets/logo.png" alt="LogiSphere AI" style="height:36px; object-fit:contain;" />
    </div>
    <div style="padding:20px 20px 8px;">
      <span style="color:var(--text-muted); font-size:10px; font-weight:600; text-transform:uppercase; letter-spacing:0.1em;">Operational Control</span>
    </div>
    <nav style="flex:1; padding:0 10px;">
      <router-link
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        style="display:flex; align-items:center; gap:10px; padding:10px 12px; border-radius:8px; text-decoration:none; margin-bottom:2px; font-size:13px; color:var(--text-secondary); transition:all 0.15s;"
        active-class="active-nav"
      >
        <span style="font-size:16px;">{{ item.icon }}</span>
        {{ item.label }}
      </router-link>
    </nav>
    <div style="padding:16px; border-top:1px solid var(--border);">
      <div style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.2); border-radius:8px; padding:8px 12px; margin-bottom:12px; display:flex; align-items:center; gap:8px;">
        <span style="width:6px; height:6px; background:#10B981; border-radius:50%; display:inline-block;"></span>
        <span style="color:#10B981; font-size:11px; font-weight:600;">LIVE ML SYNC ACTIVE</span>
      </div>
      <div style="display:flex; align-items:center; justify-content:space-between; padding:0 4px;">
        <div>
          <p style="color:var(--text-primary); font-size:13px; font-weight:500; margin:0;">{{ auth.user?.email?.split('@')[0] }}</p>
          <p style="color:var(--text-muted); font-size:11px; margin:0;">Administrator</p>
        </div>
        <button @click="handleLogout" style="background:none; border:none; color:var(--text-muted); font-size:12px; cursor:pointer;">Logout</button>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const navItems = [
  { path: '/dashboard', label: 'Dashboard', icon: '⊞' },
  { path: '/shipments', label: 'Shipment Visibility', icon: '🚢' },
  { path: '/routes', label: 'Route Optimization', icon: '🗺️' },
  { path: '/ai-assistant', label: 'AI Assistant', icon: '🤖' },
  { path: '/inventory', label: 'Inventory Engine', icon: '📦' },
  { path: '/warehouse', label: 'Warehouse', icon: '🏭' },
  { path: '/customs', label: 'Customs Compliance', icon: '📋' },
  { path: '/finance', label: 'Finance Hub', icon: '💰' },
]

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
a { color: var(--text-secondary); }
a:hover { background: var(--border); color: var(--text-primary); }
a.active-nav { background: rgba(59,130,246,0.15); color: #60A5FA; }
</style>