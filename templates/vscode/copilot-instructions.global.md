```instructions
# GitHub Copilot Global Instructions - OSP Group

## Core Principles

Always prioritize **usability, clarity, and aesthetics** in the output. Code should not only function but also feel smooth and visually consistent.

Favor **clean, minimal, and modern design patterns** that enhance user experience. Avoid clutter and overly complex solutions.

## Audience

Assume the instruction-giver is a **UX/Product Designer with limited coding experience**. Explanations and outputs must be **explicit, descriptive, and self-contained**. Do not assume prior coding knowledge.

## Output Quality

Automatically **generate complete and working solutions**, avoiding half-finished code or requiring extra setup unless absolutely necessary.

Follow **best practices** in structure, naming conventions, accessibility, and performance.

## UI Development Standards

When building UIs, always:

- Use **consistent spacing, typography, and color hierarchy**.
- Follow **accessibility guidelines** (contrast, alt text, keyboard navigation, ARIA roles if web).
- Default to **mobile-first responsive layouts**.
- Write code that is **modular and scalable**, easy to extend or adapt later.
- Include **comments and inline guidance** in plain, easy-to-understand language so a designer can read and understand what the code does.

## Decision Making

- Where choices are possible, **pick the option that improves user experience and aesthetics** rather than the fastest hack.
- Always provide **sensible defaults** and avoid requiring unnecessary configuration.
- If context is unclear, **make a smart assumption and state it**, rather than leaving code incomplete.

## Code Style

Be concise: remove redundant code or explanations, but never sacrifice clarity.

---

## Documentation Organization (MANDATORY)

All documentation files must be organized within the `docs/` folder structure. **Never create markdown files in the root directory** (except README.md).

When creating or moving documentation:

### Directory Structure

- **User Guides & Tutorials** → `docs/guides/`
  - Feature guides, user instructions, how-to documents
  
- **Setup & Configuration** → `docs/setup/`
  - Installation guides, environment setup, deployment checklists, configuration references
  
- **Development & Technical** → `docs/development/`
  - Architecture decisions, API documentation, technical specifications, active development notes
  
- **Completed/Historical Work** → `docs/archive/`
  - Implementation completion reports, old schemas, deprecated features, historical decisions
  
- **Obsolete Content** → Delete immediately
  - Don't archive debug reports, troubleshooting logs, or temporary documentation

### Rules

1. **Always place new documentation in the appropriate `docs/` subfolder** based on its purpose and audience
2. **Check `docs/README.md`** for the current organization structure and guidelines
3. **Move completed work to `docs/archive/`** when features are stable and documentation is historical
4. **Delete obsolete files** rather than archiving them if they have no historical value
5. **Keep root directory clean** - only README.md should exist at the root level

---

## GitHub Projects Workflow (MANDATORY)

**[Your Organization] uses GitHub Projects as the single source of truth for all work.**

### Project Board Information

- **Organization:** your-org-name
- **Project:** "Your Project Board Name"
- **URL:** https://github.com/orgs/your-org-name/projects/[NUMBER]
- **Scope:** All repositories

### Workflow Rules (ALWAYS FOLLOW)

#### 1. Before Starting Work

- Check the project board FIRST
- Verify the issue exists and is assigned to you
- Update issue status to "In Progress"
- Review acceptance criteria and dependencies

#### 2. Creating New Tasks

- ALWAYS create a GitHub Issue first (never just start coding)
- Add issue to project board immediately using:
  ```bash
  gh project item-add [PROJECT_NUMBER] --owner [ORG] --url [ISSUE_URL]
  ```
- Use proper labels: priority (P0/P1/P2/P3), type (bug/enhancement/documentation)
- Link related issues with "Depends on #X" or "Blocks #X"
- Add estimated effort (story points)

#### 3. During Development

- Reference issue numbers in commit messages: "Fixes #1" or "Relates to #2"
- Update issue with progress notes and blockers
- Check task boxes in the issue as you complete them
- Keep commits small and focused

#### 4. When Completing Work

- Mark all task checkboxes as complete
- Add final summary comment to issue
- Ensure all acceptance criteria met
- Close issue (will auto-move to "Done" on board)
- Update related issues if dependencies are unblocked

#### 5. Issue Structure (REQUIRED)

Every issue must include:

```markdown
**Priority:** P0/P1/P2/P3
**Labels:** [appropriate labels]
**Estimated Effort:** [story points: 1, 2, 3, 5, 8, 13, 21]
**Depends on:** #[issue number] (if applicable)

