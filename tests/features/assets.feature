Feature: Assets
    Scenario: Create, update and delete an Asset
        When we send client.sets.create
        """
        {
            "docs": [{
                "name": "foo",
                "destination_name": "internal"
            }]
        }
        """
        When we upload a binary file with metadata.assets.create
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
        When we upload a binary file with metadata.assets.update
        """
        {
            "item_id": "#ASSETS._id#",
            "headers": {"If-Match": "#ASSETS._etag#"},
            "updates": {"name": "Updated Jpeg Example"}
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
       When we send client.sets.create
        """
        {
            "docs": [{
                "name": "foo",
                "destination_name": "internal"
            }]
        }
        """
        When we upload a binary file with metadata.assets.create
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
        When we download a binary file lenth is right.assets.get_binary_by_id
        """
        {
            "item_id": "#ASSETS._id#",
            "length": 12186
        }
        """
