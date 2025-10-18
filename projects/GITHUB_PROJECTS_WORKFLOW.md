# GitHub Projects Workflow - OSP Group

**Last Updated:** October 18, 2025  
**Status:** ✅ Active and Configured

---

## 🎯 Overview

**OSP Group uses GitHub Projects as the single source of truth for all work across all repositories.**

- **Project Name:** OSP Group - Master Project Board
- **URL:** https://github.com/orgs/osp-group/projects/1
- **Scope:** All repositories (crm, contabilidade, digital, docs)
- **Team Members:** All OSP Group contributors

---

## 📋 Quick Access

| Resource | Link |
|----------|------|
| **Project Board** | https://github.com/orgs/osp-group/projects/1 |
| **CRM Issues** | https://github.com/osp-group/crm/issues |
| **Contabilidade Issues** | https://github.com/osp-group/contabilidade/issues |
| **Digital Issues** | https://github.com/osp-group/digital/issues |
| **Documentation Hub** | https://github.com/osp-group/docs |

---

## 🔄 Daily Workflow

### Morning Routine (5 min)

1. **Open Project Board:** https://github.com/orgs/osp-group/projects/1
2. **Check "In Progress" column** - Resume work on active tasks
3. **Review "Todo" column** - Pick next priority task
4. **Update status** - Move issues as needed

### Starting New Work

```bash
# 1. Check project board first
open https://github.com/orgs/osp-group/projects/1

# 2. Find issue, verify it's assigned to you
# 3. Move to "In Progress" column
# 4. Start working
```

### During Development

1. **Reference issues in commits:**
   ```bash
   git commit -m "Add CRM data model fields - Relates to #2"
   git commit -m "Fix database migration script - Fixes #1"
   ```

2. **Update issue progress:**
   - Check off completed tasks in issue
   - Add comments with findings or blockers
   - Tag team members if help needed

3. **Link related work:**
   - Use "Depends on #X" in issue descriptions
   - Use "Blocks #X" for dependencies
   - Cross-reference between repositories: "osp-group/crm#1"

### Completing Work

1. **Final checklist:**
   - [ ] All tasks checked off
   - [ ] Tests passing
   - [ ] Documentation updated
   - [ ] Changes deployed/merged

2. **Close issue:**
   - Add final comment with summary
   - Close issue (will auto-move to "Done")
   - Notify dependent issues

3. **Update project board:**
   - Verify issue moved to "Done"
   - Unblock any dependent tasks
   - Pick next task from "Todo"

---

## 📝 Creating New Issues (MANDATORY PROCESS)

### Rule #1: ALWAYS Create an Issue First

**Never start coding without an issue.** Every piece of work must be tracked.

### Issue Creation Steps

1. **Navigate to appropriate repository:**
   - CRM work → https://github.com/osp-group/crm/issues/new
   - Website work → https://github.com/osp-group/contabilidade/issues/new
   - Digital site → https://github.com/osp-group/digital/issues/new

2. **Use standard format:**

```markdown
**Priority:** P0 (Critical) / P1 (High) / P2 (Medium) / P3 (Low)
**Labels:** [Select appropriate labels]
**Estimated Effort:** [1-8 story points]
**Depends on:** #[issue-number] (if blocked by another issue)

## Description
[Clear, concise description of what needs to be done and why]

## Current State
- What's working
- What's not working
- What's missing

## Tasks
- [ ] Specific, actionable task 1
- [ ] Specific, actionable task 2
- [ ] Specific, actionable task 3
- [ ] Test the implementation
- [ ] Update documentation

## Acceptance Criteria
- ✅ Clear definition of "done"
- ✅ What success looks like
- ✅ How to verify it works

## Resources
- Link to relevant docs
- API documentation
- Related issues
```

3. **Add to project board immediately:**

```bash
# Get the issue URL after creation, then:
gh project item-add 1 --owner osp-group --url [issue-url]

# Example:
gh project item-add 1 --owner osp-group --url https://github.com/osp-group/crm/issues/6
```

4. **Set appropriate labels:**
   - **Priority:** `P0-critical`, `P1-high`, `P2-medium`, `P3-low`
   - **Type:** `bug`, `enhancement`, `documentation`, `testing`
   - **Area:** `crm`, `firebase`, `deployment`, `seo`, etc.
   - **Status:** `blocked`, `needs-review`, `in-progress`

---

## 🏷️ Issue Labels System

### Priority Labels (REQUIRED)

| Label | Meaning | SLA |
|-------|---------|-----|
| `P0-critical` | Blocking, system down, data loss | Start immediately |
| `P1-high` | Important, affects users, blocks other work | Within 1 day |
| `P2-medium` | Normal priority, planned work | Within 1 week |
| `P3-low` | Nice to have, improvements | When capacity available |

### Type Labels

| Label | Use For |
|-------|---------|
| `bug` | Something broken that needs fixing |
| `enhancement` | New feature or improvement |
| `documentation` | Documentation updates |
| `testing` | Test creation or test fixes |
| `refactor` | Code cleanup, no functionality change |
| `performance` | Performance optimization |
| `security` | Security-related work |

### Repository Labels

| Label | Repository |
|-------|-----------|
| `crm` | Twenty CRM related |
| `contabilidade` | Accounting website |
| `digital` | Digital services website |
| `docs` | Documentation repository |
| `all-repos` | Affects multiple repositories |

---

## 📊 Project Board Views

### Board View (Default - Daily Use)

**Columns:**
1. **Backlog** - New issues, not yet prioritized
2. **Todo** - Prioritized, ready to start
3. **In Progress** - Currently being worked on
4. **Done** - Completed work

**How to use:**
- Drag issues between columns as status changes
- Filter by repository, assignee, or label
- Group by priority to see critical items first

