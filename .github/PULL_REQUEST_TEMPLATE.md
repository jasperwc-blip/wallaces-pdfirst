## Summary

Describe the change.

## Checklist

- [ ] Tests pass locally.
- [ ] Portable build completes on Windows.
- [ ] README/docs updated if behavior changed.
- [ ] No generated `build`, `dist`, `.venv-build`, or `__pycache__` files committed.
- [ ] Privacy/safety impact considered.

## Test Notes

Commands run:

```bat
python -m unittest discover -s app\tests
build_portable.bat
```

