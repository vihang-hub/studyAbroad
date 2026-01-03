/**
 * Supabase client for frontend
 * Provides Supabase configuration and client
 */

import { createClient } from '@supabase/supabase-js';
import { getConfig } from './config';

/**
 * Get Supabase configuration
 */
export function getSupabaseConfig() {
  const config = getConfig();
  return {
    url: config.SUPABASE_URL,
    anonKey: config.SUPABASE_ANON_KEY,
  };
}

/**
 * Get Supabase client instance
 * @throws Error if Supabase is not configured
 */
export function getSupabase() {
  const { url, anonKey } = getSupabaseConfig();
  if (!url || !anonKey) {
    throw new Error('Supabase is not configured. Set SUPABASE_URL and SUPABASE_ANON_KEY.');
  }
  return createClient(url, anonKey);
}
