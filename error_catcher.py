import sys, os
import importlib
import flake8.api.legacy
from io import StringIO
import re
import cProfile

class Errors:
    # Contains all error codes as well as special error messages for certain codes
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
            F403: "F403 Package not installed or is unavailable.",
            F405: "F405 {} is undefined."
        }

# Define some regex expressions for matching errors and location
get_error = re.compile("[FE]\d{1,3}")
get_loc = re.compile("\w+.py:\d+:\d+:")

def ret_lint(file):
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

    for issue in lint.split("\n"):
        yield issue


def get_lint(file_name):
    print(file_name)
    errors_to_return = {}
    warnings_to_return = {}
    verified_packages = []
    # sys.path.append("/".join(file.split("/")[:-1]))
    sys.path.append(file_name.rstrip("/"))
    for i in ret_lint(file_name):
        try:
            matched_error = re.match(get_error, i)  # try to match the lint line with an error marker
            if matched_error != None:  # is this lint an error?
                error_code = matched_error.group(0)
                error_loc = re.match(get_loc, i)
                # Verify star import (warning by F403)
                if error_code == Errors.F403:
                    if not scan_import(i):
                        # Package doesn't exist
                        error_msg = "{}: {}".format(error_loc, Errors.msg[error_code])
                        i = err_msg
                        # i = ":".join(i.split(":")[:3]) + ": F403 Package not installed or is unavailable."
                    else:
                        # Add package as verified
                        verified_packages.append(i.split("'")[1].split()[1])
                        continue
                # If F405 is thrown, check if object is in a verified import
                elif error_code == Errors.F405:
                    if any(pkg in verified_packages for pkg in i.split(":")[-1][1:].split(", ")):
                        continue
                    else:
                        error_msg = "{}: {}".format(error_loc, Errors.msg[error_code])
                        i = error_msg
                i = "E: " + i
                errors_to_return[i] = int(i.split(":")[2])
            else:
                # Add as warning
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
    # print(get_lint("./mainwindow_controller.py"))
    cProfile.run('get_lint("./icons_rc.py")')
