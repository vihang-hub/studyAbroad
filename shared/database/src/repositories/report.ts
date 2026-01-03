/**
 * Report repository
 * Handles report CRUD operations with soft delete support
 */

import { SoftDeleteBaseRepository } from './base';
import { Report, mapToReport } from '../types';

/**
 * Report repository implementation
 */
export class ReportRepository extends SoftDeleteBaseRepository<Report> {
  protected tableName = 'reports';
  protected idField = 'report_id';

  /**
   * Find report by ID (excludes soft-deleted)
   */
  async findById(reportId: string, userId: string): Promise<Report | null> {
    const { rows } = await this.db.query<any>(
      `SELECT * FROM reports
       WHERE report_id = $1
         AND user_id = $2
         AND ${this.whereActive()}`,
      [reportId, userId],
    );

    return rows[0] ? mapToReport(rows[0]) : null;
  }

  /**
   * Find report by ID including soft-deleted records
   */
  async findByIdIncludingDeleted(reportId: string, userId: string): Promise<Report | null> {
    const { rows } = await this.db.query<any>(
      `SELECT * FROM reports
       WHERE report_id = $1
         AND user_id = $2`,
      [reportId, userId],
    );

    return rows[0] ? mapToReport(rows[0]) : null;
  }

  /**
   * List all active reports for a user
   */
  async listByUser(
    userId: string,
    limit: number = 50,
    offset: number = 0,
  ): Promise<Report[]> {
    const { rows } = await this.db.query<any>(
      `SELECT * FROM reports
       WHERE user_id = $1
         AND ${this.whereActive()}
       ORDER BY created_at DESC
       LIMIT $2 OFFSET $3`,
      [userId, limit, offset],
    );

    return rows.map(mapToReport);
  }

  /**
   * Count total active reports for a user
   */
  async countByUser(userId: string): Promise<number> {
    const { rows } = await this.db.query<{ count: string }>(
      `SELECT COUNT(*) as count FROM reports
       WHERE user_id = $1
         AND ${this.whereActive()}`,
      [userId],
    );

    return parseInt(rows[0].count, 10);
  }

  /**
   * Create a new report
   */
  async create(data: {
    userId: string;
    subject: string;
    country: string;
    content: any;
    citations: any[];
    status: 'generating' | 'completed' | 'failed';
    expiresAt: Date;
  }): Promise<Report> {
    const { rows } = await this.db.query<any>(
      `INSERT INTO reports (user_id, subject, country, content, citations, status, expires_at)
       VALUES ($1, $2, $3, $4, $5, $6, $7)
       RETURNING *`,
      [
        data.userId,
        data.subject,
        data.country,
        JSON.stringify(data.content),
        JSON.stringify(data.citations),
        data.status,
        data.expiresAt,
      ],
    );

    return mapToReport(rows[0]);
  }

  /**
   * Update report status
   */
  async updateStatus(
    reportId: string,
    userId: string,
    status: 'generating' | 'completed' | 'failed',
  ): Promise<void> {
    await this.db.query(
      `UPDATE reports
       SET status = $1, updated_at = NOW()
       WHERE report_id = $2
         AND user_id = $3
         AND ${this.whereActive()}`,
      [status, reportId, userId],
    );
  }

  /**
   * Update report content and citations
   */
  async updateContent(
    reportId: string,
    userId: string,
    content: any,
    citations: any[],
  ): Promise<void> {
    await this.db.query(
      `UPDATE reports
       SET content = $1, citations = $2, updated_at = NOW()
       WHERE report_id = $3
         AND user_id = $4
         AND ${this.whereActive()}`,
      [JSON.stringify(content), JSON.stringify(citations), reportId, userId],
    );
  }

  /**
   * Soft delete expired reports (background job)
   * Returns number of reports soft-deleted
   */
  async softDeleteExpired(): Promise<number> {
    const { rowCount } = await this.db.query(
      `UPDATE reports
       SET deleted_at = NOW()
       WHERE expires_at < NOW()
         AND ${this.whereActive()}`,
    );

    return rowCount;
  }

  /**
   * List all reports expiring soon (for notification purposes)
   */
  async listExpiringSoon(daysBeforeExpiry: number = 3): Promise<Report[]> {
    const { rows } = await this.db.query<any>(
      `SELECT * FROM reports
       WHERE expires_at <= NOW() + INTERVAL '${daysBeforeExpiry} days'
         AND expires_at > NOW()
         AND ${this.whereActive()}
       ORDER BY expires_at ASC`,
    );

    return rows.map(mapToReport);
  }

  /**
   * Count total active reports in the system
   */
  async countAll(): Promise<number> {
    const { rows } = await this.db.query<{ count: string }>(
      `SELECT COUNT(*) as count FROM reports
       WHERE ${this.whereActive()}`,
    );

    return parseInt(rows[0].count, 10);
  }

  /**
   * Count soft-deleted reports in the system
   */
  async countDeleted(): Promise<number> {
    const { rows } = await this.db.query<{ count: string }>(
      `SELECT COUNT(*) as count FROM reports
       WHERE ${this.whereDeleted()}`,
    );

    return parseInt(rows[0].count, 10);
  }
}
