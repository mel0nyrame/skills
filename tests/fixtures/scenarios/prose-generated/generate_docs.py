import ast
from pathlib import Path


source = Path(__file__).with_name('export.py')
output = source.parent / 'docs' / 'export.md'
output.parent.mkdir(exist_ok=True)
output.write_text(ast.get_docstring(ast.parse(source.read_text(encoding='utf-8'))) + '\n',
                  encoding='utf-8')
