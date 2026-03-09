# Refactoring Plan

> **Based on:** CODE_REVIEW_REPORT.md
> **Estimated scope:** 4 phases, ~18 tasks

## Overview

The primary goal is to fix three silent runtime bugs and a broken test suite before any other work. Once tests are green and the bugs are resolved, the plan moves to architecture cleanup (duplicate redirect logic, session reuse), then best-practice alignment (isinstance, wraps, type hints), and finally documentation and polish. This ordering ensures every subsequent change is verified by a working test suite.

---

## Phase 1: Fix Critical Bugs and Restore the Test Suite

*Goal: get to a green, trustworthy test suite that catches regressions*

Before anything else, three runtime bugs and a broken test fixture must be fixed. These are hard to miss once exercised, which means they are also currently undetected — the test suite does not exercise these paths. Fixing the tests first creates the safety net for all subsequent phases.

### Tasks

- [x] **1.1** Fix infinite recursion in `EmVoxel.contour`
  - **What:** Change `return self.contour` to `return self._contour` on models.py:434.
  - **Why:** Every call to `.contour` currently recurses until `RecursionError`. This is a one-character fix.
  - **Files:** `onedep_deposition/models.py`
  - **Done when:** `EmVoxel(spacing={"x":1,"y":1,"z":1}, contour=2.5).contour` returns `2.5`.

- [x] **1.2** Fix `Depositor` crash when depositions list is non-empty
  - **What:** Change `self._depositions.append(**deposition)` to `self._depositions.append(Deposit(**deposition))` on models.py:282.
  - **Why:** `list.append` does not accept keyword arguments; this raises `TypeError` at runtime.
  - **Files:** `onedep_deposition/models.py`
  - **Done when:** Constructing a `Depositor` with a non-empty `depositions` list does not raise.

- [x] **1.3** Fix `DepositedFilesSet` silently discarding warnings
  - **What:** Change the condition on models.py:472 from `if errors else []` to `if warnings else []` for the `_warnings` list comprehension.
  - **Why:** The current code uses the `errors` variable as the guard for warnings, so if `errors` is empty/None, warnings are always thrown away.
  - **Files:** `onedep_deposition/models.py`
  - **Done when:** A `DepositedFilesSet` constructed with `errors=None, warnings=[{"code":"w1","message":"msg"}]` has `len(set.warnings) == 1`.

- [x] **1.4** Fix test fixture to match current `Deposit` model
  - **What:** Add `pdb_id`, `emdb_id`, and `bmrb_id` keys to `deposition_mocked_data` in `test_deposit_api.py:setUp`. Use `"?"` as the placeholder value (consistent with how the API returns unassigned IDs).
  - **Why:** The DAOTHER-9556 refactor added these required fields to `Deposit.__init__` but the test fixture was not updated. Tests that construct `Deposit(**deposition_mocked_data)` raise `TypeError` before any assertion runs.
  - **Files:** `onedep_deposition/tests/test_deposit_api.py`
  - **Done when:** All existing tests pass with `python -m unittest discover`.

- [x] **1.5** Add tests for the three fixed bugs
  - **What:** Add a test for `EmVoxel.contour`, a test for `Depositor` with a populated depositions list, and a test for `DepositedFilesSet` with warnings but no errors.
  - **Why:** These paths were untested, which is why the bugs were not caught. Tests prevent regression.
  - **Files:** `onedep_deposition/tests/test_deposit_api.py` (or a new `test_models.py`)
  - **Done when:** Running the test suite exercises all three fixed code paths without failures.

- [x] **1.6** Fix `import mock` → `from unittest import mock` in `test_rest_adapter.py`
  - **What:** Replace the standalone `mock` package import (Python 2 backport) with the stdlib `unittest.mock`.
  - **Why:** The `mock` package is not installed in the environment; this caused the entire `test_rest_adapter` module to fail to load.
  - **Files:** `onedep_deposition/tests/test_rest_adapter.py`
  - **Done when:** All 23 tests pass with no import errors.

---

## Phase 2: Architecture and Correctness Fixes

*Goal: remove the duplicate redirect logic, fix the hostname setter, and introduce session reuse*

### Tasks

