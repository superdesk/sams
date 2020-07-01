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
            "_status": "ERR",
            "_issues": {"name": {"required": 1}},
            "_error": {
                "code": 400,
                "message": "Insertion failure: 1 document(s) contain(s) error(s)"
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
            "_status": "ERR",
            "_issues": {
                "name": {"required": 1},
                "destination_name": {"required": 1}
            },
            "_error": {
                "code": 400,
                "message": "Insertion failure: 1 document(s) contain(s) error(s)"
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
            "_status": "ERR",
            "_issues": {
                "state": "unallowed value test"
            },
            "_error": {
                "code": 400,
                "message": "Insertion failure: 1 document(s) contain(s) error(s)"
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
            "error": "Destination \"bar\" isnt configured",
            "message": {"destination_name": {"exists": 1}},
            "code": 400
        }
        """
        Given app config
        """
        {
            "STORAGE_DESTINATION_1": "MongoGridFS,internal,mongodb://localhost/tests_sams",
            "STORAGE_DESTINATION_2": "MongoGridFS,bar,mongodb://localhost/tests_sams"
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
        # TODO: Make error response consistent regardless of HTTP method used
        #       This is due to the way Eve reports errors on POST and PATCH differently
        Then we get error 400
        """
        {
            "_issues": {"validator exception": "400: Destination \"unknown\" isnt configured"},
            "_status": "ERR"
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
        Given app config
        """
        {
            "STORAGE_DESTINATION_1": "MongoGridFS,internal,mongodb://localhost/tests_sams",
            "STORAGE_DESTINATION_2": "MongoGridFS,bar,mongodb://localhost/tests_sams"
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
        # TODO: Make error response consistent regardless of HTTP method used
        #       This is due to the way Eve reports errors on POST and PATCH differently
        Then we get error 400
        """
        {
            "_issues": {"validator exception": "400: Destination can only be changed in draft state"},
            "_status": "ERR"
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
        # TODO: Make error response consistent regardless of HTTP method used
        #       This is due to the way Eve reports errors on POST and PATCH differently
        Then we get error 400
        """
        {
            "_issues": {"validator exception": "400: Destination config can only be changed in draft state"},
            "_status": "ERR"
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
        # TODO: Make error response consistent regardless of HTTP method used
        #       This is due to the way Eve reports errors on POST and PATCH differently
        Then we get error 400
        """
        {
            "_issues": {"validator exception": "400: Destination can only be changed in draft state"},
            "_status": "ERR"
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
        # TODO: Make error response consistent regardless of HTTP method used
        #       This is due to the way Eve reports errors on POST and PATCH differently
        Then we get error 400
        """
        {
            "_issues": {"validator exception": "400: Destination config can only be changed in draft state"},
            "_status": "ERR"
        }
        """

    Scenario: Cannot change state back to draft
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
        # TODO: Make error response consistent regardless of HTTP method used
        #       This is due to the way Eve reports errors on POST and PATCH differently
        Then we get error 400
        """
        {
            "_issues": {"validator exception": "400: Cannot change state from \"usable\" to draft"},
            "_status": "ERR"
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
        # TODO: Make error response consistent regardless of HTTP method used
        #       This is due to the way Eve reports errors on POST and PATCH differently
        Then we get error 400
        """
        {
            "_issues": {"validator exception": "400: Cannot change state from \"disabled\" to draft"},
            "_status": "ERR"
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

    Scenario: Cannot delete a Set that is not draft
        When we send client.sets.create
        """
        {"docs": [{
            "name": "test1",
            "destination_name": "bar"
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
            "destination_name": "bar"
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
            "error": "Can only delete Sets that are in draft state",
            "message": "Can only delete Sets that are in draft state",
            "code": 400
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
        Then we get error 400
        """
        {
            "error": "Can only delete Sets that are in draft state",
            "message": "Can only delete Sets that are in draft state",
            "code": 400
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
        {"args": {"where": {"name": "set2"}}}
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
        {"args": {"where": {"state": "draft"}}}
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
        {"args": {
            "page": 1,
            "sort": [["name", 1]],
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
        {"args": {
            "page": 2,
            "sort": [["name", 1]],
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
        {"args": {
            "page": 3,
            "sort": [["name", 1]],
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
        {"args": {
            "page": 4,
            "sort": [["name", 1]],
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
