# ApolloMed Technical Interview
## Date: May 4, 2023

## Overview
This simple program utilizes Amazon's API gateway and Lambda to perform some tasks (through the Lambda function) and returns a `json` to the client. In this particular example, we're taking in a set of grades and returning some measures of central tendency.

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

