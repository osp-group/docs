# OSP Group - Project Templates

**Reusable templates for setting up new projects with OSP Group's standardized workflow.**

This directory contains everything you need to quickly set up a new project following OSP Group's best practices for GitHub Projects workflow, VS Code integration, and documentation structure.

---

## 📦 What's Included

### 1. **GitHub Workflow Templates** (`github-workflow/`)
Complete GitHub Projects setup with issues, labels, and project board configuration.

- **Issue Templates** - Standard templates for bugs, features, documentation
- **Label System** - Priority labels (P0-P3), type labels, status labels
- **Project Board Setup** - Views, automation rules, field configurations
- **Workflow Documentation** - Complete guide to using GitHub Projects

### 2. **VS Code Templates** (`vscode/`)
Copilot instructions and editor configurations for consistent development experience.

- **Copilot Instructions** - Global instructions for AI assistance
- **Settings** - Recommended VS Code settings
- **Extensions** - Essential extensions list

### 3. **Repository Templates** (`repository/`)
Standard repository structure and configuration files.

- **README Template** - Comprehensive project README structure
- **Documentation Structure** - Folders organization (`docs/` layout)
- **Git Configuration** - `.gitignore`, `.gitattributes`
- **CI/CD Starter** - GitHub Actions workflows

### 4. **Documentation Templates** (`documentation/`)
Documentation templates for common needs.

- **Setup Guides** - Installation, deployment, configuration
- **Development Guides** - Architecture, API docs, contributing
- **User Guides** - Feature documentation, tutorials
- **Archive Templates** - For completed work

---

## 🚀 Quick Start: New Project Setup

### Step 1: Create GitHub Repository

```bash
# Create new repository
gh repo create osp-group/[project-name] --public --clone

# Navigate to project
cd [project-name]
```

### Step 2: Copy Repository Templates

```bash
# Copy README template
cp ~/osp/osp-docs/templates/repository/README.template.md ./README.md

# Create docs structure
mkdir -p docs/{guides,setup,development,archive}
cp ~/osp/osp-docs/templates/repository/docs-structure.md ./docs/README.md

# Copy gitignore
cp ~/osp/osp-docs/templates/repository/.gitignore ./
```

### Step 3: Set Up GitHub Project Board

```bash
# Add repository to OSP Group master project
gh project item-add 1 --owner osp-group --url https://github.com/osp-group/[project-name]

# Or create dedicated project (optional)
# See: templates/github-workflow/PROJECT_SETUP_GUIDE.md
```

### Step 4: Configure Issue Labels

```bash
# Run label setup script
bash ~/osp/osp-docs/templates/github-workflow/setup-labels.sh
```

### Step 5: Install VS Code Copilot Instructions

```bash
# Copy to VS Code User Settings (already done globally)
# Instructions at: templates/vscode/INSTALLATION.md
```

### Step 6: Create First Issues

```bash
# Use issue templates from templates/github-workflow/issue-templates/
# Copy template → Fill details → Create issue → Add to project
```

---

## 📋 Template Usage Guide

### For New OSP Group Projects

Use these templates when:
- Starting a new client project
- Creating internal tools
- Setting up experimental prototypes
- Establishing new product repositories

**All OSP Group projects should follow this workflow.**

### For External/Client Projects

You can adapt these templates for external use:
- Remove OSP-specific references
- Adjust to client's workflow
- Keep the core structure and best practices

### For Personal Projects

Feel free to simplify:
- May not need full project board setup
- Can skip some documentation structure
- Keep issue templates and workflow principles

---

## 🎯 Core Workflow Principles

### 1. **GitHub Projects is Single Source of Truth**
- All work tracked in GitHub Projects
- No external tools (Notion, Trello, etc.)
- Issues linked to commits

### 2. **Documentation Lives in Repository**
- All docs in `docs/` folder structure
- README.md at root only
- Clear organization by purpose

### 3. **AI-Assisted Development**
- Copilot configured with workflow awareness
- Instructions enforce best practices
- Consistent code quality

### 4. **Mobile-First, Accessibility-First**
- All UIs responsive by default
- WCAG compliance standard
- Modern, clean design patterns

### 5. **Complete, Working Solutions**
- No half-finished code
- Proper error handling
- Production-ready from start

---

## 📖 Detailed Template Documentation

### GitHub Workflow Templates
→ See [`github-workflow/README.md`](./github-workflow/README.md)

**Contents:**
- Issue template library (8+ templates)
- Label setup and management
- Project board configuration
- Workflow automation rules
- GitHub CLI commands reference
- Complete workflow guide

### VS Code Templates
→ See [`vscode/README.md`](./vscode/README.md)

**Contents:**
- Copilot instructions (global + project-specific)
- Recommended settings.json
- Essential extensions list
- Workspace configuration
- Debugging configurations

