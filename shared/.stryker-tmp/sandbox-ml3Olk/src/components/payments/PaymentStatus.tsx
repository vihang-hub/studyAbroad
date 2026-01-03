/**
 * Payment status display (Portable)
 * Shows current payment state with appropriate styling
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
import type { PaymentStatus as PaymentStatusType } from '../../types/payment';
export interface PaymentStatusProps {
  status: PaymentStatusType;
  amount?: number;
  currency?: string;
  errorMessage?: string;
  className?: string;
}
const statusConfig: Record<PaymentStatusType, {
  label: string;
  color: string;
  bg: string;
  border: string;
}> = stryMutAct_9fa48("157") ? {} : (stryCov_9fa48("157"), {
  pending: stryMutAct_9fa48("158") ? {} : (stryCov_9fa48("158"), {
    label: stryMutAct_9fa48("159") ? "" : (stryCov_9fa48("159"), 'Payment Pending'),
    color: stryMutAct_9fa48("160") ? "" : (stryCov_9fa48("160"), 'text-yellow-700'),
    bg: stryMutAct_9fa48("161") ? "" : (stryCov_9fa48("161"), 'bg-yellow-50'),
    border: stryMutAct_9fa48("162") ? "" : (stryCov_9fa48("162"), 'border-yellow-200')
  }),
  succeeded: stryMutAct_9fa48("163") ? {} : (stryCov_9fa48("163"), {
    label: stryMutAct_9fa48("164") ? "" : (stryCov_9fa48("164"), 'Payment Successful'),
    color: stryMutAct_9fa48("165") ? "" : (stryCov_9fa48("165"), 'text-green-700'),
    bg: stryMutAct_9fa48("166") ? "" : (stryCov_9fa48("166"), 'bg-green-50'),
    border: stryMutAct_9fa48("167") ? "" : (stryCov_9fa48("167"), 'border-green-200')
  }),
  failed: stryMutAct_9fa48("168") ? {} : (stryCov_9fa48("168"), {
    label: stryMutAct_9fa48("169") ? "" : (stryCov_9fa48("169"), 'Payment Failed'),
    color: stryMutAct_9fa48("170") ? "" : (stryCov_9fa48("170"), 'text-red-700'),
    bg: stryMutAct_9fa48("171") ? "" : (stryCov_9fa48("171"), 'bg-red-50'),
    border: stryMutAct_9fa48("172") ? "" : (stryCov_9fa48("172"), 'border-red-200')
  }),
  refunded: stryMutAct_9fa48("173") ? {} : (stryCov_9fa48("173"), {
    label: stryMutAct_9fa48("174") ? "" : (stryCov_9fa48("174"), 'Payment Refunded'),
    color: stryMutAct_9fa48("175") ? "" : (stryCov_9fa48("175"), 'text-gray-700'),
    bg: stryMutAct_9fa48("176") ? "" : (stryCov_9fa48("176"), 'bg-gray-50'),
    border: stryMutAct_9fa48("177") ? "" : (stryCov_9fa48("177"), 'border-gray-200')
  })
});
export function PaymentStatus({
  status,
  amount = undefined,
  currency = stryMutAct_9fa48("178") ? "" : (stryCov_9fa48("178"), 'gbp'),
  errorMessage = undefined,
  className = stryMutAct_9fa48("179") ? "Stryker was here!" : (stryCov_9fa48("179"), '')
}: PaymentStatusProps) {
  if (stryMutAct_9fa48("180")) {
    {}
  } else {
    stryCov_9fa48("180");
    const config = statusConfig[status];
    return <div className={stryMutAct_9fa48("181") ? `` : (stryCov_9fa48("181"), `p-4 rounded-lg border ${config.bg} ${config.border} ${className}`)}>
      <div className="flex items-center gap-2">
        <div className={stryMutAct_9fa48("182") ? `` : (stryCov_9fa48("182"), `font-medium ${config.color}`)}>{config.label}</div>
        {stryMutAct_9fa48("185") ? amount && status === 'succeeded' || <div className="text-sm text-gray-600">
            (
            {new Intl.NumberFormat('en-GB', {
            style: 'currency',
            currency
          }).format(amount / 100)}
            )
          </div> : stryMutAct_9fa48("184") ? false : stryMutAct_9fa48("183") ? true : (stryCov_9fa48("183", "184", "185"), (stryMutAct_9fa48("187") ? amount || status === 'succeeded' : stryMutAct_9fa48("186") ? true : (stryCov_9fa48("186", "187"), amount && (stryMutAct_9fa48("189") ? status !== 'succeeded' : stryMutAct_9fa48("188") ? true : (stryCov_9fa48("188", "189"), status === (stryMutAct_9fa48("190") ? "" : (stryCov_9fa48("190"), 'succeeded')))))) && <div className="text-sm text-gray-600">
            (
            {new Intl.NumberFormat(stryMutAct_9fa48("191") ? "" : (stryCov_9fa48("191"), 'en-GB'), stryMutAct_9fa48("192") ? {} : (stryCov_9fa48("192"), {
            style: stryMutAct_9fa48("193") ? "" : (stryCov_9fa48("193"), 'currency'),
            currency
          })).format(stryMutAct_9fa48("194") ? amount * 100 : (stryCov_9fa48("194"), amount / 100))}
            )
          </div>)}
      </div>
      {stryMutAct_9fa48("197") ? errorMessage && status === 'failed' || <p className="mt-2 text-sm text-red-600">{errorMessage}</p> : stryMutAct_9fa48("196") ? false : stryMutAct_9fa48("195") ? true : (stryCov_9fa48("195", "196", "197"), (stryMutAct_9fa48("199") ? errorMessage || status === 'failed' : stryMutAct_9fa48("198") ? true : (stryCov_9fa48("198", "199"), errorMessage && (stryMutAct_9fa48("201") ? status !== 'failed' : stryMutAct_9fa48("200") ? true : (stryCov_9fa48("200", "201"), status === (stryMutAct_9fa48("202") ? "" : (stryCov_9fa48("202"), 'failed')))))) && <p className="mt-2 text-sm text-red-600">{errorMessage}</p>)}
    </div>;
  }
}