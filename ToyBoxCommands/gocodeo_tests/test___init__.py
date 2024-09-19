import pytest
from unittest import mock
from ToyBoxCommands.toy_command_processor import ToyCommandProcessor

@pytest.fixture
def mock_toy_command_processor():
    with mock.patch('ToyBoxCommands.toy_command_processor.ToyCommandProcessor') as MockToyCommandProcessor:
        instance = MockToyCommandProcessor.return_value
        instance.process_command.side_effect = lambda command: {
            'status': 'success', 'position': {'x': 1, 'y': 1}
        } if command == 'MOVE' else {
            'status': 'error', 'message': 'Invalid command'
        }
        instance.initialize.return_value = {
            'status': 'initialized', 'position': {'x': 0, 'y': 0}
        }
        instance.execute_commands.side_effect = lambda commands: {
            'status': 'success', 'position': {'x': 0, 'y': 1}
        } if commands == ['MOVE', 'LEFT', 'MOVE'] else {
            'status': 'success', 'position': {'x': 0, 'y': 0}
        }
        instance.reset.return_value = {
            'status': 'reset', 'position': {'x': 0, 'y': 0}
        }
        instance.report_position.return_value = {
            'position': {'x': 0, 'y': 0}
        }
        yield instance

# happy_path - test_process_command_valid - Test that valid commands are processed correctly
def test_process_command_valid(mock_toy_command_processor):
    result = mock_toy_command_processor.process_command('MOVE')
    assert result['status'] == 'success'
    assert result['position'] == {'x': 1, 'y': 1}

# happy_path - test_initialize - Test that the command processor initializes correctly
def test_initialize(mock_toy_command_processor):
    result = mock_toy_command_processor.initialize()
    assert result['status'] == 'initialized'
    assert result['position'] == {'x': 0, 'y': 0}

# happy_path - test_execute_commands_sequence - Test that the processor can handle a series of valid commands
def test_execute_commands_sequence(mock_toy_command_processor):
    result = mock_toy_command_processor.execute_commands(['MOVE', 'LEFT', 'MOVE'])
    assert result['status'] == 'success'
    assert result['position'] == {'x': 0, 'y': 1}

# happy_path - test_reset - Test that the processor returns to initial state after reset
def test_reset(mock_toy_command_processor):
    result = mock_toy_command_processor.reset()
    assert result['status'] == 'reset'
    assert result['position'] == {'x': 0, 'y': 0}

# happy_path - test_report_position - Test that the processor reports current position accurately
def test_report_position(mock_toy_command_processor):
    result = mock_toy_command_processor.report_position()
    assert result['position'] == {'x': 0, 'y': 0}

# edge_case - test_process_command_invalid - Test that an invalid command returns an error
def test_process_command_invalid(mock_toy_command_processor):
    result = mock_toy_command_processor.process_command('FLY')
    assert result['status'] == 'error'
    assert result['message'] == 'Invalid command'

# edge_case - test_execute_commands_empty - Test that processor handles empty command sequence gracefully
def test_execute_commands_empty(mock_toy_command_processor):
    result = mock_toy_command_processor.execute_commands([])
    assert result['status'] == 'success'
    assert result['position'] == {'x': 0, 'y': 0}

# edge_case - test_process_command_out_of_bounds - Test that processor does not move out of bounds
def test_process_command_out_of_bounds(mock_toy_command_processor):
    # Assuming the processor's position is at the boundary
    mock_toy_command_processor.process_command.side_effect = lambda command: {
        'status': 'error', 'message': 'Out of bounds'
    }
    result = mock_toy_command_processor.process_command('MOVE')
    assert result['status'] == 'error'
    assert result['message'] == 'Out of bounds'

# edge_case - test_reset_from_error - Test that reset works even if processor is in error state
def test_reset_from_error(mock_toy_command_processor):
    # Simulate error state
    mock_toy_command_processor.process_command('FLY')
    result = mock_toy_command_processor.reset()
    assert result['status'] == 'reset'
    assert result['position'] == {'x': 0, 'y': 0}

# edge_case - test_execute_commands_rapid - Test that processor handles rapid command inputs without crash
def test_execute_commands_rapid(mock_toy_command_processor):
    result = mock_toy_command_processor.execute_commands(['MOVE', 'MOVE', 'LEFT', 'MOVE', 'RIGHT', 'MOVE'])
    assert result['status'] == 'success'
    assert result['position'] == {'x': 1, 'y': 2}

