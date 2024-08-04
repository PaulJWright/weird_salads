Overview
--------
Potential Technologies:

* api (FastAPI)
* data [small data files (if needed), probably where the SQLite DB will be stored...]
* database (scripts alembic migrations)
* inventory [deals with inventory-related tasks]
* order [deals with the order tasks]
* streamlit_app (streamlit frontend)
* tests [openastronomy location for tests]

API Design
==========

.. image:: ../docs/misc/api_design.jpg
  :alt: API Design Doc

Repository Design
=================

Below is the proposed directory structure for the `weird_salads` project:

.. code-block:: text

    weird_salads/
    ├── weird_salads/                   # Main application package
    │   ├── README.rst
    │   ├── data/                       # Small data-related files (/SQLite DB)
    │   ├── database/                   # DB related utils, e.g. alembic
    │   ├── api/                        # FastAPI-related code
    │   │   ├── __init__.py
    │   │   ├── app.py                  # FastAPI app and routers
    │   │   ├── endpoints/
    │   │   ├── schemas/
    │   │   │   ├── orders_schema.py    # Orders Pydantic schemas
    │   │   │   └── inventory_schema.py # Inventory Pydantic schemas
    │   │   └── ...
    │   ├── inventory/                  # Inventory module
    │   │   ├── inventory_service/      # Business logic
    │   │   │   ├── exceptions.py       # inventory-specific exceptions
    │   │   │   ├── inventory_service.py
    │   │   │   └── ...
    │   │   ├── repository/             # Data layer access
    │   │   │   ├── __init__.py
    │   │   │   ├── inventory_repository.py
    │   │   │   ├── models.py
    │   │   │   └── ...
    │   │   └── ...
    │   ├── orders/                     # Orders module (similar to Inventory)
    │   │   ├── orders_service/
    │   │   │   ├── exceptions.py
    │   │   │   ├── orders_service.py
    │   │   │   └── orders.py
    │   │   ├── repository/
    │   │   │   ├── orders_repository.py
    │   │   │   ├── models.py
    │   │   │   └── ...
    │   │   └── ...
    │   ├── streamlit_app/              # Streamlit frontend
    │   ├── tests/                      # Unit and integration tests
    │   ├── utils/                      # Shared utility functions
    │   │   ├── unit_of_work.py         # Unit of work for transaction management
    │   │   └── ...
    │   └── version.py                  # Version information
    └── ...
