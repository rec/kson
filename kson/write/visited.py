def visited(check_circular):
    visited = set()

    def visit(item):
        if check_circular and isinstance(item, (list, dict)):
            i = id(item)
            if i in visited:
                raise ValueError('Circular reference detected')
            visited.add(i)

    return visit
