# Claude Code Project Rules - Adaptive Lighting

## Project Context

This is a Home Assistant custom component that dynamically adjusts light brightness and color temperature based on the sun's position throughout the day. It provides a circadian lighting experience by automatically transitioning between warm colors at night and cool colors during the day.

**Version:** 1.26.0
**Codeowners:** @basnijholt, @RubenKelevra, @th3w1zard1, @protyposis

**Key Features:**

- Sun-position based brightness and color temperature calculation
- Per-light manual override detection (sleep mode, brightness/color overrides)
- Multiple adaptation modes (color_temp, color, brightness)
- Integration with Home Assistant's entity registry and device tracking
- WebAssembly-based configuration visualization tool

**Tech Stack:**

- Python 3.10+ (Home Assistant custom component)
- pytest / pytest-asyncio (testing)
- Docker (test infrastructure)
- Home Assistant Core integration patterns

**External Dependencies:**

- `ulid-transform` (for unique identifiers)
- Home Assistant Core's `light` integration

## Code Quality Standards (2025)

### Python (PEP 8 + Modern Best Practices)

- **Linter:** `ruff` with `ALL` rules enabled (see `.ruff.toml` for exceptions)
- **Formatter:** `black` (via pre-commit)
- **Security:** `gitleaks` for secret detection
- **Max complexity:** 25 (McCabe)
- **Target version:** Python 3.10+

### Ruff Configuration

The project uses comprehensive Ruff linting with specific rule exceptions:

```toml
select = ["ALL"]
ignore = ["ANN", "D401", "E501", "FBT001", "FBT002", ...]
```

See `.ruff.toml` for complete configuration and per-file ignores.

### Docker

- **Linter:** `hadolint` for Dockerfile best practices
- **Test image:** `basnijholt/adaptive-lighting:latest`
- **Multi-arch support:** amd64, arm64

### Pre-commit Hooks

The following hooks are configured (`.pre-commit-config.yaml`):

1. `pre-commit-hooks` v5.0.0 - Large files, trailing whitespace, line endings
2. `ruff-pre-commit` v0.14.6 - Linting with auto-fix
3. `black` 25.1.0 - Code formatting
4. `hadolint-py` - Dockerfile linting
5. `gitleaks` v8.16.3 - Secret detection
6. `rumdl` v0.0.181 - Markdown linting
7. `conventional-precommit-linter` - Commit message format

## Automation Rules

### On Python File Edit (`*.py`)

**Trigger:** `on.edit_file:*.py` OR `on.write:*.py`
**Actions:**

1. Run `ruff check --fix .` for linting
2. Run `ruff format .` for formatting consistency check
3. Consider invoking `/skills run python-ci-skill`

### On Dockerfile Edit

**Trigger:** `on.edit_file:Dockerfile` OR `on.write:Dockerfile`
**Actions:**

1. Run `hadolint Dockerfile` for best practices

### On Home Assistant Config Edit

**Trigger:** `on.edit_file:custom_components/adaptive_lighting/*.py`
**Actions:**

1. Validate against Home Assistant integration patterns
2. Check for proper async handling
3. Consider invoking `/skills run ha-addon-skill --validate-config`

## Development Workflow

### Running Tests

**Option 1: Docker (Recommended for reproducibility)**

```bash
docker run -v $(pwd):/app basnijholt/adaptive-lighting:latest
```

**Option 2: Build Docker image locally**

```bash
docker build -t basnijholt/adaptive-lighting:latest .
```

**Option 3: Pre-commit checks**

```bash
pre-commit run --all-files
```

### Before Committing

1. Run all quality checks (linting, formatting)
2. Ensure tests pass via Docker
3. Update documentation if API/config changes
4. Follow conventional commit format

### CI/CD Expectations

- All Python code must pass `ruff check` with zero errors
- Pre-commit hooks must pass
- Docker test image must build and tests must pass
- Hassfest validation must pass
- HACS validation must pass

## Skills Available

### `/skills run python-ci-skill`

Runs comprehensive Python quality checks:

- Linting (ruff)
- Formatting validation
- Security scan (bandit)
- Generates patch suggestions

### `/skills run ha-addon-skill`

