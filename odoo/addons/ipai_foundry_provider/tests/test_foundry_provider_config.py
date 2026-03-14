"""Tests for ipai.foundry.provider.config — exact field map and validation rules.

Canonical test values derived from confirmed Azure screenshots:
  Foundry Project:    data-intel-ph
  Project Endpoint:   https://data-intel-ph-resource.services.ai.azure.com/api/projects/data-intel-ph
  Resource Endpoint:  https://data-intel-ph-resource.services.ai.azure.com/
  OpenAI Endpoint:    https://data-intel-ph-resource.openai.azure.com/
"""

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestFoundryProviderConfig(TransactionCase):

    # =====================================================================
    # Canonical values — the exact baseline from Azure screenshots
    # =====================================================================
    CANONICAL_PROJECT_NAME = "data-intel-ph"
    CANONICAL_PROJECT_ENDPOINT = (
        "https://data-intel-ph-resource.services.ai.azure.com/api/projects/data-intel-ph"
    )
    CANONICAL_RESOURCE_ENDPOINT = "https://data-intel-ph-resource.services.ai.azure.com/"
    CANONICAL_OPENAI_ENDPOINT = "https://data-intel-ph-resource.openai.azure.com/"
    CANONICAL_RESOURCE_STEM = "data-intel-ph-resource"

    def _create_config(self, **overrides):
        """Create a config record with canonical defaults, allowing overrides."""
        vals = {
            "name": "Test Config",
            "foundry_project_name": self.CANONICAL_PROJECT_NAME,
            "foundry_project_endpoint": self.CANONICAL_PROJECT_ENDPOINT,
            "foundry_resource_endpoint": self.CANONICAL_RESOURCE_ENDPOINT,
            "azure_openai_endpoint": self.CANONICAL_OPENAI_ENDPOINT,
            "auth_mode": "entra_id",
        }
        vals.update(overrides)
        return self.env["ipai.foundry.provider.config"].create(vals)

    # =====================================================================
    # 1. Happy path — canonical values pass all validators
    # =====================================================================

    def test_canonical_values_pass(self):
        """All canonical values from Azure screenshots must pass validation."""
        config = self._create_config()
        self.assertEqual(config.foundry_project_name, self.CANONICAL_PROJECT_NAME)
        self.assertEqual(config.foundry_project_endpoint, self.CANONICAL_PROJECT_ENDPOINT)
        self.assertEqual(config.foundry_resource_endpoint, self.CANONICAL_RESOURCE_ENDPOINT)
        self.assertEqual(config.azure_openai_endpoint, self.CANONICAL_OPENAI_ENDPOINT)

    # =====================================================================
    # 2. Normalization — endpoint expansion
    # =====================================================================

    def test_normalize_short_name_to_project_endpoint(self):
        """Short resource name + project name → full project endpoint."""
        config = self._create_config()
        result = config._normalize_foundry_project_endpoint(
            "data-intel-ph-resource", "data-intel-ph"
        )
        self.assertEqual(result, self.CANONICAL_PROJECT_ENDPOINT)

    def test_normalize_resource_endpoint_to_project_endpoint(self):
        """Resource endpoint + project name → full project endpoint."""
        config = self._create_config()
        result = config._normalize_foundry_project_endpoint(
            "https://data-intel-ph-resource.services.ai.azure.com",
            "data-intel-ph",
        )
        self.assertEqual(result, self.CANONICAL_PROJECT_ENDPOINT)

    def test_normalize_already_canonical_project_endpoint(self):
        """Already-canonical endpoint → returned unchanged."""
        config = self._create_config()
        result = config._normalize_foundry_project_endpoint(
            self.CANONICAL_PROJECT_ENDPOINT, self.CANONICAL_PROJECT_NAME
        )
        self.assertEqual(result, self.CANONICAL_PROJECT_ENDPOINT)

    def test_normalize_short_name_to_resource_endpoint(self):
        """Short resource name → full resource endpoint with trailing slash."""
        config = self._create_config()
        result = config._normalize_foundry_resource_endpoint("data-intel-ph-resource")
        self.assertEqual(result, self.CANONICAL_RESOURCE_ENDPOINT)

    def test_normalize_resource_endpoint_trailing_slash(self):
        """Resource endpoint without trailing slash → adds trailing slash."""
        config = self._create_config()
        result = config._normalize_foundry_resource_endpoint(
            "https://data-intel-ph-resource.services.ai.azure.com"
        )
        self.assertEqual(result, self.CANONICAL_RESOURCE_ENDPOINT)

    def test_normalize_short_name_to_openai_endpoint(self):
        """Short resource name → full OpenAI endpoint with trailing slash."""
        config = self._create_config()
        result = config._normalize_azure_openai_endpoint("data-intel-ph-resource")
        self.assertEqual(result, self.CANONICAL_OPENAI_ENDPOINT)

    def test_normalize_openai_endpoint_trailing_slash(self):
        """OpenAI endpoint without trailing slash → adds trailing slash."""
        config = self._create_config()
        result = config._normalize_azure_openai_endpoint(
            "https://data-intel-ph-resource.openai.azure.com"
        )
        self.assertEqual(result, self.CANONICAL_OPENAI_ENDPOINT)

    def test_normalize_empty_string(self):
        """Empty input → empty output for all normalizers."""
        config = self._create_config()
        self.assertEqual(config._normalize_foundry_project_endpoint("", ""), "")
        self.assertEqual(config._normalize_foundry_resource_endpoint(""), "")
        self.assertEqual(config._normalize_azure_openai_endpoint(""), "")

    # =====================================================================
    # 3. Extraction helpers
    # =====================================================================

    def test_extract_project_endpoint_parts(self):
        """Extract resource stem + project name from canonical project endpoint."""
        config = self._create_config()
        resource, project = config._extract_project_endpoint_parts(
            self.CANONICAL_PROJECT_ENDPOINT
        )
        self.assertEqual(resource, self.CANONICAL_RESOURCE_STEM)
        self.assertEqual(project, self.CANONICAL_PROJECT_NAME)

    def test_extract_foundry_resource_name(self):
        """Extract resource stem from canonical resource endpoint."""
        config = self._create_config()
        stem = config._extract_foundry_resource_name(self.CANONICAL_RESOURCE_ENDPOINT)
        self.assertEqual(stem, self.CANONICAL_RESOURCE_STEM)

    def test_extract_openai_resource_name(self):
        """Extract resource stem from canonical OpenAI endpoint."""
        config = self._create_config()
        stem = config._extract_openai_resource_name(self.CANONICAL_OPENAI_ENDPOINT)
        self.assertEqual(stem, self.CANONICAL_RESOURCE_STEM)

    def test_extract_from_invalid_returns_none(self):
        """Invalid endpoints return None."""
        config = self._create_config()
        r, p = config._extract_project_endpoint_parts("https://example.com")
        self.assertIsNone(r)
        self.assertIsNone(p)
        self.assertIsNone(config._extract_foundry_resource_name("https://example.com"))
        self.assertIsNone(config._extract_openai_resource_name("https://example.com"))

    # =====================================================================
    # 4. Audience selection
    # =====================================================================

    def test_audience_foundry_project(self):
        """Foundry project operations → ai.azure.com audience."""
        config = self._create_config()
        self.assertEqual(
            config._get_auth_audience("foundry_project"),
            "https://ai.azure.com/.default",
        )

    def test_audience_azure_openai(self):
        """Azure OpenAI inference → cognitiveservices audience."""
        config = self._create_config()
        self.assertEqual(
            config._get_auth_audience("azure_openai"),
            "https://cognitiveservices.azure.com/.default",
        )

    def test_audience_unsupported_raises(self):
        """Unsupported operation type → ValidationError."""
        config = self._create_config()
        with self.assertRaises(ValidationError):
            config._get_auth_audience("unknown_type")

    # =====================================================================
    # 5. Connection target selectors
    # =====================================================================

    def test_connection_target_foundry_project(self):
        """Foundry project target returns project endpoint + correct audience."""
        config = self._create_config()
        target = config._get_connection_target("foundry_project")
        self.assertEqual(target["endpoint"], self.CANONICAL_PROJECT_ENDPOINT)
        self.assertEqual(target["audience"], "https://ai.azure.com/.default")

    def test_connection_target_azure_openai(self):
        """Azure OpenAI target returns OpenAI endpoint + correct audience."""
        config = self._create_config(
            model_deployment_name="gpt-4.1",
        )
        target = config._get_connection_target("azure_openai")
        self.assertEqual(target["endpoint"], self.CANONICAL_OPENAI_ENDPOINT)
        self.assertEqual(
            target["audience"], "https://cognitiveservices.azure.com/.default"
        )
        self.assertEqual(target["deployment"], "gpt-4.1")

    def test_connection_target_unsupported_raises(self):
        """Unsupported connection target type → ValidationError."""
        config = self._create_config()
        with self.assertRaises(ValidationError):
            config._get_connection_target("unknown")

    # =====================================================================
    # 6. V1 — Project endpoint format + name match
    # =====================================================================

    def test_v1_missing_project_endpoint_raises(self):
        """Empty project endpoint → ValidationError."""
        with self.assertRaises(ValidationError):
            self._create_config(foundry_project_endpoint="")

    def test_v1_malformed_project_endpoint_raises(self):
        """Non-matching project endpoint → ValidationError."""
        with self.assertRaises(ValidationError):
            self._create_config(
                foundry_project_endpoint="https://example.com/not-valid"
            )

    def test_v1_project_name_mismatch_raises(self):
        """Project name in endpoint differs from field → ValidationError."""
        with self.assertRaises(ValidationError):
            self._create_config(
                foundry_project_name="different-project",
                foundry_project_endpoint=(
                    "https://data-intel-ph-resource.services.ai.azure.com"
                    "/api/projects/data-intel-ph"
                ),
            )

    def test_v1_project_endpoint_with_trailing_slash_passes(self):
        """Trailing slash on project endpoint should pass."""
        config = self._create_config(
            foundry_project_endpoint=self.CANONICAL_PROJECT_ENDPOINT + "/",
        )
        self.assertTrue(config.id)

    # =====================================================================
    # 7. V2 — Resource endpoint format
    # =====================================================================

    def test_v2_valid_resource_endpoint_passes(self):
        """Canonical resource endpoint passes."""
        config = self._create_config()
        self.assertTrue(config.id)

    def test_v2_invalid_resource_endpoint_raises(self):
        """Non-matching resource endpoint → ValidationError."""
        with self.assertRaises(ValidationError):
            self._create_config(
                foundry_resource_endpoint="https://example.com/invalid"
            )

    def test_v2_empty_resource_endpoint_passes(self):
        """Empty resource endpoint is allowed (optional field)."""
        config = self._create_config(foundry_resource_endpoint="")
        self.assertTrue(config.id)

    # =====================================================================
    # 8. V3 — Azure OpenAI endpoint format
    # =====================================================================

    def test_v3_valid_openai_endpoint_passes(self):
        """Canonical OpenAI endpoint passes."""
        config = self._create_config()
        self.assertTrue(config.id)

    def test_v3_invalid_openai_endpoint_raises(self):
        """Non-matching OpenAI endpoint → ValidationError."""
        with self.assertRaises(ValidationError):
            self._create_config(
                azure_openai_endpoint="https://example.com/not-openai"
            )

    def test_v3_empty_openai_endpoint_passes(self):
        """Empty OpenAI endpoint is allowed (optional field)."""
        config = self._create_config(azure_openai_endpoint="")
        self.assertTrue(config.id)

    # =====================================================================
    # 9. V4 — Resource stem consistency
    # =====================================================================

    def test_v4_consistent_stems_pass(self):
        """All endpoints using same resource stem → passes."""
        config = self._create_config()
        self.assertTrue(config.id)

    def test_v4_mismatched_resource_stem_raises(self):
        """Resource endpoint with different stem → ValidationError."""
        with self.assertRaises(ValidationError):
            self._create_config(
                foundry_resource_endpoint="https://other-resource.services.ai.azure.com/",
            )

    def test_v4_mismatched_openai_stem_raises(self):
        """OpenAI endpoint with different stem → ValidationError."""
        with self.assertRaises(ValidationError):
            self._create_config(
                azure_openai_endpoint="https://other-resource.openai.azure.com/",
            )

    def test_v4_partial_endpoints_same_stem_pass(self):
        """Only project + resource (no OpenAI) with same stem → passes."""
        config = self._create_config(azure_openai_endpoint="")
        self.assertTrue(config.id)

    # =====================================================================
    # 10. V5 — Auth mode requirements
    # =====================================================================

    def test_v5_entra_id_managed_identity_passes(self):
        """Entra ID with no secret fields (managed identity) → passes."""
        config = self._create_config(
            auth_mode="entra_id",
            tenant_id="",
            client_id="",
            client_secret_ref="",
            api_key_secret_ref="",
        )
        self.assertTrue(config.id)

    def test_v5_entra_id_service_principal_passes(self):
        """Entra ID with full SP shape → passes."""
        config = self._create_config(
            auth_mode="entra_id",
            tenant_id="00000000-0000-0000-0000-000000000001",
            client_id="00000000-0000-0000-0000-000000000002",
            client_secret_ref="kv://kv-ipai-dev/foundry-client-secret",
        )
        self.assertTrue(config.id)

    def test_v5_entra_id_partial_sp_raises(self):
        """Entra ID with partial SP fields (missing client_secret_ref) → ValidationError."""
        with self.assertRaises(ValidationError):
            self._create_config(
                auth_mode="entra_id",
                tenant_id="00000000-0000-0000-0000-000000000001",
                client_id="00000000-0000-0000-0000-000000000002",
                client_secret_ref="",
            )

    def test_v5_api_key_with_ref_passes(self):
        """API Key mode with kv:// reference → passes."""
        config = self._create_config(
            auth_mode="api_key",
            api_key_secret_ref="kv://kv-ipai-dev/foundry-api-key",
        )
        self.assertTrue(config.id)

    def test_v5_api_key_without_ref_raises(self):
        """API Key mode with empty reference → ValidationError."""
        with self.assertRaises(ValidationError):
            self._create_config(
                auth_mode="api_key",
                api_key_secret_ref="",
            )

    # =====================================================================
    # 11. V6 — Secret reference shape
    # =====================================================================

    def test_v6_kv_prefix_passes(self):
        """kv:// prefixed secret → passes."""
        config = self._create_config(
            auth_mode="api_key",
            api_key_secret_ref="kv://kv-ipai-dev/foundry-api-key",
        )
        self.assertTrue(config.id)

    def test_v6_raw_secret_raises(self):
        """Raw secret value (no kv:// prefix) → ValidationError."""
        with self.assertRaises(ValidationError):
            self._create_config(
                auth_mode="api_key",
                api_key_secret_ref="sk-1234567890abcdef",
            )

    def test_v6_raw_client_secret_raises(self):
        """Raw client secret (no kv:// prefix) → ValidationError."""
        with self.assertRaises(ValidationError):
            self._create_config(
                auth_mode="entra_id",
                tenant_id="00000000-0000-0000-0000-000000000001",
                client_id="00000000-0000-0000-0000-000000000002",
                client_secret_ref="raw-secret-value",
            )

    # =====================================================================
    # 12. What NOT to do — negative cases
    # =====================================================================

    def test_do_not_use_openai_endpoint_for_project_operations(self):
        """OpenAI endpoint must NOT be used for project operations."""
        config = self._create_config()
        target = config._get_connection_target("foundry_project")
        self.assertNotEqual(target["endpoint"], self.CANONICAL_OPENAI_ENDPOINT)
        self.assertNotIn("openai.azure.com", target["endpoint"])

    def test_do_not_use_project_endpoint_for_openai_inference(self):
        """Project endpoint must NOT be used for OpenAI inference."""
        config = self._create_config()
        target = config._get_connection_target("azure_openai")
        self.assertNotEqual(target["endpoint"], self.CANONICAL_PROJECT_ENDPOINT)
        self.assertNotIn("/api/projects/", target["endpoint"])

    def test_do_not_accept_bare_resource_name_as_endpoint(self):
        """Bare resource name (no protocol) must fail project endpoint validation."""
        with self.assertRaises(ValidationError):
            self._create_config(
                foundry_project_endpoint="data-intel-ph-resource",
            )
