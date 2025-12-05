# adsp_interview_task

## Set Up
Set up should be as simple as cloning the repo and running `docker-compose up --build`, this installs all dependencies copies the sample .env file to the correct location, and sets up a crontab to run the data retrieval script once a day at 4:00am.
### Unit tests
The unit tests can be run once the containers are available with the command:
`docker exec -it adsp_interview_task-web-1 sh -c "cd /code && python -m unittest discover -p 'Test*.py' -b"`
### Script flags
* `-f` allows passing a single force ID to the script, which overrides the `FORCES` environment variable
* `-d` allows passing a specific date (YYYY-MM format), otherwise the script uses the date two months before now.
* `--no_store` bypasses actually storing retrieved results and displays only the last item in the result set.

## Database choice
I have chosen MongoDB for this, as it has relatively simple mechanisms for de-duplicating the data (which can only be gotten per-month), and provides a lot of facility for running aggregations without needing to reformat the data from its original form.  Also, this choice should be robust and scale well, as MongoDB's facility for sharding should handle much of what is needed.  The main tradeoff here is that accessing any single record is less simple than it would be in, for example, a relational schema.  I considered this a small issue, as it seems any single record is unlikely to be of interest.

## Code structure
Since the database handles much of the complexity of making data ready for consumption, this made the bulk of the implementation retrieving the data from the API.  As such, the solution is broadly in a service oriented architecture, where the top level script makes use of an API service and a Store service. 
### API Service/Client
The API client handles HTTP operations and returns the records as a single list, this could present some issues with memory use and response times for sufficiently large responses, although none presented during development.
### Store Service
This abstracts interacting with the actual physical store, as some formatting to enable de-duplication is needed.  This presents a simple interface that only takes a list of records to be stored.

## Other considerations
* Scalability: Database scalability should be handled by MongoDB, this script itself can also be horizontally scaled as it has an option to pass a force ID via a `-f` option.  This means that rather than having multiple forces through a single script, this can be controlled through the cron system itself, where new forces can be added with a new cron job, and jobs can be time offset to reduce simultaneous system load.
* Testability: while there is a suite of unit tests, these would probably be cleaner if the solution implemented full dependency injection. However, between the unit tests in place currently and the script flags, I believe what has been implemented is testable enough for now.
* Schema design: ideally, there would be a Schema in place in MongoDB to validate inserted data against, however at present this is only a simple document store.
* Production deployment: as it stands, I believe this could be deployed to a containerised environment relatively simply, as the solution is already containerised.  If there were, however, a requirement for this to be in a full server environment, this should be simple to achieve.  Most notably, at present for local development, there is no authorisation enabled in MongoDB.  This would need to be changed for any production deployment, which would require code changes.
* Logging: at present, the solution only outputs with simple `print` calls, which mean that errors and some limited tracing appears in docker logs.  This is another thing that, were this to be deployed to a production environment, would need to be updated, probably to use an external system such as Sentry, or AWS Cloudwatch.