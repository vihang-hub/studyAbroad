/**
 * Portable Stripe client initialization
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
import { loadStripe, Stripe } from '@stripe/stripe-js';
export interface StripeConfig {
  publishableKey: string;
  priceAmount: number; // In pence (e.g., 299 for £2.99)
  currency: string;
}
let stripePromise: Promise<Stripe | null> | null = null;

/**
 * Get Stripe configuration from environment variables
 */
export function getStripeConfig(): StripeConfig {
  if (stryMutAct_9fa48("406")) {
    {}
  } else {
    stryCov_9fa48("406");
    const publishableKey = stryMutAct_9fa48("409") ? (process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY || process.env.STRIPE_PUBLISHABLE_KEY) && '' : stryMutAct_9fa48("408") ? false : stryMutAct_9fa48("407") ? true : (stryCov_9fa48("407", "408", "409"), (stryMutAct_9fa48("411") ? process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY && process.env.STRIPE_PUBLISHABLE_KEY : stryMutAct_9fa48("410") ? false : (stryCov_9fa48("410", "411"), process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY || process.env.STRIPE_PUBLISHABLE_KEY)) || (stryMutAct_9fa48("412") ? "Stryker was here!" : (stryCov_9fa48("412"), '')));
    if (stryMutAct_9fa48("415") ? false : stryMutAct_9fa48("414") ? true : stryMutAct_9fa48("413") ? publishableKey : (stryCov_9fa48("413", "414", "415"), !publishableKey)) {
      if (stryMutAct_9fa48("416")) {
        {}
      } else {
        stryCov_9fa48("416");
        throw new Error(stryMutAct_9fa48("417") ? "" : (stryCov_9fa48("417"), 'Stripe publishable key is required. Set NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY or STRIPE_PUBLISHABLE_KEY'));
      }
    }
    return stryMutAct_9fa48("418") ? {} : (stryCov_9fa48("418"), {
      publishableKey,
      priceAmount: 299,
      // £2.99 per query
      currency: stryMutAct_9fa48("419") ? "" : (stryCov_9fa48("419"), 'gbp')
    });
  }
}

/**
 * Get Stripe client instance (singleton)
 */
export function getStripe(): Promise<Stripe | null> {
  if (stryMutAct_9fa48("420")) {
    {}
  } else {
    stryCov_9fa48("420");
    if (stryMutAct_9fa48("423") ? false : stryMutAct_9fa48("422") ? true : stryMutAct_9fa48("421") ? stripePromise : (stryCov_9fa48("421", "422", "423"), !stripePromise)) {
      if (stryMutAct_9fa48("424")) {
        {}
      } else {
        stryCov_9fa48("424");
        const config = getStripeConfig();
        stripePromise = loadStripe(config.publishableKey);
      }
    }
    return stripePromise;
  }
}

/**
 * Format price for display
 * @param amountInPence - Amount in pence (e.g., 299)
 * @returns Formatted string (e.g., "£2.99")
 */
export function formatPrice(amountInPence: number): string {
  if (stryMutAct_9fa48("425")) {
    {}
  } else {
    stryCov_9fa48("425");
    const pounds = stryMutAct_9fa48("426") ? amountInPence * 100 : (stryCov_9fa48("426"), amountInPence / 100);
    return new Intl.NumberFormat(stryMutAct_9fa48("427") ? "" : (stryCov_9fa48("427"), 'en-GB'), stryMutAct_9fa48("428") ? {} : (stryCov_9fa48("428"), {
      style: stryMutAct_9fa48("429") ? "" : (stryCov_9fa48("429"), 'currency'),
      currency: stryMutAct_9fa48("430") ? "" : (stryCov_9fa48("430"), 'GBP')
    })).format(pounds);
  }
}