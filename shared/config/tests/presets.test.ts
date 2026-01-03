/**
 * Tests for Environment Presets
 *
 * Verifies preset configurations for different environments.
 */

import { describe, it, expect } from 'vitest';
import {
  DEV_PRESET,
  TEST_PRESET,
  PRODUCTION_PRESET,
  EnvironmentPresets,
  getPreset,
  mergePreset,
} from '../src/presets';

describe('Environment Presets', () => {
  describe('DEV_PRESET', () => {
    it('should have correct development settings', () => {
      expect(DEV_PRESET.ENVIRONMENT_MODE).toBe('dev');
      expect(DEV_PRESET.ENABLE_SUPABASE).toBe(false);
      expect(DEV_PRESET.ENABLE_PAYMENTS).toBe(false);
      expect(DEV_PRESET.LOG_LEVEL).toBe('debug');
      expect(DEV_PRESET.LOG_PRETTY_PRINT).toBe(true);
    });

    it('should use local database', () => {
      expect(DEV_PRESET.DATABASE_URL).toContain('localhost');
      expect(DEV_PRESET.DATABASE_URL).toContain('studyabroad_dev');
    });
  });

  describe('TEST_PRESET', () => {
    it('should have correct test settings', () => {
      expect(TEST_PRESET.ENVIRONMENT_MODE).toBe('test');
      expect(TEST_PRESET.ENABLE_SUPABASE).toBe(true);
      expect(TEST_PRESET.ENABLE_PAYMENTS).toBe(false);
      expect(TEST_PRESET.LOG_LEVEL).toBe('debug');
      expect(TEST_PRESET.LOG_PRETTY_PRINT).toBe(false);
    });
  });

  describe('PRODUCTION_PRESET', () => {
    it('should have correct production settings', () => {
      expect(PRODUCTION_PRESET.ENVIRONMENT_MODE).toBe('production');
      expect(PRODUCTION_PRESET.ENABLE_SUPABASE).toBe(true);
      expect(PRODUCTION_PRESET.ENABLE_PAYMENTS).toBe(true);
      expect(PRODUCTION_PRESET.LOG_LEVEL).toBe('error');
      expect(PRODUCTION_PRESET.LOG_CONSOLE_ENABLED).toBe(false);
    });

    it('should use production log directory', () => {
      expect(PRODUCTION_PRESET.LOG_DIR).toBe('/var/log/app');
    });
  });

  describe('EnvironmentPresets map', () => {
    it('should contain all environment modes', () => {
      expect(EnvironmentPresets).toHaveProperty('dev');
      expect(EnvironmentPresets).toHaveProperty('test');
      expect(EnvironmentPresets).toHaveProperty('production');
    });

    it('should map to correct presets', () => {
      expect(EnvironmentPresets.dev).toBe(DEV_PRESET);
      expect(EnvironmentPresets.test).toBe(TEST_PRESET);
      expect(EnvironmentPresets.production).toBe(PRODUCTION_PRESET);
    });
  });

  describe('getPreset()', () => {
    it('should return dev preset for dev mode', () => {
      const preset = getPreset('dev');
      expect(preset).toBe(DEV_PRESET);
    });

    it('should return test preset for test mode', () => {
      const preset = getPreset('test');
      expect(preset).toBe(TEST_PRESET);
    });

    it('should return production preset for production mode', () => {
      const preset = getPreset('production');
      expect(preset).toBe(PRODUCTION_PRESET);
    });
  });

  describe('mergePreset()', () => {
    it('should merge dev preset with overrides', () => {
      const merged = mergePreset('dev', { LOG_LEVEL: 'info' });

      expect(merged.ENVIRONMENT_MODE).toBe('dev');
      expect(merged.LOG_LEVEL).toBe('info'); // Override
      expect(merged.ENABLE_SUPABASE).toBe(false); // From preset
    });

    it('should merge test preset with overrides', () => {
      const merged = mergePreset('test', { LOG_DIR: '/custom/logs' });

      expect(merged.ENVIRONMENT_MODE).toBe('test');
      expect(merged.LOG_DIR).toBe('/custom/logs'); // Override
      expect(merged.ENABLE_SUPABASE).toBe(true); // From preset
    });

    it('should merge production preset with overrides', () => {
      const merged = mergePreset('production', {
        LOG_CONSOLE_ENABLED: true,
        LOG_LEVEL: 'warn',
      });

      expect(merged.ENVIRONMENT_MODE).toBe('production');
      expect(merged.LOG_CONSOLE_ENABLED).toBe(true); // Override
      expect(merged.LOG_LEVEL).toBe('warn'); // Override
      expect(merged.ENABLE_PAYMENTS).toBe(true); // From preset
    });

    it('should not mutate original preset', () => {
      const original = { ...DEV_PRESET };
      mergePreset('dev', { LOG_LEVEL: 'error' });

      expect(DEV_PRESET).toEqual(original);
    });
  });
});
