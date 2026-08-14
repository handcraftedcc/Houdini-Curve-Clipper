# Third-Party Notices

CurveClipper bundles native Python extension modules derived from `pyclipr` and
statically compiled with several open-source C++ libraries. CurveClipper's own
license does not replace the licenses listed here.

This notice is intended to accompany every source or binary distribution of
CurveClipper. Complete license texts are in `THIRD_PARTY_LICENSES/`.

## Component inventory

### pyclipr bindings

- Project: `pyclipr`
- Copyright/attribution: Luke Parry, Luktug, and contributors
- License: Boost Software License 1.0 (`BSL-1.0`)
- Used in: `python3.11libs/pyclipr` and `python3.13libs/pyclipr`
- Upstream: <https://github.com/drlukeparry/pyclipr>
- License text: `THIRD_PARTY_LICENSES/pyclipr-and-Clipper2-BSL-1.0.txt`

Both the Python 3.11 and Python 3.13 packages are based on the official
`pyclipr` 0.1.8 Windows wheels. Their exact upstream source archive is
available at:

<https://files.pythonhosted.org/packages/e3/96/c8049cfb9166c1f50d878535f2d1cdae1303e994dea7783a3f9075aa0679/pyclipr-0.1.8.tar.gz>

SHA-256: `ff8360330f827dc4801a57cd18d3bc925814b6a9a05f14be1e0f8f72cc27488f`

The unmodified upstream CPython 3.11 wheel has SHA-256
`c453c85664245beb94e1b2bf49f441faa640da73832a59cfa6a6fbd340e3d890`.
The unmodified upstream CPython 3.13 wheel has SHA-256
`9ae1c856116fc3b46546f724ca20b1145f085b7bb09d2e743260db59615c2fcb`.
The `.pyd` files in this repository come directly from those wheels.

Both packages register Clipper2's existing native `Bevel` enum value in their
respective `pyclipr/__init__.py` files; the native binaries are unmodified.

### Clipper2

- Copyright: Angus Johnson, 2010-2025, and contributors
- License: Boost Software License 1.0 (`BSL-1.0`)
- Version used: 2.0.1 by both Python builds
- Upstream: <https://github.com/AngusJohnson/Clipper2>
- License text: `THIRD_PARTY_LICENSES/pyclipr-and-Clipper2-BSL-1.0.txt`

Clipper2 is compiled into the `.pyd` extension modules. Its corresponding
source is included in the pyclipr source archive linked above and is also
available from the upstream release tag `Clipper2_2.0.1`.

### Eigen

- Copyright: Eigen authors and contributors; individual source files contain
  their applicable notices
- Primary license: Mozilla Public License 2.0 (`MPL-2.0`)
- Version used: 5.0.1 by both Python builds
- Upstream: <https://gitlab.com/libeigen/eigen>
- License texts: `THIRD_PARTY_LICENSES/Eigen-5.0.1/`

Eigen is a header-only library and portions are incorporated into the native
extension modules. In accordance with MPL-2.0 section 3.2, the corresponding
Eigen Source Code Form is available in the exact pyclipr source archive linked
above. Recipients may modify and redistribute that Eigen source under its
applicable licenses. No modifications were made to the Eigen sources for these
builds.

Eigen describes itself as primarily MPL-2.0 and contains some files under
other compatible licenses. The copied `COPYING.*` files preserve the notices
shipped with each version. The binding includes Eigen's standard `Eigen/Eigen`
headers; no Eigen LGPL-only unsupported module is intentionally used.

### pybind11

- Copyright (c) 2016 Wenzel Jakob and contributors
- License: BSD 3-Clause (`BSD-3-Clause`)
- Version used: 3.0.1 by both Python builds
- Upstream: <https://github.com/pybind/pybind11>
- License text: `THIRD_PARTY_LICENSES/pybind11-BSD-3-Clause.txt`

The BSD copyright notice, conditions, and disclaimer are reproduced in the
license file as required for binary redistribution.

## Runtime dependency

`pyclipr` imports NumPy at runtime. NumPy is supplied by the user's Houdini or
Python environment and is not copied into this repository. Its license and
notices accompany that separate installation.

## Distribution checklist

When redistributing CurveClipper:

1. Keep the top-level `LICENSE`, this notice, and `THIRD_PARTY_LICENSES/` with
   the package.
2. Keep existing copyright and license notices in source files and Python
   package metadata.
3. Keep the corresponding-source links and version information above current
   whenever either native extension is rebuilt.
4. If Eigen itself is modified, publish the modified Eigen source files under
   MPL-2.0 and clearly document how recipients can obtain them.
5. Do not use upstream project names or contributor names to imply endorsement.

This file is a good-faith compliance record, not legal advice. A qualified
attorney should review licensing before commercial distribution if the
project's provenance or build inputs change.
