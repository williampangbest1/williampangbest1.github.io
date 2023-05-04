# ApolloMed Technical Interview
## Date: May 4, 2023

## Overview
This simple program utilizes Amazon's API gateway and Lambda to perform some tasks (through the Lambda function) and returns a `json` to the client. In this particular example, we're taking in a set of grades and returning some measures of central tendency.

The code for the lambda function can be found on [lambda_function.py](https://github.com/williampangbest1/williampangbest1.github.io/blob/main/projects/simpleGradesapi/lamda_function.py).

### Usage
To test it out yourself, you can use the below PATH:
<a>https://aip93x2bi0.execute-api.us-west-2.amazonaws.com/getData</a> . This is configured under the GET route (I also have setup a dummy POST route, more on that later) and is used to fetch data. If you were to click on the link right now, you will get an error that says `{"message":"Not Found"}`. This is because no input arguments have been given and as such this error message was generated. 

The lambda function is currently configured to take in {key:value} pairs for five students, named `student1`, `student2`, `student3`, `student4`, `student5`. To make it easy to input this information, I suggest using a website such as [Postman](https://www.postman.com), which has a custom GUI that automatically converts the key value pair inputs into HTML arguments (and does many other things, of course). 

![postman-figure](https://github.com/williampangbest1/williampangbest1.github.io/blob/main/projects/simpleGradesapi/img/postman_demo.png)

You can, of course, entering things manually yourself as well. The query begins after the PATH, followed by a delimiter `?`. The key comes first, followed by the value. For instance, if we want to enter the exam score of `student1` and `student2`, we want to type `PATH?student1=10&student2=50`. The entire query used is reproduced below:

<a>https://aip93x2bi0.execute-api.us-west-2.amazonaws.com/getGrades?student1=10&student2=50&student3=100&student4=30&student5=-10</a>

What should be returned is a `json` that contains measures of the central tendency that has been computed using `numpy`. For the above key value pairs, I got:

`{"Mean": "36.0", "Median": "30.0", "Std": "37.74"}`.

Feel free to test with other values!

### Setting Up API Gateway
Setting up API Gateway was relatively simple thanks to its simply GUI (*before that, I was playing with ElasticBeanstalk and spent a lot of time debugging the security permissions through IAM and using the eb-command line interface to upload my app to perform some simple sentiment analysis, but happy to discuss that later*) 

![apigateway-figure](https://github.com/williampangbest1/williampangbest1.github.io/blob/main/projects/simpleGradesapi/img/postman_demo.png)

The main takehome message is that you need to link the API to your lambda function, and then setup different routes (if you so choose). I decided to setup a GET and POST route as the GET route is used to fetch data (say making a query from a database stored in a s3 bucket on AWS), and the POST route would be used to write to the database. 

As such, you can call the POST route as well, which I've called `/addGrades`.

<a>https://aip93x2bi0.execute-api.us-west-2.amazonaws.com/addGrades</a>

This currently does not work as there is nothing to write to the database! As such, you'll get a message that simply says "This has not been implemented yet".

![postman-addGrades](https://github.com/williampangbest1/williampangbest1.github.io/blob/main/projects/simpleGradesapi/img/postman_addGrades.png)

### Setting Up Lambda
Setting up Lambda wasn't too trcky intially, until I realized that getting Python packages (such as pandas) loaded was not as straightfoward as I thought. I intially set up the environment to work with `python 3.10` (the latest release as of writing), but there no inherent support for pandas on Lambda. As such, I had to go download the respective packages myself from Python's website, un-wheel it, put everything into a folder called `python`, then upload it back to Lambda as a custom layer. Even though I followed all the steps recommended online, I was unable to get it working as some dependencies were probably not supported, and as such I gave up. I then realized that for `python 3.9` (and probably lower), AWS offers a pre-loaded layer that allows for Pandas integration. With that figured out, it was only a click of a button to get Pandas working.

![lambda-Pandas](https://github.com/williampangbest1/williampangbest1.github.io/blob/main/projects/simpleGradesapi/img/lambda_pandas.png)

And with that, I was off to writing code!

### Debugging, CloudWatch
The trickiest part was debugging because the error statements are not very clear, unlike running Python code on an IDE like VSCode. For instance, if you missed a bracket or a comma and try deploying, you would still be able to deploy but will be greeted with this message when you test the URL:

```{"message":"Internal Server Error"}```

One tool that can help with debugging (in addition to adding breakpoints and running the code sequentially) is to use AWS Cloudwatch.

To understand what the parameters are being received, you can write a simple lambda function that prints out the information being fed in into the Cloudwatch log.

For instance:

```
import json

def lambda_handler(event, context):
    # TODO implement
    print(event)
```

We can then check our logs:
![cloudwatch](https://github.com/williampangbest1/williampangbest1.github.io/blob/main/projects/simpleGradesapi/img/cloudwatch.png)

This is a bit messy, so you can use a parser such as [this one](https://jsonformatter.curiousconcept.com) from CuriousConcept to make it legible and pretty. 

```
{
   "version":"2.0",
   "routeKey":"GET /get",
   "rawPath":"/get",
   "rawQueryString":"",
   "headers":{
      "accept":"*/*",
      "accept-encoding":"gzip, deflate, br",
      "cache-control":"no-cache",
      "content-length":"0",
      "host":"9nv5qhfufg.execute-api.us-west-2.amazonaws.com",
      "postman-token":"[REMOVED]",
      "user-agent":"PostmanRuntime/7.32.2",
      "x-amzn-trace-id":"[REMOVED]",
      "x-forwarded-for":"76.119.158.11",
      "x-forwarded-port":"443",
      "x-forwarded-proto":"https"
   },
   "requestContext":{
      "accountId":"[REMOVED]",
      "apiId":"9nv5qhfufg",
      "domainName":"9nv5qhfufg.execute-api.us-west-2.amazonaws.com",
      "domainPrefix":"9nv5qhfufg",
      "http":{
         "method":"GET",
         "path":"/get",
         "protocol":"HTTP/1.1",
         "sourceIp":"[REMOVED]",
         "userAgent":"PostmanRuntime/7.32.2"
      },
      "requestId":"EZtXeh4wvHcEJ1A=",
      "routeKey":"GET /get",
      "stage":"$default",
      "time":"04/May/2023:14:35:01 +0000",
      "timeEpoch":1683210901920
   },
   "isBase64Encoded":false
}
```
Notice here that we get 



