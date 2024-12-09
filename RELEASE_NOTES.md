# 0.2.2

- Fixed a bug where if the Blobstore returned an non-json response, logging the response would
  fail due to attempting to concatenate string and binary types. This would shadow the real
  error returned from the Blobstore.

# 0.2.1

- fixed several bugs regarding downloading files from Google Drive. How long the current method
  will continue to work is unknown.
- updates python to 3.8.10 by updating the base image.

# 0.2.0
- added `unpack_files` function

# 0.1.4
- objects saved to the workspace are now sorted prior to serialization. This prevents errors due
  to workspace sort memory limits, and also moves the sort compute load (which is the most
  expensive part of saving objects) from the workspace server node to the SDK job nodes.
- Clean up the way filenames are fetched from a URL, using either the URL itself or a header
- Limit filename length to at most 255 characters to prevent filesystem errors

# 0.1.3
- tidying for github consistency
- Added Actions workflow for KB SDK tests
- Added Dependabot and LGTM configurations
- Updated `README.md` to include standard build, coverage, and LGTM badging.

# 0.1.2
- deprecate handle service with handle service 2
- replace the colon(:) [that was reported to have caused download error for Windows users] with
  underscore in shock filenames

# 0.1.1
- close no longer used sockets.

# 0.1.0
- shock attributes are now ignored on upload. In a future release they will be removed altogether
  and specifying attributes for upload will be an error.
- shock indexes and attributes are no longer copied during a copy or ownership operation.
