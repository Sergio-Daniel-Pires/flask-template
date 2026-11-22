[[ project_name ]] documentation
================================

This documentation covers implementation, development, deployment, and data
decisions. API schemas live only in Swagger.

Start the API and open <http://localhost:5000/api/docs> for the API reference.

.. toctree::
   :maxdepth: 2

   architecture
   development
   testing
   api
   deployment
[[#if database]]
   database
[[/if]]

Security
--------

The security baseline and consciously accepted risks (ACK) are recorded in
``SECURITY.md`` at the project root. API-only documentation stays in Swagger;
implementation details stay in this Sphinx tree.
