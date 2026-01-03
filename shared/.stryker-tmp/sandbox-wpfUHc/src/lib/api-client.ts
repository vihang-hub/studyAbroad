/**
 * Generic typed fetch wrapper for backend API calls
 * Configurable backend URL via environment variables
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
import type { ApiResponse, ApiError, FetchOptions } from '../types/api';
export interface ApiClientConfig {
  baseUrl: string;
  defaultHeaders?: Record<string, string>;
}

/**
 * Get API client configuration from environment variables
 */
export function getApiConfig(): ApiClientConfig {
  if (stryMutAct_9fa48("311")) {
    {}
  } else {
    stryCov_9fa48("311");
    const baseUrl = stryMutAct_9fa48("314") ? (process.env.NEXT_PUBLIC_API_URL || process.env.API_URL) && 'http://localhost:8000' : stryMutAct_9fa48("313") ? false : stryMutAct_9fa48("312") ? true : (stryCov_9fa48("312", "313", "314"), (stryMutAct_9fa48("316") ? process.env.NEXT_PUBLIC_API_URL && process.env.API_URL : stryMutAct_9fa48("315") ? false : (stryCov_9fa48("315", "316"), process.env.NEXT_PUBLIC_API_URL || process.env.API_URL)) || (stryMutAct_9fa48("317") ? "" : (stryCov_9fa48("317"), 'http://localhost:8000')));
    return stryMutAct_9fa48("318") ? {} : (stryCov_9fa48("318"), {
      baseUrl,
      defaultHeaders: stryMutAct_9fa48("319") ? {} : (stryCov_9fa48("319"), {
        'Content-Type': stryMutAct_9fa48("320") ? "" : (stryCov_9fa48("320"), 'application/json')
      })
    });
  }
}

/**
 * Generic typed fetch function
 * @param endpoint - API endpoint (e.g., '/reports')
 * @param options - Fetch options
 * @returns Typed API response
 */
export async function fetchApi<T>(endpoint: string, options: FetchOptions = {}): Promise<ApiResponse<T>> {
  if (stryMutAct_9fa48("321")) {
    {}
  } else {
    stryCov_9fa48("321");
    const config = getApiConfig();
    const {
      baseUrl = config.baseUrl,
      token,
      ...fetchOptions
    } = options;
    const url = stryMutAct_9fa48("322") ? `` : (stryCov_9fa48("322"), `${baseUrl}${endpoint}`);
    const headers: Record<string, string> = stryMutAct_9fa48("323") ? {} : (stryCov_9fa48("323"), {
      ...config.defaultHeaders,
      ...(stryMutAct_9fa48("326") ? fetchOptions.headers as Record<string, string> && {} : stryMutAct_9fa48("325") ? false : stryMutAct_9fa48("324") ? true : (stryCov_9fa48("324", "325", "326"), fetchOptions.headers as Record<string, string> || {}))
    });
    if (stryMutAct_9fa48("328") ? false : stryMutAct_9fa48("327") ? true : (stryCov_9fa48("327", "328"), token)) {
      if (stryMutAct_9fa48("329")) {
        {}
      } else {
        stryCov_9fa48("329");
        headers.Authorization = stryMutAct_9fa48("330") ? `` : (stryCov_9fa48("330"), `Bearer ${token}`);
      }
    }
    try {
      if (stryMutAct_9fa48("331")) {
        {}
      } else {
        stryCov_9fa48("331");
        const response = await fetch(url, stryMutAct_9fa48("332") ? {} : (stryCov_9fa48("332"), {
          ...fetchOptions,
          headers
        }));
        const data = await response.json().catch(stryMutAct_9fa48("333") ? () => undefined : (stryCov_9fa48("333"), () => null));
        if (stryMutAct_9fa48("336") ? false : stryMutAct_9fa48("335") ? true : stryMutAct_9fa48("334") ? response.ok : (stryCov_9fa48("334", "335", "336"), !response.ok)) {
          if (stryMutAct_9fa48("337")) {
            {}
          } else {
            stryCov_9fa48("337");
            const error: ApiError = stryMutAct_9fa48("338") ? {} : (stryCov_9fa48("338"), {
              code: stryMutAct_9fa48("341") ? data?.code && 'UNKNOWN_ERROR' : stryMutAct_9fa48("340") ? false : stryMutAct_9fa48("339") ? true : (stryCov_9fa48("339", "340", "341"), (stryMutAct_9fa48("342") ? data.code : (stryCov_9fa48("342"), data?.code)) || (stryMutAct_9fa48("343") ? "" : (stryCov_9fa48("343"), 'UNKNOWN_ERROR'))),
              message: stryMutAct_9fa48("346") ? data?.message && response.statusText : stryMutAct_9fa48("345") ? false : stryMutAct_9fa48("344") ? true : (stryCov_9fa48("344", "345", "346"), (stryMutAct_9fa48("347") ? data.message : (stryCov_9fa48("347"), data?.message)) || response.statusText),
              details: stryMutAct_9fa48("348") ? data.details : (stryCov_9fa48("348"), data?.details),
              statusCode: response.status
            });
            return stryMutAct_9fa48("349") ? {} : (stryCov_9fa48("349"), {
              success: stryMutAct_9fa48("350") ? true : (stryCov_9fa48("350"), false),
              error
            });
          }
        }
        return stryMutAct_9fa48("351") ? {} : (stryCov_9fa48("351"), {
          success: stryMutAct_9fa48("352") ? false : (stryCov_9fa48("352"), true),
          data: data as T
        });
      }
    } catch (error) {
      if (stryMutAct_9fa48("353")) {
        {}
      } else {
        stryCov_9fa48("353");
        const apiError: ApiError = stryMutAct_9fa48("354") ? {} : (stryCov_9fa48("354"), {
          code: stryMutAct_9fa48("355") ? "" : (stryCov_9fa48("355"), 'NETWORK_ERROR'),
          message: error instanceof Error ? error.message : stryMutAct_9fa48("356") ? "" : (stryCov_9fa48("356"), 'Network request failed'),
          statusCode: 0
        });
        return stryMutAct_9fa48("357") ? {} : (stryCov_9fa48("357"), {
          success: stryMutAct_9fa48("358") ? true : (stryCov_9fa48("358"), false),
          error: apiError
        });
      }
    }
  }
}

