android_gcm_mock
============

Implementation of Android Mock allowing several configurations


## HOW TO RUN THE ANDROID GCM MOCK

    pyhton android_mock.py --port 8081 ----bind_address 0.0.0.0

    The application is started in localhost using the 8081 port and allowing connections from all the hosts

##Usage


### Basic Usage

    The mock emulates the Android GCM behaviour. To obtain a response emulating the Android GCM send a request to the
    http:{host}:{port}/

    If no error responses_saved or error_saved the mock returns a 200 OK with the following body

    ´´´
    response_template = {'failure': 0,
                     'canonical_ids': 0,
                     'success': len(registrations_id),
                     'multicast_id': 6616353152392206975,
                     'results': []
                     }
    ´´´

    for every registration_id included in the request, a result is added in the result list.

    If there are some responses saved before, the response served to the client is the response saved.

    If there are some error saved before, the response served to the client is the error saved.

    The behaviour of the Android GCM Mock follow the following logic:

    if error saved:
        return error saved
    elif response saved:
        return response saved
    else:
        return 200 OK and response with all the registrations_ids as success


### Save response

    To save a response send a request to the following path:

    http:{host}:{port}/save_response

    In the body should be included the response to be served by the mock.

    The response is saved in a queue with FIFO logical.

    The server responses with 200 OK


### Save error

    To save a error send a request to the following path:

    http:{host}:{port}/save_error

    In the body should be included only the HTTP error code to be served by the mock.

    The response is saved in a queue with FIFO logical.

    The server responses with 200 OK

### Reset Errors and responses

    To reset the errors send a request to the following path:

    http:{host}:{port}/reset_responses

    The server responses with 200 responses deleted


### Retrieve errors

    To get all the errors send a request to the following path:

    http:{host}:{port}/get_errors

    The server responses with 200 and JSON with all the errors saved


### Retrieve responses

    To get all the responses send a request to the following path:

    http:{host}:{port}/get_responses

    The server responses with 200 and JSON with all the responses saved


### Stats

    The mock include statistics to obtain all the headers received and all the bodies.

    To get all the bodies received in the mock send a request to:

    http:{host}:{port}/stats

    To get all the headers received in the mock send a request to:

    http:{host}:{port}/get_headers

    To reset all the stats send a request to:

    http:{host}:{port}/reset_stats
