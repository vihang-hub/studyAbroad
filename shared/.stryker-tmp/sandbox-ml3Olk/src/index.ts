/**
 * @study-abroad/shared
 * Portable, reusable components for plug-and-play across projects
 *
 * Exports:
 * - Types (User, Report, Payment, API contracts)
 * - Lib (Clerk, Stripe, Supabase clients)
 * - Hooks (useAuth, useSupabase)
 * - Components (LoginForm, SignupForm, CheckoutButton, etc.)
 */
// @ts-nocheck


// Types
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
export * from './types/user';
export * from './types/report';
export * from './types/payment';
export * from './types/api';

// Lib (Portable client initialization)
export * from './lib/clerk';
export * from './lib/stripe';
export * from './lib/supabase';
export * from './lib/api-client';

// Hooks
export * from './hooks/useAuth';
export * from './hooks/useSupabase';
export * from './hooks/usePayment';

// Components - Authentication
export * from './components/auth';

// Components - Payments
export * from './components/payments';
export const SHARED_VERSION = stryMutAct_9fa48("310") ? "" : (stryCov_9fa48("310"), '0.1.0');