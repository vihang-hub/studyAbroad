/**
 * Tests for utility functions
 */

import { describe, it, expect } from 'vitest';
import { cn } from '../../src/lib/utils';

describe('utils', () => {
  describe('cn (className merge utility)', () => {
    it('should merge multiple class strings', () => {
      const result = cn('class1', 'class2', 'class3');
      expect(result).toBe('class1 class2 class3');
    });

    it('should handle single class', () => {
      const result = cn('single-class');
      expect(result).toBe('single-class');
    });

    it('should handle empty inputs', () => {
      const result = cn();
      expect(result).toBe('');
    });

    it('should filter out falsy values', () => {
      const result = cn('class1', null, undefined, false, 'class2');
      expect(result).toBe('class1 class2');
    });

    it('should merge Tailwind classes with conflicts', () => {
      // twMerge should handle conflicting Tailwind classes
      const result = cn('bg-red-500', 'bg-blue-500');
      expect(result).toBe('bg-blue-500');
    });

    it('should handle conditional classes', () => {
      const isActive = true;
      const isDisabled = false;
      const result = cn(
        'base-class',
        isActive && 'active',
        isDisabled && 'disabled'
      );
      expect(result).toBe('base-class active');
    });

    it('should handle object syntax for conditional classes', () => {
      const result = cn('base', { active: true, disabled: false });
      expect(result).toBe('base active');
    });

    it('should handle array of classes', () => {
      const result = cn(['class1', 'class2'], 'class3');
      expect(result).toBe('class1 class2 class3');
    });

    it('should handle mixed inputs', () => {
      const result = cn(
        'base',
        ['array1', 'array2'],
        { conditional: true },
        null,
        'string'
      );
      expect(result).toBe('base array1 array2 conditional string');
    });

    it('should merge padding classes correctly', () => {
      const result = cn('p-4', 'p-2');
      expect(result).toBe('p-2');
    });

    it('should merge margin classes correctly', () => {
      const result = cn('mx-4', 'mx-auto');
      expect(result).toBe('mx-auto');
    });

    it('should handle responsive variants', () => {
      const result = cn('text-sm', 'md:text-base', 'lg:text-lg');
      expect(result).toBe('text-sm md:text-base lg:text-lg');
    });

    it('should handle state variants', () => {
      const result = cn('bg-blue-500', 'hover:bg-blue-600', 'focus:ring-2');
      expect(result).toBe('bg-blue-500 hover:bg-blue-600 focus:ring-2');
    });

    it('should handle complex component composition', () => {
      const baseStyles = 'flex items-center justify-center rounded-md';
      const sizeStyles = 'px-4 py-2 text-sm';
      const colorStyles = 'bg-blue-500 text-white';
      const hoverStyles = 'hover:bg-blue-600';

      const result = cn(baseStyles, sizeStyles, colorStyles, hoverStyles);
      expect(result).toContain('flex');
      expect(result).toContain('items-center');
      expect(result).toContain('bg-blue-500');
      expect(result).toContain('hover:bg-blue-600');
    });
  });
});
