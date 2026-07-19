# Hackathon Live Demo Script: Setu

**Goal:** In 3 minutes, demonstrate the core capabilities of Setu: Bilingual Voice AI, Role-Based Access Control, Network Graph Visualization, and Administrative Auditing.

## Setup Before Demo
1. Run `npm run dev` in the `client` folder.
2. Ensure the app is loaded on `http://localhost:5173` on the Login Screen.

---

## 1. Introduction (30 seconds)
**Speaker:** "Hello judges. We are Team [Name], and this is Setu. Setu solves the critical bottleneck in Indian policing: officers struggle to extract rapid, actionable intelligence from thousands of text-heavy FIRs, especially when systems are built only for English."

**Speaker:** "Setu is a bilingual, conversational AI interface to the crime database. Let me show you how a Station Officer uses it."

## 2. Role-Based Access & Querying (45 seconds)
**Action:** On the Login Screen, select **Station Officer**. Leave Station ID as `S-101`. Click Login.
**Speaker:** "I log in as a Station Officer. Note that my access is strictly limited to my jurisdiction. If I ask a question..."

**Action:** Type (or use Voice Capture): *"Show me recent chain snatching incidents."*
**Action:** Wait for the AI to return the result.
**Speaker:** "Setu uses a Hybrid Retrieval system. It instantly pulls the relevant cases, generates a synthesized answer, and provides exact case citations so the officer can verify the truth. No hallucinations."

**Action:** Type the follow-up: *"Who are the known associates of the suspect in that case?"*
**Speaker:** "And Setu is truly conversational. Notice how I just said 'that case'—the AI remembers the context of my previous question and automatically applies it to find the associates without needing me to re-type the case details."

## 3. The Network Graph (30 seconds)
**Action:** Point to the Network Graph on the right side of the screen.
**Speaker:** "Data isn't just text. On the right, Setu automatically visualizes the criminal network using D3.js. Officers can instantly see how this chain-snatching suspect connects to other locations or known modus operandi, finding links they would have missed reading paper files."

## 4. Bilingual Support & Export (45 seconds)
**Action:** Click the "ಕನ್ನಡ" (Kannada) language toggle in the header.
**Speaker:** "Because rural policing happens in local languages, Setu is natively bilingual. If I ask a question in Kannada, the underlying AI routes it to a dedicated Kannada semantic search index we built."

**Action:** Click the **"📄 Export to PDF"** button.
**Speaker:** "Once the officer finds a crucial lead, they can export the intelligence to PDF with one click. The CSS strips away the UI, leaving a clean, secure report ready for the official case file." *(Show the print preview screen briefly, then cancel).*

## 5. Security & Audit Logs (30 seconds)
**Action:** Refresh the page to go back to Login. Select **System Admin** and click Login.
**Action:** Click the **"Audit Logs"** toggle in the header.
**Speaker:** "Finally, with great AI power comes great responsibility. How do we prevent misuse? I'll log in as a System Admin. Setu maintains an immutable Audit Trail. We log exactly who asked what, in what language, and exactly which cases the AI used to generate the answer. Total accountability."

**Speaker:** "Setu bridges the gap between raw data and actionable intelligence. Thank you."

## 6. Q&A / Prepared Responses
**If asked about "Socio-Demographic Insights" or "Behavioral Profiling":**
**Speaker:** "We looked closely at those requirements and made a deliberate call: we implement the legitimate version of both, without the part that causes real harm. We interpret 'behavioral profiling' strictly as modus operandi pattern analysis, and 'socio-demographic insights' strictly as aggregate area-level trend data. We deliberately excluded individual-level demographic scoring because those proxies can encode historical policing bias—a known failure mode we wanted to proactively avoid for real-world adoptability."
