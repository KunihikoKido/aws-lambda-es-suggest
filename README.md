# Elasticsearch Suggest for AWS Lambda
## About
Elasticsearch をバックエンドに、キーワードサジェストAPIをサーバーレスで実装するためのLambdaファンクションです。Elasticsearchのキーワードサジェスト用インデックスは「[Elasticsearch キーワードサジェスト日本語のための設計](https://medium.com/hello-elasticsearch/elasticsearch-%E3%82%AD%E3%83%BC%E3%83%AF%E3%83%BC%E3%83%89%E3%82%B5%E3%82%B8%E3%82%A7%E3%82%B9%E3%83%88%E6%97%A5%E6%9C%AC%E8%AA%9E%E3%81%AE%E3%81%9F%E3%82%81%E3%81%AE%E8%A8%AD%E8%A8%88-352a230030dd#.756g0snd2)」を参考に構築してください。

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

## with Amazon API Gateway
### _Example Settings:_

_Method and Resources:_
```
GET /suggest
```

_Query Strings:_
* ``q``: キーワード

_Cross-Origin Resource Sharing (CORS):_

※クロスドメインで使用する場合は有効にする。

_Request mapping template:_
```json
{
    "query": "$util.urlDecode($input.params('q'))",
    "host": "http://<your_elasticsearch_server:9200>",
    "index": "userkeyword",
    "doc_type": "logs",
    "exclude_pattern": ".{1}",
    "size": 8
}
```

_Example Request:_
```
GET /suggest?q=%E9%8A%80%E5%BA%A7%20%E3%83%A9%E3%83%B3%E3%83%81
```
