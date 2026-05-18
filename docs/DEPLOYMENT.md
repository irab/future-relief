# Deploying Documentation to GitHub Pages

This guide explains how the documentation is automatically deployed to GitHub Pages.

## Automatic Deployment

The documentation is automatically built and deployed when you:

1. Push changes to the `main` or `master` branch
2. Modify files in the `docs/` directory, `mkdocs.yml`, or the workflow file
3. Manually trigger the workflow from GitHub Actions

## GitHub Actions Workflow

The workflow (`.github/workflows/docs.yml`) automatically:

1. **Checks out** your repository
2. **Sets up Python** environment
3. **Installs** MkDocs and required plugins
4. **Builds** the documentation site
5. **Deploys** to GitHub Pages

## Manual Deployment

To manually trigger deployment:

1. Go to **Actions** tab in GitHub
2. Select **Deploy Documentation** workflow
3. Click **Run workflow**
4. Select branch and click **Run workflow**

## Enabling GitHub Pages

If GitHub Pages isn't enabled yet:

1. Go to **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. The workflow will automatically deploy

## Local Testing

Before pushing, test locally:

```bash
# Install dependencies
pip install -r docs/requirements.txt

# Serve locally
mkdocs serve

# Build to check for errors
mkdocs build --strict
```

## Custom Domain

To use a custom domain:

1. Add a `CNAME` file in the `docs/` directory with your domain
2. Configure DNS settings as per GitHub Pages instructions
3. The workflow will automatically include the CNAME file

## Troubleshooting

### Build Fails

- Check that all markdown files are valid
- Ensure `mkdocs.yml` syntax is correct
- Check GitHub Actions logs for specific errors

### Pages Not Updating

- Wait a few minutes for deployment to complete
- Check GitHub Actions for deployment status
- Clear browser cache

### Missing Pages

- Ensure all files referenced in `mkdocs.yml` exist
- Check file paths are correct
- Verify navigation structure
