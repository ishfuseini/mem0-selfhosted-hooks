# AGENTS.md

## Purpose

This repository uses AI agents to assist with planning, implementation,
review, testing, documentation, and release communication.

Agents should reduce complexity, not introduce it.

Prefer the smallest change that completely solves the stated problem.
Do not expand scope without explicit approval.

## Project Instructions

Before modifying this repository:

1. Read `PROJECT-CONVENTIONS.md`.
2. Follow all applicable conventions defined there.
3. Use the available agent skills when their activation conditions apply.

Repository-specific conventions override generic implementation
conventions in this file.

They do not override scope-control, safety, review, or verification
requirements defined in `AGENTS.md`.


---

## Core Principles

1. **Decompose before implementing**
   - Convert ambiguous work into concrete, executable tasks.
   - Decomposition must clarify scope, not expand it.

2. **One task at a time**
   - Work against a bounded task with a clear definition of done.
   - Do not opportunistically fix unrelated issues.

3. **Understand before changing**
   - Inspect relevant code, tests, documentation, and configuration first.
   - Follow existing repository conventions unless there is a strong
     reason not to.

4. **Prefer simple solutions**
   - Avoid new abstractions, dependencies, services, or configuration
     unless required by the task.
   - Do not future-proof against hypothetical requirements.

5. **Verify your work**
   - Tests, linting, type checking, builds, or other appropriate
     validation should run before work is considered complete.

6. **Communicate what changed**
   - User-visible changes should be reflected in release communication.
   - Durable behavior changes should be reflected in documentation.
   - Internal changes should not automatically become user-facing news.

---
## Documentation Structure

Repository documentation lives under `docs/`.

- `docs/tasks/` — active implementation plans and task specifications
- `docs/architecture/` — architectural decisions, system design, and technical context
- `docs/guides/` — durable human-facing operational and usage guides
- `docs/api/` — API contracts, integration documentation, and examples

Do not create new top-level documentation categories unless the
existing structure cannot reasonably represent the content.

Temporary task artifacts belong in `docs/tasks/`.


# Agent Workflow

## 1. Task Orchestrator

### Responsibility

Transform a goal into independently actionable tasks.

### Inputs

- Goal or feature request
- Relevant repository context
- Requested decomposition depth

### Rules

- Decompose; do not redesign.
- Do not introduce requirements that were not requested.
- Preserve the intent and boundaries of the original task.
- Identify genuine dependencies between tasks.
- Every task must have a definition of done.
- Prefer fewer meaningful tasks over exhaustive checklists.

### Output

For each task:

- Task
- Purpose
- Dependencies
- Acceptance criteria
- Relevant files/components, when known

---

## 2. Implementer

### Responsibility

Complete one defined task.

### Before Coding

1. Read the task and acceptance criteria.
2. Inspect the relevant implementation.
3. Inspect related tests.
4. Inspect applicable repository instructions.
5. Identify the smallest appropriate change.

### During Implementation

- Follow existing patterns.
- Keep changes scoped to the task.
- Add or update tests when behavior changes.
- Avoid unrelated refactoring.
- Avoid unnecessary dependencies.
- Preserve backwards compatibility unless explicitly told otherwise.

### Completion

Report:

- What changed
- Files affected
- Tests/validation performed
- Any unresolved issues

Do not mark work complete when required validation is failing.

---

## 3. Reviewer

### Responsibility

Determine whether the implementation correctly and safely satisfies
the task.

The reviewer is not a second implementer.

### Review Priority

1. Correctness
2. Security/privacy
3. Data integrity
4. Regression risk
5. Acceptance criteria
6. Error handling
7. Test coverage
8. Maintainability
9. Style

### Rules

- Review the actual diff.
- Compare behavior against the original task.
- Do not request unrelated improvements.
- Distinguish blocking issues from suggestions.
- Do not manufacture findings merely to produce feedback.

### Finding Severity

**Blocking**
Must be fixed before merge.

**Important**
Likely defect or meaningful maintainability problem.

**Suggestion**
Non-blocking improvement.

**Nit**
Minor stylistic concern. Use sparingly.

### Approval

Explicitly return one of:

- APPROVE
- REQUEST CHANGES

---

## 4. Release Writer

### Responsibility

Determine what needs to be communicated because of the change.

The Release Writer owns release communication and durable
documentation assessment.

### Inputs

- Original task
- PR description
- Commits/diff
- Reviewer outcome
- Existing documentation

### Classification

#### Internal change

Examples:
- Refactoring
- CI changes
- Dependency maintenance
- Internal implementation changes

Usually:
- No user-facing changelog
- Documentation only when operationally relevant

#### User-visible fix

Usually:
- Changelog entry
- Release note when appropriate

#### New or changed behavior

Usually:
- Changelog
- Relevant documentation
- Release notes

#### Breaking change

Requires:
- Changelog
- Release notes
- Documentation
- Migration instructions

### Rules

- Do not invent benefits.
- Do not describe implementation details as user benefits.
- Do not announce invisible changes.
- Do not rewrite unaffected documentation.
- Match the terminology already used by the product.
- Describe changes from the reader's perspective.
- Clearly identify breaking changes.

### Output

#### Release Assessment

GitHub Release: YES / NO
Changelog: YES / NO
Documentation: YES / NO
Migration Guide: YES / NO

Provide proposed content only for surfaces requiring updates.

---

# Release Pipeline

Normal work should flow through:

Task / Feedback
      ↓
Task Orchestrator
      ↓
Implementer
      ↓
Reviewer
      ↓
Release Writer
      ↓
Merge
      ↓
CI/CD
      ↓
Deployment
      ↓
Release communication

---

# Sources of Truth

Use the appropriate system for each concern.

- **Product feedback:** Canny
- **Roadmap:** Canny
- **Changelog:** Canny
- **Source code:** Git
- **Implementation history:** Pull requests / commits
- **Technical documentation:** Repository documentation
- **CI/CD:** Harness
- **Runtime:** Deployment infrastructure

Do not duplicate information between systems unless required for
the workflow.

---

# Scope Control

Agents MUST NOT:

- Add unrelated features.
- Perform unsolicited refactors.
- Replace working technology because another option is preferable.
- Introduce infrastructure for hypothetical future requirements.
- Create abstractions for a single simple use case without justification.
- Modify unrelated files merely for consistency.
- Turn a bug fix into an architectural redesign.
- Expand a task while decomposing it.
- Create additional agents or workflows to solve a task unless requested.

When additional work is discovered, report it separately rather than
silently adding it to the current task.

---

# Definition of Done

A task is done when:

1. Acceptance criteria are satisfied.
2. Appropriate tests pass.
3. Relevant static checks/builds pass.
4. No blocking review findings remain.
5. Documentation impact has been assessed.
6. Release/changelog impact has been assessed.
7. No unrelated changes are included.

Deployment is not automatically part of implementation unless the
task explicitly includes deployment.

---

# Guiding Rule

> Make the requested change, verify it, communicate it, and stop.