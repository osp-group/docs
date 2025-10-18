# VS Code Templates

Configuration templates for VS Code, including Copilot instructions, settings, and extensions.

---

## 📦 Contents

1. **Copilot Instructions** - AI assistant configuration
2. **Settings** - Recommended VS Code settings
3. **Extensions** - Essential extensions list
4. **Workspace Configuration** - Project-specific settings

---

## 🚀 Quick Setup

### 1. Install Copilot Instructions (Global)

Copy the global Copilot instructions to your VS Code User Settings:

**macOS/Linux:**
```bash
mkdir -p ~/Library/Application\ Support/Code/User/prompts/
cp copilot-instructions.global.md \
   ~/Library/Application\ Support/Code/User/prompts/copilot-instructions.instructions.md
```

**Windows:**
```powershell
mkdir -p $env:APPDATA\Code\User\prompts\
cp copilot-instructions.global.md `
   $env:APPDATA\Code\User\prompts\copilot-instructions.instructions.md
```

### 2. Add Project-Specific Instructions (Optional)

For project-specific Copilot behavior, copy to your project:

```bash
cp copilot-instructions.project.md .github/copilot-instructions.md
```

### 3. Install Recommended Extensions

```bash
# Install all recommended extensions
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat
code --install-extension eamodio.gitlens
code --install-extension esbenp.prettier-vscode
code --install-extension dbaeumer.vscode-eslint
# ... (see extensions.json for full list)
```

Or copy `extensions.json` to `.vscode/extensions.json` and VS Code will prompt to install.

### 4. Copy Settings

```bash
# For project settings
mkdir -p .vscode
cp settings.json .vscode/settings.json

# For global settings, manually merge with your existing settings
```

---

## 📄 File Descriptions

### `copilot-instructions.global.md`
**Purpose:** Global Copilot instructions that apply to all projects
**Location:** VS Code User Settings directory
**Scope:** All workspaces

**Contains:**
- Core development principles (usability, clarity, aesthetics)
- UI development standards (accessibility, mobile-first)
- Documentation organization rules
- GitHub Projects workflow (mandatory)
- OSP Group specific conventions

**When to update:**
- Organization-wide workflow changes
- New best practices adopted
- Tool or framework standards change

### `copilot-instructions.project.md`
**Purpose:** Project-specific Copilot instructions
**Location:** `.github/copilot-instructions.md` in repository
**Scope:** Current project only

**Contains:**
- Project-specific tech stack
- Custom coding conventions
- API patterns and structures
- Project architecture notes
- Domain-specific terminology

**When to update:**
- Project architecture changes
- New patterns established
- Team conventions updated

### `settings.json`
**Purpose:** Recommended VS Code settings
**Location:** `.vscode/settings.json` in repository (or user settings)

**Includes:**
- Editor formatting rules
- File associations
- Language-specific settings
- Extension configurations
- Git settings

### `extensions.json`
**Purpose:** Recommended VS Code extensions
**Location:** `.vscode/extensions.json` in repository

**Categories:**
- Essential (Copilot, GitLens, etc.)
- Language support (TypeScript, Python, etc.)
- Formatters & Linters
- Git tools
- Documentation tools
- DevOps tools

### `launch.json`
**Purpose:** Debugging configurations
**Location:** `.vscode/launch.json` in repository

**Configurations for:**
- Node.js debugging
- Browser debugging
- Python debugging
- Docker debugging
- Jest testing

---

## 🎯 Best Practices

### Copilot Instructions

**✅ Do:**
- Keep instructions clear and actionable
- Update when workflow changes
- Include examples for complex patterns
- Reference documentation links
- Test instructions with real scenarios

**❌ Don't:**
- Make instructions too long (>1000 lines)
- Include project secrets or credentials
- Assume Copilot knows your internal tools
- Leave outdated instructions in place

### VS Code Settings

**✅ Do:**
- Use workspace settings for project-specific config
- Use user settings for personal preferences
- Document why non-standard settings exist
- Keep settings organized by category
- Version control workspace settings

**❌ Don't:**
- Override user settings unnecessarily
- Include absolute file paths
- Commit personal API keys
- Enable auto-save in team projects (without agreement)

### Extension Management

**✅ Do:**
- Recommend essential extensions only
- Group extensions by purpose
- Document why each extension is needed
- Keep extension list updated
- Test extension compatibility

**❌ Don't:**
- Require 20+ extensions
- Include experimental extensions as required
- Override user's extension settings
- Require paid extensions (unless agreed)

---

## 🔧 Customization Guide

### Adding GitHub Projects to Instructions

If using a different GitHub organization:

```markdown
## GitHub Projects Workflow (MANDATORY)

