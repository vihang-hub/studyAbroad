/**
 * Tests for Report repository
 */
// @ts-nocheck


import { describe, it, expect, beforeEach, vi } from 'vitest';
import { ReportRepository } from '../../src/repositories/report';
import { DatabaseAdapter } from '../../src/adapters/base';

describe('ReportRepository', () => {
  let repository: ReportRepository;
  let mockAdapter: DatabaseAdapter;

  beforeEach(() => {
    mockAdapter = {
      query: vi.fn(),
      beginTransaction: vi.fn(),
      close: vi.fn(),
      getType: vi.fn(() => 'postgres'),
    } as any;

    repository = new ReportRepository(mockAdapter);
  });

  const mockReportRow = {
    report_id: 'report-123',
    user_id: 'user-123',
    subject: 'Computer Science',
    country: 'UK',
    content: { section1: 'content' },
    citations: [{ title: 'Source 1', url: 'https://example.com' }],
    status: 'completed',
    created_at: new Date('2025-01-01'),
    expires_at: new Date('2025-01-31'),
    updated_at: new Date('2025-01-01'),
    deleted_at: null,
  };

  describe('findById', () => {
    it('should find active report by ID', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [mockReportRow],
        rowCount: 1,
      });

      const result = await repository.findById('report-123', 'user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('WHERE report_id = $1'),
        ['report-123', 'user-123'],
      );
      expect(result?.reportId).toBe('report-123');
      expect(result?.deletedAt).toBeNull();
    });

    it('should not find soft-deleted report', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      const result = await repository.findById('report-123', 'user-123');

      expect(result).toBeNull();
    });

    it('should not find report from different user', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      const result = await repository.findById('report-123', 'different-user');

      expect(result).toBeNull();
    });

    it('should include deleted_at IS NULL filter', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      await repository.findById('report-123', 'user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('deleted_at IS NULL'),
        expect.any(Array),
      );
    });
  });

  describe('findByIdIncludingDeleted', () => {
    it('should find soft-deleted report', async () => {
      const deletedRow = {
        ...mockReportRow,
        deleted_at: new Date('2025-01-15'),
      };

      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [deletedRow],
        rowCount: 1,
      });

      const result = await repository.findByIdIncludingDeleted('report-123', 'user-123');

      expect(result?.reportId).toBe('report-123');
      expect(result?.deletedAt).toEqual(new Date('2025-01-15'));
    });

    it('should not include deleted_at filter', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      await repository.findByIdIncludingDeleted('report-123', 'user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.not.stringContaining('deleted_at IS NULL'),
        expect.any(Array),
      );
    });
  });

  describe('listByUser', () => {
    it('should list active reports for user', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [mockReportRow, { ...mockReportRow, report_id: 'report-456' }],
        rowCount: 2,
      });

      const result = await repository.listByUser('user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('WHERE user_id = $1'),
        ['user-123', 50, 0],
      );
      expect(result).toHaveLength(2);
    });

    it('should support pagination', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      await repository.listByUser('user-123', 10, 20);

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('LIMIT $2 OFFSET $3'),
        ['user-123', 10, 20],
      );
    });

    it('should order by created_at DESC', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      await repository.listByUser('user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('ORDER BY created_at DESC'),
        expect.any(Array),
      );
    });

    it('should exclude soft-deleted reports', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      await repository.listByUser('user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('deleted_at IS NULL'),
        expect.any(Array),
      );
    });

    it('should use default limit and offset', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      await repository.listByUser('user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(expect.any(String), ['user-123', 50, 0]);
    });
  });

  describe('countByUser', () => {
    it('should count active reports', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [{ count: '5' }],
        rowCount: 1,
      });

      const result = await repository.countByUser('user-123');

      expect(result).toBe(5);
    });

    it('should exclude soft-deleted reports', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [{ count: '3' }],
        rowCount: 1,
      });

      await repository.countByUser('user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('deleted_at IS NULL'),
        ['user-123'],
      );
    });
  });

  describe('create', () => {
    it('should create a new report', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [mockReportRow],
        rowCount: 1,
      });

      const result = await repository.create({
        userId: 'user-123',
        subject: 'Computer Science',
        country: 'UK',
        content: { section1: 'content' },
        citations: [{ title: 'Source 1', url: 'https://example.com' }],
        status: 'generating',
        expiresAt: new Date('2025-01-31'),
      });

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('INSERT INTO reports'),
        expect.arrayContaining([
          'user-123',
          'Computer Science',
          'UK',
          expect.any(String), // JSON stringified content
          expect.any(String), // JSON stringified citations
          'generating',
          expect.any(Date),
        ]),
      );
      expect(result.reportId).toBe('report-123');
    });

    it('should stringify content and citations', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [mockReportRow],
        rowCount: 1,
      });

      await repository.create({
        userId: 'user-123',
        subject: 'Computer Science',
        country: 'UK',
        content: { section1: 'content', section2: 'more' },
        citations: [{ title: 'Source 1', url: 'https://example.com' }],
        status: 'generating',
        expiresAt: new Date('2025-01-31'),
      });

      const call = (mockAdapter.query as any).mock.calls[0];
      expect(call[1][3]).toBe(JSON.stringify({ section1: 'content', section2: 'more' }));
      expect(call[1][4]).toBe(JSON.stringify([{ title: 'Source 1', url: 'https://example.com' }]));
    });
  });

  describe('updateStatus', () => {
    it('should update report status', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 1,
      });

      await repository.updateStatus('report-123', 'user-123', 'completed');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('UPDATE reports'),
        ['completed', 'report-123', 'user-123'],
      );
    });

    it('should update updated_at timestamp', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 1,
      });

      await repository.updateStatus('report-123', 'user-123', 'completed');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('updated_at = NOW()'),
        expect.any(Array),
      );
    });

    it('should only update active reports', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 1,
      });

      await repository.updateStatus('report-123', 'user-123', 'completed');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('deleted_at IS NULL'),
        expect.any(Array),
      );
    });
  });

  describe('updateContent', () => {
    it('should update report content and citations', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 1,
      });

      const newContent = { section1: 'new content' };
      const newCitations = [{ title: 'New Source', url: 'https://new.com' }];

      await repository.updateContent('report-123', 'user-123', newContent, newCitations);

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('UPDATE reports'),
        [JSON.stringify(newContent), JSON.stringify(newCitations), 'report-123', 'user-123'],
      );
    });
  });

  describe('softDelete', () => {
    it('should soft delete report', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 1,
      });

      await repository.softDelete('report-123', 'user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('UPDATE reports'),
        ['report-123', 'user-123'],
      );
      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('SET deleted_at = NOW()'),
        expect.any(Array),
      );
    });

    it('should only soft delete active reports', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 1,
      });

      await repository.softDelete('report-123', 'user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('AND deleted_at IS NULL'),
        expect.any(Array),
      );
    });
  });

  describe('restore', () => {
    it('should restore soft-deleted report', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 1,
      });

      await repository.restore('report-123', 'user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('SET deleted_at = NULL'),
        ['report-123', 'user-123'],
      );
    });

    it('should only restore deleted reports', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 1,
      });

      await repository.restore('report-123', 'user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('AND deleted_at IS NOT NULL'),
        expect.any(Array),
      );
    });
  });

  describe('isDeleted', () => {
    it('should return true for deleted report', () => {
      const deletedReport = {
        ...mockReportRow,
        deletedAt: new Date('2025-01-15'),
      };

      const result = repository.isDeleted(deletedReport as any);

      expect(result).toBe(true);
    });

    it('should return false for active report', () => {
      const activeReport = {
        ...mockReportRow,
        deletedAt: null,
      };

      const result = repository.isDeleted(activeReport as any);

      expect(result).toBe(false);
    });
  });

  describe('softDeleteExpired', () => {
    it('should soft delete expired reports', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 3,
      });

      const result = await repository.softDeleteExpired();

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('WHERE expires_at < NOW()'),
      );
      expect(result).toBe(3);
    });

    it('should only delete active reports', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 2,
      });

      await repository.softDeleteExpired();

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('AND deleted_at IS NULL'),
      );
    });
  });

  describe('listExpiringSoon', () => {
    it('should list reports expiring within default 3 days', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [mockReportRow],
        rowCount: 1,
      });

      const result = await repository.listExpiringSoon();

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining("INTERVAL '3 days'"),
      );
      expect(result).toHaveLength(1);
    });

    it('should support custom expiry window', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      await repository.listExpiringSoon(7);

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining("INTERVAL '7 days'"),
      );
    });

    it('should only include active reports', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      await repository.listExpiringSoon();

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('deleted_at IS NULL'),
      );
    });

    it('should order by expires_at ASC', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      await repository.listExpiringSoon();

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('ORDER BY expires_at ASC'),
      );
    });
  });

  describe('countAll', () => {
    it('should count all active reports', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [{ count: '100' }],
        rowCount: 1,
      });

      const result = await repository.countAll();

      expect(result).toBe(100);
    });

    it('should exclude soft-deleted reports', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [{ count: '50' }],
        rowCount: 1,
      });

      await repository.countAll();

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('WHERE deleted_at IS NULL'),
      );
    });
  });

  describe('countDeleted', () => {
    it('should count soft-deleted reports', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [{ count: '15' }],
        rowCount: 1,
      });

      const result = await repository.countDeleted();

      expect(result).toBe(15);
    });

    it('should only count deleted reports', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [{ count: '10' }],
        rowCount: 1,
      });

      await repository.countDeleted();

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('WHERE deleted_at IS NOT NULL'),
      );
    });
  });
});
