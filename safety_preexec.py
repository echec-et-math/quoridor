import importlib

def secure_importer(name, globals=None, locals=None, fromlist=(), level=0):
    allowed_modules = ['numpy', 'scipy', 'math', 'random']
    allowed_froms = [None, 'numpy']
    # not exactly a good verification layer
    frommodule = globals['__name__'] if globals else None
    if not name in allowed_modules or not frommodule in allowed_froms:
        raise ImportError("module '%s' is restricted."%name)

    return importlib.__import__(name, globals, locals, fromlist, level)

__builtins__.__dict__['__import__'] = secure_importer