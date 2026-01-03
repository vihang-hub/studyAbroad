/**
 * Feature Flag Provider for Next.js App
 * Wraps the app with feature flag context for environment-based toggles
 *
 * Uses @study-abroad/shared-feature-flags for consistent feature flag logic
 * across frontend and backend
 */

'use client';

import React, {
  createContext, useContext, useEffect, useState,
} from 'react';
import {
  FeatureFlags,
  type FeatureFlagState,
  type EnvironmentMode,
  Feature,
} from '@study-abroad/shared-feature-flags';
import { getConfig } from '@/lib/config';
import { logInfo } from '@/lib/logger';

interface FeatureFlagContextType {
  flags: FeatureFlagState;
  environmentMode: EnvironmentMode;
  isFeatureEnabled: (feature: Feature) => boolean;
  isLoading: boolean;
}

const FeatureFlagContext = createContext<FeatureFlagContextType | undefined>(undefined);

interface FeatureFlagProviderProps {
  children: React.ReactNode;
}

/**
 * Feature Flag Provider Component
 * Initializes feature flags based on environment configuration
 */
export function FeatureFlagProvider({ children }: FeatureFlagProviderProps) {
  const [flags, setFlags] = useState<FeatureFlagState>({
    ENABLE_SUPABASE: false,
    ENABLE_PAYMENTS: false,
  });
  const [environmentMode, setEnvironmentMode] = useState<EnvironmentMode>('development');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    try {
      // Get configuration
      const config = getConfig();

      // Initialize feature flags
      const featureFlags = new FeatureFlags(config.mode);

      // Set environment mode
      setEnvironmentMode(config.mode);

      // Evaluate all feature flags
      const evaluatedFlags: FeatureFlagState = {
        ENABLE_SUPABASE: featureFlags.isEnabled('ENABLE_SUPABASE'),
        ENABLE_PAYMENTS: featureFlags.isEnabled('ENABLE_PAYMENTS'),
      };

      setFlags(evaluatedFlags);

      // Log feature flag initialization
      logInfo('Feature flags initialized', {
        environmentMode: config.mode,
        flags: evaluatedFlags,
      });
    } catch (error) {
      console.error('[FeatureFlagProvider] Failed to initialize feature flags:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const isFeatureEnabled = (feature: Feature): boolean => flags[feature] || false;

  const value: FeatureFlagContextType = {
    flags,
    environmentMode,
    isFeatureEnabled,
    isLoading,
  };

  return (
    <FeatureFlagContext.Provider value={value}>
      {children}
    </FeatureFlagContext.Provider>
  );
}

/**
 * Hook to access feature flags
 */
export function useFeatureFlags(): FeatureFlagContextType {
  const context = useContext(FeatureFlagContext);
  if (!context) {
    throw new Error('useFeatureFlags must be used within a FeatureFlagProvider');
  }
  return context;
}

/**
 * Hook to check if a specific feature is enabled
 */
export function useFeature(feature: Feature): boolean {
  const { isFeatureEnabled } = useFeatureFlags();
  return isFeatureEnabled(feature);
}

/**
 * Hook to get the current environment mode
 */
export function useEnvironment(): EnvironmentMode {
  const { environmentMode } = useFeatureFlags();
  return environmentMode;
}

/**
 * Component to conditionally render based on feature flag
 */
interface FeatureGateProps {
  feature: Feature;
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export function FeatureGate({ feature, children, fallback = null }: FeatureGateProps) {
  const isEnabled = useFeature(feature);

  if (!isEnabled && fallback) {
    return <>{fallback}</>;
  }

  return isEnabled ? <>{children}</> : null;
}

/**
 * Component to conditionally render based on environment
 */
interface EnvironmentGateProps {
  environments: EnvironmentMode[];
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export function EnvironmentGate({
  environments,
  children,
  fallback = null,
}: EnvironmentGateProps) {
  const currentEnvironment = useEnvironment();
  const isAllowed = environments.includes(currentEnvironment);

  if (!isAllowed && fallback) {
    return <>{fallback}</>;
  }

  return isAllowed ? <>{children}</> : null;
}
