# Quick Start Guide - GitHub Projects Workflow

**Get up and running with OSP Group's workflow in 15 minutes.**

---

## 🎯 Overview

This workflow ensures all work is tracked, visible, and coordinated through GitHub Projects. No external tools needed.

**Core Principle:** GitHub Projects is the single source of truth for all work.

---

## ⚡ 5-Minute Setup

### Step 1: Access the Project Board (1 min)

Visit: https://github.com/orgs/[your-org]/projects/[NUMBER]

**Bookmark this page** - you'll visit it daily.

### Step 2: Understand the Board (2 min)

The board has 4 columns:

| Column | Meaning |
|--------|---------|
| **Backlog** | Ideas and future work, not prioritized yet |
| **Todo** | Ready to work on, prioritized |
| **In Progress** | Actively being worked on |
| **Done** | Completed work |

**Your daily focus:** Move issues from **Todo** → **In Progress** → **Done**

### Step 3: Find Your First Task (2 min)

1. Look at the **Todo** column
2. Find an issue assigned to you
3. Check the priority label: P0 (critical) → P1 (high) → P2 (medium) → P3 (low)
4. **Start with highest priority first**

---

## 📋 Daily Workflow

### Morning Routine (5 minutes)

```bash
# 1. Check the project board
open https://github.com/orgs/[your-org]/projects/[NUMBER]

# 2. Pull latest changes
cd ~/your-project
git checkout main
git pull origin main

# 3. Pick your task (highest priority in Todo column)
# 4. Move issue to "In Progress"
# 5. Create feature branch
git checkout -b feature/issue-123-short-description
```

### Working on a Task (Ongoing)

```bash
# 1. Make changes
# 2. Commit with issue reference
git commit -m "feat: add login form (Relates to #123)"

# 3. Update issue with progress
# Add comments: "✅ Completed UI design" or "🚧 Working on API integration"

# 4. Check off task boxes in issue as you complete them
```

### Completing a Task (10 minutes)

```bash
# 1. Push your changes
git push origin feature/issue-123-short-description

# 2. Create Pull Request
gh pr create --title "Add login form" --body "Fixes #123"

# 3. Request review
gh pr review --approve

# 4. After merge: Close issue
gh issue close 123 --comment "✅ Completed and deployed"

# Issue automatically moves to "Done" column
```

---

## 🆕 Creating a New Issue

### When to Create an Issue

**Always create an issue when:**
- Starting any new work
- Finding a bug
- Proposing a feature
- Planning documentation
- Deploying changes

**Even if it's small** - create an issue first!

### Quick Issue Creation

```bash
# Create a quick issue
gh issue create \
  --title "Fix login button alignment" \
  --label "bug,P2" \
  --assignee @me \
  --body "Login button is misaligned on mobile devices"

# Add to project board
gh project item-add [PROJECT_NUMBER] --owner [ORG] --url [ISSUE_URL]
```

### Issue Template (Copy & Paste)

```markdown
**Priority:** P2
**Labels:** bug
**Estimated Effort:** 2

## Description
[What needs to be done?]

## Tasks
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Acceptance Criteria
- ✅ Criteria 1
- ✅ Criteria 2
- ✅ Criteria 3
```

---

## 🏷️ Understanding Labels

### Priority (Required)

- **P0** - 🔴 Critical: Production down, data loss, blocking issues
- **P1** - 🟠 High: Important features, major bugs, security
- **P2** - 🟡 Medium: Standard work, minor bugs
- **P3** - 🟢 Low: Nice-to-have, cleanup, enhancements

**When in doubt, use P2.**

### Type (Required)

- `bug` - Something is broken
- `enhancement` - New feature or improvement
- `documentation` - Docs work
- `deployment` - Infrastructure/deployment
- `refactoring` - Code cleanup
- `testing` - Test creation

**Pick the one that best describes your work.**

### Status (Optional)

- `blocked` - Can't proceed, waiting on something
- `needs-review` - Ready for code review
- `needs-testing` - Ready for QA

**Use these to communicate blockers.**

---

## 💡 Pro Tips

