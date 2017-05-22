import os
import psycopg2
import urlparse

DATABASE_URL='postgres://ehddgphisfwedk:a79251b8a465c1f65ab7d62f13d63c68ec2e439a01ff1fb60c634ccb62f72c4f@ec2-23-23-237-68.compute-1.amazonaws.com:5432/d3h38vj40ov5bk?sslmode=require'
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
)
