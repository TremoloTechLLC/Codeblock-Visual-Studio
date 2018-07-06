from modulefinder import ModuleFinder
import ast
import _ast

finder = ModuleFinder()
file = "/home/kai/git/codeblock-visual-studio/mainwindow_controller.py"
testvar = "poop to you!"

def get_imports(file):
    finder.run_script(path)
    for name, mod in finder.modules.items():
        pass

def get_variables(node, file):
    variables = set()
    if hasattr(node, 'body'):
        for subnode in node.body:
            variables |= get_variables(subnode)
    elif isinstance(node, _ast.Assign):
        for name in node.targets:
            if isinstance(name, _ast.Name):
                variables.add(name.id)
    return variables

def get_functions(file):
    filetxt = file(open(path).readlines()) # path may need to be changed

    current_line = 0
    finalfuncnames = []
    funcs = {}
    funcnumlines = []
    funclines = []
    fullfunclines = []
    removeend = []
    leading_whitespace = 0
    for line in filetxt:
        current_line = current_line + 1
        if "def " in line:
            funcnumlines.append(current_line)
            print(funcnumlines, "linenumoffuncs")
            finalfuncnames.append(line)
            print(finalfuncnames, "funcnamesfinallist")

    for lof in funcnumlines:
        print(lof, "forlines")
        funcname = filetxt[lof-1]
        top_leading_whitespace = len(filetxt[lof]) - len(filetxt[lof].lstrip())
        print(top_leading_whitespace, "initalwhitespace")
        funcbody = filetxt[lof]
        for body in filetxt[lof:]:
            leading_whitespace = len(body) - len(body.lstrip())
            print(leading_whitespace, "whitespacebody")
            if leading_whitespace < top_leading_whitespace:
                break
            funclines.append(body)
            print(funclines, "finalfunclines")
        fullfunclines.append(funclines)
        print(fullfunclines, "fullfunclines")
        funclines = []

    funcs = dict(zip(finalfuncnames, fullfunclines))

    print(funcs, "totalyfinal")
    return funcs

get_functions(file)
