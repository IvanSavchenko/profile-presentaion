"""Scripts for current app."""

from httperfpy import Httperf

from app.extensions import batch


@batch.option('-h', '--host', dest='host', default='127.0.0.1',
              help='Host which make requests.')
@batch.option('-p', '--port', dest='port', default=5000,
              help='Port for address.')
@batch.option('-u', '--uri', dest='uri', default='/',
              help='Set up current url for request.')
@batch.option('-n', '--num-counts', dest='num', default=1000,
              help='Number of connection to current address.')
@batch.option('-r', '--rate', dest='rate', default=25,
              help='Number of packges per second will be send.')
def make_connections(host, port, uri, num, rate):
    """Script function to make number of connection to define address.

    Example: python jsonapi.py -h 127.0.01 -p 5000 -u /user -n 1000 -r 100
    """
    perf = Httperf(server=host, port=port, uri=uri, num_conns=num,
                   rate=rate)

    perf.parser = True
    results = perf.run()

    print results['connection_time_avg'] + 'is_avg'
    print results['connection_time_max'] + 'is_max'

    return True
