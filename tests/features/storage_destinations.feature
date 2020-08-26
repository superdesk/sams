Feature: Storage Destinations
    Scenario: Get all destinations
        When we send client.destinations.search
        Then we get existing resource
        """
        {"_items": [
            {"_id": "internal", "provider": "MongoGridFS"},
            {"_id": "during_draft", "provider": "MongoGridFS"}
        ]}
        """

    Scenario: Get a single destination
        When we send client.destinations.get_by_id
        """
        {"item_id": "unknown"}
        """
        Then we get error 404
        """
        {
            "error": "05001",
            "description": "Destination \"unknown\" not registered with the system"
        }
        """
        When we send client.destinations.get_by_id
        """
        {"item_id": "internal"}
        """
        Then we get existing resource
        """
        {"_id": "internal", "provider": "MongoGridFS"}
        """

    Scenario: Write methods are not allowed
        When we send client.destinations.create
        """
        {"docs": [{"_id": "mock", "provider": "MongoGridFS"}]}
        """
        Then we get error 405
        When we send client.destinations.update
        """
        {
            "item_id": "internal",
            "updates": {"provider": "MongoGridFS"}
        }
        """
        Then we get error 405
        When we send client.destinations.delete
        """
        {"item_id": "internal"}
        """
        Then we get error 405
