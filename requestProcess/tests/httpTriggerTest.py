from unittest.mock import Mock
import main_test
import json

"""Test to validate the code with the correct input data"""
def test_withData():
    data = {'response_url':'https','text':'tesla inc'}
    req = Mock(get_json=Mock(return_value=data), args=data)
    # Call tested function
    assert main_test.requestProcess(req) == json.dumps({'response_type': 'in_channel','text': 'Processing your request, One Moment...','attachments': []})

"""Test to validate the code with the empty input data"""
def test_withoutData():
    data = {}
    req = Mock(get_json=Mock(return_value=data), args=data)
    # Call tested function
    assert main_test.requestProcess(req) == json.dumps({'response_type': 'in_channel','text': 'Please enter a valid text','attachments': []})

"""Test to validate the code with the invalid input format"""
def test_invalidData():
    data = ''
    req = Mock(get_json=Mock(return_value=data), args=data)
    # Call tested function
    assert main_test.requestProcess(req) == json.dumps({'response_type': 'in_channel','text': 'Issue with getting the response','attachments': []})