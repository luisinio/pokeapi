=============
Poke-berries statistics API
=============

The Poke-berries statistics API provides information about different types of berries.

Requirements
------------

- Python 3.x
- Flask
- requests
- cachetools
- asyncio
- aiohttp
- pytest

Installation
------------

1. Clone the repository:

   .. code-block:: shell

      $ git clone https://github.com/luis/pokeapi.git

2. Navigate to the project directory:

   .. code-block:: shell

      $ cd pokeapi

3. Create a virtual environment:

   .. code-block:: shell

      $ python3 -m venv venv

4. Activate the virtual environment:

   .. code-block:: shell

      $ source venv/bin/activate

5. Install the dependencies:

   .. code-block:: shell

      $ pip install -r requirements.txt

Usage
-----

The API offers the following endpoint to retrieve statistics about the berries:

**Get Berry Statistics**

Endpoint: `/allBerryStats`
Method: GET
Response: JSON with berry statistics

Example response:

.. code-block:: json

   {
       "berries_names": [
           "aguav",
           "apicot",
           "aspear",
           ...
       ],
       "frequency_growth_time": {
           "2": 5,
           "3": 5,
           ...
       },
       "max_growth_time": 24,
       "mean_growth_time": 15.0,
       "median_growth_time": 15.0,
       "min_growth_time": 2,
       "variance_growth_time": 61.5
   }

Contribution
------------

If you wish to contribute to this project, follow these steps:

1. Create a new branch:

   .. code-block:: shell

      $ git checkout -b feature/new-feature

2. Make the necessary changes.

3. Commit your changes:

   .. code-block:: shell

      $ git commit -m "Add new feature"

4. Push your changes to the repository:

   .. code-block:: shell

      $ git push origin feature/new-feature

5. Open a pull request on GitHub.

License
-------

This project is licensed under the MIT License. See the LICENSE file for more details.
