def rook_in_danger(plan):
    rook_index= []
    for row in plan:
        if row.count('#') > 1:
            return True
        elif '#' in row:
            if row.index('#') in rook_index:
                return True
            else:
                rook_index.append(row.index('#'))
    return False
