/**
 * Portable Supabase client initialization
 * Configurable via environment variables for different projects
 */
// @ts-nocheck
function stryNS_9fa48() {
  var g = typeof globalThis === 'object' && globalThis && globalThis.Math === Math && globalThis || new Function("return this")();
  var ns = g.__stryker__ || (g.__stryker__ = {});
  if (ns.activeMutant === undefined && g.process && g.process.env && g.process.env.__STRYKER_ACTIVE_MUTANT__) {
    ns.activeMutant = g.process.env.__STRYKER_ACTIVE_MUTANT__;
  }
  function retrieveNS() {
    return ns;
  }
  stryNS_9fa48 = retrieveNS;
  return retrieveNS();
}
stryNS_9fa48();
function stryCov_9fa48() {
  var ns = stryNS_9fa48();
  var cov = ns.mutantCoverage || (ns.mutantCoverage = {
    static: {},
    perTest: {}
  });
  function cover() {
    var c = cov.static;
    if (ns.currentTestId) {
      c = cov.perTest[ns.currentTestId] = cov.perTest[ns.currentTestId] || {};
    }
    var a = arguments;
    for (var i = 0; i < a.length; i++) {
      c[a[i]] = (c[a[i]] || 0) + 1;
    }
  }
  stryCov_9fa48 = cover;
  cover.apply(null, arguments);
}
function stryMutAct_9fa48(id) {
  var ns = stryNS_9fa48();
  function isActive(id) {
    if (ns.activeMutant === id) {
      if (ns.hitCount !== void 0 && ++ns.hitCount > ns.hitLimit) {
        throw new Error('Stryker: Hit count limit reached (' + ns.hitCount + ')');
      }
      return true;
    }
    return false;
  }
  stryMutAct_9fa48 = isActive;
  return isActive(id);
}
import { createClient, SupabaseClient } from '@supabase/supabase-js';
export interface SupabaseConfig {
  url: string;
  anonKey: string;
}
let supabaseClient: SupabaseClient | null = null;

/**
 * Get Supabase configuration from environment variables
 */
export function getSupabaseConfig(): SupabaseConfig {
  if (stryMutAct_9fa48("431")) {
    {}
  } else {
    stryCov_9fa48("431");
    const url = stryMutAct_9fa48("434") ? (process.env.NEXT_PUBLIC_SUPABASE_URL || process.env.SUPABASE_URL) && '' : stryMutAct_9fa48("433") ? false : stryMutAct_9fa48("432") ? true : (stryCov_9fa48("432", "433", "434"), (stryMutAct_9fa48("436") ? process.env.NEXT_PUBLIC_SUPABASE_URL && process.env.SUPABASE_URL : stryMutAct_9fa48("435") ? false : (stryCov_9fa48("435", "436"), process.env.NEXT_PUBLIC_SUPABASE_URL || process.env.SUPABASE_URL)) || (stryMutAct_9fa48("437") ? "Stryker was here!" : (stryCov_9fa48("437"), '')));
    const anonKey = stryMutAct_9fa48("440") ? (process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || process.env.SUPABASE_ANON_KEY) && '' : stryMutAct_9fa48("439") ? false : stryMutAct_9fa48("438") ? true : (stryCov_9fa48("438", "439", "440"), (stryMutAct_9fa48("442") ? process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY && process.env.SUPABASE_ANON_KEY : stryMutAct_9fa48("441") ? false : (stryCov_9fa48("441", "442"), process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || process.env.SUPABASE_ANON_KEY)) || (stryMutAct_9fa48("443") ? "Stryker was here!" : (stryCov_9fa48("443"), '')));
    if (stryMutAct_9fa48("446") ? !url && !anonKey : stryMutAct_9fa48("445") ? false : stryMutAct_9fa48("444") ? true : (stryCov_9fa48("444", "445", "446"), (stryMutAct_9fa48("447") ? url : (stryCov_9fa48("447"), !url)) || (stryMutAct_9fa48("448") ? anonKey : (stryCov_9fa48("448"), !anonKey)))) {
      if (stryMutAct_9fa48("449")) {
        {}
      } else {
        stryCov_9fa48("449");
        throw new Error(stryMutAct_9fa48("450") ? "" : (stryCov_9fa48("450"), 'Supabase URL and anon key are required. Set NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY'));
      }
    }
    return stryMutAct_9fa48("451") ? {} : (stryCov_9fa48("451"), {
      url,
      anonKey
    });
  }
}

/**
 * Get Supabase client instance (singleton)
 */
export function getSupabase(): SupabaseClient {
  if (stryMutAct_9fa48("452")) {
    {}
  } else {
    stryCov_9fa48("452");
    if (stryMutAct_9fa48("455") ? false : stryMutAct_9fa48("454") ? true : stryMutAct_9fa48("453") ? supabaseClient : (stryCov_9fa48("453", "454", "455"), !supabaseClient)) {
      if (stryMutAct_9fa48("456")) {
        {}
      } else {
        stryCov_9fa48("456");
        const config = getSupabaseConfig();
        supabaseClient = createClient(config.url, config.anonKey, stryMutAct_9fa48("457") ? {} : (stryCov_9fa48("457"), {
          auth: stryMutAct_9fa48("458") ? {} : (stryCov_9fa48("458"), {
            persistSession: stryMutAct_9fa48("459") ? false : (stryCov_9fa48("459"), true),
            autoRefreshToken: stryMutAct_9fa48("460") ? false : (stryCov_9fa48("460"), true)
          })
        }));
      }
    }
    return supabaseClient;
  }
}

/**
 * Create a new Supabase client with custom configuration
 * Useful for server-side or service role operations
 */
export function createSupabaseClient(url: string, key: string): SupabaseClient {
  if (stryMutAct_9fa48("461")) {
    {}
  } else {
    stryCov_9fa48("461");
    return createClient(url, key, stryMutAct_9fa48("462") ? {} : (stryCov_9fa48("462"), {
      auth: stryMutAct_9fa48("463") ? {} : (stryCov_9fa48("463"), {
        persistSession: stryMutAct_9fa48("464") ? true : (stryCov_9fa48("464"), false),
        autoRefreshToken: stryMutAct_9fa48("465") ? true : (stryCov_9fa48("465"), false)
      })
    }));
  }
}