Validates Home Assistant integration compliance:

- manifest.json validation
- Config flow validation
- Services and translations checks

### `/skills run security-scan-skill`

Runs security analysis:

- SAST with semgrep
- Python security with bandit
- Secret detection patterns

### `./.claude/skills/version-management-skill/run.sh`

Manages semantic versioning:

- Validates current version format
- Bumps version (major/minor/patch)
- Updates manifest.json

## Token Efficiency Guidelines

### Use Haiku for Simple Tasks

- File searches, basic linting, formatting
- Simple validation tasks
- Hook execution

### Use Sonnet for Complex Tasks

- Refactoring with business logic changes
- Security remediation
- Architectural decisions

### Use Task Tool for Open-Ended Exploration

When searching for patterns or exploring codebase structure, use:

```text
/task explore "Find all light adaptation logic" --thoroughness medium
```

## Project-Specific Rules

### Core Component Structure

The main component is organized as:

| File | Lines | Purpose |
|------|-------|---------|
| `switch.py` | ~2700 | Main switch entity logic (complexity hotspot) |
| `color_and_brightness.py` | ~500 | Sun position calculations |
| `const.py` | ~450 | Constants and config schema |
| `adaptation_utils.py` | ~230 | Adaptation helpers |
| `config_flow.py` | ~130 | HA config flow UI |
| `__init__.py` | ~100 | Integration setup |

### Light Adaptation Logic

- Use `SunLightSettings` for sun position calculations
- Color temperature ranges: configurable min/max (default 2000K-6500K)
- Brightness ranges: configurable min/max (default 1%-100%)
- Transition times: configurable based on time of day

### Home Assistant Integration Patterns

- Always use `async_add_entities` for entity registration
- Use `async_write_ha_state()` for state updates
- Implement proper `async_will_remove_from_hass()` cleanup
- Follow HA's entity naming conventions
- Use `EntityCategory` for diagnostic entities

### Testing Patterns

- Use `pytest-asyncio` with `asyncio_mode = auto`
- Mock Home Assistant core components appropriately
- Test files mirror source structure in `tests/`

## Dependency Management

### Automated Updates with Renovate

This project uses [Renovate Bot](https://docs.renovatebot.com/) for automated dependency management:

- **Configuration**: `.github/renovate.json`
- **Dashboard**: Maintained as a GitHub issue

### What Gets Updated

- **GitHub Actions**: All workflow action versions
- **Pre-commit hooks**: Tool versions
- **Docker base images**: In CI workflows

### Update Strategy

- **Patch/Minor updates**: Review and merge if CI passes
- **Major updates**: Careful review for breaking changes
- **Security vulnerabilities**: Prioritize immediate fix

## Versioning and Release Workflow

### Semantic Versioning

This project follows [Semantic Versioning 2.0.0](https://semver.org/):

- **Major (X.0.0)**: Breaking changes, incompatible API changes
- **Minor (0.X.0)**: New features, backward compatible additions
- **Patch (0.0.X)**: Bug fixes, backward compatible fixes

### Single Source of Truth

- Version is defined in `custom_components/adaptive_lighting/manifest.json`
- All other references derive from this file

### Release Process

1. **Make Changes**: Implement features/fixes in code
2. **Update Version**: Bump version in `manifest.json`
3. **Update Changelog**: Document changes
4. **Push to GitHub**: CI will validate and build

## Upstream Contribution Guidelines

All changes should be kept clean and upstreamable to `basnijholt/adaptive-lighting`:

- Follow TDD: Red, Green, Refactor
- Work in small, reviewable feature branches
- Write clear commit messages (conventional commits)
- Include tests for new functionality
- Update documentation as needed

## Reference Links

- **Ruff:** <https://docs.astral.sh/ruff/>
- **Hadolint:** <https://github.com/hadolint/hadolint>
- **Home Assistant Integration Dev:** <https://developers.home-assistant.io/docs/creating_integration_manifest>
- **Home Assistant Core:** <https://github.com/home-assistant/core>
- **Adaptive Lighting Docs:** <https://github.com/basnijholt/adaptive-lighting#readme>
- **Semantic Versioning:** <https://semver.org/>
