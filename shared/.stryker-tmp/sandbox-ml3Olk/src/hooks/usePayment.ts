/**
 * Payment flow hook (Portable)
 * Handles checkout creation and redirect logic
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
import { useState, useCallback } from 'react';
import { api } from '../lib/api-client';
import type { CreateCheckoutRequest, CreateCheckoutResponse } from '../types/payment';
export interface UsePaymentOptions {
  apiEndpoint?: string;
  onSuccess?: (reportId: string) => void;
  onError?: (error: string) => void;
}
export interface UsePaymentResult {
  isLoading: boolean;
  error: string | null;
  createCheckout: (query: string) => Promise<void>;
  clearError: () => void;
}
export function usePayment({
  apiEndpoint = stryMutAct_9fa48("242") ? "" : (stryCov_9fa48("242"), '/reports/initiate'),
  onSuccess,
  onError
}: UsePaymentOptions = {}): UsePaymentResult {
  if (stryMutAct_9fa48("243")) {
    {}
  } else {
    stryCov_9fa48("243");
    const [isLoading, setIsLoading] = useState(stryMutAct_9fa48("244") ? true : (stryCov_9fa48("244"), false));
    const [error, setError] = useState<string | null>(null);
    const createCheckout = useCallback(async (query: string) => {
      if (stryMutAct_9fa48("245")) {
        {}
      } else {
        stryCov_9fa48("245");
        setIsLoading(stryMutAct_9fa48("246") ? false : (stryCov_9fa48("246"), true));
        setError(null);
        try {
          if (stryMutAct_9fa48("247")) {
            {}
          } else {
            stryCov_9fa48("247");
            const request: CreateCheckoutRequest = stryMutAct_9fa48("248") ? {} : (stryCov_9fa48("248"), {
              query
            });
            const response = await api.post<CreateCheckoutResponse>(apiEndpoint, request);
            if (stryMutAct_9fa48("251") ? !response.success && !response.data : stryMutAct_9fa48("250") ? false : stryMutAct_9fa48("249") ? true : (stryCov_9fa48("249", "250", "251"), (stryMutAct_9fa48("252") ? response.success : (stryCov_9fa48("252"), !response.success)) || (stryMutAct_9fa48("253") ? response.data : (stryCov_9fa48("253"), !response.data)))) {
              if (stryMutAct_9fa48("254")) {
                {}
              } else {
                stryCov_9fa48("254");
                throw new Error(stryMutAct_9fa48("257") ? response.error?.message && 'Failed to create checkout' : stryMutAct_9fa48("256") ? false : stryMutAct_9fa48("255") ? true : (stryCov_9fa48("255", "256", "257"), (stryMutAct_9fa48("258") ? response.error.message : (stryCov_9fa48("258"), response.error?.message)) || (stryMutAct_9fa48("259") ? "" : (stryCov_9fa48("259"), 'Failed to create checkout'))));
              }
            }
            const {
              report_id: reportId
            } = response.data as {
              report_id: string;
            };

            // Trigger success callback with report ID
            if (stryMutAct_9fa48("261") ? false : stryMutAct_9fa48("260") ? true : (stryCov_9fa48("260", "261"), reportId)) {
              if (stryMutAct_9fa48("262")) {
                {}
              } else {
                stryCov_9fa48("262");
                stryMutAct_9fa48("263") ? onSuccess(reportId) : (stryCov_9fa48("263"), onSuccess?.(reportId));
              }
            }
          }
        } catch (err) {
          if (stryMutAct_9fa48("264")) {
            {}
          } else {
            stryCov_9fa48("264");
            const errorMessage = err instanceof Error ? err.message : stryMutAct_9fa48("265") ? "" : (stryCov_9fa48("265"), 'Payment failed');
            setError(errorMessage);
            stryMutAct_9fa48("266") ? onError(errorMessage) : (stryCov_9fa48("266"), onError?.(errorMessage));
          }
        } finally {
          if (stryMutAct_9fa48("267")) {
            {}
          } else {
            stryCov_9fa48("267");
            setIsLoading(stryMutAct_9fa48("268") ? true : (stryCov_9fa48("268"), false));
          }
        }
      }
    }, stryMutAct_9fa48("269") ? [] : (stryCov_9fa48("269"), [apiEndpoint, onSuccess, onError]));
    const clearError = useCallback(() => {
      if (stryMutAct_9fa48("270")) {
        {}
      } else {
        stryCov_9fa48("270");
        setError(null);
      }
    }, stryMutAct_9fa48("271") ? ["Stryker was here"] : (stryCov_9fa48("271"), []));
    return stryMutAct_9fa48("272") ? {} : (stryCov_9fa48("272"), {
      isLoading,
      error,
      createCheckout,
      clearError
    });
  }
}