// Real test suite, for once `npm install` has been run (needs vitest +
// @testing-library/react, both already in package.json's devDependencies).
// scripts/verify_ssr.tsx covers the same rendering ground with lighter
// tooling for a pre-npm-install sanity check — this is the one to build
// on and extend as real interaction tests get added (typing a query,
// clicking send, toggling language), not a duplicate to maintain in parallel.

import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import App from "../App";
import { ChatWindow } from "./ChatWindow";

describe("App", () => {
  it("renders the product title", () => {
    render(<App />);
    expect(screen.getByText(/Setu/)).toBeInTheDocument();
  });

  it("renders both language toggle buttons", () => {
    render(<App />);
    expect(screen.getByText("English")).toBeInTheDocument();
    expect(screen.getByText("ಕನ್ನಡ")).toBeInTheDocument();
  });

  it("defaults to English", () => {
    render(<App />);
    const englishButton = screen.getByText("English");
    expect(englishButton).toHaveAttribute("aria-pressed", "true");
  });
});

describe("ChatWindow", () => {
  it("renders the English placeholder when language=en", () => {
    render(<ChatWindow language="en" />);
    expect(screen.getByPlaceholderText(/Ask a question/)).toBeInTheDocument();
  });

  it("renders the Kannada placeholder when language=kn", () => {
    render(<ChatWindow language="kn" />);
    expect(screen.getByPlaceholderText(/ಪ್ರಶ್ನೆ ಕೇಳಿ/)).toBeInTheDocument();
  });

  it("starts with an empty chat history", () => {
    const { container } = render(<ChatWindow language="en" />);
    expect(container.querySelectorAll(".chat-turn").length).toBe(0);
  });
});
