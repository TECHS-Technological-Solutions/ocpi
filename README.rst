=======
Py-OCPI
=======

.. image:: https://img.shields.io/pypi/v/py-ocpi.svg?style=flat
   :target: https://pypi.org/project/py-ocpi/
.. image:: https://pepy.tech/badge/py-ocpi/month
   :target: https://pepy.tech/project/py-ocpi
.. image:: https://github.com/TECHS-Technological-Solutions/ocpi/workflows/pypi/badge.svg
   :target: https://github.com/TECHS-Technological-Solutions/ocpi/actions?query=workflow:pypi
.. image:: https://coveralls.io/repos/github/TECHS-Technological-Solutions/ocpi/badge.svg
   :target: https://coveralls.io/github/TECHS-Technological-Solutions/ocpi
   
Introduction
============

This Library is a Python implementation of the Open Charge Point Interface (OCPI)


Getting Started
===============

Installation
------------

install Py-OCPI like this:

.. code-block:: bash

    pip install py-ocpi


How Does it Work?
-----------------

Modules that communicate with central system will use crud for retrieving required data. the data that is retrieved from central system may
not be compatible with OCPI protocol. So the data will be passed to adapter to make it compatible with schemas defined by OCPI. User only needs to
modify crud and adapter based on central system architecture.

Example
-------

https://github.com/TECHS-Technological-Solutions/ocpi/blob/830dba5fb3bbc7297326a4963429d7a9f850f28d/examples/v_2_2_1.py#L1-L205

License
=======

This project is licensed under the terms of the MIT license.
