# psytican-bot

Psytican Helper bot — a small helper bot for Psytican services.

## Quick Start

Install dependencies with Poetry (recommended):

```bash
poetry install
poetry run psytican-bot
```

Or run directly with Python for development:

```bash
python -m src.main
```

## Configuration

- Primary config file: `config.yaml`
- Credentials: `credentials.json`, `privkey.json`

Adjust settings in [src/configs/config.py](src/configs/config.py) or provide environment-specific values.

## Development

Run tests with `pytest`:

```bash
poetry run pytest -q
```

Lint and format with the tools in `pyproject.toml` (mypy, flake8, black, isort, pylint).

## Contributing

Contributions are welcome. Please follow the repository's code style and tests.

## Security

If you find a security vulnerability, please report it privately as described in [SECURITY.md](SECURITY.md).

## Helm Chart

You can install the Helm chart from the local `chart` directory or from the OCI registry at `oci://ghcr.io/raider444/charts/psytican-bot`.

- From the OCI registry (recommended for releases):

```bash
# If the registry is private, authenticate first:
helm registry login ghcr.io --username <USERNAME> --password <TOKEN>

# Install directly from the OCI registry (replace <chart-version> if needed):
helm install psytican-bot oci://ghcr.io/raider444/charts/psytican-bot --version <chart-version> \
	--namespace psytican --create-namespace
```

- From the checked-out local chart (useful for development):

```bash
# Install or upgrade using the local chart directory
helm upgrade --install psytican-bot ./chart -n psytican --create-namespace
```

Notes:
- To pull a chart archive locally: `helm chart pull oci://ghcr.io/raider444/charts/psytican-bot:TAG` and `helm chart export --destination . <chart-ref>`.
- Replace `psytican-bot`, namespace, and version values to fit your environment.

## License

MIT — see [LICENSE](LICENSE) for details.
