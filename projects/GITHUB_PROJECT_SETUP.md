# 🎯 GitHub Project Setup Guide for OSP Group

## Overview

This guide will help you set up and use GitHub Projects to track all OSP Group tasks and documentation.

## ✅ What We've Created

1. **Central Documentation Repository**: https://github.com/osp-group/docs
2. **Organized Documentation Structure**:
   ```
   osp-group/docs/
   ├── architecture/          # System architecture docs
   ├── deployment/           # Deployment guides
   ├── integration/          # Integration guides
   ├── planning/             # Strategic planning
   ├── projects/             # Project tracking
   └── repositories/         # Repo-specific docs
       ├── contabilidade/
       ├── crm/
       └── digital/
   ```

## 📊 Setting Up GitHub Project Board

### Step 1: Create Organization Project

1. Go to https://github.com/orgs/osp-group/projects
2. Click **"New project"**
3. Choose **"Board"** template
4. Name it: **"OSP Group - Master Board"**
5. Click **"Create project"**

### Step 2: Configure Project Views

**Default Board View:**
- Columns: `📋 Backlog`, `🟡 Todo`, `🔄 In Progress`, `✅ Done`

**Add Custom Fields:**
1. Click Settings (top right)
2. Add these fields:
   - **Priority**: Select (P0-Critical, P1-High, P2-Medium, P3-Low)
   - **Repository**: Select (contabilidade, crm, digital, docs)
   - **Effort**: Number (story points 1-13)
   - **Due Date**: Date
   - **Assignee**: Person

### Step 3: Create Issues from Templates

Use the templates in `projects/GITHUB_ISSUES_TEMPLATE.md`:

#### Critical: CRM Database Migration
1. Go to https://github.com/osp-group/crm/issues/new
2. Copy content from template section "🔴 CRITICAL: CRM Database Migration"
3. Labels: `critical`, `bug`, `crm`, `deployment`
4. Add to project: OSP Group - Master Board
5. Set Priority: P0
6. Assign column: 🔄 In Progress

#### High Priority: Website-CRM Integration
1. Go to https://github.com/osp-group/contabilidade/issues/new
2. Copy template section "🟡 Website-CRM Integration"
3. Labels: `enhancement`, `integration`, `contabilidade`, `crm`
4. Add to project
5. Set Priority: P1
6. Assign column: 📋 Backlog
7. Link blocking issue: "Blocked by #1 in crm repo"

#### More Issues:
- Custom Domain Configuration → osp-group/docs
- SEO Optimization → osp-group/contabilidade
- Digital Website Enhancement → osp-group/digital

### Step 4: Configure Automation

1. In Project settings, enable workflows:
   - **Item added to project**: Auto-set status to "Todo"
   - **Item closed**: Auto-move to "Done"
   - **Item reopened**: Auto-move back to "In Progress"

2. **Status Field Automation**:
   - When status = "In Progress" → Assign current date
   - When status = "Done" → Record completion date

## 🔄 Daily Workflow

### Morning Standup
1. Visit https://github.com/orgs/osp-group/projects/1 (your project number)
2. Review **"In Progress"** column
3. Update issue comments with progress
4. Move completed items to **"Done"**

### Task Updates
```bash
# When starting work on a task
1. Move issue to "In Progress" column
2. Assign yourself
3. Add comment: "Starting work on this"

# When blocked
1. Add label: `blocked`
2. Comment: what's blocking you
3. Link to blocking issue

# When complete
1. Close the issue
2. Reference in commit: "Fixes #123"
3. Issue auto-moves to Done
```

### Weekly Review
Every Friday:
1. Review **"Done"** column - celebrate wins! 🎉
2. Update **"Backlog"** - add new discovered tasks
3. Review **"Blocked"** items - escalate if needed
4. Update project documentation in `osp-group/docs`

## 📝 Issue Best Practices

### Writing Good Issues

**Title Format:**
- `[REPO] Brief description`
- Example: `[CRM] Database migrations not executing on Railway`

**Description Must Include:**
1. **Context**: What's the current situation?
2. **Problem**: What's not working?
3. **Expected**: What should happen?
4. **Steps**: How to reproduce/implement?
5. **Acceptance Criteria**: How do we know it's done?

### Labels to Use

| Label | Meaning | Use When |
|-------|---------|----------|
| `critical` | P0 - Blocking production | System down, security issue |
| `bug` | Something broken | Errors, unexpected behavior |
| `enhancement` | New feature/improvement | Adding functionality |
| `documentation` | Docs update needed | Missing or outdated docs |
| `deployment` | Deployment related | Infrastructure, CI/CD |
| `integration` | Cross-system integration | Connecting services |
| `blocked` | Cannot proceed | Waiting on dependency |
| `good first issue` | Easy for newcomers | Simple, well-defined tasks |

## 🔗 Cross-Repository References

**Link Issues Across Repos:**
```markdown
Blocked by osp-group/crm#1
Related to osp-group/contabilidade#5
Fixes osp-group/docs#3
```

**In Commits:**
```bash
git commit -m "Add CRM integration

Implements integration between website and CRM.

Fixes osp-group/contabilidade#2
Related to osp-group/crm#1"
```

## 📊 Project Metrics & Reporting

### Weekly Metrics
Track in `projects/ACTIVE_PROJECTS.md`:
- Issues opened this week
- Issues closed this week
- Average time to close
- Issues by priority
- Issues by repository

### Monthly Review
Update in `projects/ACTIVE_PROJECTS.md`:
- Completed projects
- Ongoing projects status
- Blocked items resolution
- Team velocity (story points per week)

## 🎯 Current Project Status

Visit https://github.com/osp-group/docs/blob/main/projects/ACTIVE_PROJECTS.md for:
- All active projects
- Current priorities
- Project metrics
- Recent updates
- Backlog items

## 🆘 Need Help?

1. **Urgent Issues**: Create issue with `critical` label
2. **Questions**: Create issue with `question` label in `osp-group/docs`
3. **Documentation**: Update `osp-group/docs` directly via PR
4. **Process Improvements**: Open issue in `osp-group/docs` with `process` label

## 📚 Resources

- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [Writing Good Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues)
- [Linking PRs to Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue)
- [Project Automation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project)

---

## 🚀 Next Steps

1. [ ] Create GitHub Project in osp-group organization
2. [ ] Create issues from templates in each repository
3. [ ] Add all issues to project board
4. [ ] Configure project automation
5. [ ] Share project board link with team
6. [ ] Start daily/weekly workflow

**Project Board URL** (after creation): https://github.com/orgs/osp-group/projects/[YOUR_PROJECT_NUMBER]

---

**Last Updated:** October 18, 2025  
**Maintained by:** OSP Group Team
