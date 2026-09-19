Run these commands inside the original benchmark virtual environment and commit the outputs before archival release:

```powershell
python --version > environment/python-version.txt
pip freeze > environment/requirements-lock.txt
```
