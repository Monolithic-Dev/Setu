import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Catalyst Functions in production are same-origin; this proxies
      // /server/* to a local Catalyst dev server during `npm run dev`.
      // TODO(Phase 8): confirm the actual local dev port `catalyst serve`
      // uses once real Catalyst CLI access exists — 3000 is a placeholder.
      "/server": "http://localhost:3000",
    },
  },
  test: {
    environment: "jsdom",
    setupFiles: ["./src/test-setup.ts"],
    globals: true,
  },
});
