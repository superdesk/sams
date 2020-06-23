:mod:`sams.sets` -- Internal Service for Sets
=============================================

.. automodule:: sams.sets


Resource Schema
---------------
.. autoclass:: sams.sets.resource.SetsResource
    :members: url,endpoint_name,internal_resource
    :undoc-members:

States
------
.. automodule:: sams.sets.resource
    :members: SET_STATES

Service
-------
.. autoclass:: sams.sets.service.SetsService
    :members: validate_patch,on_delete
