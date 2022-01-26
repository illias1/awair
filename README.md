Task: make two services for processing devices.json file.
The first service is supposed to parse the JSON and save the entries into the second service's DB + expose reading rest API

As I understand (with little background), the file is more accessible for IoT devices to interact. So there is a simple need to bring the updated data to the DB, which is a basic cron job. This is why I thought a cloud function was the best choice. Sure, there is a time limitation in addition to the memory. But this is solvable by calling the same function again and starting from where the previous one ended.
Since a rest API was another requirement, I structured it as an HTTP trigger in the same project. Honestly, I almost never interacted with a rest, so not sure how I did. 

As for the DB, I am used to Hasura from my personal projects and like graphql, so it was quite a natural choice. I could have included Hasura files as well, but since I'm already way behind schedule just going to give you access to the cloud console.

The file is publicly hosted to simplify the job, but there is a way to do the same with an AWS library with authentication. 

To run the project in your local, you need:
- serverless CLI installed
- `virtualenv venv --python=python3`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `sls wsgi serve`

To run the upload simply curl
```
curl -H "Content-Type: application/json" -X POST http://localhost:5000/upload_devices -d '{}'
```
And the endpoints for rest are:
- `/device/<id>`
- `/devices/type/<type>`
- `/devices/status/<status>`
- `/devices`

`limit` and `offset` are query params: `/devices?limit=10&offset=4`
