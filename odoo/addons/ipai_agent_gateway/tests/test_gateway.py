"""
Gateway integration tests.

Tests the agent gateway controllers with mocked request context.
"""

from odoo.tests.common import TransactionCase


class TestAgentGateway(TransactionCase):
    """Test suite for the Odoo Agent Gateway."""

    def setUp(self):
        super().setUp()
        self.partner = self.env["res.partner"].create({
            "name": "Test Customer",
            "email": "test@example.com",
            "customer_rank": 1,
        })

    def test_audit_log_immutable(self):
        """Audit logs cannot be modified or deleted."""
        log = self.env["ipai.agent.audit.log"].create({
            "trace_id": "test-trace-001",
            "tool": "odoo.search_partners",
            "user_id": self.env.uid,
            "company_id": self.env.company.id,
            "input_summary": "{}",
            "output_summary": '{"count": 1}',
            "request_timestamp": "2026-03-13 00:00:00",
        })

        with self.assertRaises(Exception):
            log.write({"tool": "modified"})

        with self.assertRaises(Exception):
            log.unlink()

    def test_audit_log_creation(self):
        """Audit logs can be created."""
        log = self.env["ipai.agent.audit.log"].create({
            "trace_id": "test-trace-002",
            "tool": "odoo.get_invoices",
            "user_id": self.env.uid,
            "company_id": self.env.company.id,
            "input_summary": '{"state": "posted"}',
            "output_summary": '{"count": 0}',
            "success": True,
            "request_timestamp": "2026-03-13 00:00:00",
        })
        self.assertEqual(log.tool, "odoo.get_invoices")
        self.assertTrue(log.success)
