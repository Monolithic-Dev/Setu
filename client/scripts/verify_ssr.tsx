// SSR smoke test — runtime-verifies the actual components render, using
// only globally-available react/react-dom/tsx, without needing `npm
// install` or vitest first. This is NOT a replacement for the real test
// suite the team should build with vitest + @testing-library/react (see
// src/App.test.tsx) — it's a lighter-weight check that catches "does this
// even render without crashing" before that heavier setup exists.
//
// Written after discovering two real things by actually trying to run
// this, not just reading the code:
//   1. import.meta.env is a Vite build-time injection, undefined outside
//      a real Vite runtime — src/api/queryClient.ts now guards against
//      this with optional chaining (`import.meta.env?.VITE_API_BASE`).
//   2. Components must be invoked via React.createElement/JSX, not a bare
//      function call, or hooks fail outside React's render context. That
//      was a bug in an earlier draft of *this* script, not the app code.
//
// Run: NODE_PATH=<path-to-global-node_modules> npx tsx client/scripts/verify_ssr.tsx
// (Once `npm install` has been run in client/, plain `npx tsx
// scripts/verify_ssr.tsx` from client/ works without NODE_PATH.)

import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import App from "../src/App";
import { ChatWindow } from "../src/components/Chat/ChatWindow";

let failures = 0;

function check(label: string, condition: boolean) {
  console.log(`${condition ? "PASS" : "FAIL"}: ${label}`);
  if (!condition) failures++;
}

try {
  const appHtml = renderToStaticMarkup(React.createElement(App));
  check("App renders without throwing", appHtml.length > 0);
  check("App shows the product title", appHtml.includes("Setu"));
  check("App shows the Kannada language toggle", appHtml.includes("ಕನ್ನಡ"));
  check("App shows the English language toggle", appHtml.includes("English"));
} catch (e) {
  console.error("App component FAILED to render:", e);
  failures++;
}

try {
  const chatHtmlEn = renderToStaticMarkup(React.createElement(ChatWindow, { language: "en" }));
  check("ChatWindow (English) renders without throwing", chatHtmlEn.length > 0);
  check("ChatWindow (English) shows the English placeholder", chatHtmlEn.includes("Ask a question"));

  const chatHtmlKn = renderToStaticMarkup(React.createElement(ChatWindow, { language: "kn" }));
  check("ChatWindow (Kannada) renders without throwing", chatHtmlKn.length > 0);
  check("ChatWindow (Kannada) shows real Kannada text, not boxes/garbage",
        chatHtmlKn.includes("ಪ್ರಶ್ನೆ ಕೇಳಿ"));
} catch (e) {
  console.error("ChatWindow component FAILED to render:", e);
  failures++;
}

console.log(`\n${failures === 0 ? "All checks passed." : `${failures} check(s) FAILED.`}`);
process.exit(failures === 0 ? 0 : 1);
