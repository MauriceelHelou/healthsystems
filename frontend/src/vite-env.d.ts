/// <reference types="vite/client" />

interface ImportMetaEnv {
  // API Configuration
  readonly VITE_API_URL?: string;
  readonly VITE_API_TIMEOUT?: string;
  readonly VITE_ENABLE_API_LOGGING?: string;

  // Environment
  readonly VITE_ENVIRONMENT?: string;
  readonly MODE?: string;

  // Feature Flags
  readonly VITE_ENABLE_DEBUG?: string;
  readonly VITE_ENABLE_ANALYTICS?: string;
  readonly VITE_ENABLE_PATHFINDING?: string;
  readonly VITE_ENABLE_CRISIS_EXPLORER?: string;
  readonly VITE_ENABLE_PATHWAY_EXPLORER?: string;
  readonly VITE_ENABLE_NODE_IMPORTANCE?: string;
  readonly VITE_ENABLE_ALCOHOLISM_SYSTEM?: string;
  readonly VITE_ENABLE_SYSTEMS_MAP?: string;
  readonly VITE_ENABLE_EXPERIMENTAL?: string;

  // Analytics
  readonly VITE_GOOGLE_ANALYTICS_ID?: string;
  readonly VITE_SENTRY_DSN?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
