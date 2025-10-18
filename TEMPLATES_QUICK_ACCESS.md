# 🚀 Quick Access: Workflow Templates

**Use these templates to set up new projects with OSP Group's standardized workflow.**

---

## 📦 Template Package Location

All templates are in: **`/templates/`** directory

```
templates/
├── README.md ← Start here for overview
├── INSTALLATION_GUIDE.md ← Complete setup guide
├── QUICK_START.md ← 15-minute user guide
├── github-workflow/ ← GitHub Projects workflow
├── vscode/ ← VS Code configuration
├── repository/ ← Project structure (TODO)
└── documentation/ ← Doc templates (TODO)
```

---

## ⚡ Quick Links

### For Setting Up New Project
→ **[Complete Installation Guide](./templates/INSTALLATION_GUIDE.md)** (30-45 min)
- Step-by-step project setup
- All commands included
- Verification checklist

### For New Team Members
→ **[Quick Start Guide](./templates/github-workflow/QUICK_START.md)** (15 min)
- Daily workflow
- How to use project board
- Common commands

### For Template Overview
→ **[Templates README](./templates/README.md)** (10 min read)
- What's included
- When to use what
- Core principles

### For VS Code Setup
→ **[VS Code Templates](./templates/vscode/README.md)** (10 min)
- Copilot instructions installation
- Recommended extensions
- Settings configuration

---

## 🎯 Common Tasks

### Set Up a New Project

```bash
# 1. Create repository
gh repo create osp-group/[project-name] --public --clone
cd [project-name]

# 2. Copy documentation structure
mkdir -p docs/{guides,setup,development,archive}
cp ~/osp/osp-docs/templates/repository/docs-structure.md ./docs/README.md

# 3. Set up GitHub labels
bash ~/osp/osp-docs/templates/github-workflow/setup-labels.sh

# 4. Add to project board
gh project item-add 1 --owner osp-group --url https://github.com/osp-group/[project-name]

# 5. Copy issue templates
mkdir -p .github/ISSUE_TEMPLATE
cp ~/osp/osp-docs/templates/github-workflow/issue-templates/* .github/ISSUE_TEMPLATE/
```

→ **Full guide:** [INSTALLATION_GUIDE.md](./templates/INSTALLATION_GUIDE.md)

### Create an Issue

```bash
# Quick issue creation
gh issue create \
  --title "Your task description" \
  --label "P2,enhancement" \
  --assignee @me

# Add to project board
gh project item-add 1 --owner osp-group --url [issue-url]
```

→ **Issue templates:** [issue-templates/](./templates/github-workflow/issue-templates/)

### Install Copilot Instructions

```bash
# macOS/Linux
cp ~/osp/osp-docs/templates/vscode/copilot-instructions.global.md \
   ~/Library/Application\ Support/Code/User/prompts/copilot-instructions.instructions.md

# Restart VS Code
```

→ **Full guide:** [vscode/README.md](./templates/vscode/README.md)

---

## 📚 All Available Templates

### GitHub Workflow Templates

| Template | Purpose | Lines |
|----------|---------|-------|
| [README.md](./templates/github-workflow/README.md) | Workflow overview | 400+ |
| [QUICK_START.md](./templates/github-workflow/QUICK_START.md) | Daily workflow guide | 500+ |
| [setup-labels.sh](./templates/github-workflow/setup-labels.sh) | Automated label setup | 150+ |
| [bug-report.md](./templates/github-workflow/issue-templates/bug-report.md) | Bug report template | 200+ |
| [feature-request.md](./templates/github-workflow/issue-templates/feature-request.md) | Feature template | 250+ |
| [documentation.md](./templates/github-workflow/issue-templates/documentation.md) | Documentation template | 200+ |
| [deployment-task.md](./templates/github-workflow/issue-templates/deployment-task.md) | Deployment template | 300+ |

### VS Code Templates

| Template | Purpose | Lines |
|----------|---------|-------|
| [README.md](./templates/vscode/README.md) | VS Code setup guide | 400+ |
| [copilot-instructions.global.md](./templates/vscode/copilot-instructions.global.md) | Copilot instructions | 400+ |

### Main Documentation

| File | Purpose | Lines |
|------|---------|-------|
| [README.md](./templates/README.md) | Template package overview | 500+ |
| [INSTALLATION_GUIDE.md](./templates/INSTALLATION_GUIDE.md) | Complete setup guide | 600+ |
| [TEMPLATES_SUMMARY.md](./templates/TEMPLATES_SUMMARY.md) | Summary and status | 500+ |

**Total:** 12 files, ~4,000 lines of documentation and templates

---

## 🎓 Training Materials

### New Team Member Onboarding (90 min)

1. **Read:** [Quick Start Guide](./templates/github-workflow/QUICK_START.md) - 15 min
2. **Review:** Issue templates - 10 min
3. **Practice:** Create test issue and PR - 30 min
4. **Setup:** Install VS Code configuration - 15 min
5. **Review:** Project board walkthrough - 20 min

### External Contributor Onboarding (30 min)

1. **Read:** [Quick Start Guide](./templates/github-workflow/QUICK_START.md) - 15 min
2. **Review:** Project board basics - 10 min
3. **Practice:** Create first issue - 5 min

---

## 📊 Template Status

### ✅ Complete (Phase 1)

- Main documentation and guides
- GitHub workflow templates (core)
- VS Code Copilot instructions
- Issue templates (4 of 8)
- Automated label setup script

### 📝 TODO (Phase 2)

- Repository structure templates
- Documentation templates (API, architecture, etc.)
- Additional issue templates (4 more)
- VS Code settings and extensions
- GitHub Actions workflow templates

---

## 🔗 Related Documentation

**Current Workflow (OSP Group):**
- [GitHub Projects Workflow](./projects/GITHUB_PROJECTS_WORKFLOW.md) - Complete workflow guide
- [Issues Priority List](./projects/ISSUES_PRIORITY_LIST.md) - All current issues
- [Project Setup Guide](./projects/GITHUB_PROJECT_SETUP.md) - Project board setup

**Architecture & Planning:**
- [Architecture Documentation](./architecture/) - System design
- [Planning Documents](./planning/) - Strategic planning
- [Repository Guides](./repositories/) - Per-repo documentation

---

## 💡 Tips

### For Project Setup
- Follow INSTALLATION_GUIDE.md step-by-step
- Don't skip verification steps
- Test workflow with sample issue
- Invite team early in process

### For Daily Work
- Check project board every morning
- Always create issue before coding
- Update issue status as you work
- Reference issue numbers in commits

### For Template Customization
- Templates are organization-agnostic
- Find and replace placeholder values
- Keep core structure intact
- Document your customizations

---

## 📞 Support

**Template Questions:** Create issue in `osp-group/docs` with label `template-question`

**Setup Problems:** See [INSTALLATION_GUIDE.md](./templates/INSTALLATION_GUIDE.md) Troubleshooting section

**Feature Requests:** Create issue with label `template-enhancement`

**Bug Reports:** Create issue with label `template-bug`

---

## 🎯 Success Metrics

Templates are working if:
- ✅ New project setup takes <1 hour
- ✅ All projects use same workflow
- ✅ Documentation is consistent
- ✅ New team members productive in <2 hours
- ✅ 90%+ issues use templates
- ✅ Project board is single source of truth

---

**Last Updated:** October 18, 2025
**Version:** 1.0.0
**Maintained by:** OSP Group Development Team

**Start here:** [templates/README.md](./templates/README.md) 📦
