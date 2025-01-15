# llm-logs-feedback

[![PyPI](https://img.shields.io/pypi/v/llm-logs-feedback.svg)](https://pypi.org/project/llm-logs-feedback/)
[![Changelog](https://img.shields.io/github/v/release/luebken/llm-logs-feedback?include_prereleases&label=changelog)](https://github.com/luebken/llm-logs-feedback/releases)
[![Tests](https://github.com/luebken/llm-logs-feedback/actions/workflows/test.yml/badge.svg)](https://github.com/luebken/llm-logs-feedback/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/luebken/llm-logs-feedback/blob/main/LICENSE)

This is a plugin for [LLM](https://llm.datasette.io/) to provide and manage feedback on `llm logs` which represent prompts and reponses.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-logs-feedback
```
## Usage

This plugin adds two new commands to provide feedback to the last prompt / response: 
 * `llm feedback+1`: to provide positive feedback 
 * `llm feedback-1`: to provide negative feedback

 Both commands accept an optional comment. So some example usage could be: 

 ```sh
 llm feedback+1 "this worked great during refactoring."
 llm feedback-1 "not helplful. too lengthy."
 ```

## Development

see [development.md](development.md)