import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://kvmqnfhhnirqscvpthti.supabase.co'
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bXFuZmhobmlycXNjdnB0aHRpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI1MjA1MzcsImV4cCI6MjA5ODA5NjUzN30.MC4Gzm5dvSs0Fs0R4DX_fTzS7pc8P4zYBBUofwQ1xms'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
