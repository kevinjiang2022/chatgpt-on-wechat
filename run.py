import os
import sys
import subprocess
import shutil


def main():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    run_sh = os.path.join(base_dir, "run.sh")
    if not os.path.isfile(run_sh):
        sys.stderr.write("run.sh not found\n")
        return 1
    bash = shutil.which("bash")
    if not bash:
        sys.stderr.write("bash not found\n")
        return 1
    cmd = [bash, run_sh] + sys.argv[1:]
    return subprocess.call(cmd, cwd=base_dir, env=os.environ.copy())


if __name__ == "__main__":
    raise SystemExit(main())
