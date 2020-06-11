.. _sets:

Sets
====

Usage
-----

.. automodule:: sams.sets

.. autodata:: service

The Set service instance can be found under :data:`sams.sets.service` and used all::

    from sams.sets import service as sets_service

    def test_sets():
        sets_service.post([{....}])
        sets_service.patch(set_id, {...})
        sets_service.delete_action({...})
        sets_service.find({...})

This service instance can only be used after the application has bootstrapped.

Resource Schema
---------------

.. automodule:: sams.sets.resource

The schema is:

``_id`` *bson.ObjectId*

    Globally unique id, generated automatically by the system.

``state`` *string*

    The state of the Set. One of ``draft|usable|disbled``.

    .. autodata:: resource.set_states

``name`` *string*

    Unique name for the Set

``description`` *string*

    A short description on what this set is designated for

``destination_name`` *string*

    The name of a system configured destination (to be developed)

``destination_config`` *dict*

    A dictionary containing the configuration options for the specific destination used


Service
----------

.. automodule:: sams.sets.service

.. autoclass:: SetsService
    :members: validate_patch,on_delete
