def multi_agent_search(game, state, agents=2):
    value, move = multi_agent_max_search(game, state, agents)
    return (value, move)


def multi_agent_max_search(game, state, agents=2, depth=0, abg=None):
    game.call(state)
    if game.cut_off(state, depth):
        return game.utility(state), None

    if not abg:
        abg = [float('inf') for _ in range(agents)]

    v = None
    move = None
    for action in game.actions(state):
        v2, a2 = multi_agent_max_search(game, game.result(state, action),
                                        agents, depth + 1, abg)
        if not v or v2 > v:
            v, move = v2, action
        if v >= abg[(depth - 1) % agents] or v >= abg[(depth - 2) % agents]:
            game.clean(state)
            return v, action
        abg[(depth % agents)] = max(abg[(depth % agents)], v)
        game.clean(state)
    return v, move