- [ ] **2.1** Remove duplicate redirect handling from `create_deposition`
  - **What:** Remove the `try/except InvalidDepositSiteException` block inside `create_deposition` (deposit_api.py:63–69). The `@handle_invalid_deposit_site` decorator already handles this on the method. The internal handler also means the decorator never fires for `create_deposition`, breaking symmetry with all other methods.
  - **Why:** Two retry paths for the same exception on the same method is confusing and makes the redirect behaviour inconsistent across the class.
  - **Files:** `onedep_deposition/deposit_api.py`
  - **Done when:** `create_deposition` has no internal `try/except InvalidDepositSiteException`, and existing redirect tests (if any) still pass.

- [ ] **2.2** Fix `RestAdapter.hostname` setter to update `self._hostname`
  - **What:** Add `self._hostname = hostname` inside the `hostname` setter (rest_adapter.py:41–47) before the `self.url` update.
  - **Why:** The setter updates `self.url` but not `self._hostname`, so reading `adapter.hostname` after assigning it still returns the old value.
  - **Files:** `onedep_deposition/rest_adapter.py`
  - **Done when:** `adapter.hostname = "http://new-host"` followed by `adapter.hostname` returns `"http://new-host"`.

- [ ] **2.3** Introduce `requests.Session` in `RestAdapter`
  - **What:** Create a `requests.Session` in `RestAdapter.__init__`, set the `Authorization` header on it, and replace the `requests.request(...)` calls in `_do` with `self._session.request(...)`. Pass `verify=self._ssl_verify` to the session or per-request.
  - **Why:** A session reuses TCP connections and TLS sessions across multiple API calls, which is significant for workflows that upload many files.
  - **Files:** `onedep_deposition/rest_adapter.py`
  - **Done when:** Existing tests pass; a new test confirms the session's `Authorization` header is set.

---

## Phase 3: Best Practice Enforcement

*Goal: align with Python idioms and fix type annotation accuracy*

### Tasks

- [ ] **3.1** Replace `type(x) is Y` with `isinstance(x, Y)`
  - **What:** Update all four occurrences:
    - `deposit_api.py:230` — `type(orcid) is str` → `isinstance(orcid, str)`
    - `deposit_api.py:232` — `type(orcid) is list` → `isinstance(orcid, list)`
    - `models.py:59` — `type(exp_type) is ExperimentType` → `isinstance(exp_type, ExperimentType)`
    - `models.py:63` — `type(subtype) is EMSubType` → `isinstance(subtype, EMSubType)`
  - **Why:** `type() is` breaks for subclasses and is non-idiomatic. `isinstance` is the correct tool.
  - **Files:** `onedep_deposition/deposit_api.py`, `onedep_deposition/models.py`
  - **Done when:** No `type(` calls remain in the source; tests pass.

- [ ] **3.2** Add `@functools.wraps` to the `create_api` CLI decorator
  - **What:** Import `functools` in cli.py and add `@functools.wraps(func)` to the inner `decorator` function inside `create_api`.
  - **Why:** Without it, Click cannot read the decorated function's name or docstring for `--help` output.
  - **Files:** `onedep_deposition/cli/cli.py`
  - **Done when:** `onedep-deposition deposition create --help` shows the correct help text.

- [ ] **3.3** Fix `Response.data` type annotation
  - **What:** Change the return type of the `data` property from `List[Dict]` to `Union[Dict, List, None]` (or `Any` as a conservative choice). Update the constructor annotation for the `data` parameter similarly.
  - **Why:** The annotation is actively wrong — callers do dict-style access on it — and will produce false IDE/mypy warnings.
  - **Files:** `onedep_deposition/models.py`
  - **Done when:** No type-checker errors are produced when accessing `response.data["dep_id"]`.

- [ ] **3.4** Scope SSL warning suppression to the specific warning class
  - **What:** Replace `requests.packages.urllib3.disable_warnings()` with `requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)`.
  - **Why:** The current call silences *all* urllib3 warnings globally in the process. The scoped version only suppresses the expected InsecureRequestWarning.
  - **Files:** `onedep_deposition/rest_adapter.py`
  - **Done when:** Only `InsecureRequestWarning` is suppressed when `ssl_verify=False`.

