# Fortran Mission Lab

Two actual Fortran programs calculate a five-day flight at a fixed 24,000 km/h.
`mission.f90` uses modern free-form Fortran; `mission77.f` preserves fixed-format
columns and labeled jumps. Both must reach 2,880,000 km on day five.

## Results dashboard

https://ekim5sg.github.io/fortran-mission-lab/

The mobile-friendly dashboard displays actual output from the latest successful
GitHub build. Its day slider explores saved results, rather than executing Fortran
in the browser. Raw reports, source files, compiler details, validation log, and
JSON results are downloadable. The page includes its build time, commit, and run.

### One-time Pages setup

Open repository **Settings → Pages → Build and deployment → Source**, select
**GitHub Actions**, then rerun the workflow if its publishing job previously failed.
No secrets, personal access tokens, Hostek configuration, or local compiler needed.

## Run again

Open **Actions → Fortran Mission - Compile and Run → Run workflow**, choose `main`,
and run it. Pushes to main also build and publish automatically. Pull requests
compile, validate, and generate a dashboard preview without publishing it.

The run summary shows both reports. Artifacts include `fortran-mission-linux-results`
(Linux executables, compiler version, raw reports, and verification results) and
`fortran-mission-dashboard` (the complete static dashboard). Publication runs only
after compilation, execution, validation, and dashboard generation succeed.

## Run locally

With GNU Fortran and Python 3 installed:

```sh
mkdir -p results
gfortran --version > results/compiler.txt
gfortran -std=f2008 -Wall -Wextra -fcheck=all mission.f90 -o results/mission-modern
gfortran -std=legacy -Wall -Wextra -fcheck=all mission77.f -o results/mission77
./results/mission-modern > results/modern-output.txt
./results/mission77 > results/fortran77-output.txt
python3 verify_outputs.py results/modern-output.txt results/fortran77-output.txt > results/verification.txt
python3 build_dashboard.py
python3 -m http.server --directory _site 8000
```

Open http://localhost:8000/ to view the generated page. The executables target your
build machine, not iOS or browsers. Constant-speed model only: no orbital mechanics.

Michael Givens / MikeGyver Studio
