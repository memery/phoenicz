import statekeeper

def test_statekeeper(logger):
    state = statekeeper.StateKeeper()
    key, value = 'testkey', '1234'

    logger.print('Checking caller id...')
    assert state._caller_id() == __file__

    logger.print('Testing set/get value...')
    state[key] = value
    assert state[key] == value

    logger.print('Testing get with invalid value...')
    try:
        state['invalidkey']
    except KeyError:
        pass

    logger.print('Trying to delete key...')
    del state[key]
    try:
        state[key]
    except KeyError:
        pass

    logger.print('Testing in-operator...')
    state[key] = value
    assert key in state

    logger.print('Testing shared dict set/get...')
    state.shared[key] = value
    assert state.shared[key] == value

    logger.print('Trying to remove shared...')
    try:
        state.shared = None
    except AttributeError:
        pass

    return True


def test_run_all(logger):
    logger.print('Running all tests...')
    assert test_statekeeper(logger.deeper('StateKeeper'))
    logger.print('All tests complete!')
    return True
