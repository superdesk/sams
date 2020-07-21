:mod:`sams.assets` -- Internal Service for Assets
=================================================

.. automodule:: sams.assets


Resource Schema
---------------
.. autoclass:: sams.assets.resource.AssetsResource
    :members: url,endpoint_name,internal_resource
    :undoc-members:

Service
-------
.. autoclass:: sams.assets.service.AssetsService
    :members: post,patch,on_deleted,upload_binary,download_binary
    :member-order: bysource
