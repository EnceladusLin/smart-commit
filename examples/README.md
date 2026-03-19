# SmartCommit demo

## Example staged diff summary

```text
src/auth.py (+45 -12)
tests/test_auth.py (+28 -5)
README.md (+3 -1)
```

## Example generated message

```text
feat(auth): add JWT token refresh mechanism
- implement refresh_token endpoint
- add expiration check before validation
- update tests for refresh flow
- fix auth example in README
```

## Demo flow

```bash
git add .
smart-commit --dry-run
```
