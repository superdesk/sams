Feature: Public File Server
    Background: Set up Set and initial file
        Given server config
        """
        {"SAMS_PUBLIC_URL": "http://localhost:5750"}
        """
        When we send client.sets.create
        """
        {
            "docs": [{
                "name": "foo",
                "state": "usable",
                "destination_name": "internal"
            }]
        }
        """
        Then we get OK response
        When we upload a binary file with client.assets.create
        """
        {
            "docs": {
                "set_id": "#SETS._id#",
                "filename": "file_example-jpg.jpg",
                "name": "Jpeg Example",
                "description": "Jpeg file asset example",
                "state": "public"
            },
            "filename": "file_example-jpg.jpg"
        }
        """
        Then we get OK response

    Scenario: Download a public file
        When we download from the file server /assets/#SETS._id#/#ASSETS._id#
        Then we get file response with headers
        """
        {
            "Content-Type": "#ASSETS.mimetype#",
            "Content-Length": #ASSETS.length#,
            "Content-Disposition": "Inline; filename=#ASSETS.filename#"
        }
        """

    Scenario: Error 404 returned if Set is not found
        When we download from the file server /assets/5f9a41d6d19d982d57494248/#ASSETS._id#
        Then we get error 404

    Scenario: Error 404 returned if Asset is not found
        When we download from the file server /assets/#SETS._id#/5f9a41d6d19d982d57494248
        Then we get error 404

    Scenario: Error 404 returned if Set is disabled
        When we send client.sets.update
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"},
            "updates": {"state": "disabled"}
        }
        """
        Then we get OK response
        When we download from the file server /assets/#SETS._id#/#ASSETS._id#
        Then we get error 404

    Scenario: Error 404 returned if Asset is not public
        When we send client.assets.update
        """
        {
            "item_id": "#ASSETS._id#",
            "headers": {"If-Match": "#ASSETS._etag#"},
            "updates": {"state": "draft"}
        }
        """
        Then we get OK response
        When we download from the file server /assets/#SETS._id#/#ASSETS._id#
        Then we get error 404
        When we send client.assets.update
        """
        {
            "item_id": "#ASSETS._id#",
            "headers": {"If-Match": "#ASSETS._etag#"},
            "updates": {"state": "internal"}
        }
        """
        Then we get OK response
        When we download from the file server /assets/#SETS._id#/#ASSETS._id#
        Then we get error 404

    Scenario: Error 404 returned if Asset is not stored in provided Set
        When we send client.sets.create
        """
        {
            "docs": [{
                "name": "bar",
                "state": "usable",
                "destination_name": "internal"
            }]
        }
        """
        Then we get OK response
        When we download from the file server /assets/#SETS._id#/#ASSETS._id#
        Then we get error 404

    Scenario: Consume Assets public URL hateoas
        When we send client.assets.get_by_id
        """
        {"item_id": "#ASSETS._id#"}
        """
        Then we get existing resource
        """
        {
            "_links": {
                "public": {
                    "title": "Public Asset",
                    "href": "http://localhost:5750/assets/#SETS._id#/#ASSETS._id#"
                }
            }
        }
        """

    Scenario: Consume Assets no public URL hateoas when Set is not usable
        When we send client.sets.update
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"},
            "updates": {"state": "disabled"}
        }
        """
        When we send client.assets.get_by_id
        """
        {"item_id": "#ASSETS._id#"}
        """
        Then we get existing resource
        """
        {
            "_links": {"public": "__no_value__"}
        }
        """

    Scenario: Consume Assets no public URL hateoas when Asset is not public
        When we send client.assets.update
        """
        {
            "item_id": "#ASSETS._id#",
            "headers": {"If-Match": "#ASSETS._etag#"},
            "updates": {"state": "internal"}
        }
        """
        When we send client.assets.get_by_id
        """
        {"item_id": "#ASSETS._id#"}
        """
        Then we get existing resource
        """
        {
            "_links": {"public": "__no_value__"}
        }
        """

    Scenario: Consume Assets no public URL hateoas when SAMS_PUBLIC_URL is not set
        Given server config
        """
        {"SAMS_PUBLIC_URL": null}
        """
        When we send client.assets.get_by_id
        """
        {"item_id": "#ASSETS._id#"}
        """
        Then we get existing resource
        """
        {
            "_links": {"public": "__no_value__"}
        }
        """
