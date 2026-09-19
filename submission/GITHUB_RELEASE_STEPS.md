# GitHub -> Zenodo release steps

## 1. Create repository
Suggested repository name: `jev-jmle-benchmark`.

If GitHub CLI is installed:

```powershell
gh auth login
gh repo create jev-jmle-benchmark --public --source . --remote origin --push
```

Otherwise create an empty public repository in GitHub's UI, then run:

```powershell
git init
git add .
git commit -m "Initial reproducibility release"
git branch -M main
git remote add origin https://github.com/<OWNER>/jev-jmle-benchmark.git
git push -u origin main
```

## 2. Freeze a release
After replacing placeholders and adding the exact `pip freeze` file:

```powershell
git add .
git commit -m "Prepare paper release v1.0.0"
git tag -a v1.0.0-paper -m "Paper reproducibility release"
git push origin main --tags
```

Create a GitHub Release from `v1.0.0-paper`.

## 3. Zenodo
Connect GitHub to Zenodo, enable the repository, then create the GitHub Release. Zenodo will ingest enabled releases and mint a DOI. Add the DOI back to the manuscript and citation metadata in a follow-up commit/release if necessary.
