## Production Standards Mandate
In all workspaces and for all tasks, you MUST prioritize industry-standard, production-ready approaches over quick hacks or minimal viable products. Code architecture, tooling choices, error handling, and design patterns must reflect professional, enterprise-grade engineering. 

## Strict Git Workflow Constraint
For every completed task or logical unit of work, you MUST proactively execute the following Git workflow before ending your turn:
1. **Branch:** Create a dedicated, properly named feature branch (e.g., `git checkout -b feat/describe-feature`).
2. **Commit:** Stage relevant files and use standard conventional commit messages (e.g., `feat: ...`, `fix: ...`).
3. **Push:** Push the branch to the remote repository (`git push -u origin <branch-name>`).
4. **Pull Request:** Create a Pull Request using `gh pr create`. 
   - You MUST include a highly detailed, industry-standard PR description covering:
     - **What:** Summary of the changes.
     - **Why:** The rationale and business/technical context.
     - **How:** High-level architectural approach or key implementation details.
     - **Verification:** How the changes were tested (unit tests, manual testing, etc.).
   - If the GitHub CLI is not authenticated, output the direct URL for the user to create the PR, and provide the markdown template for the PR description in your response so the user can copy-paste it.
