import http.client
import json

def send_request(conn, method, url, payload_object, headers=None):
    if headers is None:
        headers = {'Content-Type': 'application/json'}
    payload = json.dumps(payload_object)
    conn.request(method, url, payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
    return json.loads(data.decode("utf-8"))

appConn = http.client.HTTPConnection("localhost", 3000)

print('Test GET /hello')
response = send_request(appConn, 'GET', '/hello', {})
print('Response', response)
assert response['status'] == 'ok'
assert response['response'] == 'hello world'

print('Test GET /hello/Marijan')
response = send_request(appConn, 'GET', '/hello/Marijan', {'name': 'Marijan'})
print('Response', response)
assert response['status'] == 'ok'
assert response['response'] == 'hello Marijan'


serviceConn = http.client.HTTPConnection("localhost", 3001)

print('Test POST /api/v1/hello')
response = send_request(serviceConn, 'POST', '/api/v1/hello/', {'params': []})
print('Response', response)
print(response)
assert response['status'] == 'ok'
assert response['result'] == 'hello world'


print('Test POST /api/v1/hello (with parameter')
response = send_request(serviceConn, 'POST', '/api/v1/hello/', {'params': ['Marijan']})
print('Response', response)
assert response['status'] == 'ok'
assert response['result'] == 'hello Marijan'