## Description
[Clear description of the task]

## Tasks
- [ ] Specific actionable task 1
- [ ] Specific actionable task 2
- [ ] Specific actionable task 3

## Acceptance Criteria
- ✅ Clear definition of done 1
- ✅ Clear definition of done 2
- ✅ Clear definition of done 3
```

#### 6. Project Board Views

- **Board View** - Use for daily workflow (Backlog → Todo → In Progress → Done)
- **Table View** - Use for filtering and bulk updates
- **Roadmap View** - Use for long-term planning and dependencies

### Never

- ❌ Start coding without an issue
- ❌ Work on tasks not on the project board
- ❌ Close issues without updating the board
- ❌ Create tasks in external tools (Notion, Trello, etc.)
- ❌ Commit without referencing issue number
- ❌ Skip acceptance criteria or leave them vague
- ❌ Work on multiple issues simultaneously (focus on one at a time)

### Commands Reference

```bash
# List all projects
gh project list --owner [ORG]

# View project
gh project view [NUMBER] --owner [ORG]

# Add issue to project
gh project item-add [NUMBER] --owner [ORG] --url [ISSUE_URL]

# Create issue and add to project
gh issue create --title "Task" --label "P1,bug" --assignee @me
gh project item-add [NUMBER] --owner [ORG] --url [ISSUE_URL]
```

### Central Documentation

- All project management docs in repository: `/docs/projects/`
- Issue templates: `/docs/projects/ISSUES_PRIORITY_LIST.md`
- Setup guide: `/docs/projects/GITHUB_PROJECT_SETUP.md`
- Workflow guide: `/docs/projects/GITHUB_PROJECTS_WORKFLOW.md`

---

## Quality Standards

### Code Quality

- Write tests for all new features (unit + integration)
- Ensure code coverage >80%
- No linting errors
- No console warnings in production
- Proper error handling and user feedback

### Performance

- Images optimized and properly sized
- Lazy loading for non-critical resources
- Database queries optimized (no N+1 queries)
- Bundle size monitored (<200KB for critical path)

### Security

- Input validation and sanitization
- XSS and CSRF protection
- Secure authentication and authorization
- Sensitive data encrypted
- Dependencies regularly updated

### Accessibility

- WCAG 2.1 AA compliance minimum
- Semantic HTML
- Keyboard navigation support
- Screen reader compatibility
- Sufficient color contrast (4.5:1 for text)

---

## Development Workflow

### Git Workflow

1. Create feature branch from `main`: `feature/issue-123-short-description`
2. Make focused commits with clear messages
3. Reference issue in commits: `fix: resolve login bug (Fixes #123)`
4. Push to origin and create Pull Request
5. Link PR to issue
6. Request review from team
7. Address feedback
8. Merge when approved and CI passes

### Commit Message Format

```
<type>: <description> (Fixes #issue)

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting changes
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

### Pull Request Checklist

- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] No linting errors
- [ ] Accessibility checked
- [ ] Performance impact considered
- [ ] Security implications reviewed
- [ ] Issue linked and referenced
- [ ] Self-review completed

---

## Anti-Patterns to Avoid

### Code Anti-Patterns

- ❌ Deeply nested conditionals (>3 levels)
- ❌ Large functions (>50 lines)
- ❌ Duplicate code (DRY principle)
- ❌ Magic numbers (use named constants)
- ❌ Overly clever code (prioritize clarity)
- ❌ Premature optimization
- ❌ Global state when not needed

### UI Anti-Patterns

- ❌ Inconsistent spacing/typography
- ❌ Low contrast text
- ❌ Non-responsive layouts
- ❌ Missing loading states
- ❌ Poor error messages
- ❌ No keyboard navigation
- ❌ Missing alt text for images

### Workflow Anti-Patterns

- ❌ Working without an issue
- ❌ Committing directly to main
- ❌ Large PRs (>500 lines)
- ❌ Unclear commit messages
- ❌ Skipping code review
- ❌ Not updating documentation
- ❌ Ignoring CI failures

---

**Version:** 1.0.0
**Last Updated:** October 18, 2025
**Organization:** [Your Organization Name]

```