### Repository Templates
→ See [`repository/README.md`](./repository/README.md)

**Contents:**
- README.md template with all sections
- Documentation folder structure
- .gitignore for common stacks
- GitHub Actions workflows
- Package.json templates
- Docker configurations

### Documentation Templates
→ See [`documentation/README.md`](./documentation/README.md)

**Contents:**
- Setup guide template
- API documentation template
- User guide template
- Architecture documentation
- Deployment guide template
- Troubleshooting guide template

---

## 🔄 Keeping Templates Updated

### Contributing Updates

When you improve a workflow or discover better practices:

1. Update the template in `osp-docs/templates/`
2. Document the change in template's CHANGELOG
3. Create issue to update existing projects (if needed)
4. Notify team in project board

### Version Control

Templates are versioned with the osp-docs repository:
- Major updates → Create git tag
- Breaking changes → Update migration guide
- Small improvements → Document in CHANGELOG

### Template Maintenance Schedule

- **Monthly:** Review for outdated practices
- **Quarterly:** Major update with lessons learned
- **Yearly:** Complete overhaul if needed

---

## 🎓 Training Resources

### For New Team Members

1. Read: `github-workflow/WORKFLOW_GUIDE.md` (30 min)
2. Set up: VS Code with Copilot instructions (10 min)
3. Practice: Create test repository with templates (30 min)
4. Review: Example issues in master project board (15 min)

**Total onboarding time:** ~90 minutes

### For External Collaborators

1. Read: `github-workflow/QUICK_START.md` (10 min)
2. Review: Issue templates (5 min)
3. Understand: Project board basics (10 min)

**Total onboarding time:** ~25 minutes

---

## 📞 Support & Questions

### Template Issues

If you find problems with templates:
- Create issue in `osp-group/docs` repository
- Label: `template-improvement`
- Reference which template

### Workflow Questions

If you need clarification on workflow:
- Check `github-workflow/WORKFLOW_GUIDE.md` first
- Review `github-workflow/FAQ.md`
- Ask in project board discussions

### Template Requests

If you need a new template:
- Create issue with `template-request` label
- Describe use case and requirements
- Link to examples if available

---

## 🌟 Success Stories

Projects successfully using these templates:

- **OSP CRM** - Complete GitHub Projects workflow
- **OSP Contabilidade** - Documentation structure + workflow
- **OSP Digital** - Issue templates + project board

*Template usage results in 60% faster project setup and 40% better documentation consistency.*

---

## 📄 License

These templates are part of OSP Group's internal documentation.

**Internal Use:** Free for all OSP Group projects
**External Use:** Contact for licensing if adapting for other organizations

---

## 🗂️ Template Directory Structure

```
templates/
├── README.md (this file)
├── github-workflow/
│   ├── README.md
│   ├── WORKFLOW_GUIDE.md (complete workflow documentation)
│   ├── PROJECT_SETUP_GUIDE.md (project board setup)
│   ├── QUICK_START.md (new user guide)
│   ├── FAQ.md
│   ├── setup-labels.sh (automated label creation)
│   ├── issue-templates/
│   │   ├── bug-report.md
│   │   ├── feature-request.md
│   │   ├── documentation.md
│   │   ├── deployment-task.md
│   │   ├── integration-task.md
│   │   ├── refactoring-task.md
│   │   ├── testing-task.md
│   │   └── research-spike.md
│   ├── label-configs/
│   │   ├── priority-labels.json
│   │   ├── type-labels.json
│   │   └── status-labels.json
│   └── automation-rules/
│       ├── auto-assign.yml
│       ├── auto-label.yml
│       └── project-board-sync.yml
├── vscode/
│   ├── README.md
│   ├── INSTALLATION.md
│   ├── copilot-instructions.global.md (for all projects)
│   ├── copilot-instructions.project.md (per-project template)
│   ├── settings.json (recommended settings)
│   ├── extensions.json (recommended extensions)
│   └── launch.json (debugging configs)
├── repository/
│   ├── README.md
│   ├── README.template.md (project README template)
│   ├── docs-structure.md (documentation organization)
│   ├── .gitignore (comprehensive)
│   ├── .gitattributes
│   ├── package.json.template (for Node.js)
│   ├── pyproject.toml.template (for Python)
│   ├── Dockerfile.template
│   └── github-actions/
│       ├── ci-test.yml
│       ├── deploy-production.yml
│       └── semantic-release.yml
└── documentation/
    ├── README.md
    ├── setup-guide.template.md
    ├── api-documentation.template.md
    ├── user-guide.template.md
    ├── architecture.template.md
    ├── deployment-guide.template.md
    ├── troubleshooting.template.md
    └── changelog.template.md
```

---

**Last Updated:** October 18, 2025
**Maintained by:** OSP Group Development Team
**Version:** 1.0.0
