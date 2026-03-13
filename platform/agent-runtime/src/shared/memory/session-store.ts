/**
 * Session Store
 *
 * Manages per-user, per-session, and per-project state.
 * In production, backed by Azure Database for PostgreSQL (via Supabase).
 */

export interface SessionState {
  session_id: string;
  user_id: number;
  company_id: number;
  created_at: string;
  updated_at: string;
  context: {
    referenced_entities: ReferencedEntity[];
    pending_actions: PendingAction[];
    conversation_history: ConversationEntry[];
  };
}

export interface ReferencedEntity {
  model: string;
  id: number;
  name: string;
  last_accessed: string;
}

export interface PendingAction {
  tool: string;
  parameters: Record<string, unknown>;
  status: "pending" | "confirmed" | "rejected";
  created_at: string;
}

export interface ConversationEntry {
  role: "user" | "assistant";
  content: string;
  timestamp: string;
  tools_used?: string[];
}

/**
 * In-memory session store for development.
 * Replace with PostgreSQL-backed store for production.
 */
export class InMemorySessionStore {
  private sessions = new Map<string, SessionState>();

  async get(sessionId: string): Promise<SessionState | null> {
    return this.sessions.get(sessionId) ?? null;
  }

  async set(session: SessionState): Promise<void> {
    session.updated_at = new Date().toISOString();
    this.sessions.set(session.session_id, session);
  }

  async delete(sessionId: string): Promise<void> {
    this.sessions.delete(sessionId);
  }

  async create(sessionId: string, userId: number, companyId: number): Promise<SessionState> {
    const now = new Date().toISOString();
    const session: SessionState = {
      session_id: sessionId,
      user_id: userId,
      company_id: companyId,
      created_at: now,
      updated_at: now,
      context: {
        referenced_entities: [],
        pending_actions: [],
        conversation_history: [],
      },
    };
    this.sessions.set(sessionId, session);
    return session;
  }

  async addEntity(sessionId: string, entity: ReferencedEntity): Promise<void> {
    const session = await this.get(sessionId);
    if (!session) return;

    // Deduplicate by model+id
    session.context.referenced_entities = session.context.referenced_entities.filter(
      (e) => !(e.model === entity.model && e.id === entity.id),
    );
    session.context.referenced_entities.push(entity);

    // Keep last 20 entities
    if (session.context.referenced_entities.length > 20) {
      session.context.referenced_entities = session.context.referenced_entities.slice(-20);
    }

    await this.set(session);
  }

  async addConversation(sessionId: string, entry: ConversationEntry): Promise<void> {
    const session = await this.get(sessionId);
    if (!session) return;

    session.context.conversation_history.push(entry);

    // Keep last 50 turns
    if (session.context.conversation_history.length > 50) {
      session.context.conversation_history = session.context.conversation_history.slice(-50);
    }

    await this.set(session);
  }
}
