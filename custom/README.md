# Custom Spack Configuration Scopes

## Overview

This section of `spack-config` is unique - it is not the base configuration that we symlink in our spack instances (like `vX.X/gadi` or `common/ci-runner`). It is custom configuration scopes outside of the base spack configuration used for different purposes.

For example, we may have custom, environment-level `spack.config.install_tree`s for certain manifests that are restricted for use, and to clean up those `install_trees` we need that same configuration information as a custom scope.

## Custom Scopes

### UKMO Restricted Scope

This scope is used for packages that are under a UKMO license agreement. They have a separate `install_tree` that is locked down via ACLs to only authorised users, separate from the base `install_tree`.
