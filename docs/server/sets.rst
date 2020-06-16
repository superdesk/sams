.. _sets:

Sets
====
A set a collection of *Assets*. It is used as a way to organise and restrict access to
the *Assets* it holds.

All access to the binary or metadata of assets will go through this service. There must
be at least one Set configured in the system.

A single Set can be designated as the default Set. When access is requested to an asset
without a set being provided, the default set will be used.

Usage
----
.. automodule:: sams.sets
    :members: service

Resource Schema
---------------
.. autoclass:: sams.sets.resource.SetsResource
    :members: url,endpoint_name,internal_resource
    :undoc-members:

States
------
.. automodule:: sams.sets.resource
    :members: SET_STATES

Storage Destination
-------------------
The ``destination_name`` and ``destination_config`` will determine where the assets will
be stored.

The value of ``destination_name`` must exist in the ``STORAGE_DESTINATIONS`` application
config.

The ``destination_config`` will compliment the ``destination_name`` with a additional
config attributes specific to the set.

Service
-------
.. autoclass:: sams.sets.service.SetsService
    :members: validate_patch,on_delete