**[Your Org] uses GitHub Projects as the single source of truth.**

### Project Board Information
- **Organization:** your-org-name
- **Project:** "Your Project Board Name"
- **URL:** https://github.com/orgs/your-org/projects/[N]
```

### Adding Project-Specific Tech Stack

In `copilot-instructions.project.md`:

```markdown
## Tech Stack

**Frontend:**
- React 18+ with TypeScript
- TailwindCSS for styling
- React Query for data fetching
- Zustand for state management

**Backend:**
- Node.js with Express
- PostgreSQL with Drizzle ORM
- Redis for caching
- JWT authentication

**Patterns:**
- Use functional components only
- Custom hooks in `hooks/` directory
- API routes in `routes/` directory
- Database models in `db/schema/`
```

### Adding Team Conventions

```markdown
## Team Conventions

**File Naming:**
- Components: PascalCase (UserProfile.tsx)
- Utilities: camelCase (formatDate.ts)
- Constants: SCREAMING_SNAKE_CASE (API_ENDPOINTS.ts)
- Styles: kebab-case (user-profile.module.css)

**Commit Messages:**
- feat: New feature
- fix: Bug fix
- docs: Documentation
- refactor: Code improvement
- test: Test addition/update
- chore: Maintenance
```

---

## 📚 Extension Recommendations

### Essential (Required)

| Extension | Purpose | ID |
|-----------|---------|-----|
| GitHub Copilot | AI code completion | GitHub.copilot |
| GitHub Copilot Chat | AI chat assistant | GitHub.copilot-chat |
| GitLens | Git supercharging | eamodio.gitlens |
| Prettier | Code formatter | esbenp.prettier-vscode |
| ESLint | JavaScript linter | dbaeumer.vscode-eslint |

### Language Support

| Extension | Purpose | ID |
|-----------|---------|-----|
| TypeScript | TypeScript support | (built-in) |
| Python | Python support | ms-python.python |
| Go | Go support | golang.go |

### Developer Experience

| Extension | Purpose | ID |
|-----------|---------|-----|
| Error Lens | Inline error display | usernamehw.errorlens |
| Todo Tree | TODO highlighting | Gruntfuggly.todo-tree |
| Path Intellisense | Path autocomplete | christian-kohler.path-intellisense |
| Auto Rename Tag | HTML tag renaming | formulahendry.auto-rename-tag |

### Documentation

| Extension | Purpose | ID |
|-----------|---------|-----|
| Markdown All in One | Markdown support | yzhang.markdown-all-in-one |
| Markdown Preview Enhanced | Better MD preview | shd101wyy.markdown-preview-enhanced |

### DevOps

| Extension | Purpose | ID |
|-----------|---------|-----|
| Docker | Docker support | ms-azuretools.vscode-docker |
| YAML | YAML support | redhat.vscode-yaml |
| DotENV | .env file support | mikestead.dotenv |

---

## 🔍 Troubleshooting

### Copilot Instructions Not Working

1. **Check file location:**
   ```bash
   # macOS/Linux
   ls -la ~/Library/Application\ Support/Code/User/prompts/
   
   # Windows
   dir %APPDATA%\Code\User\prompts\
   ```

2. **Check file name:** Must end with `.instructions.md`

3. **Restart VS Code:** Copilot loads instructions on startup

4. **Check Copilot status:** Ensure Copilot is active and authenticated

### Settings Not Applied

1. **Check workspace vs user settings:** Workspace overrides user
2. **Check for syntax errors:** Settings must be valid JSON
3. **Reload window:** Cmd/Ctrl + Shift + P → "Reload Window"
4. **Check extension conflicts:** Disable conflicting extensions

### Extensions Not Installing

1. **Check internet connection:** Extensions download from marketplace
2. **Check VS Code version:** Some extensions require newer versions
3. **Check workspace trust:** Enable workspace trust for extensions
4. **Install manually:** Search in Extensions view

---

## 📞 Support

**Template Issues:** Create issue in `osp-group/docs` with label `template-vscode`

**VS Code Help:** [VS Code Documentation](https://code.visualstudio.com/docs)

**Copilot Help:** [GitHub Copilot Docs](https://docs.github.com/en/copilot)

---

**Last Updated:** October 18, 2025
**Version:** 1.0.0
