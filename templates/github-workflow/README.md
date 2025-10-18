# GitHub Workflow Templates

Complete GitHub Projects workflow system with issue templates, labels, and automation rules.

---

## 📋 Contents

1. **[WORKFLOW_GUIDE.md](./WORKFLOW_GUIDE.md)** - Complete daily workflow guide
2. **[PROJECT_SETUP_GUIDE.md](./PROJECT_SETUP_GUIDE.md)** - Setting up GitHub Projects
3. **[QUICK_START.md](./QUICK_START.md)** - 5-minute new user guide
4. **[FAQ.md](./FAQ.md)** - Common questions and answers
5. **Issue Templates** - 8 ready-to-use issue templates
6. **Label Configurations** - Priority, type, and status labels
7. **Automation Rules** - GitHub Actions for workflow automation

---

## 🎯 Quick Setup (5 minutes)

### 1. Copy Issue Templates

```bash
# Copy all templates to your repository
cp -r ~/osp/osp-docs/templates/github-workflow/issue-templates \
      ./.github/ISSUE_TEMPLATE/
```

### 2. Set Up Labels

```bash
# Run automated label setup
bash ~/osp/osp-docs/templates/github-workflow/setup-labels.sh
```

### 3. Add to Project Board

```bash
# Add repository to OSP master project
gh project item-add 1 --owner osp-group \
   --url https://github.com/osp-group/[your-repo]
```

### 4. Create First Issue

```bash
# Use GitHub web interface or:
gh issue create --title "Initial Setup" \
                --label "P1,setup" \
                --assignee @me \
                --body-file .github/ISSUE_TEMPLATE/deployment-task.md
```

✅ **Done!** Your repository now uses OSP Group's workflow.

---

## 📄 Available Issue Templates

### 1. **Bug Report** (`bug-report.md`)
For reporting bugs, errors, or unexpected behavior.

**When to use:**
- Application crashes or errors
- UI/UX issues
- Data inconsistencies
- Performance problems

**Includes:**
- Environment details
- Steps to reproduce
- Expected vs actual behavior
- Screenshots/logs section

### 2. **Feature Request** (`feature-request.md`)
For proposing new features or enhancements.

**When to use:**
- New functionality needed
- Enhancement to existing features
- UI/UX improvements
- Integration requests

**Includes:**
- User story format
- Success criteria
- Dependencies
- Design considerations

### 3. **Documentation** (`documentation.md`)
For documentation tasks - creation, updates, or improvements.

**When to use:**
- Missing documentation
- Outdated guides
- API documentation
- User manuals

**Includes:**
- Documentation type
- Target audience
- Content outline
- Success criteria

### 4. **Deployment Task** (`deployment-task.md`)
For deployment, infrastructure, or DevOps tasks.

**When to use:**
- Production deployments
- Environment setup
- Configuration changes
- Infrastructure updates

**Includes:**
- Deployment checklist
- Rollback plan
- Verification steps
- Monitoring setup

### 5. **Integration Task** (`integration-task.md`)
For integrating external services, APIs, or systems.

**When to use:**
- Third-party API integration
- Service connections
- Webhook setup
- OAuth implementation

**Includes:**
- Integration overview
- Authentication requirements
- Data flow diagram
- Testing plan

### 6. **Refactoring Task** (`refactoring-task.md`)
For code refactoring, optimization, or technical debt.

**When to use:**
- Code cleanup
- Performance optimization
- Dependency updates
- Architecture improvements

**Includes:**
- Current state analysis
- Proposed changes
- Risk assessment
- Testing strategy

### 7. **Testing Task** (`testing-task.md`)
For creating or improving tests (unit, integration, E2E).

**When to use:**
- Test coverage gaps
- New test suites
- Test automation
- QA procedures

**Includes:**
- Test type and scope
- Coverage goals
- Test scenarios
- Success criteria

### 8. **Research Spike** (`research-spike.md`)
For time-boxed research or investigation tasks.

**When to use:**
- Technology evaluation
- Proof of concept
- Problem investigation
- Decision making

**Includes:**
- Research questions
- Time box limit
- Deliverables
- Decision criteria

---

## 🏷️ Label System

### Priority Labels

| Label | Color | Usage |
|-------|-------|-------|
| **P0 - Critical** | `#d73a4a` (red) | Blocking issues, production down, data loss |
| **P1 - High** | `#ff6b6b` (orange-red) | Important features, major bugs, security |
| **P2 - Medium** | `#fbca04` (yellow) | Standard features, minor bugs |
| **P3 - Low** | `#0e8a16` (green) | Nice-to-have, enhancements, cleanup |

### Type Labels

| Label | Color | Usage |
|-------|-------|-------|
| `bug` | `#d73a4a` | Something isn't working |
| `enhancement` | `#a2eeef` | New feature or request |
| `documentation` | `#0075ca` | Improvements or additions to docs |
| `deployment` | `#5319e7` | Deployment and infrastructure |
| `integration` | `#1d76db` | External service integration |
| `refactoring` | `#fbca04` | Code improvement without new features |
| `testing` | `#d4c5f9` | Test creation or improvement |
| `research` | `#e99695` | Investigation or POC |

