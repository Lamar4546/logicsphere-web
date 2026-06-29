import { defineStore } from 'pinia'
import { supabase } from '../lib/supabase'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('ls_token') || null,
    user: JSON.parse(localStorage.getItem('ls_user') || 'null'),
  }),
  actions: {
    async login(email, password) {
      const { data, error } = await supabase.auth.signInWithPassword({ email, password })
      if (error) throw error
      this.token = data.session.access_token
      this.user = data.user
      localStorage.setItem('ls_token', this.token)
      localStorage.setItem('ls_user', JSON.stringify(data.user))
    },
    async register(email, password) {
      const { data, error } = await supabase.auth.signUp({ email, password })
      if (error) throw error
      return data
    },
    logout() {
      supabase.auth.signOut()
      this.token = null
      this.user = null
      localStorage.removeItem('ls_token')
      localStorage.removeItem('ls_user')
    }
  }
})
