## Download API V1

## Endpoints

* /api/v1
*/api/v1/status

## Stack used

Redis + Celery as a queue solutiom
Django + Django Rest Framework as an API solution
BeautifullSoup package for text retrieval
Requests standard package for image retrieval ( regex for .jpg and other image extensions )

## What went wrong

Django Rest Framework has a lot of generic methods and good ORM solution. I decided not to use AmazonS3 drives for this solution as I wanted
it to be easily reproduced on any other computer which procuded some unexpected errors. I decided to have a download endpoint inside the API for both image
and text retrieval. I decided not to store text and image inside database so they could be easily moved to another data storage and database could be small even with
thousands of files connected to it. Django produced wrong urls for datafiles ( it wouldn't happen with external solution like S3 drive) so I have searched django documentation like for two hours
to find a serialized method to change the default method for files retrieval. So even if all files are stored outside the database the are served inside api as string for text and as md4 string for images.
I have applied also additional filter to be able to use enddpoint like /api/v1/download/?url=http://www.onet.pl to search for images specified by url field. The same is done for /images endpoint and /text endpoint.
Docker-compose file were created for easy reproducibility.


## What could be updated

Tests for all endpoints. Tests for models creations. Tests for tasks. All endpoints allow for post,get,put,delete but maybe some of them should be read only. Serialization is not checked inside celery tasks so it could be also improved. Storage could be also changed for external like S3 drive. CD solution could be provided like .gitlab-ci or .travis-ci.
Solution could be implemented also using amazon API gateway, SQS and lambda with terraform file for infrastructure creation if cloud solution was needed. Lambda files are good enough for files transformation or text retrieval from webpages and scale infinitely.


## API

Check IP address for online solution http://34.245.183.237:8000/api/v1/