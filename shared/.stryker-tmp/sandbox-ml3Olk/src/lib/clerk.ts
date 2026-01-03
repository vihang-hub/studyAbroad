/**
 * Portable Clerk client initialization
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
export interface ClerkConfig {
  publishableKey: string;
  signInUrl?: string;
  signUpUrl?: string;
  afterSignInUrl?: string;
  afterSignUpUrl?: string;
}

/**
 * Get Clerk configuration from environment variables
 * Defaults can be overridden by consuming projects
 */
export function getClerkConfig(): ClerkConfig {
  if (stryMutAct_9fa48("375")) {
    {}
  } else {
    stryCov_9fa48("375");
    const publishableKey = stryMutAct_9fa48("378") ? (process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY || process.env.CLERK_PUBLISHABLE_KEY) && '' : stryMutAct_9fa48("377") ? false : stryMutAct_9fa48("376") ? true : (stryCov_9fa48("376", "377", "378"), (stryMutAct_9fa48("380") ? process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY && process.env.CLERK_PUBLISHABLE_KEY : stryMutAct_9fa48("379") ? false : (stryCov_9fa48("379", "380"), process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY || process.env.CLERK_PUBLISHABLE_KEY)) || (stryMutAct_9fa48("381") ? "Stryker was here!" : (stryCov_9fa48("381"), '')));
    if (stryMutAct_9fa48("384") ? false : stryMutAct_9fa48("383") ? true : stryMutAct_9fa48("382") ? publishableKey : (stryCov_9fa48("382", "383", "384"), !publishableKey)) {
      if (stryMutAct_9fa48("385")) {
        {}
      } else {
        stryCov_9fa48("385");
        throw new Error(stryMutAct_9fa48("386") ? "" : (stryCov_9fa48("386"), 'Clerk publishable key is required. Set NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY or CLERK_PUBLISHABLE_KEY'));
      }
    }
    return stryMutAct_9fa48("387") ? {} : (stryCov_9fa48("387"), {
      publishableKey,
      signInUrl: stryMutAct_9fa48("390") ? process.env.NEXT_PUBLIC_CLERK_SIGN_IN_URL && '/login' : stryMutAct_9fa48("389") ? false : stryMutAct_9fa48("388") ? true : (stryCov_9fa48("388", "389", "390"), process.env.NEXT_PUBLIC_CLERK_SIGN_IN_URL || (stryMutAct_9fa48("391") ? "" : (stryCov_9fa48("391"), '/login'))),
      signUpUrl: stryMutAct_9fa48("394") ? process.env.NEXT_PUBLIC_CLERK_SIGN_UP_URL && '/signup' : stryMutAct_9fa48("393") ? false : stryMutAct_9fa48("392") ? true : (stryCov_9fa48("392", "393", "394"), process.env.NEXT_PUBLIC_CLERK_SIGN_UP_URL || (stryMutAct_9fa48("395") ? "" : (stryCov_9fa48("395"), '/signup'))),
      afterSignInUrl: stryMutAct_9fa48("398") ? process.env.NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL && '/chat' : stryMutAct_9fa48("397") ? false : stryMutAct_9fa48("396") ? true : (stryCov_9fa48("396", "397", "398"), process.env.NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL || (stryMutAct_9fa48("399") ? "" : (stryCov_9fa48("399"), '/chat'))),
      afterSignUpUrl: stryMutAct_9fa48("402") ? process.env.NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL && '/chat' : stryMutAct_9fa48("401") ? false : stryMutAct_9fa48("400") ? true : (stryCov_9fa48("400", "401", "402"), process.env.NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL || (stryMutAct_9fa48("403") ? "" : (stryCov_9fa48("403"), '/chat')))
    });
  }
}

/**
 * Validate Clerk JWT token (backend use)
 * @param _token - JWT token from Authorization header
 * @returns Decoded user ID if valid
 */
export async function validateClerkToken(_token: string): Promise<string | null> {
  if (stryMutAct_9fa48("404")) {
    {}
  } else {
    stryCov_9fa48("404");
    // This will be implemented in backend using Clerk SDK
    // Kept here as a shared interface contract
    throw new Error(stryMutAct_9fa48("405") ? "" : (stryCov_9fa48("405"), 'validateClerkToken should be implemented in backend'));
  }
}