/**
 * Stripe Checkout button (Portable)
 * Configurable price and product
 */
// @ts-nocheck


'use client';

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
import { useState } from 'react';
import { formatPrice } from '../../lib/stripe';
export interface CheckoutButtonProps {
  query: string;
  amount?: number; // In pence (default: 299 for £2.99)
  currency?: string;
  onCheckoutStart?: () => void;
  onCheckoutSuccess?: (reportId: string) => void;
  onCheckoutError?: (error: string) => void;
  disabled?: boolean;
  className?: string;
}
export function CheckoutButton({
  query,
  amount = 299,
  currency: _currency = stryMutAct_9fa48("121") ? "" : (stryCov_9fa48("121"), 'gbp'),
  onCheckoutStart = () => {},
  onCheckoutSuccess = () => {},
  onCheckoutError = () => {},
  disabled = stryMutAct_9fa48("122") ? true : (stryCov_9fa48("122"), false),
  className = stryMutAct_9fa48("123") ? "Stryker was here!" : (stryCov_9fa48("123"), '')
}: CheckoutButtonProps) {
  if (stryMutAct_9fa48("124")) {
    {}
  } else {
    stryCov_9fa48("124");
    const [isLoading, setIsLoading] = useState(stryMutAct_9fa48("125") ? true : (stryCov_9fa48("125"), false));
    const handleCheckout = async () => {
      if (stryMutAct_9fa48("126")) {
        {}
      } else {
        stryCov_9fa48("126");
        setIsLoading(stryMutAct_9fa48("127") ? false : (stryCov_9fa48("127"), true));
        stryMutAct_9fa48("128") ? onCheckoutStart() : (stryCov_9fa48("128"), onCheckoutStart?.());
        try {
          if (stryMutAct_9fa48("129")) {
            {}
          } else {
            stryCov_9fa48("129");
            // This will be implemented by the consuming app
            // Call backend API to create checkout session
            const response = await fetch(stryMutAct_9fa48("130") ? "" : (stryCov_9fa48("130"), '/api/reports/initiate'), stryMutAct_9fa48("131") ? {} : (stryCov_9fa48("131"), {
              method: stryMutAct_9fa48("132") ? "" : (stryCov_9fa48("132"), 'POST'),
              headers: stryMutAct_9fa48("133") ? {} : (stryCov_9fa48("133"), {
                'Content-Type': stryMutAct_9fa48("134") ? "" : (stryCov_9fa48("134"), 'application/json')
              }),
              body: JSON.stringify(stryMutAct_9fa48("135") ? {} : (stryCov_9fa48("135"), {
                query
              }))
            }));
            if (stryMutAct_9fa48("138") ? false : stryMutAct_9fa48("137") ? true : stryMutAct_9fa48("136") ? response.ok : (stryCov_9fa48("136", "137", "138"), !response.ok)) {
              if (stryMutAct_9fa48("139")) {
                {}
              } else {
                stryCov_9fa48("139");
                throw new Error(stryMutAct_9fa48("140") ? "" : (stryCov_9fa48("140"), 'Failed to create checkout session'));
              }
            }
            const data = await response.json();

            // Redirect to success page or handle in-app
            stryMutAct_9fa48("141") ? onCheckoutSuccess(data.reportId) : (stryCov_9fa48("141"), onCheckoutSuccess?.(data.reportId));
          }
        } catch (error) {
          if (stryMutAct_9fa48("142")) {
            {}
          } else {
            stryCov_9fa48("142");
            const message = error instanceof Error ? error.message : stryMutAct_9fa48("143") ? "" : (stryCov_9fa48("143"), 'Checkout failed');
            stryMutAct_9fa48("144") ? onCheckoutError(message) : (stryCov_9fa48("144"), onCheckoutError?.(message));
          }
        } finally {
          if (stryMutAct_9fa48("145")) {
            {}
          } else {
            stryCov_9fa48("145");
            setIsLoading(stryMutAct_9fa48("146") ? true : (stryCov_9fa48("146"), false));
          }
        }
      }
    };
    return <button type="button" onClick={handleCheckout} disabled={stryMutAct_9fa48("149") ? (disabled || isLoading) && !query.trim() : stryMutAct_9fa48("148") ? false : stryMutAct_9fa48("147") ? true : (stryCov_9fa48("147", "148", "149"), (stryMutAct_9fa48("151") ? disabled && isLoading : stryMutAct_9fa48("150") ? false : (stryCov_9fa48("150", "151"), disabled || isLoading)) || (stryMutAct_9fa48("152") ? query.trim() : (stryCov_9fa48("152"), !(stryMutAct_9fa48("153") ? query : (stryCov_9fa48("153"), query.trim())))))} className={stryMutAct_9fa48("154") ? `` : (stryCov_9fa48("154"), `px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium ${className}`)}>
      {isLoading ? stryMutAct_9fa48("155") ? "" : (stryCov_9fa48("155"), 'Processing...') : stryMutAct_9fa48("156") ? `` : (stryCov_9fa48("156"), `Generate Report (${formatPrice(amount)})`)}
    </button>;
  }
}