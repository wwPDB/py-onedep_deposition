# Code Review Report

> **Repository:** py-onedep_deposition
> **Reviewed:** 2026-03-06
> **Severity legend:** 🔴 Critical · 🟠 High · 🟡 Medium · 🔵 Low · ℹ️ Info

## Executive Summary

`py-onedep_deposition` is a Python client library and CLI for the wwPDB OneDep deposition REST API. It allows researchers to programmatically create structural biology depositions (X-ray, EM, NMR, etc.), manage files, and trigger processing. The architecture is clean and well-layered — CLI → DepositApi → RestAdapter — and the intent of each module is clear.

The codebase has three silent bugs in `models.py` that will crash at runtime: an infinite-recursion property, a `list.append(**kwargs)` call, and a copy-paste condition that silently discards warnings. More urgently, the test suite is broken because a recent refactor of `Deposit.__init__` (adding `pdb_id`/`emdb_id`/`bmrb_id`) was not reflected in the shared test fixture, so several tests fail with `TypeError` before any assertion runs. Fixing these bugs and restoring the test suite should be the immediate priority before any further development.

Beyond the bugs, the codebase shows some inconsistency introduced during growth: duplicate redirect logic (inside `create_deposition` *and* in the decorator), inconsistent use of `isinstance` vs `type() is`, and a globally disabled SSL warning that affects the entire process. None of these are blocking, but they should be addressed to improve reliability and correctness.

---

## 1. Architecture & Design

The three-layer design (CLI / API / HTTP adapter) is sound. The `DepositApi` class provides a clean facade over the REST adapter, and the experiment-type-specific convenience methods (`create_em_deposition`, `create_xray_deposition`, etc.) are a good usability addition. The `models.py` data-class hierarchy covers the domain well.

