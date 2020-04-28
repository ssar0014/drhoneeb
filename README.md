## **What is an API?**
-	An API is basically a set of rules which lets programs (client and server) communicate in order to get and send information in the form of requests
-	It stands for Application Programming Interface.
-	REST is an architectural style of APIs. The REST architecture allows APIs to be built in a specific way such that a user should be able to get a piece of data or resource, when linked to a specific URL.
-	REST – Representational State Transfer
-	APIs which obey REST architecture are called REST APIs or RESTful APIs.
-	REST APIs are designed to be compliant with HTTP. There are one or more endpoints created which are then exposed to the clients. The clients then communicate with the API using these endpoints via relevant HTTP methods.

-	We will mostly be using the GET and POST requests to upload photos from the app and getting results back

-	There are 2 ways to make HTTP requests with android:

o	`OKhttp` - https://square.github.io/okhttp/

o	`HttpURLConnection` https://developer.android.com/reference/java/net/HttpURLConnection.html

What is Middleware?
* Need to do more research
Web Server Gateway Interface?
* Need to do more research
What Web server should be used?
* Need to do more research


## **Serverless Deep Learning with Tensorflow and AWS**

Why do we want to go serverless?
- A serverless approach is very scalable. It can scale up to 10k concurrent requests without writing any additional logic. It’s perfect for handling random high loads, as it doesn’t take any additional time to scale.
- We don’t have to pay for unused server time. Serverless architectures have pay-as-you-go model. Meaning, if you have 25k requests per month, you will only pay for 25k requests.
- The infrastructure itself becomes a lot easier. You don’t have to handle Docker containers, logic for multiple requests, or cluster orchestration.

However, there are certain limitations of serverless approach:
- AWS Lambda has limits to the number of requests that can be made in a given time
- In some large scale applications, where the number of requests are extremely high - like 10M or more per month, having a dedicated cluster will be better in terms of load handling as well as being cost effective
- Lambda and Tensorflow both take time to startup. This could create problems with applications where near real-time computation is needed.

Since our application is both small scale and does not need real time computation speed, we can go ahead with the Tensorflow and Lambda stack, which also has the following:

1. `API Gateway` for managing requests

2. `AWS Lambda` for processing

3. `S3 Buckets` for holding the trained model

4. `Serverless Framework` for handling deployment and configuration

### More Documentation to Follow

### Need to add a list of current and potential challenges