### Tip 1: Check the Board Daily

Start each day by visiting the project board. It shows:
- What's high priority
- What you're working on
- What's blocked
- What's completed

**Bookmark it and check it every morning.**

### Tip 2: Keep Issues Small

Break large tasks into smaller issues:

❌ Bad: "Build entire authentication system" (too big)
✅ Good: 
- "Add login form UI"
- "Implement JWT authentication"
- "Add password reset flow"
- "Write auth tests"

**Small issues = faster progress = better tracking.**

### Tip 3: Update Issues Frequently

Add comments as you work:
- "✅ Completed database schema"
- "🚧 Working on API endpoints"
- "❌ Blocked: Need API key from DevOps"

**Communication prevents duplicate work and helps teammates.**

### Tip 4: Link Related Issues

If issues depend on each other:

```markdown
**Depends on:** #45
**Blocks:** #67
**Related to:** #23
```

**This shows the team what's blocking what.**

### Tip 5: Close Issues Promptly

When work is done:
1. Check all task boxes ✅
2. Verify acceptance criteria met
3. Add final summary comment
4. Close the issue

**Closed issues = clear progress tracking.**

---

## 🚫 Common Mistakes

### Mistake 1: Starting Work Without an Issue

❌ **Wrong:**
```bash
git checkout -b feature/new-button
# Start coding...
```

✅ **Right:**
```bash
gh issue create --title "Add new button"
gh project item-add ...
git checkout -b feature/issue-45-new-button
# Start coding...
```

### Mistake 2: Not Updating Issue Status

❌ **Wrong:**
- Issue stays in "Todo" even though you're working on it
- Team doesn't know what you're doing

✅ **Right:**
- Move to "In Progress" when you start
- Add progress comments
- Move to "Done" when complete

### Mistake 3: Vague Issue Titles

❌ **Wrong:**
- "Fix bug"
- "Update things"
- "Make it better"

✅ **Right:**
- "Fix login button alignment on mobile"
- "Update user profile API to include avatar"
- "Improve dashboard load time by 50%"

### Mistake 4: Working on Too Many Issues

❌ **Wrong:**
- 5 issues in "In Progress" assigned to you
- Context switching constantly
- Nothing gets finished

✅ **Right:**
- 1-2 issues max in "In Progress"
- Finish before starting new work
- Clear "Done" column regularly

---

## ❓ Quick FAQ

**Q: Do I really need an issue for everything?**
A: Yes! Even 5-minute fixes. It takes 30 seconds to create an issue.

**Q: What if something is urgent?**
A: Use P0 priority and add "urgent" label. Notify team in Slack/Teams.

**Q: Can I work on something not on the board?**
A: No. Create an issue first, add to board, then start.

**Q: What if I'm blocked?**
A: Add `blocked` label, comment why, notify the person/team who can unblock.

**Q: How do I prioritize my work?**
A: P0 first, then P1, then P2, then P3. Check board's "Todo" column.

**Q: Should I close issues for others?**
A: Only if you completed their work with permission. Otherwise, comment and let them close.

---

## 📚 Next Steps

### Learn More

1. **Full Workflow Guide** - Complete daily routines and best practices
   → See: `WORKFLOW_GUIDE.md`

2. **Issue Templates** - Templates for bugs, features, docs, etc.
   → See: `issue-templates/` directory

3. **GitHub CLI Guide** - Command reference and automation
   → See: `WORKFLOW_GUIDE.md` (Commands section)

### Practice

1. Create a test issue in the project
2. Move it through all columns (Todo → In Progress → Done)
3. Practice the commit → PR → close workflow
4. Ask questions in team chat

---

## 📞 Need Help?

**Workflow Questions:** Check `FAQ.md` or ask in team chat

**Technical Issues:** Create issue with `help-wanted` label

**Urgent Problems:** Slack/Teams with @channel mention

---

**Remember:** 
- 📋 Check board daily
- 🎯 Always create issues first
- 💬 Update progress frequently
- ✅ Close issues when done

**You've got this! 🚀**

---

**Last Updated:** October 18, 2025
**Version:** 1.0.0
