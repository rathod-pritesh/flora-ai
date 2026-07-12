from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound

def detect_language(code: str):
    
    if "package main" in code and "func main" in code:
        return "Go"
    
    if "def" in code:
        return "Python"
    
    if "console.log(" in code:
        return "JavaScript"
    
    try:
        lexer = guess_lexer(code)
        return lexer.name
    
    except ClassNotFound:
        return "Unknown"
