1. Files created
All changes are confined to pilot-output/:

order_webhook.py — typed, framework-independent validator and normalizer.
test_order_webhook.py — 17 focused standard-library tests.
README.md — usage, behavior, boundaries, and documentation scope.
2. Implementation summary
validate_order_webhook validates the supplied order and returns a typed dictionary containing only the specified order and item fields. Invalid input raises ValueError. The implementation uses Python’s standard library only and makes no network, database, authentication, logging, or persistence calls.

3. Validation and normalization
It trims order IDs and SKUs; trims and lowercases email; enforces the stated basic email shape and three uppercase ASCII currency letters; requires a non-empty list of item mappings; and rejects missing fields, boolean or non-positive quantities, and unsupported or invalid prices. Prices become finite, non-negative Decimal values; floats are parsed through str(value), with no rounding or quantization.

4. Tests created
Coverage includes valid normalization and supported price types; missing order and item fields; malformed email and currency; non-mapping inputs/items; empty or invalid item collections; blank identifiers; boolean, zero, negative, and non-integer quantities; and boolean, unsupported, negative, malformed, and non-finite prices.

5. Exact commands and results
Final test command:
python -m unittest discover -s pilot-output -p test_order_webhook.py

Actual output:
.................
----------------------------------------------------------------------
Ran 17 tests in 0.005s

OK

Syntax check:
python -m compileall -q pilot-output

Completed with exit code 0 and no output.

The test-first run, before the implementation existed, failed at import with ModuleNotFoundError: No module named 'order_webhook' (1 test-loader error), as expected for the missing module.

6. Unrun checks and limitations
The full repository suite, linting, and static type checking were not run. No integration checks were applicable to this standalone validator. Canonical project documentation, Obsidian notes, Graphify data, and the central HTML report were not updated, per the constraint not to modify canonical repository files.

7. Decisions and assumptions
The scenario does not prescribe a result model, so the normalized structure is a typed dictionary. Email validation follows only the stated basic rule; it is not RFC validation and does not establish mailbox existence. No packages were installed, and the final worktree contains only the three pilot-output/ artifacts.