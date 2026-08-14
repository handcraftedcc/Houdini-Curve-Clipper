# CurveClipper

CurveClipper is a Houdini package containing curve boolean and offset HDAs. It
uses the native [`pyclipr`](https://github.com/drlukeparry/pyclipr) bindings for
Clipper2.

## Included Python builds

- `python3.11libs/pyclipr` is the Python 3.11 Windows x64 package used by
  Houdini 21.
- `python3.13libs/pyclipr` is the Python 3.13 Windows x64 package used by
  Houdini 22.

Both verified packages use `pyclipr` 0.1.8 and Clipper 2.0.1, built for their
respective CPython ABIs. They support `JoinType.Bevel` and the
`ClipperOffset.arcTolerance`, `miterLimit`, and `preserveCollinear` setters.

Do not substitute the `pyclipr2` 0.1.9 Windows wheel. Its CPython 3.13 build
was found to omit `JoinType.Bevel`, and its `ClipperOffset` property setters
reject valid values.

## Install the Houdini package

Edit `CurveClipper.json` and replace `PATH/TO/PACKAGE/CurveClipper` with the
absolute path to this directory. Copy the JSON file into your Houdini packages
directory, normally:

```text
%USERPROFILE%\Documents\houdini22.0\packages
```

Restart Houdini after changing a native `.pyd` file. Windows keeps imported
Python extensions locked while Houdini is running.

## Build pyclipr for Python 3.13 on Windows

### Requirements

- Houdini 22 with its bundled Python 3.13 installation.
- Visual Studio 2022 Build Tools with **Desktop development with C++** and a
  Windows SDK.
- Git.
- CMake newer than 3.15.
- A C++17-capable compiler.

Run the following from an **x64 Native Tools Command Prompt for VS 2022** or a
PowerShell session initialized with the Visual Studio developer environment.
Adjust the Houdini build number and package path as needed:

```powershell
$HoudiniRoot = "C:\Program Files\Side Effects Software\Houdini 22.0.368"
$Python = "$HoudiniRoot\python313\python.exe"
$PackageRoot = "C:\path\to\CurveClipper"

& $Python -m pip install --upgrade build cmake ninja

git clone --recursive https://github.com/drlukeparry/pyclipr.git
Set-Location .\pyclipr
git submodule update --init --recursive
```

For an exact reproduction, use the source associated with the `pyclipr` 0.1.8
release rather than a later `main` branch revision.

### Expose the Bevel enum

Clipper2 contains the Bevel join at enum value `1`, but pyclipr 0.1.8 does not
publish its Python name. Before building, edit
`python/pyclipr/module.cpp`. Find the `JoinType` binding and add the Bevel line:

```cpp
py::enum_<Clipper2Lib::JoinType>(
    m, "JoinType", py::arithmetic(),
    "The join type to be used for the offsetting / inflation of paths")
    .value("Square", Clipper2Lib::JoinType::Square, "Square join type")
    .value("Bevel",  Clipper2Lib::JoinType::Bevel,  "Bevel join type")
    .value("Round",  Clipper2Lib::JoinType::Round,  "Round join type")
    .value("Miter",  Clipper2Lib::JoinType::Miter,  "Miter join type");
```

This binds the real native Bevel implementation; it does not alias Bevel to
Square.

### Build the wheel

```powershell
& $Python -m build --wheel
```

The result should be similar to:

```text
dist\pyclipr-0.1.8-cp313-cp313-win_amd64.whl
```

The `cp313` and `win_amd64` tags are important. A wheel built for another
Python ABI or architecture will not load in Houdini's Python 3.13 runtime.

### Stage and install the wheel

Close every Houdini process before replacing the extension. Installing into a
staging directory makes it easy to verify the wheel before copying it into the
package:

```powershell
$Stage = Join-Path $PWD "wheel-stage"
New-Item -ItemType Directory -Force $Stage | Out-Null

& $Python -m pip install --no-deps --target $Stage `
    .\dist\pyclipr-0.1.8-cp313-cp313-win_amd64.whl

$Destination = Join-Path $PackageRoot "python3.13libs\pyclipr"
if (Test-Path $Destination) {
    Rename-Item $Destination "pyclipr.backup"
}
Copy-Item -Recurse (Join-Path $Stage "pyclipr") $Destination
```

Once the new package has passed the test below, the backup and staging folder
can be removed.

## Verification

With Houdini closed, run this smoke test using Houdini's bundled interpreter:

```powershell
$env:PYTHONPATH = "$PackageRoot\python3.13libs"

& $Python -c @'
import numpy as np
import pyclipr

assert pyclipr.JoinType.Bevel == pyclipr.JoinType(1)

offsetter = pyclipr.ClipperOffset()
offsetter.scaleFactor = 100
offsetter.arcTolerance = 0.0
offsetter.miterLimit = 2.0
offsetter.preserveCollinear = True

path = np.array([[0.0, 0.0], [10.0, 0.0], [14.0, 10.0], [0.0, 10.0]])
offsetter.addPaths(
    [path],
    pyclipr.JoinType.Bevel,
    pyclipr.EndType.Round,
)

result = offsetter.execute(5.0)
assert result

print("pyclipr:", pyclipr.__version__)
print("Clipper:", pyclipr.clipperVersion)
print("Bevel and ClipperOffset property test passed")
'@
```

Expected versions for the package currently included here:

```text
pyclipr: 0.1.8
Clipper: 2.0.1
```

If `JoinType.Bevel` is missing, confirm that the C++ binding change was made
before building. If a property assignment reports an incompatible
`Clipper2Lib::ClipperOffset` argument, confirm that the installed distribution
is `pyclipr`, not `pyclipr2`.

## License

CurveClipper's original project content is available under the Boost Software
License 1.0 (`BSL-1.0`). See [LICENSE](LICENSE).

The bundled native `pyclipr` extensions incorporate third-party software under
BSL-1.0, BSD-3-Clause, MPL-2.0, and compatible licenses. Those components remain
under their own licenses. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
and [THIRD_PARTY_LICENSES](THIRD_PARTY_LICENSES) for attribution, complete
license texts, and corresponding-source information.

## AI Disclaimer

AI-assisted tools were used during development for code investigation,
compatibility work, documentation, and testing support. AI-generated or
AI-suggested material was reviewed and tested by the project maintainer before
inclusion. AI assistance does not change the ownership or licensing of this
project or its third-party components, and it does not provide any warranty of
correctness, fitness, security, or legal compliance. Human contributors remain
responsible for the final contents and should independently validate the tool
for production use.
