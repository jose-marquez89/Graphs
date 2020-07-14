def earliest_ancestor(ancestors, starting_node):
    # build graph (adjaceny list)
    ad_list = {}
    for parent, child in ancestors:
        if child not in ad_list:
            ad_list[child] = {parent}
        else:
            ad_list[child] = ad_list[child].union({parent})

    s = [starting_node]

    while len(s) > 0:
        earliest = s.pop()
        for ancestor in ad_list[earliest]:
            s.append(ancestor)

    return earliest


    


