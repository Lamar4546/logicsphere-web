import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

import Login from '../views/login.vue'
import Dashboard from '../views/Dashboard.vue'
import Shipments from '../views/Shipments.vue'
import Routes from '../views/Routes.vue'
import AIAssistant from '../views/AIAssistant.vue'
import Inventory from '../views/Inventory.vue'
import Warehouse from '../views/Warehouse.vue'
import Customs from '../views/Customs.vue'
import Finance from '../views/Finance.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', component: Login },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/shipments', component: Shipments, meta: { requiresAuth: true } },
  { path: '/routes', component: Routes, meta: { requiresAuth: true } },
  { path: '/ai-assistant', component: AIAssistant, meta: { requiresAuth: true } },
  { path: '/inventory', component: Inventory, meta: { requiresAuth: true } },
  { path: '/warehouse', component: Warehouse, meta: { requiresAuth: true } },
  { path: '/customs', component: Customs, meta: { requiresAuth: true } },
  { path: '/finance', component: Finance, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.token) {
    return '/login'
  }
})

export default router