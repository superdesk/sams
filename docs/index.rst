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

Welcome. This is the home of the SAMS technical documentation. You will learn
here mainly about the SAMS server application and client library.

What is SAMS
------------

Super Asset Management Service (a.k.a. SAMS) is an API that provides the
administration, production and consumption of Assets. In SAMS, an Asset is a
file and it's associated metadata.

Assets are stored in a Set, which can be thought of like a storage drive.
Each Set has a dedicated Storage Destination, which can be one of the following:

* Amazon Simple Storage Service (S3)
* MongoDB GridFS

The Asset's binary will be stored using the Set's configured Storage Destination,
while the metadata will be stored in MongoDB and Elasticsearch.

Managing Assets
---------------

All Assets must be managed (created, updated and deleted) through SAMS,
as SAMS contains metadata and actions that are not available across all
storage destination types.

There are two ways to manage these Assets:

* Using the :class:`~sams_client.client.SamsClient` Python client library
* Using the Superdesk SAMS Workspace - a UI to manage Assets in SAMS

We currently do not have a mechanism to import, or synchronise,
existing Assets from S3 or GridFS into SAMS.


Contents
--------

.. toctree::
    :maxdepth: 3

    getting_started
    running
    config
    cli
    technical_reference
    api_reference
    client_reference
    errors
    changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
