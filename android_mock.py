#!/usr/bin/python2.7
#-*- coding: utf-8 -*-
#
# Authors:
#    Antonio Robres
#

from bottle import run, post, request, error, route, HTTPError, get
import ujson
from optparse import OptionParser
from collections import deque

response_template = {'failure': 0,
                     'canonical_ids': 0,
                     'success': 0,
                     'multicast_id': 6616353152392206975,
                     'results': []
                     }
responses_saved = deque()
requests_handled = deque()
responses_error = deque()
device_notifications = []
headers = []


@error(404)
def error404(error):

    return 'Nothing here, sorry'


@post("/")
def return_response():
    '''
    Response with a GCM response mocked. If there are saved responses in the dict "responses_saved", send the first
     response and deletes it. If there isn't responses saved before, send a GCM response with all the receivers as
     success.
    :return: code error or json body with response saved or with all the receivers success.
    '''

    data = request.body.read()
    headers.append(request.headers.items())
    body_received = ujson.loads(data)
    requests_handled.append(body_received)
    response = response_template
    if responses_error:
        response_error = responses_error.popleft()
        print "MOCKING GCM ERROR RESPONSE: {}".format(response_error)
        return HTTPError(int(response_error), "['Internal Server Error']")

    elif not responses_saved:
        response['success'] = len(body_received['registration_ids'])
        for x in range(len(body_received['registration_ids'])):
            response['results'].append(({u'message_id': u'0:1370674827295849'}))
    else:
        response = responses_saved.popleft()
        print "MOCKING GCM RESPONSE: {}".format(response)

    return ujson.dumps(response)


@post("/save_response")
def save_response():
    '''
    Store the body provided in a dict to be used later.
    :return: 200 OK
    '''
    data = request.body.read()
    body_received = ujson.loads(data)
    responses_saved.append(body_received)
    return 'OK'


@route("/reset_responses")
def reset_responses():
    """Reset all the saved responses (including the Error responses saved)
    :return: 200 responses deleted
    """
    responses_saved.clear()
    responses_error.clear()
    print "Responses: {} | Errors: {}".format(responses_saved, responses_error)
    return 'responses deleted'


@get("/get_responses")
def get_responses():
    """get all the saved responses.
    :return: 200 JSON with all the responses
    """

    return ujson.dumps(responses_saved)


@route("/reset_stats")
def reset_stats():
    """Reset all the stats
    :return: 200 stats reset
    """
    requests_handled.clear()
    del headers[:]
    del device_notifications[:]
    return 'stats reset'


@route("/stats")
def stats():
    """
    Retrieve all the stats available including a list with all the requests received
    :returns: 200 JSON with all the requests received
    """

    body = {'num_requests': len(requests_handled),
            'requests': list(requests_handled)}
    return ujson.dumps(body)


@post("/save_error")
def save_error():
    """
    Save an error to be included in the following responses
    :returns: 200 OK
    """
    data = request.body.read()
    responses_error.append(data)
    return 'OK'


@get("/get_errors")
def get_error():
    """
    Obtain a list with all the errors
    :returns: 200 JSON with all the errors
    """
    return ujson.dumps(responses_error)


@route("/get_header")
def get_header():
    """
     Retrieve all the headers obtained in the requests
     :returns: JSON with all the headers
    """
    body = {'headers': headers}
    return ujson.dumps(body)


def main():

    parser = OptionParser()
    parser.add_option(
        "-p", "--port",
        dest="port",
        help="Server port [%default]",
        type="int",
        default=8082)

    parser.add_option(
        "-b", "--bind_address",
        dest="bind",
        help="Bind addreess [%default]",
        default="0.0.0.0")

    (options, args) = parser.parse_args()

    print "Starting server on %s:%s" % (options.bind, int(options.port))
    run(host=options.bind, port=options.port, debug=True, reloader=True)


if __name__ == "__main__":
    main()
