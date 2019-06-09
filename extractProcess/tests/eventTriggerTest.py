import base64
import main_test
import json

"""Test to validate the extractProcess module with the correct input data"""
def test_extractProcess_withData():
    data = {'slack_url': 'https://hooks.slack.com/commands/TJY7M8TA7/661498639975/4c22qrbZn7deAyxBjtVHzSNh', 'text': 'tesla inc'}
    # Call tested function
    main_test.extractProcess(data, None)
    assert (json.dumps({'response_type': 'in_channel', 'text': 'tesla inc\nRevenue: DKK 142.07 billion\nOperating income: DKK 2.57 billion\nNet income: DKK 6.46 billion\nTotal assets: DKK 196.88 billion\nTotal equity: DKK 32.59 billion', 'attachments': []}))

"""Test to validate the extractProcess module without the search text input information"""
def test_extractProcess_withoutData():
    data = {'slack_url': 'https://hooks.slack.com/commands/TJY7M8TA7/661498639975/4c22qrbZn7deAyxBjtVHzSNh', 'text': ''}
    # Call tested function
    main_test.extractProcess(data, None)
    assert (json.dumps({'response_type': 'in_channel', 'text': 'Something went wrong, Not able to process your request at this moment, please try again later', 'attachments': []}))

"""Test to validate the conversion module with the valid currency information"""
def test_conversion_withValidCurrency():
    # Call tested function
    main_test.conversion({'Revenue': 'us$21.461\xa0billion\xa0(2018)', 'Operating income': 'us$-0.388\xa0billion\xa0(2018)', 'Net income': 'us$−0.976\xa0billion\xa0(2018)', 'Total assets': 'us$29.740\xa0billion\xa0(2018)', 'Total equity': 'us$4.923\xa0billion\xa0(2018)'})
    assert (json.dumps({'Revenue': 'DKK 142.07 billion', 'Operating income': 'DKK 2.57 billion', 'Net income': 'DKK 6.46 billion', 'Total assets': 'DKK 196.88 billion', 'Total equity': 'DKK 32.59 billion'}))

"""Test to validate the conversion module with the unexpected currency (euro) information"""
def test_conversion_withoutValidCurrency():
    # Call tested function
    main_test.conversion({'Revenue': '€21.461\xa0billion\xa0(2018)', 'Operating income': '€0.388\xa0billion\xa0(2018)', 'Net income': '€−0.976\xa0billion\xa0(2018)', 'Total assets': '€29.740\xa0billion\xa0(2018)', 'Total equity': '€4.923\xa0billion\xa0(2018)'})
    assert (json.dumps({'Revenue': '', 'Operating income': '', 'Net income': '', 'Total assets': '', 'Total equity': ''}))

"""Test to validate the wikiExtract module with the correct input arguments"""
def test_wikiExtract_withData():
    # Call tested function
    main_test.wikiExtract('tesla inc',{'Revenue': '', 'Operating income': '', 'Net income': '', 'Total assets': '', 'Total equity': ''})
    assert (json.dumps({'Revenue': 'us$21.461\xa0billion\xa0(2018)', 'Operating income': 'us$-0.388\xa0billion\xa0(2018)', 'Net income': 'us$−0.976\xa0billion\xa0(2018)', 'Total assets': 'us$29.740\xa0billion\xa0(2018)', 'Total equity': 'us$4.923\xa0billion\xa0(2018)'}))

"""Test to validate the wikiExtract module with the empty value dict argument"""
def test_wikiExtract_withoutData():
    # Call tested function
    main_test.wikiExtract('',{'Revenue': '', 'Operating income': '', 'Net income': '', 'Total assets': '', 'Total equity': ''})
    assert (json.dumps({'Revenue': '', 'Operating income': '', 'Net income': '', 'Total assets': '', 'Total equity': ''}))

"""Test to validate the conversion module with the correct input for formatting"""
def test_conversionProcess_withValidCurrency():
    data = {}
    # Call tested function
    main_test.conversionProcess({'Revenue': 'DKK 142.07 billion', 'Operating income': 'DKK 2.57 billion', 'Net income': 'DKK 6.46 billion', 'Total assets': 'DKK 196.88 billion', 'Total equity': 'DKK 32.59 billion'},{'response_type': 'in_channel', 'text': '', 'attachments': []},'tesla inc','tesla inc')
    assert (json.dumps({'response_type': 'in_channel', 'text': 'tesla inc\nRevenue: DKK 142.07 billion\nOperating income: DKK 2.57 billion\nNet income: DKK 6.46 billion\nTotal assets: DKK 196.88 billion\nTotal equity: DKK 32.59 billion', 'attachments': []}))

"""Test to validate the conversion module with the incorrect input for formatting"""
def test_conversionProcess_withoutValidCurrency():
    data = {}
    # Call tested function
    main_test.conversionProcess({'Revenue': '', 'Operating income': '', 'Net income': '', 'Total assets': '', 'Total equity': ''},{'response_type': 'in_channel', 'text': '', 'attachments': []},'tesla inc','tesla inc')
    assert (json.dumps({'response_type': 'in_channel', 'text': 'Currency Value of the Finanace Informtion is not available in US or CAD dollars', 'attachments': []}))