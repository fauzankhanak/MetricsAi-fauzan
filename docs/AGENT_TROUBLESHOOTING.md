# 🤖 Agent Blocking Issue Troubleshooting

## 🚨 Agent Shows "Blocked" Status and Redirects to GitHub

If you're seeing an agent with "blocked" status that redirects to GitHub when clicked, here are the common causes and solutions:

## 🔍 What This Usually Means

### Common Scenarios:
1. **GitHub Bot/Agent**: Repository bot or workflow agent that's been blocked
2. **Development Agent**: CI/CD or automation agent with access issues
3. **Third-party Integration**: External service agent blocked by repository settings
4. **Cursor/VS Code Agent**: Development environment agent with permission issues

## 🛠️ Solutions by Agent Type

### GitHub Repository Agent/Bot

**If it's a GitHub bot or workflow agent:**

```bash
# Check repository settings
# Go to: https://github.com/your-username/your-repo/settings

# Check these sections:
# 1. Actions > General > Allow GitHub Actions to create and approve pull requests
# 2. Secrets and variables > Actions (check if secrets are properly set)
# 3. Branches > Branch protection rules
```

**Steps to unblock:**
1. Go to your GitHub repository
2. Click **Settings** tab
3. Go to **Actions** → **General**
4. Ensure actions are enabled
5. Check **Secrets and variables** → **Actions**
6. Verify all required secrets are set

### Cursor/VS Code Development Agent

**If this is in Cursor or VS Code:**

```bash
# Check Git authentication
git config --list | grep user
git remote -v

# Re-authenticate if needed
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# For GitHub CLI
gh auth login
gh auth status
```

**In Cursor specifically:**
1. Open Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
2. Type: "Git: Clone"
3. Re-authenticate with GitHub
4. Check Extensions → GitHub settings

### CI/CD Agent (GitHub Actions, etc.)

**If it's a CI/CD agent:**

```yaml
# Check .github/workflows/ files
# Common fix - update workflow permissions:

name: CI
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
      issues: write
    steps:
      # Your steps here
```

### Third-party Integration Agent

**If it's an external service:**

1. **Check API keys/tokens**:
   ```bash
   # Verify environment variables
   echo $GITHUB_TOKEN
   echo $API_KEY
   ```

2. **Update integration settings**:
   - Go to GitHub → Settings → Developer settings → Personal access tokens
   - Generate new token with appropriate scopes
   - Update the service configuration

## 🔐 Permission Issues

### GitHub Token Scopes

If the agent needs GitHub access, ensure your token has these scopes:
- `repo` (for private repositories)
- `workflow` (for GitHub Actions)
- `write:packages` (if using packages)
- `read:org` (for organization access)

```bash
# Create new token:
# 1. Go to https://github.com/settings/tokens
# 2. Click "Generate new token (classic)"
# 3. Select appropriate scopes
# 4. Copy token and update your service
```

### Repository Settings

Check these GitHub repository settings:
1. **Settings** → **Actions** → **General**
   - Allow all actions and reusable workflows
   - Allow GitHub Actions to create and approve pull requests

2. **Settings** → **Branches**
   - Review branch protection rules
   - Ensure agents can push to protected branches if needed

3. **Settings** → **Secrets and variables**
   - Verify all required secrets are set
   - Check secret names match what agents expect

## 🔄 Quick Fixes

### Method 1: Refresh Agent Status
```bash
# For GitHub Actions
# Go to Actions tab → Re-run failed workflows

# For local development agents
# Restart your IDE/editor
# Clear cache: Ctrl+Shift+P → "Developer: Reload Window"
```

### Method 2: Re-authenticate
```bash
# GitHub CLI
gh auth logout
gh auth login

# Git credentials
git config --global --unset credential.helper
git config --global credential.helper store
```

### Method 3: Check Network/Firewall
```bash
# Test GitHub connectivity
curl -I https://api.github.com

# Test specific repository access
curl -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/repos/username/repository
```

## 🚀 Platform-Specific Solutions

### Cursor IDE Agent Issues

```bash
# Reset Cursor settings
# 1. Close Cursor
# 2. Delete cache:
#    - Windows: %APPDATA%\Cursor\User\workspaceStorage
#    - macOS: ~/Library/Application Support/Cursor/User/workspaceStorage
#    - Linux: ~/.config/Cursor/User/workspaceStorage
# 3. Restart Cursor
# 4. Re-authenticate with GitHub
```

### VS Code Agent Issues

```bash
# Reset VS Code GitHub integration
# 1. Command Palette: "GitHub: Sign out"
# 2. Command Palette: "GitHub: Sign in"
# 3. Reload window: Ctrl+Shift+P → "Developer: Reload Window"
```

### GitHub Codespaces Agent

```bash
# If in GitHub Codespaces
# 1. Go to https://github.com/codespaces
# 2. Find your codespace
# 3. Click "..." → "Stop codespace"
# 4. Start again or rebuild
```

## 📋 Diagnostic Commands

Run these to gather information about the agent issue:

```bash
# Check Git status and remotes
git status
git remote -v
git log --oneline -5

# Check GitHub CLI status
gh auth status
gh repo view

# Check environment variables
env | grep -i github
env | grep -i git

# Check network connectivity
ping github.com
nslookup api.github.com
```

## 🔍 Identify the Specific Agent

To help identify which agent is blocked:

1. **Where do you see this blocked agent?**
   - GitHub repository page?
   - VS Code/Cursor interface?
   - CI/CD dashboard?
   - Third-party service?

2. **What happens when you click it?**
   - Which GitHub page does it redirect to?
   - Repository settings?
   - Actions page?
   - User profile?

3. **What was the last action before it got blocked?**
   - Push to repository?
   - Changed settings?
   - Updated permissions?

## 📞 Still Need Help?

If the agent is still blocked, please provide:

1. **Screenshot** of the blocked agent
2. **URL** it redirects to when clicked
3. **Platform** where you see this (GitHub, VS Code, Cursor, etc.)
4. **Recent changes** you made to repository/settings

## 🎯 Quick Action Items

**Try these in order:**

1. ✅ Refresh the page/restart the application
2. ✅ Check GitHub authentication status
3. ✅ Verify repository permissions
4. ✅ Re-authenticate with GitHub
5. ✅ Check for recent setting changes
6. ✅ Clear cache and restart

**Most common fix**: Re-authentication with GitHub usually resolves 80% of agent blocking issues.

---

**Need immediate help?** 
- Share a screenshot of the blocked agent
- Tell me which platform/service you're using
- I'll provide specific steps for your situation!