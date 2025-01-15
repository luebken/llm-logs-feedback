## Development

```sh
# Install
llm install -e .
# Check 
llm --help | grep feedback
# Uninstall
llm uninstall llm-logs-feedback
```

Or:

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-logs-feedback
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
llm install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```

## Release

Manual
```sh
python -m build
python -m twine upload dist/*
```