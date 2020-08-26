Feature: Assets
    Background: Create Set
        When we send client.sets.create
        """
        {
            "docs": [{
                "name": "foo",
                "destination_name": "internal"
            }]
        }
        """
        Then we get OK response

    Scenario: Create, update and delete an Asset
        When we upload a binary file with client.assets.create
        """
        {
            "docs": {
                "set_id": "#SETS._id#",
                "filename": "file_example-jpg.jpg",
                "name": "Jpeg Example",
                "description": "Jpeg file asset example"
            },
            "filename": "file_example-jpg.jpg"
        }
        """
        Then we get existing resource
        """
        {
            "set_id": "#SETS._id#",
            "filename": "file_example-jpg.jpg",
            "name": "Jpeg Example",
            "description": "Jpeg file asset example",
            "state": "draft",
            "binary": null,
            "_media_id": "#ASSETS._media_id#",
            "length": 12186,
            "mimetype": "image/jpeg",
            "_links": {
                "self": {
                    "title": "Asset",
                    "href": "consume/assets/#ASSETS._id#"
                }
            }
        }
        """
        When we send client.assets.get_by_id
        """
        {"item_id": "#ASSETS._id#"}
        """
        Then we get existing resource
        """
        {
            "set_id": "#SETS._id#",
            "filename": "file_example-jpg.jpg",
            "name": "Jpeg Example",
            "description": "Jpeg file asset example",
            "state": "draft",
            "binary": "#ASSETS._media_id#",
            "_media_id": "#ASSETS._media_id#",
            "length": 12186,
            "mimetype": "image/jpeg",
            "_links": {
                "self": {
                    "title": "Asset",
                    "href": "consume/assets/#ASSETS._id#"
                }
            }
        }
        """
        When we send client.assets.update
        """
        {
            "item_id": "#ASSETS._id#",
            "headers": {"If-Match": "#ASSETS._etag#"},
            "updates": {"description": "Updated Jpeg file asset example"}
        }
        """
        Then we get existing resource
        """
        {
            "set_id": "#SETS._id#",
            "filename": "file_example-jpg.jpg",
            "name": "Jpeg Example",
            "description": "Updated Jpeg file asset example"
        }
        """
        When we upload a binary file with client.assets.update
        """
        {
            "item_id": "#ASSETS._id#",
            "headers": {"If-Match": "#ASSETS._etag#"},
            "updates": {"name": "Updated Jpeg Example"},
            "filename": "file_example2-jpg.jpg"
        }
        """
        Then we get existing resource
        """
        {
            "name": "Updated Jpeg Example",
            "length": 16549,
            "mimetype": "image/jpeg"
        }
        """
        When we send client.assets.delete
        """
        {
            "item_id": "#ASSETS._id#",
            "headers": {"If-Match": "#ASSETS._etag#"}
        }
        """
        Then we get OK response
        When we send client.assets.get_by_id
        """
        {"item_id": "#ASSETS._id#"}
        """
        Then we get error 404

    Scenario: Create, Download an Asset
        When we upload a binary file with client.assets.create
        """
        {
            "docs": {
                "set_id": "#SETS._id#",
                "filename": "file_example-jpg.jpg",
                "name": "Jpeg Example",
                "description": "Jpeg file asset example"
            },
            "filename": "file_example-jpg.jpg"
        }
        """
        Then we get existing resource
        """
        {
            "set_id": "#SETS._id#",
            "filename": "file_example-jpg.jpg",
            "name": "Jpeg Example",
            "description": "Jpeg file asset example",
            "state": "draft",
            "binary": null,
            "_media_id": "#ASSETS._media_id#",
            "length": 12186,
            "mimetype": "image/jpeg",
            "_links": {
                "self": {
                    "title": "Asset",
                    "href": "consume/assets/#ASSETS._id#"
                }
            }
        }
        """
        When we download a binary file with client.assets.get_binary_by_id
        """
        {
            "item_id": "#ASSETS._id#",
            "length": 12186
        }
        """

    Scenario: Validate binary asset supplied
        When we upload a binary file with client.assets.create
        """
        {
            "docs": {
                "set_id": "#SETS._id#",
                "filename": "file_example-jpg.jpg",
                "name": "Jpeg Example",
                "description": "Jpeg file asset example"
            }
        }
        """
        Then we get error 400
        """
        {
            "error": "08001",
            "description": "Asset must contain a binary to upload"
        }
        """

    Scenario: Downloading non existent asset binary
        When we download a binary file with client.assets.get_binary_by_id
        """
        {
            "item_id": "unknown"
        }
        """
        Then we get error 404
        """
        {
            "error": "08002",
            "description": "Asset with id \"unknown\" not found"
        }
        """
