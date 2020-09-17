Feature: Sets
    Scenario: Create, update and delete a Set
        When we send client.sets.create
        """
        {
            "docs": [{
                "name": "foo",
                "destination_name": "internal"
            }]
        }
        """
        Then we get existing resource
        """
        {
            "name": "foo",
            "destination_name": "internal",
            "_links": {
                "self": {
                    "title": "Set",
                    "href": "consume/sets/#SETS._id#"
                }
            }
        }
        """
        When we send client.sets.get_by_id
        """
        {"item_id": "#SETS._id#"}
        """
        Then we get existing resource
        """
        {
            "name": "foo",
            "destination_name": "internal",
            "_links": {
                "self": {
                    "title": "Set",
                    "href": "consume/sets/#SETS._id#"
                }
            }
        }
        """
        When we send client.sets.update
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"},
            "updates": {"description": "testing"}
        }
        """
        Then we get existing resource
        """
        {
            "name": "foo",
            "destination_name": "internal",
            "description": "testing"
        }
        """
        When we send client.sets.get_by_id
        """
        {"item_id": "#SETS._id#"}
        """
        Then we get existing resource
        """
        {
            "name": "foo",
            "destination_name": "internal",
            "description": "testing"
        }
        """
        When we send client.sets.delete
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"}
        }
        """
        Then we get OK response
        When we send client.sets.get_by_id
        """
        {"item_id": "#SETS._id#"}
        """
        Then we get error 404

    Scenario: Set must have a name
        When we send client.sets.create
        """
        {"docs": [{"destination_name": "internal"}]}
        """
        Then we get error 400
        """
        {
            "error": "04001",
            "description": "Validation error",
            "errors": {
                "name": ["required"]
            }
        }
        """

    Scenario: validation on posting
        When we send client.sets.create
        """
        {"docs": [{}]}
        """
        Then we get error 400
        """
        {
            "error": "04001",
            "description": "Validation error",
            "errors": {
                "name": ["required"],
                "destination_name": ["required"]
            }
        }
        """
        When we send client.sets.create
        """
        {"docs": [{
            "name": "test",
            "destination_name": "internal",
            "state": "test"
        }]}
        """
        Then we get error 400
        """
        {
            "error": "04001",
            "description": "Validation error",
            "errors": {
                "state": ["unallowed value test"]
            }
        }
        """

    Scenario: destination_name must exist
        When we send client.sets.create
        """
        {"docs": [{
            "name": "foo",
            "destination_name": "bar"
        }]}
        """
        Then we get error 400
        """
        {
            "error": "07004",
            "description": "Destination \"bar\" isnt configured"
        }
        """
        Given server config
        """
        {
            "STORAGE_DESTINATION_1": "MongoGridFS,internal,mongodb://#DB_HOST#/tests_sams",
            "STORAGE_DESTINATION_2": "MongoGridFS,bar,mongodb://#DB_HOST#/tests_sams"
        }
        """
        When we send client.sets.create
        """
        {"docs": [{
            "name": "foo",
            "destination_name": "bar"
        }]}
        """
        Then we get OK response
        When we send client.sets.update
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"},
            "updates": {"destination_name": "unknown"}
        }
        """
        Then we get error 400
        """
        {
            "error": "07004",
            "description": "Destination \"unknown\" isnt configured"
        }
        """
        When we send client.sets.update
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"},
            "updates": {"destination_name": "internal"}
        }
        """
        Then we get OK response

    Scenario: Cannot change destination when Set is not draft
        Given server config
        """
        {
            "STORAGE_DESTINATION_1": "MongoGridFS,internal,mongodb://#DB_HOST#/tests_sams",
            "STORAGE_DESTINATION_2": "MongoGridFS,bar,mongodb://#DB_HOST#/tests_sams"
        }
        """
        When we send client.sets.create
        """
        {"docs": [{
            "name": "foo",
            "destination_name": "bar",
            "destination_config": {"test": 1}
        }]}
        """
        Then we get OK response
        When we send client.sets.update
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"},
            "updates": {
                "destination_name": "internal",
                "destination_config": {"test": 2},
                "state": "usable"
            }
        }
        """
        Then we get OK response
        When we send client.sets.update
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"},
            "updates": {"destination_name": "bar"}
        }
        """
        Then we get error 400
        """
        {
            "error": "07002",
            "description": "Destination can only be changed in draft state"
        }
        """
        When we send client.sets.update
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"},
            "updates": {"destination_config": {"test": 3}}
        }
        """
        Then we get error 400
        """
        {
            "error": "07003",
            "description": "Destination config can only be changed in draft state"
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
        Then we get OK response
        When we send client.sets.update
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"},
            "updates": {"destination_name": "bar"}
        }
        """
        Then we get error 400
        """
        {
            "error": "07002",
            "description": "Destination can only be changed in draft state"
        }
        """
        When we send client.sets.update
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"},
            "updates": {"destination_config": {"test": 3}}
        }
        """
        Then we get error 400
        """
        {
            "error": "07003",
            "description": "Destination config can only be changed in draft state"
        }
        """

    Scenario: Cannot change state back to draft
        When we send client.sets.create
        """
        {"docs": [{
            "name": "foo",
            "destination_name": "during_draft"
        }]}
        """
        Then we get OK response
        When we send client.sets.update
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"},
            "updates": {"state": "usable"}
        }
        """
        Then we get OK response
        When we send client.sets.update
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"},
            "updates": {"state": "draft"}
        }
        """
        Then we get error 400
        """
        {
            "error": "07001",
            "description": "Cannot change state from \"usable\" to draft"
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
        Then we get OK response
        When we send client.sets.update
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"},
            "updates": {"state": "draft"}
        }
        """
        Then we get error 400
        """
        {
            "error": "07001",
            "description": "Cannot change state from \"disabled\" to draft"
        }
        """
        When we send client.sets.update
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"},
            "updates": {"state": "usable"}
        }
        """
        Then we get OK response

    Scenario: Cannot delete a Set that is usable or disabled with assets
        When we send client.sets.create
        """
        {"docs": [{
            "name": "test1",
            "destination_name": "during_draft"
        }]}
        """
        Then we get OK response
        When we send client.sets.delete
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"}
        }
        """
        Then we get OK response
        When we send client.sets.create
        """
        {"docs": [{
            "name": "test2",
            "destination_name": "during_draft"
        }]}
        """
        Then we get OK response
        When we send client.sets.update
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"},
            "updates": {"state": "usable"}
        }
        """
        Then we get OK response
        When we send client.sets.delete
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"}
        }
        """
        Then we get error 400
        """
        {
            "error": "07005",
            "description": "Can only delete Sets that are in draft state or disabled with no assets"
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
        Then we get OK response
        When we send client.sets.delete
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"}
        }
        """
        Then we get OK response
        When we send client.sets.create
        """
        {"docs": [{
            "name": "test3",
            "destination_name": "during_draft"
        }]}
        """
        Then we get OK response
        When we send client.sets.update
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"},
            "updates": {"state": "usable"}
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
        Then we get OK response
        When we send client.sets.update
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"},
            "updates": {"state": "disabled"}
        }
        """
        Then we get OK response
        When we send client.sets.delete
        """
        {
            "item_id": "#SETS._id#",
            "headers": {"If-Match": "#SETS._etag#"}
        }
        """
        Then we get error 400
        """
        {
            "error": "07005",
            "description": "Can only delete Sets that are in draft state or disabled with no assets"
        }
        """
        
    Scenario: cant consume through admin interface
        When we get "/admin/sets"
        Then we get response code 405
        When we get "/admin/sets/5ef401857da9e6d2795d7882"
        Then we get response code 405

    Scenario: cant manage through consume interface
        When we post "/consume/sets"
        Then we get response code 405
        When we patch "/consume/sets"
        Then we get response code 405
        When we delete "/consume/sets/5ef401857da9e6d2795d7882"
        Then we get response code 405

    Scenario: searching sets
        When we send client.sets.create
        """
        {"docs": [
            {"name": "set1", "destination_name": "internal", "description": "set 1 test", "state": "draft"},
            {"name": "set2", "destination_name": "internal", "description": "set 2 foo", "state": "usable"},
            {"name": "set3", "destination_name": "internal", "description": "set 3 test", "state": "draft"}
        ]}
        """
        Then we get OK response
        When we send client.sets.search
        """
        {"params": {
            "where": "{\"name\": \"set2\"}"
        }}
        """
        Then we get existing resource
        """
        {
            "_items": [
                {"name": "set2", "destination_name": "internal", "description": "set 2 foo"}
            ],
            "_meta": {
                "page": 1,
                "total": 1
            }
        }
        """
        When we send client.sets.search
        """
        {"params": {
            "where": "{\"state\": \"draft\"}"
        }}
        """
        Then we get existing resource
        """
        {
            "_items": [
                {"name": "set1", "destination_name": "internal", "description": "set 1 test", "state": "draft"},
                {"name": "set3", "destination_name": "internal", "description": "set 3 test", "state": "draft"}
            ],
            "_meta": {
                "page": 1,
                "total": 2
            }
        }
        """
        When we send client.sets.search
        """
        {"params": {
            "page": 1,
            "sort": "[[\"name\", 1]]",
            "max_results": 1
        }}
        """
        Then we get existing resource
        """
        {
            "_items": [
                {"name": "set1", "destination_name": "internal", "description": "set 1 test", "state": "draft"}
            ],
            "_meta": {
                "page": 1,
                "total": 3,
                "max_results": 1
            }
        }
        """
        When we send client.sets.search
        """
        {"params": {
            "page": 2,
            "sort": "[[\"name\", 1]]",
            "max_results": 1
        }}
        """
        Then we get existing resource
        """
        {
            "_items": [
                {"name": "set2", "destination_name": "internal", "description": "set 2 foo", "state": "usable"}
            ],
            "_meta": {
                "page": 2,
                "total": 3,
                "max_results": 1
            }
        }
        """
        When we send client.sets.search
        """
        {"params": {
            "page": 3,
            "sort": "[[\"name\", 1]]",
            "max_results": 1
        }}
        """
        Then we get existing resource
        """
        {
            "_items": [
                {"name": "set3", "destination_name": "internal", "description": "set 3 test", "state": "draft"}
            ],
            "_meta": {
                "page": 3,
                "total": 3,
                "max_results": 1
            }
        }
        """
        When we send client.sets.search
        """
        {"params": {
            "page": 4,
            "sort": "[[\"name\", 1]]",
            "max_results": 1
        }}
        """
        Then we get existing resource
        """
        {
            "_items": [],
            "_meta": {
                "page": 4,
                "total": 3,
                "max_results": 1
            }
        }
        """
