/**
 * Clerk authentication hook
 * Provides user state, login, and logout functionality
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
import { useUser, useClerk } from '@clerk/clerk-react';
import { useMemo } from 'react';
import type { AuthState, UserProfile } from '../types/user';
export function useAuth(): AuthState & {
  signOut: () => Promise<void>;
  openSignIn: () => void;
  openSignUp: () => void;
} {
  if (stryMutAct_9fa48("203")) {
    {}
  } else {
    stryCov_9fa48("203");
    const {
      user,
      isLoaded,
      isSignedIn
    } = useUser();
    const {
      signOut,
      openSignIn,
      openSignUp
    } = useClerk();
    const authState: AuthState = useMemo(() => {
      if (stryMutAct_9fa48("204")) {
        {}
      } else {
        stryCov_9fa48("204");
        if (stryMutAct_9fa48("207") ? false : stryMutAct_9fa48("206") ? true : stryMutAct_9fa48("205") ? isLoaded : (stryCov_9fa48("205", "206", "207"), !isLoaded)) {
          if (stryMutAct_9fa48("208")) {
            {}
          } else {
            stryCov_9fa48("208");
            return stryMutAct_9fa48("209") ? {} : (stryCov_9fa48("209"), {
              isAuthenticated: stryMutAct_9fa48("210") ? true : (stryCov_9fa48("210"), false),
              isLoading: stryMutAct_9fa48("211") ? false : (stryCov_9fa48("211"), true),
              user: null,
              error: null
            });
          }
        }
        if (stryMutAct_9fa48("214") ? !isSignedIn && !user : stryMutAct_9fa48("213") ? false : stryMutAct_9fa48("212") ? true : (stryCov_9fa48("212", "213", "214"), (stryMutAct_9fa48("215") ? isSignedIn : (stryCov_9fa48("215"), !isSignedIn)) || (stryMutAct_9fa48("216") ? user : (stryCov_9fa48("216"), !user)))) {
          if (stryMutAct_9fa48("217")) {
            {}
          } else {
            stryCov_9fa48("217");
            return stryMutAct_9fa48("218") ? {} : (stryCov_9fa48("218"), {
              isAuthenticated: stryMutAct_9fa48("219") ? true : (stryCov_9fa48("219"), false),
              isLoading: stryMutAct_9fa48("220") ? true : (stryCov_9fa48("220"), false),
              user: null,
              error: null
            });
          }
        }
        const userProfile: UserProfile = stryMutAct_9fa48("221") ? {} : (stryCov_9fa48("221"), {
          userId: user.id,
          displayName: stryMutAct_9fa48("224") ? (user.fullName || user.username) && 'User' : stryMutAct_9fa48("223") ? false : stryMutAct_9fa48("222") ? true : (stryCov_9fa48("222", "223", "224"), (stryMutAct_9fa48("226") ? user.fullName && user.username : stryMutAct_9fa48("225") ? false : (stryCov_9fa48("225", "226"), user.fullName || user.username)) || (stryMutAct_9fa48("227") ? "" : (stryCov_9fa48("227"), 'User'))),
          email: stryMutAct_9fa48("230") ? user.primaryEmailAddress?.emailAddress && '' : stryMutAct_9fa48("229") ? false : stryMutAct_9fa48("228") ? true : (stryCov_9fa48("228", "229", "230"), (stryMutAct_9fa48("231") ? user.primaryEmailAddress.emailAddress : (stryCov_9fa48("231"), user.primaryEmailAddress?.emailAddress)) || (stryMutAct_9fa48("232") ? "Stryker was here!" : (stryCov_9fa48("232"), ''))),
          avatarUrl: user.imageUrl,
          isSubscribed: stryMutAct_9fa48("233") ? true : (stryCov_9fa48("233"), false) // Will be determined by backend
        });
        return stryMutAct_9fa48("234") ? {} : (stryCov_9fa48("234"), {
          isAuthenticated: stryMutAct_9fa48("235") ? false : (stryCov_9fa48("235"), true),
          isLoading: stryMutAct_9fa48("236") ? true : (stryCov_9fa48("236"), false),
          user: userProfile,
          error: null
        });
      }
    }, stryMutAct_9fa48("237") ? [] : (stryCov_9fa48("237"), [isLoaded, isSignedIn, user]));
    return stryMutAct_9fa48("238") ? {} : (stryCov_9fa48("238"), {
      ...authState,
      signOut: stryMutAct_9fa48("239") ? () => undefined : (stryCov_9fa48("239"), () => signOut()),
      openSignIn: stryMutAct_9fa48("240") ? () => undefined : (stryCov_9fa48("240"), () => openSignIn()),
      openSignUp: stryMutAct_9fa48("241") ? () => undefined : (stryCov_9fa48("241"), () => openSignUp())
    });
  }
}