**[🟠 High] Duplicate and conflicting redirect logic** — `create_deposition` catches `InvalidDepositSiteException` internally and retries (deposit_api.py:65–68), while the `@handle_invalid_deposit_site` decorator also catches the same exception on any decorated method (decorators.py:10–14). On `create_deposition` itself this means the decorator wrapper never sees the exception (it's swallowed inside). On all other methods only the decorator runs. This asymmetry makes the redirect behaviour inconsistent and confusing. The internal try/except in `create_deposition` should be removed in favour of relying solely on the decorator.

**[🟡 Medium] `DepositApi.__init__` hostname initialisation is confusing** — `self._hostname` is set to `None` on line 25, then a local variable `hostname` is updated to the default on line 34, but `self._hostname` is only updated inside `_connect`. Callers reading `self._hostname` before `_connect` is called would see `None`. The intent is correct but the indirection is hard to follow. (deposit_api.py:25–36)

**[🔵 Low] `_connect` is a public-ish method with an inconsistent contract** — it sets `self._hostname` only if the argument is truthy, but callers always pass a non-None value. The guard `if hostname:` inside `_connect` is dead code. (rest_adapter.py:39–41)

---

## 2. Performance

The HTTP layer creates a raw `requests.request()` call for every operation, which means a new TCP connection and TLS handshake per API call. For workflows that involve multiple operations in sequence (e.g. upload several files, then process), this is wasteful.

**[🟡 Medium] No `requests.Session` reuse** — Using a `requests.Session` would reuse persistent TCP connections and allow shared headers (e.g. `Authorization`) to be set once. (rest_adapter.py:71–75)

**[🔵 Low] O(n) file delete on overwrite** — `upload_file` with `overwrite=True` fetches all files and deletes each matching one in a separate HTTP call (deposit_api.py:282–285). For depositions with many files this multiplies requests. The API may not support bulk delete, but the behaviour is worth documenting.

---

## 3. Software Engineering Best Practices

**[🔴 Critical] Infinite recursion in `EmVoxel.contour` property** — The property returns `self.contour` (calls itself) instead of `self._contour`. Any access to `EmVoxel.contour` will raise `RecursionError`. (models.py:434)

**[🔴 Critical] `Depositor` crashes when depositions list is non-empty** — `self._depositions.append(**deposition)` is not valid Python; `list.append` takes a single positional argument. This will raise `TypeError` for any `Depositor` returned with a non-empty `depositions` list. (models.py:282)

**[🔴 Critical] `DepositedFilesSet` warnings always silently empty** — The list comprehension for `_warnings` checks `if errors` instead of `if warnings` as its condition: `... if errors else []`. If `errors` is empty or `None`, warnings are always thrown away regardless of their content. (models.py:472)

**[🟡 Medium] `type(x) is Y` instead of `isinstance`** — Used in deposit_api.py:230,232 and models.py:59,63. This breaks for subclasses and is not idiomatic Python. Should be `isinstance(x, FileType)`, `isinstance(x, str)`, etc.

**[🟡 Medium] `create_api` CLI decorator missing `@functools.wraps`** — The decorator in cli.py:42–66 replaces `__name__`, `__doc__`, and `__wrapped__` on the decorated functions. Click relies on these for help text and introspection. The `--help` output for commands using this decorator may be incorrect or misleading.

**[🟡 Medium] `Response._data` type annotation is incorrect** — The type hint says `List[Dict]` but the property actually holds whatever the JSON response root is — a `dict` for single objects, a `list` for collections, or `[]` for 204 responses. Callers access `.data["dep_id"]` (dict access) and `.data["items"]` in different places, relying on the actual runtime type. The annotation misleads IDEs and type checkers. (models.py:29)

**[🔵 Low] `**kwargs` absorbed in CLI-facing API methods to accept CLI context** — Methods like `create_xray_deposition(... **kwargs)` absorb Click's `ctx` context dictionary silently. This is a leaky abstraction; the CLI layer should unpack its own arguments rather than passing raw context through to the library API.

---

## 4. Overengineering & Technical Debt

The code is generally not over-engineered. The layering is appropriate and the models map cleanly to the domain.

**[🟡 Medium] Seven nearly-identical deposition-type methods** — `create_xray_deposition`, `create_fiber_deposition`, `create_neutron_deposition`, etc. each contain one `Experiment(...)` construction and one `create_deposition(...)` call. The only differences are the `exp_type` string and which optional parameters are forwarded. If a new experiment type is added or the signature of `create_deposition` changes, all seven methods must be updated. A table-driven or factory approach would reduce maintenance cost. (deposit_api.py:75–178)

**[🔵 Low] `tox.ini` contains leftover paths from a project template** — `flake_exclude_paths` and `black_exclude_paths` reference `wwpdb/io/...` paths that do not exist in this repository. These silently do nothing but add noise. (tox.ini:25–28)

**[🔵 Low] `RestAdapter` constructor docstring is from a copy-paste template** — The `:param hostname:` description reads "Normally, api.thecatapi.com". (rest_adapter.py:13)

**[🔵 Low] Wrong comment on default hostname** — "Default hostname is RCSB until a deposition is created" is incorrect; the default is `deposit.wwpdb.org` (wwPDB), not RCSB. (deposit_api.py:33)

---

## 5. Security

**[🟠 High] Global SSL warning suppression** — `requests.packages.urllib3.disable_warnings()` is called unconditionally when `ssl_verify=False` (rest_adapter.py:30). This silences TLS warnings for the entire process, including any other libraries in the same runtime that legitimately need those warnings. The call should at minimum be scoped to the specific `urllib3` context or use `urllib3.exceptions.InsecureRequestWarning` selectively.

**[🟡 Medium] SSL verification flag accepts user input without guard** — The CLI exposes `--no_ssl_verify` which sets `ssl_verify=False`, disabling all certificate validation. There is no warning printed to the user when this flag is used. In a shared or scripted context this is easy to accidentally leave on. The CLI should print a warning to stderr when SSL verification is disabled.

**[🔵 Low] API key stored in plaintext file** — The design intentionally stores the JWT in `~/onedepapi.jwt`. The README documents this. The file's permissions are not verified or enforced by the code, so a world-readable file would silently expose the key. Consider checking and warning if file permissions are too permissive. (cli.py:15–16)

---

## 6. Testability & Test Quality

**[🔴 Critical] Test fixture incompatible with current `Deposit` model** — `deposition_mocked_data` in test setUp does not include `pdb_id`, `emdb_id`, or `bmrb_id`, which are required positional arguments in `Deposit.__init__` after the DAOTHER-9556 refactor. `test_create_each_method_deposition_success` constructs `Deposit(**self.deposition_mocked_data)` directly and will raise `TypeError`. Several other tests that trigger `Deposit` construction through a mocked `rest_adapter.get` with this same fixture will also fail. (test_deposit_api.py:88–96)

**[🟠 High] No tests for the CLI layer** — `cli.py` contains significant logic: API key loading, input validation (email regex, ORCID regex, EMDB/BMRB format), experiment type dispatch, and `--copy-all` flag handling. None of this is tested. A broken CLI would not be caught by the test suite.

**[🟠 High] Bugs in `models.py` have no test coverage** — The three critical bugs identified in section 3 (`EmVoxel.contour`, `Depositor.depositions`, `DepositedFilesSet.warnings`) have no tests that exercise the affected code paths. This is why they survived undetected.

**[🟡 Medium] `test_add_multiple_users` does not actually test the multiple-user path** — The test calls `add_user(dep_id, orcids[0])` with a single ORCID but mocks the response to return two users. It tests that the response parsing works for two items, but does not test that `add_user` correctly builds the payload for a list input. (test_deposit_api.py:136–148)

**[🟡 Medium] Test subclass `MyDepositApi` exposes internals** — The `MyDepositApi` test helper exposes `self._rest_adapter` as `self.rest_adapter` to allow mocking. While functional, this creates a fragile coupling to the private implementation. Using `unittest.mock.patch` on `RestAdapter._do` would be cleaner.

**[🔵 Low] `tearDown` is a no-op** — `tearDown(self): pass` adds noise without value. (test_deposit_api.py:205–207)

---

## 7. Observability & Operability

The `RestAdapter._do` method logs pre/post request information at DEBUG level, which is useful for development. There is no structured logging or request-ID propagation.

**[🟡 Medium] Log line format is string-built, not structured** — `log_line_pre` and `log_line_post` are plain concatenated strings. Using `extra={}` with the logger or a structured log library would make log aggregation much easier in production. (rest_adapter.py:66–67)

**[🔵 Low] No indication to the user when a site redirect occurs** — When the API redirects the client to a different deposit site, it happens silently. A log message at INFO level (not just DEBUG) would help users understand why their connection switched hosts.

---

## 8. Documentation & Developer Experience

**[🟡 Medium] README `cli.py` invocation is stale** — The README shows `python cli.py <command>` throughout, but the package is now installed as the `onedep-deposition` entry point (per pyproject.toml:28). New users following the README will get a `ModuleNotFoundError` or run the wrong file.

**[🟡 Medium] README file type list has many duplicate entries** — The allowed file types listed under "Files" repeat `co-cif`, `vo-map`, `img-emdb`, `add-map`, `mask-map`, `half-map`, `xs-cif`, and `xs-mtz` two or three times each. (README.md:57–99)

**[🔵 Low] `pyproject.toml` keeps `requires-python = ">=3.6"` but tox only tests py310** — The declared minimum is 3.6 but there is no CI evidence it actually works on 3.6–3.9. The minimum should match what is actually tested and supported, or the tox matrix should be expanded.

**[🔵 Low] `DepositStatus` class has no docstring** — All other model classes have at least a short class-level docstring; `DepositStatus` has none. (models.py:511)

---

## Summary Table

| # | Issue | Dimension | Severity | File(s) |
|---|-------|-----------|----------|---------|
| 1 | `EmVoxel.contour` property returns `self.contour` (infinite recursion) | Best Practices | 🔴 | models.py:434 |
| 2 | `Depositor._depositions.append(**deposition)` crashes at runtime | Best Practices | 🔴 | models.py:282 |
| 3 | `DepositedFilesSet` warnings silently discarded due to wrong condition | Best Practices | 🔴 | models.py:472 |
| 4 | Test fixture missing `pdb_id`/`emdb_id`/`bmrb_id` — tests fail with TypeError | Test Quality | 🔴 | test_deposit_api.py:30–42 |
| 5 | Duplicate/conflicting redirect logic in `create_deposition` + decorator | Architecture | 🟠 | deposit_api.py:65–69, decorators.py |
| 6 | Global SSL warning suppression affects entire process | Security | 🟠 | rest_adapter.py:30 |
| 7 | No tests for CLI layer | Test Quality | 🟠 | cli/cli.py |
| 8 | No test coverage for three critical model bugs | Test Quality | 🟠 | models.py |
| 9 | No `requests.Session` — new TCP connection per call | Performance | 🟡 | rest_adapter.py:71–75 |
| 10 | `type(x) is Y` instead of `isinstance` | Best Practices | 🟡 | deposit_api.py:230,232; models.py:59,63 |
| 11 | `create_api` decorator missing `@functools.wraps` | Best Practices | 🟡 | cli/cli.py:42 |
| 12 | `Response._data` type annotation is wrong | Best Practices | 🟡 | models.py:29 |
| 13 | No SSL-disabled warning printed to user | Security | 🟡 | cli/cli.py:55 |
| 14 | `test_add_multiple_users` doesn't test multi-user payload | Test Quality | 🟡 | test_deposit_api.py:136 |
| 15 | README shows stale `python cli.py` invocation | Documentation | 🟡 | README.md |
| 16 | README file type list has many duplicates | Documentation | 🟡 | README.md:57–99 |
| 17 | Seven near-identical deposition-type methods | Tech Debt | 🟡 | deposit_api.py:75–178 |
| 18 | Log messages are plain strings, not structured | Observability | 🟡 | rest_adapter.py:66 |
| 19 | `hostname` setter in `RestAdapter` doesn't update `self._hostname` | Best Practices | 🔵 | rest_adapter.py:41–47 |
| 20 | `tox.ini` has leftover template paths for `wwpdb/io/...` | Tech Debt | 🔵 | tox.ini:25–28 |
| 21 | RestAdapter docstring mentions "thecatapi.com" | Documentation | 🔵 | rest_adapter.py:13 |
| 22 | Wrong comment: "Default hostname is RCSB" (is actually wwPDB) | Documentation | 🔵 | deposit_api.py:33 |
| 23 | `requires-python = ">=3.6"` not validated in CI | Documentation | 🔵 | pyproject.toml:12 |

---

## What's working well

- **Clean three-layer architecture.** The separation of CLI / DepositApi / RestAdapter is well thought-out and easy to navigate. Each layer has a single responsibility.
- **Experiment-type convenience methods.** The `create_em_deposition`, `create_nmr_deposition`, etc. wrappers give users a discoverable, type-safe API for the most common workflows without exposing the complexity of `Experiment` objects.
- **Solid HTTP error handling in `RestAdapter._do`.** The method distinguishes request exceptions, non-2xx responses, bad JSON, and the domain-specific `invalid_location` redirect case — all handled explicitly with typed exceptions and meaningful messages.
- **Good use of enumerations.** The `Country`, `FileType`, `ExperimentType`, and `EMSubType` enums make the API self-documenting and prevent invalid string values from reaching the server.
- **Test coverage for the happy and error paths of the core API.** `test_deposit_api.py` covers creation, retrieval, user management, file upload, and processing flows. The structure is clear and maintainable once the fixture is fixed.
- **tox CI setup.** The presence of flake8, pylint, black, and coverage in tox shows a commitment to code quality tooling.
