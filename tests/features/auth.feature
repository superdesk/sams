Feature: Authentication mechanisms
    Scenario: Public authentication
        Given server config
        """
        {"SAMS_AUTH_TYPE": "sams.auth.public"}
        """
        Given client config
        """
        {"SAMS_AUTH_TYPE": "sams_client.auth.public"}
        """
        When we get "/"
        Then we get OK response

    Scenario: BASIC authentication
        Given server config
        """
        {
            "SAMS_AUTH_TYPE": "sams.auth.basic",
            "CLIENT_API_KEYS": "7f2ababa423061c5,09f4923dd04b6cf1"
        }
        """
        When we get "/"
        Then we get error 401
        """
        {
            "error": "04003",
            "description": "Please provide proper credentials"
        }
        """
        Given client config
        """
        {
            "SAMS_AUTH_TYPE": "sams_client.auth.basic"
        }
        """
        When we get "/"
        Then we get error 401
        """
        {
            "error": "04003",
            "description": "Please provide proper credentials"
        }
        """
        Given client config
        """
        {
            "SAMS_AUTH_TYPE": "sams_client.auth.basic",
            "SAMS_AUTH_KEY": "abcd123"
        }
        """
        When we get "/"
        Then we get error 401
        """
        {
            "error": "04003",
            "description": "Please provide proper credentials"
        }
        """
        Given client config
        """
        {
            "SAMS_AUTH_TYPE": "sams_client.auth.basic",
            "SAMS_AUTH_KEY": "7f2ababa423061c5"
        }
        """
        When we get "/"
        Then we get OK response
        Given client config
        """
        {
            "SAMS_AUTH_TYPE": "sams_client.auth.basic",
            "SAMS_AUTH_KEY": "09f4923dd04b6cf1"
        }
        """
        When we get "/"
        Then we get OK response
