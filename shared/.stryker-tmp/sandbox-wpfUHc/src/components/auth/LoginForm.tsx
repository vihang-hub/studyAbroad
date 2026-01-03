/**
 * Complete login form with all auth options (Portable)
 * Configurable providers and redirect URLs
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
import { OAuthButtons } from './OAuthButtons';
import { EmailAuthForm } from './EmailAuthForm';
export interface LoginFormProps {
  providers?: ('google' | 'apple' | 'facebook')[];
  onSuccess?: () => void;
  onError?: (error: string) => void;
  showDivider?: boolean;
}
export function LoginForm({
  providers = stryMutAct_9fa48("63") ? [] : (stryCov_9fa48("63"), [stryMutAct_9fa48("64") ? "" : (stryCov_9fa48("64"), 'google'), stryMutAct_9fa48("65") ? "" : (stryCov_9fa48("65"), 'apple'), stryMutAct_9fa48("66") ? "" : (stryCov_9fa48("66"), 'facebook')]),
  onSuccess = () => {},
  onError = () => {},
  showDivider = stryMutAct_9fa48("67") ? false : (stryCov_9fa48("67"), true)
}: LoginFormProps) {
  if (stryMutAct_9fa48("68")) {
    {}
  } else {
    stryCov_9fa48("68");
    const [error, setError] = useState<string | null>(null);
    const handleError = (errorMessage: string) => {
      if (stryMutAct_9fa48("69")) {
        {}
      } else {
        stryCov_9fa48("69");
        setError(errorMessage);
        stryMutAct_9fa48("70") ? onError(errorMessage) : (stryCov_9fa48("70"), onError?.(errorMessage));
      }
    };
    return <div className="w-full max-w-md">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Welcome back</h1>
        <p className="text-gray-600">Sign in to your account to continue</p>
      </div>

      {stryMutAct_9fa48("73") ? error || <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-600">{error}</p>
        </div> : stryMutAct_9fa48("72") ? false : stryMutAct_9fa48("71") ? true : (stryCov_9fa48("71", "72", "73"), error && <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-600">{error}</p>
        </div>)}

      <OAuthButtons providers={providers} mode="signin" onError={handleError} />

      {stryMutAct_9fa48("76") ? showDivider || <div className="relative my-6">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-white text-gray-500">Or continue with email</span>
          </div>
        </div> : stryMutAct_9fa48("75") ? false : stryMutAct_9fa48("74") ? true : (stryCov_9fa48("74", "75", "76"), showDivider && <div className="relative my-6">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-white text-gray-500">Or continue with email</span>
          </div>
        </div>)}

      <EmailAuthForm mode="signin" onSuccess={onSuccess} onError={handleError} />

      <div className="mt-4 text-center">
        <a href="/signup" className="text-sm text-blue-600 hover:text-blue-700">
          Don&apos;t have an account? Sign up
        </a>
      </div>
    </div>;
  }
}