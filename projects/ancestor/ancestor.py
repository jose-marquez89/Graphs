def earliest_ancestor(ancestors, starting_node):
    # build graph (adjaceny list)
    ad_list = {}
    for parent, child in ancestors:
        if child not in ad_list:
            ad_list[child] = {parent}
        else:
            ad_list[child] = ad_list[child].union({parent})

    s = [starting_node]
    preds = {}
    generations = 0
    preds[generations] = []

    while len(s) > 0:
        earliest = s.pop()
        if len(s) == 0:
            new_gen = True
        else:
            new_gen = False
        # ancestors with no known predecessors will not be in list
        if earliest in ad_list:
            for ancestor in ad_list[earliest]:
                s.append(ancestor)
        else:
            preds[generations].append(earliest)
        if new_gen:
            generations += 1
            preds[generations] = []

    if earliest == starting_node:
        return -1
    else:
        target = preds[generations-1]
        if len(target) > 1:
            return min(target)
        return target.pop()
