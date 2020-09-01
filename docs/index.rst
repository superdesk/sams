.. SAMS documentation master file, created by
   sphinx-quickstart on Wed Jun  3 21:39:11 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to SAMS documentation!
================================
*At Sourcefabric, we develop open-source software for journalism*

.. image:: _static/logo.svg
   :width: 400px
   :alt: Superdesk
   :class: floatinglogo

Welcome. This is the home of SAMS technical documentation. You will learn
here mainly about the SAMS server application and client library.

Server Reference
----------------

Check out this technical reference to understand in detail how the SAMS server
works and can be developed further.

.. toctree::
    :maxdepth: 2

    server/factory
    server/settings
    server/auth
    server/sets
    server/storage/index
    server/assets

API Implementation
------------------

Check out this technical reference to understand in detail how the SAMS server
works and can be developed further.

.. automodule:: sams.api
    :members:

.. toctree::
    :maxdepth: 3

    server/api/service
    server/api/admin
    server/api/consume

Client Reference
----------------

The following is a technical reference for the SAMS Client library.

.. toctree::
    :maxdepth: 2

    client/python/client/index
    client/python/schemas/index
    client/python/auth

API Error Reference
-------------------

The following is a list of all the known errors that can occur.

.. toctree::
   :maxdepth: 2

   errors/base
   errors/system
   errors/config
   errors/http
   errors/resource
   errors/storage_destination
   errors/storage_providers
   errors/sets
   errors/assets

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
