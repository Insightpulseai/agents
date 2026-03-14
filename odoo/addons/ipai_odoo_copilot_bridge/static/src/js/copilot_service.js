/** @odoo-module **/

/**
 * Copilot Service — frontend bridge to the copilot backend controller.
 *
 * Provides a simple API for Odoo JS components to send messages to the
 * copilot and receive structured responses. All actual AI processing
 * happens server-side; this service only relays through the Odoo
 * JSON-RPC controller.
 */

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

const copilotService = {
    dependencies: [],

    start() {
        let currentSessionId = null;

        return {
            /**
             * Send a chat message to the copilot.
             *
             * @param {string} message - User's query
             * @param {Object} [options]
             * @param {string} [options.contextModel] - Current Odoo model
             * @param {number} [options.contextRecordId] - Current record ID
             * @returns {Promise<Object>} Copilot response
             */
            async chat(message, options = {}) {
                const result = await rpc("/ipai/copilot/chat", {
                    message,
                    session_id: currentSessionId,
                    context_model: options.contextModel || null,
                    context_record_id: options.contextRecordId || null,
                });
                currentSessionId = result.session_id;
                return result;
            },

            /**
             * Confirm a proposed write action.
             *
             * @param {Object} actionPayload - The action to confirm
             * @param {string} confirmationToken - One-time token
             * @returns {Promise<Object>} Confirmation response
             */
            async confirmAction(actionPayload, confirmationToken) {
                return rpc("/ipai/copilot/confirm", {
                    session_id: currentSessionId,
                    action_payload: actionPayload,
                    confirmation_token: confirmationToken,
                });
            },

            /**
             * Retrieve message history for the current session.
             *
             * @returns {Promise<Object>} Message history
             */
            async getHistory() {
                if (!currentSessionId) {
                    return { messages: [] };
                }
                return rpc("/ipai/copilot/history", {
                    session_id: currentSessionId,
                });
            },

            /**
             * Start a new session (clears current session ID).
             */
            newSession() {
                currentSessionId = null;
            },

            /**
             * Get the current session ID.
             *
             * @returns {string|null}
             */
            getSessionId() {
                return currentSessionId;
            },
        };
    },
};

registry.category("services").add("ipai_copilot", copilotService);
