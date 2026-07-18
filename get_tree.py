import os

ign_dirs = {'.git', 'node_modules', '.gemini', '__pycache__', '.pytest_cache', 'dist', 'build', '.idea', '.vscode'}
ign_files = {'.DS_Store', 'tree.txt', 'get_tree.py', 'package-lock.json'}

def get_tree(startpath):
    res = []
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in ign_dirs]
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        res.append('{}{}/'.format(indent, os.path.basename(root) if root != startpath else 'Datathon-Hack'))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if f not in ign_files:
                res.append('{}{}'.format(subindent, f))
    return '\n'.join(res)

with open('tree_output.txt', 'w', encoding='utf-8') as f:
    f.write(get_tree('.'))
