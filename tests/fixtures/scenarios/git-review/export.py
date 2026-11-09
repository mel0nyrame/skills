def export(rows, authenticated, permissions):
    if not authenticated:
        raise PermissionError('authentication')
    if 'export:read' not in permissions:
        raise PermissionError('permission')
    if len(rows) > 100:
        raise ValueError('row limit')
    return '\n'.join(rows).encode('utf-8')
