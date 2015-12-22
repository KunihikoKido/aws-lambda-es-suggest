# Elasticsearch Suggest for AWS Lambda
## About

#### Runtime
Python 2.7

#### Lambda Hander
lambda_function.lambda_handler

#### Input event

_Input event: sample_
```json
{
  "host": "http://<your_elasticsearch_server:9200>/",
  "index": "userkeyword",
  "doc_type": "logs",
  "query": "銀座 ランチ",
  "exclude_pattern": ".{1}",
  "size": 10
}
```
* ``host``: elasticsearch host.
* ``index``: (Optional) index name.
* ``doc_type``: (Optional) document type name.
* ``query``: user keyword.
* ``size``: (Optional) size.
* ``exclude_pattern``: (Optional) exclude pattern.


#### Execution result

_Execution result sample:_
```json
{
  "items": [
    {
      "key": "銀座 ランチ",
      "doc_count": 3
    },
    {
      "key": "銀座 ランチ イタリアン",
      "doc_count": 1
    },
    {
      "key": "銀座 ランチ 和食",
      "doc_count": 1
    },
    {
      "key": "銀座 ランチ 子連れ",
      "doc_count": 1
    },
    {
      "key": "銀座 ランチ 安い",
      "doc_count": 1
    },
    {
      "key": "銀座 ランチ 寿司",
      "doc_count": 1
    },
    {
      "key": "銀座 ランチ 日曜",
      "doc_count": 1
    },
    {
      "key": "銀座 ランチ 肉",
      "doc_count": 1
    }
  ]
}
```

## Setup on local machine
```bash
# 1. Clone this repository with lambda function name
git clone https://github.com/KunihikoKido/aws-lambda-es-suggest.git es-suggest

# 2. Create and Activate a virtualenv
cd es-suggest
virtualenv env
source env/bin/activate

# 3. Install Python modules for virtualenv
pip install -r requirements/local.txt

# 4. Install Python modules for lambda function
fab setup
```

## Run lambda function on local machine
```bash
fab invoke
```

#### Run lambda function with custom event
```bash
fab invoke:custom-event.json
```

## Make zip file
```bash
fab makezip
```

## Update function code on AWS Lambda
```bash
fab aws-updatecode
```
## Get function configuration on AWS Lambda
```bash
fab aws-getconfig
```

## Invoke function on AWS Lambda
```bash
fab aws-invoke
```

## Show fabric Available commands
```bash
fab -l
```
