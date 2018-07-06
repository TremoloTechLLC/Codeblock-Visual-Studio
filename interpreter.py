from modulefinder import ModuleFinder
import ast
import _ast

finder = ModuleFinder()
path = "/home/kai/git/codeblock-visual-studio/tkintertest.py"
file = open(path).readlines()
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
    current_line = 0
    funcs = {}
    funcnumlines = []
    funclines = []
    removeend = []
    leading_whitespace = 0
    for line in file:
        current_line = current_line + 1
        if line.startswith("def "):
            funcnumlines.append(current_line)
            func_full = line.split("def ")[1]
            for char in func_full:
                if char == "(":
                    removeend.append(char)
            finalfuncname = func_full.split(removeend[0])[0]
            print(finalfuncname, "funcnamefinal")

    for lof in funcnumlines:
        print(lof, "forlines")
        funcname = file[lof-1]
        top_leading_whitespace = len(file[lof]) - len(file[lof].lstrip())
        print(top_leading_whitespace, "initalwhitespace")
        funcbody = file[lof]
        for body in file[lof:]:
            leading_whitespace = len(body) - len(body.lstrip())
            print(leading_whitespace, "whitespacebody")
            if leading_whitespace < top_leading_whitespace:
                break
            funclines.append(body)
            print(funclines, "finalfunclines")
            funcs[finalfuncname] = funclines
        funclines = []
    print(funcs, "totalyfina")

get_functions(file)
