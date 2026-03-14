/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class CopilotPanel extends Component {
    static template = "ipai_odoo_copilot_bridge.Panel";

    setup() {
        this.rpc = useService("rpc");
        this.state = useState({
            prompt: "",
            response: "",
            loading: false,
            blocked: false,
        });
    }

    async onSend() {
        if (!this.state.prompt.trim()) return;
        this.state.loading = true;
        this.state.response = "";
        this.state.blocked = false;

        try {
            const result = await this.rpc("/ipai/copilot/respond", {
                prompt: this.state.prompt,
            });
            if (result.blocked) {
                this.state.blocked = true;
                this.state.response = result.reason || "Request blocked.";
            } else {
                this.state.response = result.content || "";
            }
        } catch {
            this.state.response = "Copilot unavailable.";
            this.state.blocked = true;
        } finally {
            this.state.loading = false;
        }
    }
}

registry.category("actions").add("ipai_odoo_copilot_bridge.panel", CopilotPanel);
