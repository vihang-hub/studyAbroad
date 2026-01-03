/**
 * Complete signup form with all auth options (Portable)
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
export interface SignupFormProps {
  providers?: ('google' | 'apple' | 'facebook')[];
  onSuccess?: () => void;
  onError?: (error: string) => void;
  showDivider?: boolean;
}
export function SignupForm({
  providers = stryMutAct_9fa48("104") ? [] : (stryCov_9fa48("104"), [stryMutAct_9fa48("105") ? "" : (stryCov_9fa48("105"), 'google'), stryMutAct_9fa48("106") ? "" : (stryCov_9fa48("106"), 'apple'), stryMutAct_9fa48("107") ? "" : (stryCov_9fa48("107"), 'facebook')]),
  onSuccess = () => {},
  onError = () => {},
  showDivider = stryMutAct_9fa48("108") ? false : (stryCov_9fa48("108"), true)
}: SignupFormProps) {
  if (stryMutAct_9fa48("109")) {
    {}
  } else {
    stryCov_9fa48("109");
    const [error, setError] = useState<string | null>(null);
    const handleError = (errorMessage: string) => {
      if (stryMutAct_9fa48("110")) {
        {}
      } else {
        stryCov_9fa48("110");
        setError(errorMessage);
        stryMutAct_9fa48("111") ? onError(errorMessage) : (stryCov_9fa48("111"), onError?.(errorMessage));
      }
    };
    return <div className="w-full max-w-md">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Create your account</h1>
        <p className="text-gray-600">Get started with your research today</p>
      </div>

      {stryMutAct_9fa48("114") ? error || <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-600">{error}</p>
        </div> : stryMutAct_9fa48("113") ? false : stryMutAct_9fa48("112") ? true : (stryCov_9fa48("112", "113", "114"), error && <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-600">{error}</p>
        </div>)}

      <OAuthButtons providers={providers} mode="signup" onError={handleError} />

      {stryMutAct_9fa48("117") ? showDivider || <div className="relative my-6">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-white text-gray-500">Or sign up with email</span>
          </div>
        </div> : stryMutAct_9fa48("116") ? false : stryMutAct_9fa48("115") ? true : (stryCov_9fa48("115", "116", "117"), showDivider && <div className="relative my-6">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-white text-gray-500">Or sign up with email</span>
          </div>
        </div>)}

      <EmailAuthForm mode="signup" onSuccess={onSuccess} onError={handleError} />

      <div className="mt-4 text-center text-sm text-gray-600">
        By signing up, you agree to our
        {stryMutAct_9fa48("118") ? "" : (stryCov_9fa48("118"), ' ')}
        <a href="/terms" className="text-blue-600 hover:text-blue-700">
          Terms of Service
        </a>
        {stryMutAct_9fa48("119") ? "" : (stryCov_9fa48("119"), ' ')}
        and
        {stryMutAct_9fa48("120") ? "" : (stryCov_9fa48("120"), ' ')}
        <a href="/privacy" className="text-blue-600 hover:text-blue-700">
          Privacy Policy
        </a>
      </div>

      <div className="mt-4 text-center">
        <a href="/login" className="text-sm text-blue-600 hover:text-blue-700">
          Already have an account? Sign in
        </a>
      </div>
    </div>;
  }
}