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
    url: config.supabaseUrl,
    anonKey: config.supabaseAnonKey,
  };
}

/**
 * Get Supabase client instance
 */
export function getSupabase() {
  const { url, anonKey } = getSupabaseConfig();
  return createClient(url, anonKey);
}
