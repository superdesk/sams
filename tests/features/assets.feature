Feature: Assets
    Scenario: Create with set state as draft or disabled, we get error
        When we send client.sets.create
        """
        {
            "docs": [{
                "name": "foo",
                "state": "draft",
                "destination_name": "internal"
            }]
        }
        """
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
        Then we get error 400
        """
        {
            "error": "08003",
            "description": "Asset upload is not allowed to an inactive Set"
        }
        """
        When we send client.sets.update
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"},
            "updates": {"state": "disabled"}
        }
        """
        Then we get existing resource
        """
        {
            "name": "foo",
            "destination_name": "internal",
            "state": "disabled"
        }
        """
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
        Then we get error 400
        """
        {
            "error": "08003",
            "description": "Asset upload is not allowed to an inactive Set"
        }
        """
    
    Scenario: Create asset, update set to disabled, update asset, get error
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
        When we send client.sets.update
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"},
            "updates": {"state": "disabled"}
        }
        """
        Then we get existing resource
        """
        {
            "name": "foo",
            "destination_name": "internal",
            "state": "disabled"
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
        Then we get error 400
        """
        {
            "error": "08003",
            "description": "Asset upload is not allowed to an inactive Set"
        }
        """

    Scenario: Create, update and delete an Asset
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
            "item_id": "#ASSETS._id#"
        }
        """
        Then we get file response with headers
        """
        {
            "Content-Type": "#ASSETS.mimetype#",
            "Content-Length": #ASSETS.length#,
            "Content-Disposition": "Inline; filename=#ASSETS.filename#"
        }
        """

    Scenario: Validate binary asset supplied
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
    
    Scenario: Get assets count distribution for sets
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
        When we send client.assets.get_assets_count
        """
        {
            "set_ids": ["#SETS._id#"]
        }
        """
        Then we get existing resource
        """
        {
            "#SETS._id#": 1
        }
        """
        When we send client.assets.get_assets_count
        """
        {
            
        }
        """
        Then we get existing resource
        """
        {
            "#SETS._id#": 1
        }
        """

    Scenario: Compress binaries to Zip
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
        Then we store response in "asset_1"
        When we upload a binary file with client.assets.create
        """
        {
            "docs": {
                "set_id": "#SETS._id#",
                "filename": "file_example-docx.docx",
                "name": "Docx Example",
                "description": "Docx file asset example"
            },
            "filename": "file_example-docx.docx"
        }
        """
        Then we store response in "asset_2"
        When we download a binary file with client.assets.get_binary_zip_by_id
        """
        {
            "item_ids": ["#asset_1._id#","#asset_2._id#"]
        }
        """
        Then we get file response with headers
        """
        {
            "Content-Type": "application/zip",
            "Content-Length": 123747,
            "Content-Disposition": "Inline"
        }
        """
        And we get zip file with assets
        """
        {
            "item_ids": ["#asset_1._id#","#asset_2._id#"]
        }
        """

    Scenario: Get assets by ids
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
                "description": "Jpeg file asset example"
            },
            "filename": "file_example-jpg.jpg"
        }
        """
        Then we store response in "asset_1"
        When we upload a binary file with client.assets.create
        """
        {
            "docs": {
                "set_id": "#SETS._id#",
                "filename": "file_example-docx.docx",
                "name": "Docx Example",
                "description": "Docx file asset example"
            },
            "filename": "file_example-docx.docx"
        }
        """
        Then we store response in "asset_2"
        When we send client.assets.get_by_ids
        """
        {
            "item_ids": ["#asset_1._id#", "#asset_2._id#"]
        }
        """
        Then we get existing resource
        """
        {"_items": [
            {"_id": "#asset_1._id#", "name": "Jpeg Example"},
            {"_id": "#asset_2._id#", "name": "Docx Example"}
        ]}
        """

    Scenario: Error raised when Asset size exceeds Set.maximum_asset_size
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
        When we upload a binary file with client.assets.create
        """
        {
            "docs": {
                "set_id": "#SETS._id#",
                "filename": "file_example-docx.docx",
                "name": "file example docx",
                "description": "Test unrestricted size"
            },
            "filename": "file_example-docx.docx"
        }
        """
        Then we get OK response
        Given server config
        """
        {"MAX_ASSET_SIZE": 102400}
        """
        When we upload a binary file with client.assets.create
        """
        {
            "docs": {
                "set_id": "#SETS._id#",
                "filename": "file_example-docx.docx",
                "name": "file example docx 2",
                "description": "Test global restriction deny"
            },
            "filename": "file_example-docx.docx"
        }
        """
        Then we get error 400
        """
        {
            "error": "08004",
            "description": "Asset size (108.69 KB) exceeds the maximum size for the Set (100.00 KB)"
        }
        """
        When we upload a binary file with client.assets.create
        """
        {
            "docs": {
                "set_id": "#SETS._id#",
                "filename": "file_example2-jpg.jpg",
                "name": "file example 2",
                "description": "Test global restriction allow"
            },
            "filename": "file_example2-jpg.jpg"
        }
        """
        Then we get OK response
        When we send client.sets.update
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"},
            "updates": {"maximum_asset_size": 16000}
        }
        """
        When we upload a binary file with client.assets.create
        """
        {
            "docs": {
                "set_id": "#SETS._id#",
                "filename": "file_example2-jpg.jpg",
                "name": "file example 2",
                "description": "Test Set restriction deny"
            },
            "filename": "file_example2-jpg.jpg"
        }
        """
        Then we get error 400
        """
        {
            "error": "08004",
            "description": "Asset size (16.16 KB) exceeds the maximum size for the Set (15.62 KB)"
        }
        """
        When we upload a binary file with client.assets.create
        """
        {
            "docs": {
                "set_id": "#SETS._id#",
                "filename": "file_example-jpg.jpg",
                "name": "file example",
                "description": "Test Set restriction allow"
            },
            "filename": "file_example-jpg.jpg"
        }
        """
        Then we get OK response

    Scenario: Ability to retrieve the list of tags used in Assets
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
        When we upload a binary file with client.assets.create
        """
        {
            "docs": {
                "set_id": "#SETS._id#",
                "filename": "file_example-jpg.jpg",
                "name": "Jpeg Example",
                "description": "Jpeg file asset example",
                "tags": [{"code": "publication", "name": "Publication"}]
            },
            "filename": "file_example-jpg.jpg"
        }
        """
        Then we get OK response
        When we upload a binary file with client.assets.create
        """
        {
            "docs": {
                "set_id": "#SETS._id#",
                "filename": "file_example-docx.docx",
                "name": "Docx Example",
                "description": "Docx file asset example",
                "tags": [
                    {"code": "publication", "name": "Publication"},
                    {"code": "docs", "name": "Documents"}
                ]
            },
            "filename": "file_example-docx.docx"
        }
        """
        Then we get OK response
        When we send client.assets.get_tag_codes
        Then we get existing resource
        """
        {
            "tags": ["publication", "docs"]
        }
        """
        When we send client.assets.get_tag_codes
        """
        {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"name.keyword": "Jpeg Example"}}
                    ]
                }
            }
        }
        """
        Then we get existing resource
        """
        {
            "tags": ["publication"]
        }
        """
         When we send client.assets.get_tag_codes
        """
        {
            "size": 1
        }
        """
        Then we get existing resource
        """
        {
            "tags": ["publication"]
        }
        """

    Scenario: Create and update an Asset with external_user_id
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
                "description": "Jpeg file asset example"
            },
            "filename": "file_example-jpg.jpg",
            "external_user_id": "test_user"
        }
        """
        Then we get existing resource
        """
        {
            "set_id": "#SETS._id#",
            "filename": "file_example-jpg.jpg",
            "name": "Jpeg Example",
            "description": "Jpeg file asset example",
            "firstcreated": "#DATE#",
            "versioncreated": "#DATE#",
            "original_creator": "test_user",
            "version_creator": "test_user",
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
            "updates": {"description": "Updated Jpeg file asset example"},
            "external_user_id": "test_user"
        }
        """
        Then we get existing resource
        """
        {
            "set_id": "#SETS._id#",
            "filename": "file_example-jpg.jpg",
            "name": "Jpeg Example",
            "description": "Updated Jpeg file asset example",
            "versioncreated": "#DATE#",
            "version_creator": "test_user"
        }
        """
        When we upload a binary file with client.assets.update
        """
        {
            "item_id": "#ASSETS._id#",
            "headers": {"If-Match": "#ASSETS._etag#"},
            "updates": {"name": "Updated Jpeg Example"},
            "filename": "file_example2-jpg.jpg",
            "external_user_id": "test_user"
        }
        """
        Then we get existing resource
        """
        {
            "name": "Updated Jpeg Example",
            "length": 16549,
            "mimetype": "image/jpeg",
            "versioncreated": "#DATE#",
            "version_creator": "test_user"
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