- [ ] **3.5** Add user-facing warning when SSL verification is disabled
  - **What:** In the CLI `create_api` decorator (cli.py:55), add `click.echo("WARNING: SSL verification is disabled.", err=True)` when `no_ssl_verify` is True.
  - **Why:** The flag is easy to leave on accidentally; a visible warning reduces the chance of that happening in production.
  - **Files:** `onedep_deposition/cli/cli.py`
  - **Done when:** Running any command with `--no_ssl_verify` prints the warning to stderr.

- [ ] **3.6** Fix the `test_add_multiple_users` test to actually test multi-user input
  - **What:** Add a separate test case that calls `add_user(dep_id, [orcid1, orcid2])` (list input) and asserts that the POST body sent to the adapter contains both ORCIDs.
  - **Why:** The existing test only verifies response parsing for two items, not that two ORCIDs in the input are correctly serialised.
  - **Files:** `onedep_deposition/tests/test_deposit_api.py`
  - **Done when:** The new test mocks `rest_adapter.post`, calls `add_user` with a list, and asserts `post` was called with `data=[{"orcid": orcid1}, {"orcid": orcid2}]`.

---

## Phase 4: Cleanup and Polish

*Goal: remove stale artifacts, fix documentation, and tidy low-severity issues*

### Tasks

- [ ] **4.1** Update README to use the installed entry point
  - **What:** Replace all occurrences of `python cli.py <command>` in README.md with `onedep-deposition <command>`. Update the example commands accordingly.
  - **Why:** The README is the primary user-facing document; showing a stale invocation immediately frustrates new users.
  - **Files:** `README.md`
  - **Done when:** Every example command in the README uses `onedep-deposition`.

- [ ] **4.2** Remove duplicate file type entries from README
  - **What:** Deduplicate the file type list under "Files" in README.md. `co-cif`, `vo-map`, `img-emdb`, `add-map`, `mask-map`, `half-map`, `xs-cif`, and `xs-mtz` each appear multiple times.
  - **Files:** `README.md`
  - **Done when:** Each file type appears exactly once in the list.

- [ ] **4.3** Clean up stale template artefacts
  - **What:**
    - Fix `tox.ini` `flake_exclude_paths` and `black_exclude_paths` to remove `wwpdb/io/...` paths that don't exist.
    - Fix `RestAdapter.__init__` docstring: replace "Normally, api.thecatapi.com" with a description of the actual parameter.
    - Fix the `deposit_api.py:33` comment: "Default hostname is RCSB" → "Default hostname is wwPDB (`deposit.wwpdb.org`)".
  - **Files:** `tox.ini`, `rest_adapter.py`, `deposit_api.py`
  - **Done when:** No stale references to unrelated projects or services remain.

- [ ] **4.4** Align `requires-python` with tested versions
  - **What:** Update `pyproject.toml` to set `requires-python = ">=3.9"` (matching the minimum in the tox matrix) or expand the tox matrix to actually test 3.6–3.8.
  - **Why:** Claiming 3.6 support that is never tested is a false promise.
  - **Files:** `pyproject.toml`, `tox.ini`
  - **Done when:** The stated minimum Python version matches the lowest version in the test matrix.

- [ ] **4.5** Remove the no-op `tearDown` method from tests
  - **What:** Delete the `tearDown(self): pass` method in `DepositApiTests`.
  - **Files:** `onedep_deposition/tests/test_deposit_api.py`
  - **Done when:** The method is gone; tests still pass.

---

## Dependency Map

- Phase 2 requires Phase 1 (tests must be green before structural changes)
- Phase 3 requires Phase 1 (tests must be green before best-practice changes)
- Task 3.6 requires Task 1.4 (fixture must be correct before adding more tests)
- Phase 4 is independent of Phases 2 and 3 (documentation/cleanup can run in parallel)

---

## Definition of Done

The refactoring is complete when:
- [ ] All tests pass with `python -m unittest discover`
- [ ] `tox -e py310` passes (unit tests, flake8, pylint, black, coverage)
- [ ] Coverage remains at or above the 70% threshold
- [ ] All 🔴 and 🟠 findings from `CODE_REVIEW_REPORT.md` are resolved
- [ ] No `type() is` patterns remain in the source
- [ ] A CHANGELOG entry or PR description summarises what was changed and why
