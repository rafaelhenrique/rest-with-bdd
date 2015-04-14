Feature: View all books registered on library

    Background: Set target server address and headers
        Given I am using server "$TEST_SERVER"
        And I set base URL to "$TEST_URL"
        And I set "Accept" header to "application/json"
        And I set "Content-Type" header to "application/json"

    Scenario: Test GET request
        When I make a GET request to "books"
        Then the response status should be 200

    Scenario: Test GET title of book by id
        When I make a GET request to "books/1"
        Then the response status should be 200
        And I should see this title "$TEST_TITLE" of book


    # We need write more features ;)