Overview
--------

This Project provides a webapp and backend, with the backend built on Python and SQLite.
The architecture is "hexagonal", with a repository pattern (+ Unit of Work pattern; `weird_salads/utils/unit_of_work.py`) for data access.

* Notes on the API/DB design are at (weird_salads/README.rst)[https://github.com/PaulJWright/weird_salads/blob/main/weird_salads/README.rst]

Start the Services
==================

To get started, run the following (for a full breakdown, see `/docker/README.rst`)

.. code:: bash

    cd docker
    docker compose up --build

Here, the docker-compose.yml defines the `location_id` and `quantity` that are used for seeding (`weird_salads/utils/database/seed_db.py`) the database from empty.
The following example during initialisation, shows that the seeding process is complete for location 1 (with a quantity of 1000 for each ingredient).

.. code:: bash

    fastapi-1    | INFO - Starting data seeding process
    fastapi-1    | INFO - Seeding completed successfully for location 1 and quantity 1000.0.

Once these services are running, the FastAPI endpoints can be accessed at http://localhost:8000, and the treamlit front-end at http://localhost:8501
The FastAPI docker image interacts with a SQlite DB that gets initiated in be found at `/data/orders.db`, and can easily viewed through a GUI, e.g. https://sqlitebrowser.org/dl/

FastAPI
-------

The FastAPI endpoints (designed in (weird_salads/README.rst)[https://github.com/PaulJWright/weird_salads/blob/main/weird_salads/README.rst]) are shown below:

.. image:: docs/misc/api_page.png
  :alt: API design

The FastAPI is semi-complete, allowing various tasks, such as viewing and creating orders, updating (deducting) stock

Streamlit
---------

The Streamlit backend is poor, with poor error handling (first time using streamlit, but chosen as a simple frontend), but has limited functionality:

.. image:: docs/misc/streanlit_menu.png
  :alt: API design

.. image:: docs/misc/streanlit_orders_report.png
  :alt: API design


Notes
-----

Positives:
- I spent time on the first day designing the API/Database, and knew that I wanted to build on the repository pattern. I chose to priortise this to reduce the scope of the project and to get a better time estimate of how long it would take
- I chose to prioritise seeding the database with a certain location to reduce the handling of `staff` and `locations` tables.

Negatives:
- I wish I had spent time properly writing unit/integration tests. This is the next thing I would do if I had time.
- I would like to further understand how to implement a proper front-end with the error handling in technology such as React.
- The handling of units in the deduction of ingredients is not complete, and was an oversight.

Summary:
- Overall, I limited scope through fixing a location in the database seeding, and concentrated on MRs that addressed end-to-end changes from the DB through to the frontend app.


Developing
==========

To get started locally, you can install the package and use it as follows:

.. code:: bash

    pip install -e .

Then you can import the utility functions in your Python script:

.. code:: python

    import weird_salads

This codebase uses pre-commit etc.

.. code:: bash

    pre-commit install

.. code:: bash

    (weird_salads) ➜  mad_salads git:(feature/initial_setup) ✗ pre-commit run --all
    ruff.....................................................................Passed
    black....................................................................Passed
    isort....................................................................Passed
    check python ast.........................................................Passed
    check for case conflicts.................................................Passed
    trim trailing whitespace.................................................Passed
    check yaml...............................................................Passed
    debug statements (python)................................................Passed
    check for added large files..............................................Passed
    fix end of files.........................................................Passed
    mixed line ending........................................................Passed
    codespell................................................................Passed


License
-------

This project is Copyright (c) Paul Wright and licensed under
the terms of the GNU GPL v3+ license. This package is based upon
the `Openastronomy packaging guide <https://github.com/OpenAstronomy/packaging-guide>`_
which is licensed under the BSD 3-clause licence. See the licenses folder for
more information.

Contributing
------------

We love contributions! weird_salads is open source,
built on open source, and we'd love to have you hang out in our community.

**Imposter syndrome disclaimer**: We want your help. No, really.

There may be a little voice inside your head that is telling you that you're not
ready to be an open source contributor; that your skills aren't nearly good
enough to contribute. What could you possibly offer a project like this one?

We assure you - the little voice in your head is wrong. If you can write code at
all, you can contribute code to open source. Contributing to open source
projects is a fantastic way to advance one's coding skills. Writing perfect code
isn't the measure of a good developer (that would disqualify all of us!); it's
trying to create something, making mistakes, and learning from those
mistakes. That's how we all improve, and we are happy to help others learn.

Being an open source contributor doesn't just mean writing code, either. You can
help out by writing documentation, tests, or even giving feedback about the
project (and yes - that includes giving feedback about the contribution
process). Some of these contributions may be the most valuable to the project as
a whole, because you're coming to the project with fresh eyes, so you can see
the errors and assumptions that seasoned contributors have glossed over.

Note: This disclaimer was originally written by
`Adrienne Lowe <https://github.com/adriennefriend>`_ for a
`PyCon talk <https://www.youtube.com/watch?v=6Uj746j9Heo>`_, and was adapted by
weird_salads based on its use in the README file for the
`MetPy project <https://github.com/Unidata/MetPy>`_.
