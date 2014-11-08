Feature: Dinky service request

    In order to demonstrate the dinky service
    As a user
    I must be able to see the service running

    Scenario: good response from the root url
      Given I have the root url of the service
      When I request the root url
      Then I should get the service information

    Scenario: good response from the hello world url
      Given I have the hello world url of the service
      When I request the hello world url
      Then I should get "Hello World"

    Scenario: error from an invalid url
      Given I have an end point that does not exists
      When I request that not existent url
      Then I should get a response with status code 404
