# License-Plate-Recognition
Automatic license plate recognition service implemented using kubernetes.

Overview
This project creates a kubernetes cluster that provides a REST API for scanning images that contain geotagged license plates and records them in a database.
The following services were deployed:
rest - the REST frontend will accept images for analysis and handle queries concerning specific license plates and geo-coordinates. The REST worker will queue tasks to workers using rabbitmq messages.

worker - Worker nodes will receive work requests to analyze images. If those images contain both a geo-tagged image and a vehicle with a license plate that can be scanned, the information is entered into the REDIS database.

rabbitmq - One node, which should be named rabbitmq should act as the rabbit-mq broker. 

redis - One node, which should be named 'redis' should provide the redis database server.

The worker will use the open source automatic license plate reader software. This is an open-source component of a more comprehensive commercial offering. One of the commercial components includes a web service similar to what we're building.

Suggested Steps
You should first deploy the rabbitmq and redis deployments because they're easy, particularly if you deploy the versions provided by the developers. For each of those, you'll need to specify a deployment and then create a Service for that deployment. Following that, you should construct the rest server because you can use that to test your redis database connection as well as connections to rabbitmq and your debugging interface. Lastly, start on the worker.

Although not explicitly required, you should create a simple python program that connects to the debugging topic exchange as described in rabbitmq. You can use that to subscribe to any informational or debug messages to understand what's going on. It's useful to deploy that service as a "logs" pod (or deployment) so you can monitor the output using kubectl logs logs-<unique id for pod>

You should use version numbers for your container images. If you're in a edit/deploy/debug cycle, your normal process to deploy new code will be to push a new container image and then delete the existing pod (rest or worker). At that point, the deployment will create a new pod. If you're using version numbers, you'll be able to insure that you're running the most recent code.

Each subdirectory contains directions in the appropriate README file. The images directory contains test images.

beetle.jpg is not geotagged and has one visible license plate (309-OJN)
car.jpg is not geotagged but has one visible license (CZTHEDA)
geotagged.jpg is geotagged but has no cars
the-meat-car.jpg is geotagged and has one visible license (789-SJL but reported as 7B9SJLD)
The plate1.png image is a PNG image -- you can use this to test what happens when non-jpg files are submitted.
