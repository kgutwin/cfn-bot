# cfn-bot

CloudFormation update tweet bot, posting under [@cfnupdates](https://twitter.com/cfnupdates)

## Requirements

* AWS CLI with Administrator permission
* [Python 3 installed](https://www.python.org/downloads/)
* [Pipenv installed](https://github.com/pypa/pipenv)
    - `pip install pipenv`
* [Docker installed](https://www.docker.com/community-edition)
* [SAM Local installed](https://github.com/awslabs/aws-sam-local) 


As you've chosen the experimental Makefile we can use Make to automate Packaging and Building steps as follows:

```bash
        ...::: Installs all required packages as defined in the Pipfile :::...
        make install

        ...::: Run Pytest under tests/ with pipenv :::...
        make test

        ...::: Creates local dev environment for Python hot-reloading w/ packages:::...
        make build SERVICE="cfnbot"

        ...::: Run SAM Local API Gateway :::...
        make run
```


## Testing

`Pytest` is used to discover tests created under `tests` folder - Here's how you can run tests our initial unit tests:


```bash
make test
```


### Local development

Given that you followed Packaging instructions then run the following to invoke your function locally:


**Invoking function locally without API Gateway**

```bash
echo '{}' | sam local invoke BotFunction
```


## Deployment

You will need to create a file in the local repo named `.twitter_keys`
with the contents:

```
export TWITTER_ACCESS_TOKEN_KEY='access-token-key'
export TWITTER_ACCESS_TOKEN_SECRET='access-token-secret'
```

The keys can be generated using the `get_access_token.py` script.

Once ready, deploy using the deployment script.

```bash
./deploy.sh
```
