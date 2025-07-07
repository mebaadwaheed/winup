# winup/web/py_to_js.py
import ast
import inspect
import textwrap

# --- Mappings for Pythonic to JS conversion ---
PYTHON_TO_JS_ATTR_MAP = {
    'font_weight': 'fontWeight',
    'inner_text': 'innerText',
    'text_content': 'textContent',
    # Add other style properties here in the future
}

OPERATOR_MAP = {
    ast.Add: '+',
    ast.Sub: '-',
    ast.Mult: '*',
    ast.Div: '/',
}

class PyToJsVisitor(ast.NodeVisitor):
    """
    Translates Python AST nodes for a simple subset of the language into a
    JavaScript string.
    """
    def __init__(self, arg_map):
        self.arg_map = arg_map
        self.js_code = []

    def visit_Name(self, node):
        # If the name is 'print', convert it to 'console.log'
        if node.id == 'print':
            self.js_code.append('console.log')
            return
        # Map python argument names to the names available in the JS scope
        self.js_code.append(self.arg_map.get(node.id, node.id))

    def visit_Constant(self, node):
        if isinstance(node.value, str):
            # Basic string literal conversion
            js_str = node.value.replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"')
            self.js_code.append(f"'{js_str}'")
        elif isinstance(node.value, (int, float)):
            self.js_code.append(str(node.value))
        elif node.value is True: self.js_code.append("true")
        elif node.value is False: self.js_code.append("false")
        elif node.value is None: self.js_code.append("null")
        else:
            raise TypeError(f"Unsupported constant type: {type(node.value)}")

    def visit_Attribute(self, node):
        self.visit(node.value)
        # Convert pythonic attribute names to JS-style names
        js_attr = PYTHON_TO_JS_ATTR_MAP.get(node.attr, node.attr)
        self.js_code.append(f".{js_attr}")

    def visit_BinOp(self, node):
        """Translates a binary operation (e.g., a + b)."""
        self.js_code.append("(")
        self.visit(node.left)
        op_char = OPERATOR_MAP.get(type(node.op))
        if not op_char:
            raise TypeError(f"Unsupported binary operator: {type(node.op).__name__}")
        self.js_code.append(f" {op_char} ")
        self.visit(node.right)
        self.js_code.append(")")

    def visit_Call(self, node):
        # Add special handling for our new get_element function
        if isinstance(node.func, ast.Name) and node.func.id == 'get_element':
            if len(node.args) != 1:
                raise ValueError("get_element() expects exactly one string argument (the ID).")
            self.js_code.append("document.getElementById(")
            self.visit(node.args[0])
            self.js_code.append(")")
            return

        self.visit(node.func)
        self.js_code.append("(")
        for i, arg in enumerate(node.args):
            self.visit(arg)
            if i < len(node.args) - 1:
                self.js_code.append(", ")
        self.js_code.append(")")

    def visit_Assign(self, node):
        if len(node.targets) != 1:
            raise ValueError("Only single assignment targets are supported for transpilation.")
        self.visit(node.targets[0])
        self.js_code.append(" = ")
        self.visit(node.value)

    def visit_Await(self, node):
        self.js_code.append("await ")
        self.visit(node.value)

    def visit_Expr(self, node):
        self.visit(node.value)
        # Append semicolon at the end of standalone expressions
        self.js_code.append(";")

    def generic_visit(self, node):
        raise TypeError(f"Unsupported Python syntax for hooks: {node.__class__.__name__}")

def transpile_hook(hook_func: callable, js_args: list) -> tuple[bool, str]:
    """
    Takes a Python function and transpiles its body to a JavaScript string.
    Returns a tuple: (is_async, transpiled_js_code).
    """
    try:
        source_code = inspect.getsource(hook_func)
        source_code = textwrap.dedent(source_code)
    except (TypeError, OSError):
        raise ValueError(
            f"Could not get source code for {hook_func}. "
            "Please use 'def' to define hook functions, not lambdas or interactive functions."
        )
    
    tree = ast.parse(source_code)
    
    func_node = tree.body[0]
    is_async = False
    
    if isinstance(func_node, ast.AsyncFunctionDef):
        is_async = True
    elif not isinstance(func_node, ast.FunctionDef):
        raise ValueError("The hook must be a standard or async Python function.")

    # Map Python argument names to the JavaScript argument names
    py_args = [arg.arg for arg in func_node.args.args]
    if len(py_args) != len(js_args):
        raise ValueError(
            f"Function '{func_node.name}' has {len(py_args)} arguments, but the hook provides {len(js_args)} JS arguments."
        )
    arg_map = dict(zip(py_args, js_args))
    
    # Transpile each statement in the function body
    js_body_parts = []
    for statement in func_node.body:
        visitor = PyToJsVisitor(arg_map)
        visitor.visit(statement)
        js_body_parts.append("".join(visitor.js_code))
        
    return is_async, "\n".join(js_body_parts) 