import sys, os
import importlib
import flake8.api.legacy
from io import StringIO
import re

class Errors:
    F402 = "F402"
    F403 = "F403"
    F404 = "F404"
    F405 = "F405"
    F406 = "F406"
    F407 = "F407"
    F8 = "F8"
    F901 = "F901"
    E999 = "E999"

    supported = [F402, F403, F404, F405, F406, F407, F8, F901, E999]
    msg = {
            F403: "Package not installed or is unavailable.",
            F405: "{} is undefined."
        }

get_error = re.compile("[FE]\d{1,3}")
get_loc = re.compile("\w+.py:\d+:\d+:")

def get_lint(file):
    # Temporarily redirect stdout to the lintstdout variable to get flake8 output
    oldstdout = sys.stdout
    sys.stdout = lintstdout = StringIO()

    # Get output using Flake8's "legacy" API
    guide = flake8.api.legacy.get_style_guide()
    guide.check_files([file])

    # Reset stdout
    sys.stdout = oldstdout

    # set lint variable to captured output
    lint = lintstdout.getvalue()

    errors_to_return = {}
    warnings_to_return = {}
    verified_packages = []
    sys.path.append("/".join(file.split("/")[:-1]))
    for i in lint.split("\n"):
        """print(i)
        try:
            if any(error in i for error in ["F402",
                                            "F403",
                                            "F404",
                                            "F405",
                                            "F406",
                                            "F407",
                                            "F8",
                                            "F901",
                                            "E999"]):"""
        try:
            matched_error = re.match(get_error, i)
            if matched_error != None:
                error_code = matched_error.group(0)
                error_loc = re.match(get_loc, i)
                if error_code == Errors.F403:
                    if not scan_import(i):
                        error_msg = "{}: {}".format(error_loc, Errors.msg[error_code])
                        i = ":".join(i.split(":")[:3]) + ": F403 Package not installed or is unavailable."
                    else:
                        verified_packages.append(i.split("'")[1].split()[1])
                        continue
                elif error_code == Errors.F405:
                    if any(pkg in verified_packages for pkg in i.split(":")[-1][1:].split(", ")):
                        continue
                    else:
                        i = ":".join(i.split(":")[:3]) + ": F405 '" + i.split("'")[1] + "'" + "is undefined."
                i = "E: " + i
                errors_to_return[i] = int(i.split(":")[2])
            else:
                i = "W: " + i
                warnings_to_return[i] = int(i.split(":")[2])
        except IndexError:
            pass
    return errors_to_return, warnings_to_return, dict()


def scan_import(line):
    line = line.split("'")[1]
    try:
        if line.startswith("from"):
            importlib.import_module(
                    line.split()[1]) # import package
        else:
            importlib.import_module(
                    line.split("import")[-1]) # import module
        return True
    except ImportError:
        return False


if __name__ == "__main__":
    print(get_lint("mainwindow_controller.py"))
