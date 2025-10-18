# Complete Project Setup Guide - OSP Group Templates

**Step-by-step guide to set up a new project with OSP Group's standardized workflow.**

**Time Required:** 30-45 minutes
**Prerequisites:** GitHub CLI installed, VS Code installed, Git configured

---

## 📋 Table of Contents

1. [Create Repository](#1-create-repository)
2. [Set Up Documentation Structure](#2-set-up-documentation-structure)
3. [Configure GitHub Labels](#3-configure-github-labels)
4. [Add to Project Board](#4-add-to-project-board)
5. [Install VS Code Configuration](#5-install-vs-code-configuration)
6. [Create Initial Issues](#6-create-initial-issues)
7. [Verify Setup](#7-verify-setup)
8. [Next Steps](#8-next-steps)

---

## 1. Create Repository

### Option A: New Repository

```bash
# Create repository
gh repo create [org]/[project-name] \
  --public \
  --description "Project description" \
  --clone

# Navigate to repository
cd [project-name]

# Create main branch and initial commit
git checkout -b main
echo "# [Project Name]" > README.md
git add README.md
git commit -m "chore: initial commit"
git push -u origin main
```

### Option B: Existing Repository

```bash
# Clone existing repository
gh repo clone [org]/[project-name]
cd [project-name]
```

**✅ Checkpoint:** You have a repository locally

---

## 2. Set Up Documentation Structure

### Copy Documentation Templates

```bash
# Create docs directory structure
mkdir -p docs/{guides,setup,development,archive}

# Copy documentation README
cp ~/osp/osp-docs/templates/repository/docs-structure.md \
   ./docs/README.md

# Copy README template
cp ~/osp/osp-docs/templates/repository/README.template.md \
   ./README.md

# Edit README.md with your project details
code README.md
```

### Update README Template

Edit `README.md` and replace placeholders:
- `[Project Name]` → Your project name
- `[Brief Description]` → Project description
- `[Tech Stack]` → Technologies used
- `[Organization]` → Your org name
- `[Repository Name]` → Your repo name

### Create Initial Documentation

```bash
# Create setup guide from template
cp ~/osp/osp-docs/templates/documentation/setup-guide.template.md \
   ./docs/setup/INSTALLATION.md

# Create architecture doc
cp ~/osp/osp-docs/templates/documentation/architecture.template.md \
   ./docs/development/ARCHITECTURE.md
```

### Commit Documentation Structure

```bash
git add docs/ README.md
git commit -m "docs: add documentation structure and README"
git push
```

**✅ Checkpoint:** Documentation structure created

---

## 3. Configure GitHub Labels

### Run Label Setup Script

```bash
# Make script executable
chmod +x ~/osp/osp-docs/templates/github-workflow/setup-labels.sh

# Run setup (will prompt for confirmation)
~/osp/osp-docs/templates/github-workflow/setup-labels.sh
```

The script will create:
- 4 Priority labels (P0-P3)
- 8 Type labels (bug, enhancement, etc.)
- 5 Status labels (blocked, in-progress, etc.)
- 5 Component labels (frontend, backend, etc.)

### Verify Labels

```bash
# List all labels
gh label list

# Or visit in browser
open https://github.com/[org]/[project-name]/labels
```

**✅ Checkpoint:** Labels configured

---

## 4. Add to Project Board

### Option A: Add to Existing Project Board

```bash
# Add repository to OSP Group master project
gh project item-add 1 \
  --owner [org] \
  --url https://github.com/[org]/[project-name]
```

### Option B: Create New Project Board (Optional)

```bash
# Create new project
gh project create \
  --owner [org] \
  --title "[Project Name] - Project Board"

# Note the project number, then:
PROJECT_NUM=[number from above]

# Link first issue to project (we'll create issues in step 6)
```

### Copy Issue Templates

```bash
# Create issue templates directory
mkdir -p .github/ISSUE_TEMPLATE

# Copy all templates
cp ~/osp/osp-docs/templates/github-workflow/issue-templates/* \
   .github/ISSUE_TEMPLATE/

# Commit templates
git add .github/
git commit -m "chore: add issue templates"
git push
```

**✅ Checkpoint:** Project board connected, templates added

---

## 5. Install VS Code Configuration

### Copy VS Code Settings

```bash
# Create .vscode directory
mkdir -p .vscode

# Copy recommended settings
cp ~/osp/osp-docs/templates/vscode/settings.json \
   .vscode/settings.json

# Copy recommended extensions
cp ~/osp/osp-docs/templates/vscode/extensions.json \
   .vscode/extensions.json

# Copy debug configurations (optional)
cp ~/osp/osp-docs/templates/vscode/launch.json \
   .vscode/launch.json
```

### Update Copilot Instructions

**Global Instructions (Already Done):**
If you followed the OSP setup, global instructions are already installed at:
- macOS/Linux: `~/Library/Application Support/Code/User/prompts/copilot-instructions.instructions.md`
- Windows: `%APPDATA%\Code\User\prompts\copilot-instructions.instructions.md`

**Project-Specific Instructions (Optional):**

```bash
# Create project instructions
mkdir -p .github
cp ~/osp/osp-docs/templates/vscode/copilot-instructions.project.md \
   .github/copilot-instructions.md

# Edit with project-specific info
code .github/copilot-instructions.md
```

### Install Recommended Extensions

```bash
# Install essential extensions
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat
code --install-extension eamodio.gitlens
code --install-extension esbenp.prettier-vscode
code --install-extension dbaeumer.vscode-eslint

# Or: Open project in VS Code, and it will prompt to install recommended extensions
code .
```

### Commit VS Code Configuration

```bash
git add .vscode/ .github/
git commit -m "chore: add VS Code configuration and Copilot instructions"
git push
```

**✅ Checkpoint:** VS Code configured

---

## 6. Create Initial Issues

### Create Setup Issues

```bash
# Issue 1: Project Setup Complete
gh issue create \
  --title "Complete initial project setup" \
  --label "P1,documentation" \
  --body "**Priority:** P1

## Description
Verify all setup steps completed successfully.

## Tasks
- [x] Repository created
- [x] Documentation structure added
- [x] Labels configured
- [x] Project board connected
- [x] VS Code configured
- [ ] Team invited
- [ ] CI/CD configured
- [ ] First deployment

## Acceptance Criteria
- ✅ All team members have access
- ✅ First successful build/deploy
- ✅ Documentation reviewed and approved"

# Add to project board
gh project item-add [PROJECT_NUM] \
  --owner [org] \
  --url $(gh issue list --limit 1 --json url -q '.[0].url')
```

```bash
# Issue 2: Configure CI/CD
gh issue create \
  --title "Set up CI/CD pipeline" \
  --label "P1,deployment" \
  --body "**Priority:** P1

## Description
Configure automated testing and deployment pipeline.

## Tasks
- [ ] Set up GitHub Actions for tests
- [ ] Configure build pipeline
- [ ] Set up staging environment
- [ ] Set up production environment
- [ ] Add deployment documentation

## Acceptance Criteria
- ✅ Tests run on every PR
- ✅ Main branch auto-deploys to staging
- ✅ Manual deployment to production works"

# Add to project board
gh project item-add [PROJECT_NUM] \
  --owner [org] \
  --url $(gh issue list --limit 1 --json url -q '.[0].url')
```

```bash
# Issue 3: Write Initial Documentation
gh issue create \
  --title "Write project documentation" \
  --label "P2,documentation" \
  --body "**Priority:** P2

## Description
Complete essential project documentation.

## Tasks
- [ ] Installation guide
- [ ] Development guide
- [ ] Architecture documentation
- [ ] API documentation
- [ ] Contributing guide

## Acceptance Criteria
- ✅ New team member can set up dev environment
- ✅ API endpoints documented
- ✅ Architecture decisions recorded"

# Add to project board
gh project item-add [PROJECT_NUM] \
  --owner [org] \
  --url $(gh issue list --limit 1 --json url -q '.[0].url')
```

**✅ Checkpoint:** Initial issues created

---

## 7. Verify Setup

### Checklist

Run through this checklist to verify everything is set up correctly:

```bash
# 1. Check repository exists and is accessible
gh repo view [org]/[project-name]

# 2. Verify documentation structure
ls -la docs/
# Should see: guides/ setup/ development/ archive/ README.md

# 3. Verify labels exist
gh label list
# Should see: P0, P1, P2, P3, bug, enhancement, etc.

# 4. Check project board
gh project view [PROJECT_NUM] --owner [org]
# Should see: 3 issues added

# 5. Verify VS Code configuration
ls -la .vscode/
# Should see: settings.json, extensions.json

# 6. Check issue templates
ls -la .github/ISSUE_TEMPLATE/
# Should see: bug-report.md, feature-request.md, etc.
```

### Test Workflow

Create a test issue to verify the complete workflow:

```bash
# 1. Create test issue
gh issue create \
  --title "Test workflow" \
  --label "P3,testing" \
  --body "Testing the complete workflow"

# 2. Add to project
gh project item-add [PROJECT_NUM] \
  --owner [org] \
  --url $(gh issue list --limit 1 --json url -q '.[0].url')

# 3. Create branch
git checkout -b feature/issue-[N]-test-workflow

# 4. Make test commit
echo "# Test" > test.md
git add test.md
git commit -m "test: verify workflow (Relates to #[N])"
git push -u origin feature/issue-[N]-test-workflow

# 5. Create PR
gh pr create \
  --title "Test workflow" \
  --body "Fixes #[N]"

# 6. Merge PR
gh pr merge --squash --delete-branch

# 7. Verify issue closed automatically
gh issue view [N]
```

**✅ Checkpoint:** Workflow tested and verified

---

## 8. Next Steps

### Invite Team Members

```bash
# Add team members to repository
gh repo add-collaborator [org]/[project-name] [username] --role write

# Grant project board access (if needed)
# This is done through GitHub web interface:
# Project Settings → Manage Access → Add people/teams
```

### Set Up Development Environment

```bash
# Install dependencies (example for Node.js project)
npm install
# or
yarn install

# Set up environment variables
cp .env.example .env
# Edit .env with your values

# Run development server
npm run dev
```

### Configure CI/CD

Create GitHub Actions workflow:

```bash
# Copy CI template
mkdir -p .github/workflows
cp ~/osp/osp-docs/templates/repository/github-actions/ci-test.yml \
   .github/workflows/test.yml

# Edit with your test commands
code .github/workflows/test.yml
```

### Schedule Team Onboarding

Share with team:
1. **Quick Start Guide** - `QUICK_START.md`
2. **Project README** - Your `README.md`
3. **Installation Guide** - `docs/setup/INSTALLATION.md`
4. **Project Board** - https://github.com/orgs/[org]/projects/[NUM]

Schedule 30-minute onboarding session to walk through workflow.

---

## 🎉 Setup Complete!

Your project is now configured with:

- ✅ Standardized documentation structure
- ✅ GitHub labels and issue templates
- ✅ Project board integration
- ✅ VS Code configuration with Copilot
- ✅ Initial issues and workflow tested

### What's Next?

1. **Start First Sprint**
   - Review backlog in project board
   - Assign issues to team members
   - Move high-priority issues to "Todo"

2. **Complete Initial Issues**
   - Set up CI/CD (Issue #2)
   - Write documentation (Issue #3)
   - Verify setup (Issue #1)

3. **Establish Team Rhythm**
   - Daily standup check-ins
   - Weekly sprint planning
   - Bi-weekly retrospectives

---

## 📚 Additional Resources

**Complete Workflow Guide:**
→ `WORKFLOW_GUIDE.md` - Daily routines, best practices

**Issue Templates:**
→ `issue-templates/` - All 8 templates

**FAQ:**
→ `FAQ.md` - Common questions

**VS Code Setup:**
→ `../vscode/README.md` - Detailed VS Code configuration

---

## 🆘 Troubleshooting

### GitHub CLI Not Working

```bash
# Check installation
gh --version

# Check authentication
gh auth status

# Re-authenticate if needed
gh auth login
```

### Labels Not Creating

```bash
# Check if you have write access
gh repo view [org]/[project-name] --json permissions

# Try manual label creation
gh label create "P0" --color "d73a4a" --description "Critical priority"
```

### Can't Add to Project Board

```bash
# Check project permissions
gh project list --owner [org]

# Refresh authentication with project scope
gh auth refresh -s project
```

### VS Code Extensions Not Installing

1. Open VS Code
2. View → Extensions
3. Search for extension by ID
4. Click Install
5. Reload window

---

## 📞 Support

**Setup Issues:** Create issue in `osp-group/docs` with label `template-setup`

**Workflow Questions:** See `FAQ.md` or ask in team chat

**Technical Problems:** Create issue with label `help-wanted`

---

**Congratulations! Your project is ready for development.** 🚀

---

**Last Updated:** October 18, 2025
**Version:** 1.0.0
