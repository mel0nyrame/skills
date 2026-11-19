# Surgical Changes & Code Execution

Apply these rules whenever writing code, refactoring, or editing existing documents and artifacts.

## 1. Pre-Edit Inspection
- Inspect the existing implementation, style, structure, and conventions before choosing an approach.
- Single-use code or disposable explanatory scripts do not need reusable abstractions—keep them simple and self-contained.

## 2. Surgical Changes
**Test:** *Can every changed line trace directly to the user's request?*

- **Match existing conventions:** Follow the surrounding structure, terminology, and formatting unless explicitly asked to change them.
- **Stay strictly in scope:** Mention unrelated bugs, formatting issues, or potential refactors in your response instead of fixing them incidentally.
- **Clean up your own residue:** Remove unused imports, variables, or functions *introduced by your changes*. Preserve pre-existing dead code unless its removal was requested.
- **Keep references synced:** Update directly affected callers, docs, or copies when your changes require it for consistency.
