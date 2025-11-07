# Contributing

I welcome **all** kinds of contributions - domain expertise, bug fixes, big features, docs, examples and more. _You don't need to be an AI expert or even a Python developer to help out. I would especially appreciate help with the following:
- Help with more question types the mcp can asnwer and scenarios it can be used in. Domain experts welcome - co coding needed here!
- Help with evaluations of outputs.
- Data analysis and insights.
- Adding more tools to the MCP server
- Adding semantic search to the database
- Improving documentation
- Identify bugs, ommissions and errors.


## Checklist

Contributions are made through
[pull requests](https://help.github.com/articles/using-pull-requests/).

Before sending a pull request, make sure to do the following:

- Fork the repo, and create a feature branch prefixed with `feature/`


_Please reach out to the mcp-openfoodtox maintainers before starting work on a large
contribution._ Get in touch at
[GitHub issues](https://github.com/spyrosze/mcp-openfoodtox/issues)


## Prerequisites

To build mcp-openfoodtox, you'll need the following installed:

- Install [uv](https://docs.astral.sh/uv/), which we use for Python package management
- Install [Python](https://www.python.org/) >= 3.12. (You may already it installed. To see your version, use `python -V` at the command line.)

  If you don't, install it using `uv python install 3.12`
- Setup by running:

```bash
make setup
```

  This will install all packages with extras and dev dependencies and setup the sqlite database.

## Development Commands

We provide a [Makefile](./Makefile) with common development commands:
```bash
make dev
```
This will start the MCP Inspector UI.
```bash
make run
```
This will start the server locally.


## AI Development

There is an AGENTS.md that outlines the project and the development priorities for AI dev assistants.

## Thank you

If you are considering contributing, **thank you**. This project is meant to provide easy acces to food safety toxicology data, and we need all the help we can get! Happy building.