/**
 * Convenience methods for common HTTP verbs
 */
export const api = stryMutAct_9fa48("359") ? {} : (stryCov_9fa48("359"), {
  get: stryMutAct_9fa48("360") ? () => undefined : (stryCov_9fa48("360"), <T,>(endpoint: string, options?: FetchOptions) => fetchApi<T>(endpoint, stryMutAct_9fa48("361") ? {} : (stryCov_9fa48("361"), {
    ...options,
    method: stryMutAct_9fa48("362") ? "" : (stryCov_9fa48("362"), 'GET')
  }))),
  post: stryMutAct_9fa48("363") ? () => undefined : (stryCov_9fa48("363"), <T,>(endpoint: string, body?: unknown, options?: FetchOptions) => fetchApi<T>(endpoint, stryMutAct_9fa48("364") ? {} : (stryCov_9fa48("364"), {
    ...options,
    method: stryMutAct_9fa48("365") ? "" : (stryCov_9fa48("365"), 'POST'),
    body: JSON.stringify(body)
  }))),
  put: stryMutAct_9fa48("366") ? () => undefined : (stryCov_9fa48("366"), <T,>(endpoint: string, body?: unknown, options?: FetchOptions) => fetchApi<T>(endpoint, stryMutAct_9fa48("367") ? {} : (stryCov_9fa48("367"), {
    ...options,
    method: stryMutAct_9fa48("368") ? "" : (stryCov_9fa48("368"), 'PUT'),
    body: JSON.stringify(body)
  }))),
  patch: stryMutAct_9fa48("369") ? () => undefined : (stryCov_9fa48("369"), <T,>(endpoint: string, body?: unknown, options?: FetchOptions) => fetchApi<T>(endpoint, stryMutAct_9fa48("370") ? {} : (stryCov_9fa48("370"), {
    ...options,
    method: stryMutAct_9fa48("371") ? "" : (stryCov_9fa48("371"), 'PATCH'),
    body: JSON.stringify(body)
  }))),
  delete: stryMutAct_9fa48("372") ? () => undefined : (stryCov_9fa48("372"), <T,>(endpoint: string, options?: FetchOptions) => fetchApi<T>(endpoint, stryMutAct_9fa48("373") ? {} : (stryCov_9fa48("373"), {
    ...options,
    method: stryMutAct_9fa48("374") ? "" : (stryCov_9fa48("374"), 'DELETE')
  })))
});