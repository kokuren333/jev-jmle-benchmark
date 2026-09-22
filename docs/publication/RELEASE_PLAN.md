# Public release plan

The repository is published as a GitHub whitepaper and reproducibility
package. The canonical public version is identified by a Git tag.

## Version policy

- `v1.0.0`: first public whitepaper release.
- Future changes to the manuscript, figures, or primary results require a
  new release tag and a short entry in the release notes.
- Historical working notes are kept under `docs/archive/` and are not part
  of the canonical whitepaper.

## Release checklist

1. Confirm that the English manuscript source, Japanese PDF, figures, tables,
   and results describe the same analysis.
2. Run the test suite and repository validation scripts.
3. Review the rendered English and Japanese PDFs.
4. Commit the release metadata and create the corresponding GitHub tag.
5. Publish the GitHub Release with links to both PDFs and the repository.

Zenodo and DOI registration are intentionally out of scope for this
publication route.
