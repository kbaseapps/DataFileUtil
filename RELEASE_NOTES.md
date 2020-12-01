#0.1.3
- tidying for github consistency
- Added Actions workflow for KB SDK tests
- Added Dependabot and LGTM configurations
- Updated `README.md` to include standard build, coverage, and LGTM badging.

#0.1.2
- deprecate handle service with handle service 2

#0.1.1
- close no longer used sockets.
- replace the colon(:) [that was reported to have caused download error for Windows users] with underscore in shock filenames

#0.1.0
- shock attributes are now ignored on upload. In a future release they will be removed altogether
  and specifying attributes for upload will be an error.
- shock indexes and attributes are no longer copied during a copy or ownership operation.