### Status Labels

| Label | Color | Usage |
|-------|-------|-------|
| `blocked` | `#d73a4a` | Cannot proceed due to dependency |
| `in-progress` | `#0e8a16` | Actively being worked on |
| `needs-review` | `#fbca04` | Waiting for code review |
| `needs-testing` | `#d4c5f9` | Waiting for QA testing |
| `on-hold` | `#bfdadc` | Paused temporarily |

---

## 🤖 Automation Rules

### Auto-Assign (`.github/workflows/auto-assign.yml`)

Automatically assigns issues to team members based on labels:
- `deployment` → DevOps team
- `documentation` → Tech writers
- `bug` → On-call engineer

### Auto-Label (`.github/workflows/auto-label.yml`)

Automatically adds labels based on:
- File paths changed in PR
- Keywords in issue title/body
- Issue template used

### Project Board Sync (`.github/workflows/project-board-sync.yml`)

Automatically updates project board when:
- Issue opened → Adds to "Backlog"
- PR opened → Links to issue, adds to "In Progress"
- PR merged → Moves issue to "Done"
- Issue closed → Archives after 7 days

---

## 📊 Project Board Setup

### Default Views

1. **Board View** (Kanban)
   - Backlog
   - Todo
   - In Progress
   - Review
   - Done

2. **Table View** (Spreadsheet)
   - All fields visible
   - Filter by priority, assignee, label
   - Bulk edit capabilities

3. **Roadmap View** (Timeline)
   - Grouped by milestone
   - Timeline visualization
   - Dependency tracking

### Custom Fields

- **Priority** (Single select) - P0, P1, P2, P3
- **Effort** (Number) - Story points (1, 2, 3, 5, 8, 13)
- **Status** (Status) - Backlog, Todo, In Progress, Review, Done
- **Sprint** (Iteration) - 2-week sprints
- **Team** (Single select) - Frontend, Backend, DevOps, Design

---

## 📖 Complete Workflow Guide

→ See [WORKFLOW_GUIDE.md](./WORKFLOW_GUIDE.md) for detailed daily workflow instructions.

**Key sections:**
- Morning routine (check board, pull updates, plan day)
- Starting work (create/assign issue, update status)
- During development (commit with references, update progress)
- Completing work (PR checklist, testing, closing issues)
- Weekly review (metrics, retrospective)

---

## 🚀 Advanced Usage

### Cross-Repository Issues

Link issues across repositories:

```markdown
**Depends on:** osp-group/crm#5
**Blocks:** osp-group/contabilidade#12
```

### Issue Templates with GitHub Forms

Create interactive forms (`.github/ISSUE_TEMPLATE/config.yml`):

```yaml
blank_issues_enabled: false
contact_links:
  - name: Questions & Discussions
    url: https://github.com/osp-group/[repo]/discussions
    about: Ask questions and discuss ideas
```

### Saved Replies

Create saved replies in GitHub settings for common responses:
- "Waiting for more information"
- "Duplicate of #X"
- "Won't fix because..."

---

## 📈 Metrics & Reporting

### Weekly Metrics

Track these metrics weekly:
- Issues created vs closed
- Average time to close (by priority)
- Blocked issues count
- PR merge time
- Code review turnaround

### Monthly Review

Review monthly:
- Velocity (story points completed)
- Bug creation rate
- Documentation coverage
- Technical debt trends

### Quarterly Goals

Set quarterly OKRs:
- Reduce P0 issues by X%
- Improve test coverage to X%
- Deploy frequency (weekly → daily)
- Documentation completeness

---

## 🎓 Training Materials

### For New Team Members

1. **Read:** [QUICK_START.md](./QUICK_START.md) - 10 minutes
2. **Watch:** Create sample issue - 5 minutes
3. **Practice:** Complete practice issue - 20 minutes
4. **Review:** Team workflow - 10 minutes

**Total:** 45 minutes onboarding

### For External Contributors

1. **Read:** [QUICK_START.md](./QUICK_START.md) - 10 minutes
2. **Review:** Issue templates - 5 minutes
3. **Practice:** Submit issue - 5 minutes

**Total:** 20 minutes onboarding

---

## ❓ FAQ

→ See complete [FAQ.md](./FAQ.md)

**Quick answers:**

**Q: Do I need an issue for every small change?**
A: Yes, even small changes should have issues. Use "P3" priority for minor tasks.

**Q: Can I work on something not on the board?**
A: No. Create an issue first, add to board, then start work.

**Q: What if I'm blocked?**
A: Add `blocked` label, comment with blocker, notify blocking person.

**Q: How do I prioritize my work?**
A: P0 → P1 → P2 → P3. Check board's "Todo" column each morning.

---

## 📞 Support

**Template Issues:** Create issue in `osp-group/docs` with label `template-issue`

**Workflow Questions:** Check [FAQ.md](./FAQ.md) or ask in discussions

**Bugs in Automation:** Create issue with label `automation-bug`

---

**Last Updated:** October 18, 2025
**Version:** 1.0.0
