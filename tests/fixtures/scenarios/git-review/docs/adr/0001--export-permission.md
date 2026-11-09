# Require export permission before size validation

Status: implemented

## Problem

Report size must not be exposed to users lacking export permission.

## Decision

Use `export:read` and check permission before size validation. This is implemented in `src/old_export.py`.

## Alternatives

Checking size first was rejected because its errors reveal report size before permission is established.

## Consequences and risks

Current implementation must retain the ordering. No test result is recorded for this fixture.
