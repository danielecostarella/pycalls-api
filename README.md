# pycalls-api
RESTful APIs for managing and storing call and contact information using Python FastAPI.

API Endpoints
-------------

### Contacts

*   `GET /api/contacts/`: Get all existing contacts
*   `POST /api/contacts/{contactId}`: Create a new contact
*   `DELETE /api/contacts/{contactId}`: Delete an existing contact
*   `PATCH /api/contacts/{contactId}`: Update an existing contact

### Calls

*   `GET /api/calls`: Get all call registry
*   `POST /api/calls`: Create a new call entry
*   `GET /api/calls/{callId}`: Get a call by Id
*   `DELETE /api/calls/{callId}`: Delete a call entry
*   `PATCH /api/calls/{callId}`: Update an existing call entry

### Find a Number

*   `GET /api/find-contact-by-number/{number}`: Get a contact from a number. This endpoint is used to look for the contact when there is an incoming call.

Installation
------------

To install and run the CID Management System REST API, follow these steps:

1.  Clone this repository: `git clone https://github.com/danielecostarella/pycalls-api.git`
2.  Navigate to the project directory: `cd pycalls-api`
3.  Install the required packages: `pip install -r requirements.txt`
4.  Run the API: `uvicorn app.main:app --host localhost --port 8000 --reload`

Usage
-----

Once the API is running, you can use any HTTP client to make requests to the API endpoints. For example, you can use `curl` to make a `GET` request to the `api/contacts` endpoint:

    curl http://localhost:8000/api/contacts

This will return a JSON response containing all the contacts in the directory.

Contributing
------------

If you'd like to contribute to this project, please follow these steps:

1.  Fork this repository.
2.  Create a new branch for your feature: `git checkout -b feature/your-feature`
3.  Implement your feature and test it.
