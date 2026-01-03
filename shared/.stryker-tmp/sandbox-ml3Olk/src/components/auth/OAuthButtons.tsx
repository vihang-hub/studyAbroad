/**
 * OAuth authentication buttons (Portable)
 * Supports Google, Apple, Facebook providers
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
import { useSignIn } from '@clerk/clerk-react';
export interface OAuthButtonsProps {
  providers?: ('google' | 'apple' | 'facebook')[];
  mode?: 'signin' | 'signup';
  onError?: (error: string) => void;
}
const providerLabels = stryMutAct_9fa48("77") ? {} : (stryCov_9fa48("77"), {
  google: stryMutAct_9fa48("78") ? "" : (stryCov_9fa48("78"), 'Continue with Google'),
  apple: stryMutAct_9fa48("79") ? "" : (stryCov_9fa48("79"), 'Continue with Apple'),
  facebook: stryMutAct_9fa48("80") ? "" : (stryCov_9fa48("80"), 'Continue with Facebook')
});
export function OAuthButtons({
  providers = stryMutAct_9fa48("81") ? [] : (stryCov_9fa48("81"), [stryMutAct_9fa48("82") ? "" : (stryCov_9fa48("82"), 'google'), stryMutAct_9fa48("83") ? "" : (stryCov_9fa48("83"), 'apple'), stryMutAct_9fa48("84") ? "" : (stryCov_9fa48("84"), 'facebook')]),
  mode: _mode = stryMutAct_9fa48("85") ? "" : (stryCov_9fa48("85"), 'signin'),
  onError = () => {}
}: OAuthButtonsProps) {
  if (stryMutAct_9fa48("86")) {
    {}
  } else {
    stryCov_9fa48("86");
    const {
      signIn
    } = useSignIn();
    const handleOAuthSignIn = async (provider: 'google' | 'apple' | 'facebook') => {
      if (stryMutAct_9fa48("87")) {
        {}
      } else {
        stryCov_9fa48("87");
        if (stryMutAct_9fa48("90") ? false : stryMutAct_9fa48("89") ? true : stryMutAct_9fa48("88") ? signIn : (stryCov_9fa48("88", "89", "90"), !signIn)) {
          if (stryMutAct_9fa48("91")) {
            {}
          } else {
            stryCov_9fa48("91");
            stryMutAct_9fa48("92") ? onError('Sign in not initialized') : (stryCov_9fa48("92"), onError?.(stryMutAct_9fa48("93") ? "" : (stryCov_9fa48("93"), 'Sign in not initialized')));
            return;
          }
        }
        try {
          if (stryMutAct_9fa48("94")) {
            {}
          } else {
            stryCov_9fa48("94");
            await signIn.authenticateWithRedirect(stryMutAct_9fa48("95") ? {} : (stryCov_9fa48("95"), {
              strategy: stryMutAct_9fa48("96") ? `` : (stryCov_9fa48("96"), `oauth_${provider}`),
              redirectUrl: stryMutAct_9fa48("97") ? "" : (stryCov_9fa48("97"), '/sso-callback'),
              redirectUrlComplete: stryMutAct_9fa48("98") ? "" : (stryCov_9fa48("98"), '/chat')
            }));
          }
        } catch (error) {
          if (stryMutAct_9fa48("99")) {
            {}
          } else {
            stryCov_9fa48("99");
            const message = error instanceof Error ? error.message : stryMutAct_9fa48("100") ? "" : (stryCov_9fa48("100"), 'OAuth sign in failed');
            stryMutAct_9fa48("101") ? onError(message) : (stryCov_9fa48("101"), onError?.(message));
          }
        }
      }
    };
    return <div className="flex flex-col gap-3">
      {providers.map(stryMutAct_9fa48("102") ? () => undefined : (stryCov_9fa48("102"), provider => <button key={provider} type="button" onClick={stryMutAct_9fa48("103") ? () => undefined : (stryCov_9fa48("103"), () => handleOAuthSignIn(provider))} className="w-full flex items-center justify-center gap-3 px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
          {/* Provider icon would go here */}
          <span className="text-sm font-medium text-gray-700">
            {providerLabels[provider]}
          </span>
        </button>))}
    </div>;
  }
}