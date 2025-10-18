#!/bin/bash

# OSP Group - GitHub Labels Setup Script
# Automatically creates standardized labels for GitHub repositories

set -e

echo "🏷️  OSP Group - GitHub Labels Setup"
echo "===================================="
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed"
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub CLI"
    echo "Run: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI installed and authenticated"
echo ""

# Get current repository
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo "📦 Repository: $REPO"
echo ""

read -p "This will create/update labels in $REPO. Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "Creating labels..."
echo ""

# Priority Labels
echo "📌 Creating Priority Labels..."

gh label create "P0" \
    --description "Critical - Blocking, production down, data loss" \
    --color "d73a4a" \
    --force 2>/dev/null || echo "  ↳ P0 already exists"

gh label create "P1" \
    --description "High - Important features, major bugs, security" \
    --color "ff6b6b" \
    --force 2>/dev/null || echo "  ↳ P1 already exists"

gh label create "P2" \
    --description "Medium - Standard features, minor bugs" \
    --color "fbca04" \
    --force 2>/dev/null || echo "  ↳ P2 already exists"

gh label create "P3" \
    --description "Low - Nice-to-have, enhancements, cleanup" \
    --color "0e8a16" \
    --force 2>/dev/null || echo "  ↳ P3 already exists"

# Type Labels
echo ""
echo "🏷️  Creating Type Labels..."

gh label create "bug" \
    --description "Something isn't working" \
    --color "d73a4a" \
    --force 2>/dev/null || echo "  ↳ bug already exists"

gh label create "enhancement" \
    --description "New feature or request" \
    --color "a2eeef" \
    --force 2>/dev/null || echo "  ↳ enhancement already exists"

gh label create "documentation" \
    --description "Improvements or additions to documentation" \
    --color "0075ca" \
    --force 2>/dev/null || echo "  ↳ documentation already exists"

gh label create "deployment" \
    --description "Deployment and infrastructure tasks" \
    --color "5319e7" \
    --force 2>/dev/null || echo "  ↳ deployment already exists"

gh label create "integration" \
    --description "External service integration" \
    --color "1d76db" \
    --force 2>/dev/null || echo "  ↳ integration already exists"

gh label create "refactoring" \
    --description "Code improvement without new features" \
    --color "fbca04" \
    --force 2>/dev/null || echo "  ↳ refactoring already exists"

gh label create "testing" \
    --description "Test creation or improvement" \
    --color "d4c5f9" \
    --force 2>/dev/null || echo "  ↳ testing already exists"

gh label create "research" \
    --description "Investigation, POC, or research spike" \
    --color "e99695" \
    --force 2>/dev/null || echo "  ↳ research already exists"

# Status Labels
echo ""
echo "📊 Creating Status Labels..."

gh label create "blocked" \
    --description "Cannot proceed due to dependency" \
    --color "d73a4a" \
    --force 2>/dev/null || echo "  ↳ blocked already exists"

gh label create "in-progress" \
    --description "Actively being worked on" \
    --color "0e8a16" \
    --force 2>/dev/null || echo "  ↳ in-progress already exists"

gh label create "needs-review" \
    --description "Waiting for code review" \
    --color "fbca04" \
    --force 2>/dev/null || echo "  ↳ needs-review already exists"

gh label create "needs-testing" \
    --description "Waiting for QA testing" \
    --color "d4c5f9" \
    --force 2>/dev/null || echo "  ↳ needs-testing already exists"

gh label create "on-hold" \
    --description "Paused temporarily" \
    --color "bfdadc" \
    --force 2>/dev/null || echo "  ↳ on-hold already exists"

# Component Labels (optional - uncomment if needed)
echo ""
echo "🧩 Creating Component Labels..."

gh label create "frontend" \
    --description "Frontend/UI related" \
    --color "1f77b4" \
    --force 2>/dev/null || echo "  ↳ frontend already exists"

gh label create "backend" \
    --description "Backend/API related" \
    --color "ff7f0e" \
    --force 2>/dev/null || echo "  ↳ backend already exists"

gh label create "database" \
    --description "Database related" \
    --color "2ca02c" \
    --force 2>/dev/null || echo "  ↳ database already exists"

gh label create "devops" \
    --description "DevOps/Infrastructure" \
    --color "d62728" \
    --force 2>/dev/null || echo "  ↳ devops already exists"

gh label create "design" \
    --description "Design/UX related" \
    --color "9467bd" \
    --force 2>/dev/null || echo "  ↳ design already exists"

# Cleanup old default labels (optional)
echo ""
read -p "Remove default GitHub labels? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧹 Removing default labels..."
    
    # List of default labels to remove
    DEFAULT_LABELS=("good first issue" "help wanted" "invalid" "question" "wontfix" "duplicate")
    
    for label in "${DEFAULT_LABELS[@]}"; do
        gh label delete "$label" --yes 2>/dev/null && echo "  ↳ Removed: $label" || true
    done
fi

echo ""
echo "✅ Label setup complete!"
echo ""
echo "📋 Summary:"
echo "  • 4 Priority labels (P0-P3)"
echo "  • 8 Type labels"
echo "  • 5 Status labels"
echo "  • 5 Component labels"
echo ""
echo "View labels at: https://github.com/$REPO/labels"
echo ""
