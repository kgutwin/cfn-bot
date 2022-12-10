import os

from cfnbot import formatter


def test_format_tweet_1():
    tweets = formatter.format_post(
        'Updated AWS::EC2::bar',
        'This is an updated resource.',
        'https://example.com',
        'December 17, 2018'
    )
    assert next(tweets) == """Updated AWS::EC2::bar

This is an updated resource.
https://example.com #ec2 #cloudformation"""
    assert next(tweets) == """Updated AWS::EC2::bar

This is an updated resource.
https://example.com #ec2 #cloudformation"""
    assert next(tweets) == """Updated AWS::EC2::bar

This is an updated...
https://example.com #ec2 #cloudformation"""


def test_format_tweet_2():
    tweets = formatter.format_post(
        'New AWS::DynamoDB::bar',
        'This is a new resource. It is great.',
        'https://example.com',
        'December 17, 2018'
    )
    assert next(tweets) == """New AWS::DynamoDB::bar

This is a new resource. It is great.
https://example.com #dynamodb #cloudformation"""
    assert next(tweets) == """New AWS::DynamoDB::bar

This is a new resource.
https://example.com #dynamodb #cloudformation"""
    assert next(tweets) == """New AWS::DynamoDB::bar

This is a new resource. It is...
https://example.com #dynamodb #cloudformation"""
    
    
def test_format_tweet_3():
    tweets = formatter.format_post(
        'The CAPABILITY_AUTO_EXPAND capability is now available.',
        'Use the CAPABILITY_AUTO_EXPAND capability to create or update a stack directly from a stack template that contains macros, without first reviewing the resulting changes in a change set first.',
        'https://example.com',
        'December 17, 2018'
    )
    assert next(tweets) == """The CAPABILITY_AUTO_EXPAND capability is now available.

Use the CAPABILITY_AUTO_EXPAND capability to create or update a stack directly from a stack template that contains macros, without first reviewing the resulting changes in a change set first.
https://example.com #cloudformation"""
    assert next(tweets) == """The CAPABILITY_AUTO_EXPAND capability is now available.

Use the CAPABILITY_AUTO_EXPAND capability to create or update a stack directly from a stack template that contains macros, without first reviewing the resulting changes in a change set first.
https://example.com #cloudformation"""
    assert next(tweets) == """The CAPABILITY_AUTO_EXPAND capability is now available.

Use the CAPABILITY_AUTO_EXPAND capability to create or update a stack directly from a stack template that contains macros, without first reviewing the resulting changes in a...
https://example.com #cloudformation"""