### Table View (Bulk Updates)

**Use for:**
- Filtering issues (e.g., "show me all P0 issues")
- Bulk updating fields
- Sorting by effort, priority, or date
- Exporting data for reporting

**Access:** Click "Table" tab in project

### Roadmap View (Planning)

**Use for:**
- Sprint/iteration planning
- Visualizing timelines
- Dependencies visualization
- Long-term planning

**Access:** Click "Roadmap" tab in project

---

## 🤖 Automation

### Built-in Workflows (Active)

1. **Auto-add new issues** - Issues are automatically added to project
2. **Auto-set status** - New items start in "Backlog"
3. **Auto-move on close** - Closed issues move to "Done"
4. **Auto-archive** - Done items archived after 30 days

### Manual Actions

**Moving issues:**
```bash
# Move to In Progress
# Drag in UI or use CLI

# Move to Done
# Close the issue - auto-moves
```

**Assigning work:**
- Assign yourself in issue sidebar
- Issues filter by assignee on board

---

## 🔗 Cross-Repository Work

### Linking Issues Across Repos

Use full references when linking between repositories:

```markdown
**Depends on:** osp-group/crm#2
**Blocks:** osp-group/contabilidade#1
**Related to:** osp-group/docs#5
```

### Example: CRM Integration Issue

```markdown
# In contabilidade repo:
## Issue #1: Update Firebase Functions for CRM Integration

**Depends on:**
- osp-group/crm#1 (Database migration must complete first)
- osp-group/crm#2 (CRM data model must be configured)

**Blocks:**
- osp-group/contabilidade#2 (Integration testing)
```

---

## 📈 Metrics & Reporting

### Weekly Review (Every Friday)

1. **Check project insights:**
   - Go to project → Insights tab
   - Review burndown chart
   - Check velocity trends

2. **Update status:**
   - Count issues by status
   - Calculate completion rate
   - Identify blockers

3. **Plan next week:**
   - Move issues from Backlog → Todo
   - Ensure P0/P1 issues are prioritized
   - Balance workload across team

### Monthly Review

1. **Repository health:**
   - Open issues count
   - Average time to close
   - Issue backlog growth

2. **Team velocity:**
   - Story points completed
   - Issues closed per person
   - Blocker frequency

3. **Process improvements:**
   - What worked well
   - What slowed us down
   - Process changes needed

---

## 🚫 What NOT to Do

### Never:

1. ❌ Start coding without an issue
2. ❌ Work on tasks not on project board
3. ❌ Create tasks in external tools (Notion, Trello, Jira)
4. ❌ Close issues without proper summary
5. ❌ Leave issues in "In Progress" for >3 days without updates
6. ❌ Skip updating task checkboxes
7. ❌ Forget to link commits to issues
8. ❌ Create issues without priority labels

### Always:

1. ✅ Check project board before starting work
2. ✅ Create issue FIRST, then code
3. ✅ Update issue as you progress
4. ✅ Reference issues in commits
5. ✅ Close issues when complete
6. ✅ Document blockers immediately
7. ✅ Help teammates by reviewing their issues
8. ✅ Keep project board up to date

---

## 🛠️ CLI Commands Reference

### View Project

```bash
# List all projects in organization
gh project list --owner osp-group

# View project details
gh project view 1 --owner osp-group
```

### Add Issues to Project

```bash
# Add single issue
gh project item-add 1 --owner osp-group --url [issue-url]

# Example
gh project item-add 1 --owner osp-group --url https://github.com/osp-group/crm/issues/1
```

### Create Issue and Add to Project

```bash
# Create issue
gh issue create --repo osp-group/crm --title "Fix bug X" --body "Description"

# Get the issue URL from output, then add to project
gh project item-add 1 --owner osp-group --url [issue-url]
```

### List Issues in Project

```bash
# View all items in project
gh project item-list 1 --owner osp-group --limit 50
```

---

## 📚 Training Resources

### For New Team Members

1. **Read this document** (you're doing it! ✅)
2. **Watch GitHub Projects tutorial:** https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/quickstart-for-projects
3. **Review existing issues** to see format
4. **Shadow a teammate** for one day
5. **Create your first issue** with help

### Official Documentation

- **GitHub Projects:** https://docs.github.com/en/issues/planning-and-tracking-with-projects
- **Best Practices:** https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects
- **GitHub CLI:** https://cli.github.com/manual/gh_project

---

## 🎯 Success Metrics

You're doing it right when:

- ✅ All work is tracked in GitHub Issues
- ✅ Project board is always up to date
- ✅ Team can see what everyone is working on
- ✅ No "surprise" work that wasn't planned
- ✅ Blockers are visible and addressed quickly
- ✅ Velocity is predictable
- ✅ Documentation stays in sync with work

---

## 📞 Getting Help

### Issue Template Problems?
Check: [ISSUES_PRIORITY_LIST.md](./ISSUES_PRIORITY_LIST.md) for examples

### Project Board Issues?
Check: [GITHUB_PROJECT_SETUP.md](./GITHUB_PROJECT_SETUP.md)

### Process Questions?
Ask in: GitHub Discussions or team chat

### Technical Issues?
Create issue in: osp-group/docs repository

---

## 📝 Changelog

### October 18, 2025
- ✅ Created unified OSP Group project board
- ✅ Renamed from "Digital" to "OSP Group - Master Project Board"
- ✅ Added all 14 existing issues to board
- ✅ Documented complete workflow
- ✅ Updated Copilot instructions with workflow requirements
- ✅ Set up cross-repository tracking

---

**Remember: GitHub Projects is your single source of truth. If it's not on the board, it doesn't exist!**

---

**Maintained by:** OSP Group Team  
**Questions?** Create an issue in osp-group/docs
