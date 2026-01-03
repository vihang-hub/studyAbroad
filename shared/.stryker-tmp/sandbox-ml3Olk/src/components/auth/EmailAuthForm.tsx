/**
 * Email/Password authentication form (Portable)
 * Supports both sign in and sign up modes
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
import { useSignIn, useSignUp } from '@clerk/clerk-react';
export interface EmailAuthFormProps {
  mode: 'signin' | 'signup';
  onSuccess?: () => void;
  onError?: (error: string) => void;
}
export function EmailAuthForm({
  mode,
  onSuccess = () => {},
  onError = () => {}
}: EmailAuthFormProps) {
  if (stryMutAct_9fa48("0")) {
    {}
  } else {
    stryCov_9fa48("0");
    const {
      signIn,
      setActive: setActiveSignIn
    } = useSignIn();
    const {
      signUp,
      setActive: setActiveSignUp
    } = useSignUp();
    const [email, setEmail] = useState(stryMutAct_9fa48("1") ? "Stryker was here!" : (stryCov_9fa48("1"), ''));
    const [password, setPassword] = useState(stryMutAct_9fa48("2") ? "Stryker was here!" : (stryCov_9fa48("2"), ''));
    const [firstName, setFirstName] = useState(stryMutAct_9fa48("3") ? "Stryker was here!" : (stryCov_9fa48("3"), ''));
    const [lastName, setLastName] = useState(stryMutAct_9fa48("4") ? "Stryker was here!" : (stryCov_9fa48("4"), ''));
    const [isLoading, setIsLoading] = useState(stryMutAct_9fa48("5") ? true : (stryCov_9fa48("5"), false));
    const handleSubmit = async (e: React.FormEvent) => {
      if (stryMutAct_9fa48("6")) {
        {}
      } else {
        stryCov_9fa48("6");
        e.preventDefault();
        setIsLoading(stryMutAct_9fa48("7") ? false : (stryCov_9fa48("7"), true));
        try {
          if (stryMutAct_9fa48("8")) {
            {}
          } else {
            stryCov_9fa48("8");
            if (stryMutAct_9fa48("11") ? mode !== 'signin' : stryMutAct_9fa48("10") ? false : stryMutAct_9fa48("9") ? true : (stryCov_9fa48("9", "10", "11"), mode === (stryMutAct_9fa48("12") ? "" : (stryCov_9fa48("12"), 'signin')))) {
              if (stryMutAct_9fa48("13")) {
                {}
              } else {
                stryCov_9fa48("13");
                if (stryMutAct_9fa48("16") ? false : stryMutAct_9fa48("15") ? true : stryMutAct_9fa48("14") ? signIn : (stryCov_9fa48("14", "15", "16"), !signIn)) throw new Error(stryMutAct_9fa48("17") ? "" : (stryCov_9fa48("17"), 'Sign in not initialized'));
                const result = await signIn.create(stryMutAct_9fa48("18") ? {} : (stryCov_9fa48("18"), {
                  identifier: email,
                  password
                }));
                if (stryMutAct_9fa48("21") ? result.status !== 'complete' : stryMutAct_9fa48("20") ? false : stryMutAct_9fa48("19") ? true : (stryCov_9fa48("19", "20", "21"), result.status === (stryMutAct_9fa48("22") ? "" : (stryCov_9fa48("22"), 'complete')))) {
                  if (stryMutAct_9fa48("23")) {
                    {}
                  } else {
                    stryCov_9fa48("23");
                    await setActiveSignIn(stryMutAct_9fa48("24") ? {} : (stryCov_9fa48("24"), {
                      session: result.createdSessionId
                    }));
                    stryMutAct_9fa48("25") ? onSuccess() : (stryCov_9fa48("25"), onSuccess?.());
                  }
                }
              }
            } else {
              if (stryMutAct_9fa48("26")) {
                {}
              } else {
                stryCov_9fa48("26");
                if (stryMutAct_9fa48("29") ? false : stryMutAct_9fa48("28") ? true : stryMutAct_9fa48("27") ? signUp : (stryCov_9fa48("27", "28", "29"), !signUp)) throw new Error(stryMutAct_9fa48("30") ? "" : (stryCov_9fa48("30"), 'Sign up not initialized'));
                const result = await signUp.create(stryMutAct_9fa48("31") ? {} : (stryCov_9fa48("31"), {
                  emailAddress: email,
                  password,
                  firstName,
                  lastName
                }));

                // Send email verification
                await signUp.prepareEmailAddressVerification(stryMutAct_9fa48("32") ? {} : (stryCov_9fa48("32"), {
                  strategy: stryMutAct_9fa48("33") ? "" : (stryCov_9fa48("33"), 'email_code')
                }));

                // For now, auto-complete without verification (development)
                if (stryMutAct_9fa48("36") ? result.status !== 'complete' : stryMutAct_9fa48("35") ? false : stryMutAct_9fa48("34") ? true : (stryCov_9fa48("34", "35", "36"), result.status === (stryMutAct_9fa48("37") ? "" : (stryCov_9fa48("37"), 'complete')))) {
                  if (stryMutAct_9fa48("38")) {
                    {}
                  } else {
                    stryCov_9fa48("38");
                    await setActiveSignUp(stryMutAct_9fa48("39") ? {} : (stryCov_9fa48("39"), {
                      session: result.createdSessionId
                    }));
                    stryMutAct_9fa48("40") ? onSuccess() : (stryCov_9fa48("40"), onSuccess?.());
                  }
                }
              }
            }
          }
        } catch (error) {
          if (stryMutAct_9fa48("41")) {
            {}
          } else {
            stryCov_9fa48("41");
            const message = error instanceof Error ? error.message : stryMutAct_9fa48("42") ? "" : (stryCov_9fa48("42"), 'Authentication failed');
            stryMutAct_9fa48("43") ? onError(message) : (stryCov_9fa48("43"), onError?.(message));
          }
        } finally {
          if (stryMutAct_9fa48("44")) {
            {}
          } else {
            stryCov_9fa48("44");
            setIsLoading(stryMutAct_9fa48("45") ? true : (stryCov_9fa48("45"), false));
          }
        }
      }
    };
    return <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      {stryMutAct_9fa48("48") ? mode === 'signup' || <>
          <div>
            {/* eslint-disable-next-line jsx-a11y/label-has-associated-control */}
            <label htmlFor="firstName" className="block text-sm font-medium text-gray-700 mb-1">
              First Name
            </label>
            <input id="firstName" type="text" value={firstName} onChange={e => setFirstName(e.target.value)} required className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
          </div>
          <div>
            {/* eslint-disable-next-line jsx-a11y/label-has-associated-control */}
            <label htmlFor="lastName" className="block text-sm font-medium text-gray-700 mb-1">
              Last Name
            </label>
            <input id="lastName" type="text" value={lastName} onChange={e => setLastName(e.target.value)} required className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
          </div>
        </> : stryMutAct_9fa48("47") ? false : stryMutAct_9fa48("46") ? true : (stryCov_9fa48("46", "47", "48"), (stryMutAct_9fa48("50") ? mode !== 'signup' : stryMutAct_9fa48("49") ? true : (stryCov_9fa48("49", "50"), mode === (stryMutAct_9fa48("51") ? "" : (stryCov_9fa48("51"), 'signup')))) && <>
          <div>
            {/* eslint-disable-next-line jsx-a11y/label-has-associated-control */}
            <label htmlFor="firstName" className="block text-sm font-medium text-gray-700 mb-1">
              First Name
            </label>
            <input id="firstName" type="text" value={firstName} onChange={stryMutAct_9fa48("52") ? () => undefined : (stryCov_9fa48("52"), e => setFirstName(e.target.value))} required className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
          </div>
          <div>
            {/* eslint-disable-next-line jsx-a11y/label-has-associated-control */}
            <label htmlFor="lastName" className="block text-sm font-medium text-gray-700 mb-1">
              Last Name
            </label>
            <input id="lastName" type="text" value={lastName} onChange={stryMutAct_9fa48("53") ? () => undefined : (stryCov_9fa48("53"), e => setLastName(e.target.value))} required className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
          </div>
        </>)}

      <div>
        {/* eslint-disable-next-line jsx-a11y/label-has-associated-control */}
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
          Email
        </label>
        <input id="email" type="email" value={email} onChange={stryMutAct_9fa48("54") ? () => undefined : (stryCov_9fa48("54"), e => setEmail(e.target.value))} required className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
      </div>

      <div>
        {/* eslint-disable-next-line jsx-a11y/label-has-associated-control */}
        <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
          Password
        </label>
        <input id="password" type="password" value={password} onChange={stryMutAct_9fa48("55") ? () => undefined : (stryCov_9fa48("55"), e => setPassword(e.target.value))} required minLength={8} className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
      </div>

      <button type="submit" disabled={isLoading} className="w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium">
        {isLoading ? stryMutAct_9fa48("56") ? "" : (stryCov_9fa48("56"), 'Loading...') : (stryMutAct_9fa48("59") ? mode !== 'signin' : stryMutAct_9fa48("58") ? false : stryMutAct_9fa48("57") ? true : (stryCov_9fa48("57", "58", "59"), mode === (stryMutAct_9fa48("60") ? "" : (stryCov_9fa48("60"), 'signin')))) ? stryMutAct_9fa48("61") ? "" : (stryCov_9fa48("61"), 'Sign In') : stryMutAct_9fa48("62") ? "" : (stryCov_9fa48("62"), 'Sign Up')}
      </button>
    </form>;
  }
}