# Fortran Mission Lab

Two actual Fortran programs calculate a five-day flight at a fixed 24,000 km/h.
`mission.f90` uses modern free-form Fortran; `mission77.f` preserves fixed-format
columns and labeled jumps. Both must reach 2,880,000 km on day five.

In GitHub, open **Actions → Fortran Mission - Compile and Run → Run workflow**.
The workflow also runs automatically on pushes to main, and checks pull requests. See the run summary for both reports.
Download `fortran-mission-linux-results` for the executables, compiler version,
raw reports, and validation result. Executables target Linux, not iOS or browsers.

For a local machine with GNU Fortran and Python 3:

```sh
mkdir -p results
gfortran -std=f2008 -Wall -Wextra -fcheck=all mission.f90 -o results/mission-modern
gfortran -std=legacy -Wall -Wextra -fcheck=all mission77.f -o results/mission77
./results/mission-modern > results/modern-output.txt
./results/mission77 > results/fortran77-output.txt
python3 verify_outputs.py results/modern-output.txt results/fortran77-output.txt
```

The verifier checks both real outputs against all five expected distances. It
allows differences in field spacing and Fortran's trailing decimal point.

## Run it again

Open Actions, select **Fortran Mission - Compile and Run**, choose **Run workflow**, and run it on `main`. No secrets, local compiler, or Hostek configuration are required.
