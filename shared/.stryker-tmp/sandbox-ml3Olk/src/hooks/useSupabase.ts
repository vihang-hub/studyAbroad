/**
 * Supabase query hooks
 * Provides typed data fetching and mutations
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
import { useEffect, useState, useCallback } from 'react';
import type { SupabaseClient, PostgrestFilterBuilder } from '@supabase/supabase-js';
import { getSupabase } from '../lib/supabase';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type QueryFilter = PostgrestFilterBuilder<any, any, any>;
export interface UseSupabaseQueryOptions<T> {
  table: string;
  select?: string;
  filter?: (query: QueryFilter) => QueryFilter;
  enabled?: boolean;
  onSuccess?: (data: T[]) => void;
  onError?: (error: Error) => void;
}
export interface UseSupabaseQueryResult<T> {
  data: T[] | null;
  isLoading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

/**
 * Generic Supabase query hook
 * @param options - Query configuration
 * @returns Query result with data, loading state, and refetch function
 */
export function useSupabaseQuery<T>(options: UseSupabaseQueryOptions<T>): UseSupabaseQueryResult<T> {
  if (stryMutAct_9fa48("273")) {
    {}
  } else {
    stryCov_9fa48("273");
    const [data, setData] = useState<T[] | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(stryMutAct_9fa48("274") ? false : (stryCov_9fa48("274"), true));
    const [error, setError] = useState<Error | null>(null);
    const supabase = getSupabase();
    const fetchData = useCallback(async () => {
      if (stryMutAct_9fa48("275")) {
        {}
      } else {
        stryCov_9fa48("275");
        if (stryMutAct_9fa48("278") ? options.enabled !== false : stryMutAct_9fa48("277") ? false : stryMutAct_9fa48("276") ? true : (stryCov_9fa48("276", "277", "278"), options.enabled === (stryMutAct_9fa48("279") ? true : (stryCov_9fa48("279"), false)))) {
          if (stryMutAct_9fa48("280")) {
            {}
          } else {
            stryCov_9fa48("280");
            setIsLoading(stryMutAct_9fa48("281") ? true : (stryCov_9fa48("281"), false));
            return;
          }
        }
        try {
          if (stryMutAct_9fa48("282")) {
            {}
          } else {
            stryCov_9fa48("282");
            setIsLoading(stryMutAct_9fa48("283") ? false : (stryCov_9fa48("283"), true));
            setError(null);
            let query = supabase.from(options.table).select(stryMutAct_9fa48("286") ? options.select && '*' : stryMutAct_9fa48("285") ? false : stryMutAct_9fa48("284") ? true : (stryCov_9fa48("284", "285", "286"), options.select || (stryMutAct_9fa48("287") ? "" : (stryCov_9fa48("287"), '*'))));
            if (stryMutAct_9fa48("289") ? false : stryMutAct_9fa48("288") ? true : (stryCov_9fa48("288", "289"), options.filter)) {
              if (stryMutAct_9fa48("290")) {
                {}
              } else {
                stryCov_9fa48("290");
                query = stryMutAct_9fa48("291") ? options : (stryCov_9fa48("291"), options.filter(query));
              }
            }
            const {
              data: result,
              error: queryError
            } = await query;
            if (stryMutAct_9fa48("293") ? false : stryMutAct_9fa48("292") ? true : (stryCov_9fa48("292", "293"), queryError)) {
              if (stryMutAct_9fa48("294")) {
                {}
              } else {
                stryCov_9fa48("294");
                throw new Error(queryError.message);
              }
            }
            setData(result as T[]);
            if (stryMutAct_9fa48("296") ? false : stryMutAct_9fa48("295") ? true : (stryCov_9fa48("295", "296"), options.onSuccess)) {
              if (stryMutAct_9fa48("297")) {
                {}
              } else {
                stryCov_9fa48("297");
                options.onSuccess(result as T[]);
              }
            }
          }
        } catch (err) {
          if (stryMutAct_9fa48("298")) {
            {}
          } else {
            stryCov_9fa48("298");
            const queryError = err instanceof Error ? err : new Error(stryMutAct_9fa48("299") ? "" : (stryCov_9fa48("299"), 'Unknown error'));
            setError(queryError);
            if (stryMutAct_9fa48("301") ? false : stryMutAct_9fa48("300") ? true : (stryCov_9fa48("300", "301"), options.onError)) {
              if (stryMutAct_9fa48("302")) {
                {}
              } else {
                stryCov_9fa48("302");
                options.onError(queryError);
              }
            }
          }
        } finally {
          if (stryMutAct_9fa48("303")) {
            {}
          } else {
            stryCov_9fa48("303");
            setIsLoading(stryMutAct_9fa48("304") ? true : (stryCov_9fa48("304"), false));
          }
        }
      }
    }, stryMutAct_9fa48("305") ? [] : (stryCov_9fa48("305"), [options, supabase]));
    useEffect(() => {
      if (stryMutAct_9fa48("306")) {
        {}
      } else {
        stryCov_9fa48("306");
        fetchData();
      }
    }, stryMutAct_9fa48("307") ? [] : (stryCov_9fa48("307"), [fetchData]));
    return stryMutAct_9fa48("308") ? {} : (stryCov_9fa48("308"), {
      data,
      isLoading,
      error,
      refetch: fetchData
    });
  }
}

/**
 * Get Supabase client instance
 * Use this for imperative operations
 */
export function useSupabaseClient(): SupabaseClient {
  if (stryMutAct_9fa48("309")) {
    {}
  } else {
    stryCov_9fa48("309");
    return getSupabase();
  }
}