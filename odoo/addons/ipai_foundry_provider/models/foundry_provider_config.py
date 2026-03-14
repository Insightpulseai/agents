import re
from urllib.parse import urlparse

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


# ---------------------------------------------------------------------------
# Canonical endpoint regexes
# ---------------------------------------------------------------------------
# Foundry project endpoint:
#   https://<resource>.services.ai.azure.com/api/projects/<project>
FOUNDRY_PROJECT_ENDPOINT_RE = re.compile(
    r"^https://([a-zA-Z0-9-]+)\.services\.ai\.azure\.com/api/projects/([a-zA-Z0-9._-]+?)/?$"
)

# Foundry resource endpoint:
#   https://<resource>.services.ai.azure.com/
FOUNDRY_RESOURCE_ENDPOINT_RE = re.compile(
    r"^https://([a-zA-Z0-9-]+)\.services\.ai\.azure\.com/?$"
)

# Azure OpenAI endpoint:
#   https://<resource>.openai.azure.com/
AZURE_OPENAI_ENDPOINT_RE = re.compile(
    r"^https://([a-zA-Z0-9-]+)\.openai\.azure\.com/?$"
)


class FoundryProviderConfig(models.Model):
    _name = "ipai.foundry.provider.config"
    _description = "Azure Foundry Provider Configuration"
    _rec_name = "name"

    # =========================================================================
    # FIELD MAP — canonical fields
    # =========================================================================

    name = fields.Char(required=True, default="Azure Foundry")
    active = fields.Boolean(default=True)

    provider_type = fields.Selection(
        selection=[
            ("azure_foundry", "Azure Foundry"),
        ],
        required=True,
        default="azure_foundry",
    )

    # -- Auth -----------------------------------------------------------------

    auth_mode = fields.Selection(
        selection=[
            ("entra_id", "Microsoft Entra ID"),
            ("api_key", "API Key"),
        ],
        required=True,
        default="entra_id",
        help=(
            "Use Entra ID for production where possible. "
            "API key mode should use secret references only."
        ),
    )

    # -- Foundry project ------------------------------------------------------
    # Canonical value:
    #   foundry_project_name       = data-intel-ph
    #   foundry_project_endpoint   = https://data-intel-ph-resource.services.ai.azure.com/api/projects/data-intel-ph
    #
    # Rule: The <project> segment in the endpoint MUST match foundry_project_name.

    foundry_project_name = fields.Char(
        string="Foundry Project",
        required=True,
        help="Logical Azure Foundry project name, e.g. data-intel-ph",
    )

    foundry_project_endpoint = fields.Char(
        string="Foundry Project API Endpoint",
        required=True,
        help="Format: https://<resource>.services.ai.azure.com/api/projects/<project>",
    )

    # -- Foundry resource -----------------------------------------------------
    # Canonical value:
    #   https://data-intel-ph-resource.services.ai.azure.com/
    #
    # Rule: The <resource> stem MUST match the one in the project endpoint.

    foundry_resource_endpoint = fields.Char(
        string="Foundry Resource Endpoint",
        help="Format: https://<resource>.services.ai.azure.com/",
    )

    # -- Azure OpenAI ---------------------------------------------------------
    # Canonical value:
    #   https://data-intel-ph-resource.openai.azure.com/
    #
    # Rule: The <resource> stem MUST match the one in the project endpoint.

    azure_openai_endpoint = fields.Char(
        string="Azure OpenAI Endpoint",
        help="Format: https://<resource>.openai.azure.com/",
    )

    # -- Azure location -------------------------------------------------------
    azure_location = fields.Char(
        string="Azure Location",
        help="Optional display/validation hint, e.g. eastus2",
    )

    # -- Model deployment -----------------------------------------------------
    model_deployment_name = fields.Char(
        string="Model Deployment",
        help="Azure OpenAI deployment name, e.g. gpt-4.1",
    )

    # -- Agent ----------------------------------------------------------------
    agent_name = fields.Char(
        string="Agent Name",
        help="Physical Azure Foundry agent name if project/agent operations are used.",
    )

    # -- Search ---------------------------------------------------------------
    search_service_name = fields.Char(string="Search Service")
    search_connection_name = fields.Char(string="Search Connection")
    search_index_name = fields.Char(string="Search Index")

    # -- API key (secret ref only) -------------------------------------------
    api_key_secret_ref = fields.Char(
        string="API Key Secret Reference",
        help="Secret reference only, e.g. kv://kv-ipai-dev/foundry-api-key",
    )

    # -- Service principal (Entra ID) ----------------------------------------
    tenant_id = fields.Char(string="Tenant ID")
    client_id = fields.Char(string="Client ID")
    client_secret_ref = fields.Char(
        string="Client Secret Reference",
        help="Secret reference only, e.g. kv://kv-ipai-dev/foundry-client-secret",
    )

    # -- Behavioral flags ----------------------------------------------------
    read_only_mode = fields.Boolean(
        string="Read-Only / Draft-Only Mode",
        default=True,
    )

    agent_memory = fields.Boolean(
        string="Agent Memory",
        default=False,
    )

    # =========================================================================
    # NORMALIZATION HELPERS
    # =========================================================================

    def _normalize_foundry_project_endpoint(self, endpoint, project_name=None):
        """Normalize user input to canonical project endpoint form.

        Accepted inputs and their normalization:
          Full URL → validated and returned as-is
          Resource endpoint + project name → appended /api/projects/<project>
          Short name (no dots) + project name → expanded to full URL
        """
        endpoint = (endpoint or "").strip().rstrip("/")
        project_name = (project_name or "").strip()
        if not endpoint:
            return ""

        # Already canonical
        if FOUNDRY_PROJECT_ENDPOINT_RE.match(endpoint):
            return endpoint

        # Resource endpoint + project name → append path
        if FOUNDRY_RESOURCE_ENDPOINT_RE.match(endpoint) and project_name:
            return f"{endpoint}/api/projects/{project_name}"

        # Partial URL on the right host
        if endpoint.startswith("https://"):
            host = urlparse(endpoint).netloc
            if (
                host.endswith(".services.ai.azure.com")
                and project_name
                and "/api/projects/" not in endpoint
            ):
                return f"https://{host}/api/projects/{project_name}"

        # Short name only (e.g. "data-intel-ph-resource")
        if not endpoint.startswith("https://") and "." not in endpoint and project_name:
            return f"https://{endpoint}.services.ai.azure.com/api/projects/{project_name}"

        return endpoint

    def _normalize_foundry_resource_endpoint(self, endpoint):
        """Normalize to https://<resource>.services.ai.azure.com/ (trailing slash)."""
        endpoint = (endpoint or "").strip()
        if not endpoint:
            return ""
        if not endpoint.startswith("https://") and "." not in endpoint:
            endpoint = f"https://{endpoint}.services.ai.azure.com"
        return endpoint.rstrip("/") + "/"

    def _normalize_azure_openai_endpoint(self, endpoint):
        """Normalize to https://<resource>.openai.azure.com/ (trailing slash)."""
        endpoint = (endpoint or "").strip()
        if not endpoint:
            return ""
        if not endpoint.startswith("https://") and "." not in endpoint:
            endpoint = f"https://{endpoint}.openai.azure.com"
        return endpoint.rstrip("/") + "/"

    # =========================================================================
    # ONCHANGE — live normalization in the UI
    # =========================================================================

    @api.onchange("foundry_project_name", "foundry_project_endpoint")
    def _onchange_foundry_project_endpoint(self):
        for rec in self:
            rec.foundry_project_endpoint = rec._normalize_foundry_project_endpoint(
                rec.foundry_project_endpoint,
                rec.foundry_project_name,
            )

    @api.onchange("foundry_resource_endpoint")
    def _onchange_foundry_resource_endpoint(self):
        for rec in self:
            rec.foundry_resource_endpoint = rec._normalize_foundry_resource_endpoint(
                rec.foundry_resource_endpoint,
            )

    @api.onchange("azure_openai_endpoint")
    def _onchange_azure_openai_endpoint(self):
        for rec in self:
            rec.azure_openai_endpoint = rec._normalize_azure_openai_endpoint(
                rec.azure_openai_endpoint,
            )

    # =========================================================================
    # DERIVED ENDPOINT METADATA
    # =========================================================================

    def _extract_project_endpoint_parts(self, endpoint):
        """Return (resource_stem, project_name) or (None, None)."""
        match = FOUNDRY_PROJECT_ENDPOINT_RE.match((endpoint or "").strip())
        if not match:
            return None, None
        return match.group(1), match.group(2)

    def _extract_foundry_resource_name(self, endpoint):
        """Return resource stem from a resource endpoint."""
        normalized = (endpoint or "").strip().rstrip("/")
        for candidate in [normalized + "/", normalized]:
            match = FOUNDRY_RESOURCE_ENDPOINT_RE.match(candidate)
            if match:
                return match.group(1)
        return None

    def _extract_openai_resource_name(self, endpoint):
        """Return resource stem from an OpenAI endpoint."""
        normalized = (endpoint or "").strip().rstrip("/")
        for candidate in [normalized + "/", normalized]:
            match = AZURE_OPENAI_ENDPOINT_RE.match(candidate)
            if match:
                return match.group(1)
        return None

    # =========================================================================
    # AUDIENCE SELECTION
    # =========================================================================
    # Core rule:
    #   foundry_project / agent APIs → https://ai.azure.com/.default
    #   azure_openai inference       → https://cognitiveservices.azure.com/.default

    def _get_auth_audience(self, operation_type):
        """Return the correct OAuth audience for the given operation type.

        operation_type:
          'foundry_project' → Foundry project / agent APIs
          'azure_openai'    → Direct Azure OpenAI model inference
        """
        self.ensure_one()
        if operation_type == "foundry_project":
            return "https://ai.azure.com/.default"
        if operation_type == "azure_openai":
            return "https://cognitiveservices.azure.com/.default"
        raise ValidationError(_("Unsupported operation type: %s") % operation_type)

    # =========================================================================
    # VALIDATORS
    # =========================================================================

    # -- V1: Project endpoint format + project name match --------------------
    @api.constrains("foundry_project_name", "foundry_project_endpoint")
    def _check_foundry_project_endpoint(self):
        for rec in self:
            endpoint = (rec.foundry_project_endpoint or "").strip()
            project_name = (rec.foundry_project_name or "").strip()

            if not endpoint:
                raise ValidationError(_("Foundry Project API Endpoint is required."))

            match = FOUNDRY_PROJECT_ENDPOINT_RE.match(endpoint)
            if not match:
                raise ValidationError(
                    _(
                        "Invalid Foundry Project API Endpoint. "
                        "Expected format: https://<resource>.services.ai.azure.com/api/projects/<project>"
                    )
                )

            endpoint_project = match.group(2)
            if project_name and endpoint_project != project_name:
                raise ValidationError(
                    _(
                        "Foundry project mismatch: endpoint project '%(ep)s' "
                        "does not match configured project '%(cfg)s'.",
                        ep=endpoint_project,
                        cfg=project_name,
                    )
                )

    # -- V2: Resource endpoint format ----------------------------------------
    @api.constrains("foundry_resource_endpoint")
    def _check_foundry_resource_endpoint(self):
        for rec in self:
            endpoint = (rec.foundry_resource_endpoint or "").strip()
            if not endpoint:
                continue
            if not FOUNDRY_RESOURCE_ENDPOINT_RE.match(endpoint.rstrip("/") + "/"):
                raise ValidationError(
                    _(
                        "Invalid Foundry Resource Endpoint. "
                        "Expected format: https://<resource>.services.ai.azure.com/"
                    )
                )

    # -- V3: Azure OpenAI endpoint format ------------------------------------
    @api.constrains("azure_openai_endpoint")
    def _check_azure_openai_endpoint(self):
        for rec in self:
            endpoint = (rec.azure_openai_endpoint or "").strip()
            if not endpoint:
                continue
            if not AZURE_OPENAI_ENDPOINT_RE.match(endpoint.rstrip("/") + "/"):
                raise ValidationError(
                    _(
                        "Invalid Azure OpenAI Endpoint. "
                        "Expected format: https://<resource>.openai.azure.com/"
                    )
                )

    # -- V4: Resource stem consistency across all three endpoints ------------
    @api.constrains(
        "foundry_project_endpoint",
        "foundry_resource_endpoint",
        "azure_openai_endpoint",
    )
    def _check_resource_stem_consistency(self):
        """All three endpoints must use the same Azure resource stem.

        Example — all must be 'data-intel-ph-resource':
          project:  https://data-intel-ph-resource.services.ai.azure.com/api/projects/data-intel-ph
          resource: https://data-intel-ph-resource.services.ai.azure.com/
          openai:   https://data-intel-ph-resource.openai.azure.com/
        """
        for rec in self:
            project_resource, _ = rec._extract_project_endpoint_parts(
                rec.foundry_project_endpoint
            )
            foundry_resource = (
                rec._extract_foundry_resource_name(rec.foundry_resource_endpoint)
                if rec.foundry_resource_endpoint
                else None
            )
            openai_resource = (
                rec._extract_openai_resource_name(rec.azure_openai_endpoint)
                if rec.azure_openai_endpoint
                else None
            )

            stems = [x for x in [project_resource, foundry_resource, openai_resource] if x]
            if stems and len(set(stems)) > 1:
                raise ValidationError(
                    _(
                        "Azure resource mismatch across endpoint families. "
                        "Project endpoint, Foundry resource endpoint, and Azure OpenAI "
                        "endpoint must use the same resource stem. "
                        "Found: %s"
                    )
                    % ", ".join(sorted(set(stems)))
                )

    # -- V5: Auth mode requirements ------------------------------------------
    @api.constrains(
        "auth_mode",
        "api_key_secret_ref",
        "tenant_id",
        "client_id",
        "client_secret_ref",
    )
    def _check_auth_mode_requirements(self):
        """Enforce auth mode contract:

        api_key mode:
          - api_key_secret_ref is required
        entra_id mode:
          - Either managed identity (no secret fields at all)
          - Or full service principal shape (tenant_id + client_id + client_secret_ref)
        """
        for rec in self:
            if rec.auth_mode == "api_key":
                if not (rec.api_key_secret_ref or "").strip():
                    raise ValidationError(
                        _(
                            "API Key Secret Reference is required when auth mode is API Key."
                        )
                    )
            elif rec.auth_mode == "entra_id":
                has_service_principal = all(
                    [
                        (rec.tenant_id or "").strip(),
                        (rec.client_id or "").strip(),
                        (rec.client_secret_ref or "").strip(),
                    ]
                )
                has_managed_identity = not any(
                    [
                        (rec.tenant_id or "").strip(),
                        (rec.client_id or "").strip(),
                        (rec.client_secret_ref or "").strip(),
                        (rec.api_key_secret_ref or "").strip(),
                    ]
                )
                if not (has_service_principal or has_managed_identity):
                    raise ValidationError(
                        _(
                            "Entra ID mode must use either managed identity "
                            "(no secret fields) or a full service principal shape "
                            "(tenant_id, client_id, client_secret_ref)."
                        )
                    )

    # -- V6: Secret reference shape ------------------------------------------
    @api.constrains("api_key_secret_ref", "client_secret_ref")
    def _check_secret_reference_shape(self):
        """Secret fields must use kv:// references, never raw secrets."""
        for rec in self:
            for value, label in [
                (rec.api_key_secret_ref, _("API Key Secret Reference")),
                (rec.client_secret_ref, _("Client Secret Reference")),
            ]:
                value = (value or "").strip()
                if not value:
                    continue
                if not value.startswith("kv://"):
                    raise ValidationError(
                        _(
                            "%s must be a secret reference "
                            "(for example kv://kv-ipai-dev/secret-name), "
                            "not a raw secret."
                        )
                        % label
                    )

    # =========================================================================
    # CONNECTION TARGET SELECTORS
    # =========================================================================

    def _get_connection_target(self, operation_type):
        """Return endpoint + audience for the given operation type.

        operation_type:
          'foundry_project' → project endpoint + ai.azure.com audience
          'azure_openai'    → OpenAI endpoint + cognitiveservices audience
        """
        self.ensure_one()
        if operation_type == "foundry_project":
            return {
                "endpoint": self.foundry_project_endpoint,
                "audience": self._get_auth_audience("foundry_project"),
            }
        if operation_type == "azure_openai":
            return {
                "endpoint": self.azure_openai_endpoint,
                "audience": self._get_auth_audience("azure_openai"),
                "deployment": self.model_deployment_name,
            }
        raise ValidationError(
            _("Unsupported connection target type: %s") % operation_type
        )
