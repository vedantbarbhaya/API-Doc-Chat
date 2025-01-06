# Crustdata Dataset API Detailed Examples

## Overview
The Crustdata Dataset API provides endpoints to retrieve various datasets related to companies, job listings, funding milestones, and more. This documentation outlines the API's functionality, including request formats, parameters, and example requests.

## Dataset API Endpoints
### 1. Job Listings
- **Description**: Retrieve job listings that were last updated by the company.
- **Parameters**:
  - `company_id`: Unique identifier of a company in the database.
  
#### Example Request
To get job listings updated on 1st Feb, 2024 for specific companies:
```json
{
  "filters": {
    "op": "and",
    "conditions": [
      {
        "column": "company_id",
        "type": "in",
        "value": [680992, 673947, 631280, 636304, 631811]
      },
      {
        "column": "date_updated",
        "type": ">",
        "value": "2024-02-01"
      }
    ]
  },
  "offset": 0,
  "limit": 100
}
```

### 2. Funding Milestones
- **Description**: Fetch funding milestones for specified companies.

### 3. Decision Makers/People Info
- **Description**: Retrieve information about decision-makers in companies.

### 4. LinkedIn Employee Headcount and LinkedIn Follower Count
- **Description**: Get employee headcount and follower count from LinkedIn.

### 5. Employee Headcount By Function
- **Description**: Fetch employee headcount categorized by function.

### 6. Glassdoor Profile Metrics
- **Description**: Retrieve metrics from Glassdoor profiles.

### 7. G2 Profile Metrics
- **Description**: Get metrics from G2 profiles.

### 8. Web Traffic
- **Description**: Fetch web traffic data for specified companies.

### 9. Investor Portfolio
- **Description**: Retrieve investor portfolio information.

## Request Body Overview
The request body is a JSON object that contains the following parameters:

### Parameters Table
| Parameter         | Required | Description                                                                 |
|-------------------|----------|-----------------------------------------------------------------------------|
| filters           | Yes      | An object containing the filter conditions.                                 |
| offset            | Yes      | The starting point of the result set. Default value is 0.                  |
| limit             | Yes      | The number of results to return in a single request. Maximum value is 100. |
| sorts             | No       | An array of sorting criteria.                                               |
| aggregations      | No       | List of column objects you want to aggregate on with aggregate type.      |
| functions         | No       | List of functions you want to apply.                                       |
| background_task   | No       | A boolean flag to trigger a background task.                               |
| sync_from_source  | No       | A boolean flag to fetch jobs in real-time.                                 |

### Example Request
To retrieve job listings:
```bash
curl --request POST \
  --url https://api.crustdata.com/data_lab/job_listings/Table/ \
  --header 'Accept: application/json, text/plain, */*' \
  --header 'Authorization: Token $token' \
  --header 'Content-Type: application/json' \
  --data '{
    "filters": {
      "op": "and",
      "conditions": [
        {"column": "company_id", "type": "in", "value": [7576, 680992, 673947, 631280, 636304, 631811]},
        {"column": "date_updated", "type": ">", "value": "2024-02-01"}
      ]
    },
    "offset": 0,
    "limit": 100,
    "sorts": []
  }'
```

### Example Response
The response will include a task ID and status:
```json
{
  "task_id": "3d729bd0-a113-4b31-b09f-65eff79f06fe",
  "task_type": "job_listings",
  "status": "not_started",
  "completed_task_result_endpoint": "/task/result/3d729bd0-a113-4b31-b09f-65eff79f06fe/",
  "created_at": "2024-12-25T02:32:42.811843Z",
  "started_at": null
}
```

## Conclusion
This documentation provides a comprehensive overview of the Crustdata Dataset API, including its endpoints, request formats, and examples. For further assistance, please reach out to support@crustdata.com.

# Crustdata API Documentation

## API Functions Overview

### 1. Job Listings

#### Description
- Retrieve job listings posted after a specific date and that exactly match one of the given titles.

#### Example Request
```bash
curl --location 'https://api.crustdata.com/data_lab/job_listings/Table/' \
--header 'Accept: application/json, text/plain, */*' \
--header 'Authorization: Token $token' \
--header 'Content-Type: application/json' \
--data '{
    "tickers": [],
    "dataset": {
      "name": "job_listings",
      "id": "joblisting"
    },
    "filters": {
      "op": "and",
      "conditions": [
        {"column": "company_id", "type": "in", "value": [631394, 7576, 680992, 673947, 631280, 636304, 631811]},
        {"column": "date_updated", "type": ">", "value": "2024-08-01"},
        {
          "column": "title",
          "type": "in",
          "value": [
            "Sales Development Representative",
            "SDR",
            "Business Development Representative",
            "BDR",
            "Business Development Manager",
            "Account Development Representative",
            "ADR",
            "Account Development Manager",
            "Outbound Sales Representative",
            "Lead Generation Specialist",
            "Market Development Representative",
            "MDR",
            "Inside Sales Representative",
            "ISR",
            "Territory Development Representative",
            "Pipeline Development Representative",
            "New Business Development Representative",
            "Customer Acquisition Specialist"
          ]
        }
      ]
    },
    "offset": 0,
    "count": 100,
    "sorts": []
}'
```

#### Count of Job Listings
- You can set `"count": 1`. The last value of the first (and the only) row would be the total count of jobs meeting the criteria.

#### Example Request for Count
```bash
curl --location 'https://api.crustdata.com/data_lab/job_listings/Table/' \
--header 'Accept: application/json, text/plain, */*' \
--header 'Accept-Language: en-US,en;q=0.9' \
--header 'Authorization: Token $token' \
--header 'Content-Type: application/json' \
--header 'Origin: https://crustdata.com' \
--data '{
    "tickers": [],
    "dataset": {
      "name": "job_listings",
      "id": "joblisting"
    },
    "filters": {
      "op": "and",
      "conditions": [
        {"column": "company_id", "type": "in", "value": [631394]},
        {
            "column": "title",
            "type": "in",
            "value": [
            "Sales Development Representative",
            "SDR",
            "Business Development Representative",
            "BDR",
            "Business Development Manager",
            "Account Development Representative",
            "ADR",
            "Account Development Manager",
            "Outbound Sales Representative",
            "Lead Generation Specialist",
            "Market Development Representative",
            "MDR",
            "Inside Sales Representative",
            "ISR",
            "Territory Development Representative",
            "Pipeline Development Representative",
            "New Business Development Representative",
            "Customer Acquisition Specialist"
            ]
        }
      ]
    },
    "offset": 0,
    "count": 1,
    "sorts": []
}'
```

### 2. Funding Milestones

#### Description
- Use this request to get a time-series of funding milestones with `company_id` equal to any one of [637158, 674265, 674657].

#### Example Request
```bash
curl --request POST \
  --url https://api.crustdata.com/data_lab/funding_milestone_timeseries/ \
  --header 'Accept: application/json, text/plain, */*' \
  --header 'Accept-Language: en-US,en;q=0.9' \
  --header 'Authorization: Token $auth_token' \
  --header 'Content-Type: application/json' \
  --header 'Origin: https://crustdata.com' \
  --header 'Referer: https://crustdata.com/' \
  --data '{"filters":{"op": "or", "conditions": [{"column": "company_id", "type": "in", "value": [637158,674265,674657]}]},"offset":0,"count":1000,"sorts":[]}'
```

### 3. Decision Makers

#### Description
- Retrieve decision makers for a given `company_id`.

#### Example Request
```bash
curl --request POST \
  --url https://api.crustdata.com/data_lab/decision_makers/ \
  --header 'Accept: application/json, text/plain, */*' \
  --header 'Accept-Language: en-US,en;q=0.9' \
  --header 'Authorization: Token $auth_token' \
  --header 'Content-Type: application/json' \
  --header 'Origin: http://localhost:3000' \
  --header 'Referer: http://localhost:3000/' \
  --data '{"filters":{"op": "and", "conditions": [{"column": "company_id", "type": "in", "value": [632328]}] },"offset":0,"count":100,"sorts":[]}'
```

### 4. Specific Decision Makers

#### Description
- Retrieve decision makers with specific titles for a given `company_id`.

#### Example Request
```bash
curl --request POST \
  --url https://api.crustdata.com/data_lab/decision_makers/ \
  --header 'Accept: application/json, text/plain, */*' \
  --header 'Accept-Language: en-US,en;q=0.9' \
  --header 'Authorization: Token $auth_token' \
  --header 'Content-Type: application/json' \
  --header 'Origin: http://localhost:3000' \
  --header 'Referer: http://localhost:3000/' \
  --data '{"filters":{"op": "and", "conditions": [{"column": "company_id", "type": "in", "value": [632328]}] },"offset":0,"count":100,"sorts":[]}'
```

## Parsing the Response
- The response format is the same as that of the Company Discovery: Screening API. You can refer to the [Parsing the response documentation](https://crustdata.notion.site/Parsing-the-response-c66d5236e8ea40df8af114f6d447ab48?pvs=24#28de6e16940c4615b5872020a345766a) for more details.

## Conclusion
This documentation provides an overview of the Crustdata API functions, including how to retrieve job listings, funding milestones, and decision makers. Each section includes example requests to help you get started.

# API Documentation Summary

## API Request for Decision Makers

### Request Format
To retrieve decision makers, you can use the following request format:

```bash
curl --request POST \
  --url https://api.crustdata.com/data_lab/decision_makers/ \
  --header 'Accept: application/json, text/plain, */*' \
  --header 'Accept-Language: en-US,en;q=0.9' \
  --header 'Authorization: Token $auth_token' \
  --header 'Content-Type: application/json' \
  --data '{
    "filters": {
      "op": "or",
      "conditions": [
        {
          "column": "company_id",
          "type": "in",
          "value": [632328]
        },
        {
          "column": "title",
          "type": "in",
          "value": ["vice president", "chief"]
        }
      ]
    },
    "offset": 0,
    "count": 100,
    "sorts": []
  }'
```

### Python Example
Here is an example of how to make the same request using Python:

```python
import requests

url = "https://api.crustdata.com/data_lab/decision_makers/"
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Authorization": "Token YOUR_AUTH_TOKEN",  # Replace with your actual token
    "Content-Type": "application/json"
}

payload = {
    "filters": {
        "op": "or",
        "conditions": [
            {
                "column": "company_id",
                "type": "in",
                "value": [632328]
            },
            {
                "column": "title",
                "type": "in",
                "value": ["vice president", "chief"]
            }
        ]
    },
    "offset": 0,
    "count": 100,
    "sorts": []
}

response = requests.post(url, headers=headers, json=payload)

# Print the response status and data
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
```

## API Request for People Profiles by LinkedIn's Flagship URL

### Request Format
To retrieve people profiles by their LinkedIn's flagship URL, use the following request format:

```bash
curl --request POST \
  --url https://api.crustdata.com/data_lab/decision_makers/ \
  --header 'Accept: application/json, text/plain, */*' \
  --header 'Accept-Language: en-US,en;q=0.9' \
  --header 'Authorization: Token $auth_token' \
  --header 'Content-Type: application/json' \
  --data '{
    "filters": {
      "op": "and",
      "conditions": [
        {
          "column": "linkedin_flagship_profile_url",
          "type": "in",
          "value": ["https://www.linkedin.com/in/alikashani"]
        }
      ]
    },
    "offset": 0,
    "count": 100,
    "sorts": []
  }'
```

### Python Example
Here is an example of how to make the same request using Python:

```python
import requests
import json

url = "https://api.crustdata.com/data_lab/decision_makers/"
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Authorization': 'Token $auth_token',  # Replace with your actual token
    'Content-Type': 'application/json',
    'Origin': 'http://localhost:3000',
    'Referer': 'http://localhost:3000/'
}

data = {
    "filters": {
        "op": "or",
        "conditions": [
            {
                "column": "linkedin_flagship_profile_url",
                "type": "in",
                "value": ["https://www.linkedin.com/in/alikashani"]
            }
        ]
    },
    "offset": 0,
    "count": 100,
    "sorts": []
}

response = requests.post(url, headers=headers, json=json.dumps(data))
print(response.text)
```

## API Request for People Profiles by LinkedIn URN

### Request Format
To retrieve people profiles by their LinkedIn URN, use the following request format:

```bash
curl --request POST \
  --url https://api.crustdata.com/data_lab/decision_makers/ \
  --header 'Accept: application/json, text/plain, */*' \
  --header 'Accept-Language: en-US,en;q=0.9' \
  --header 'Authorization: Token $auth_token' \
  --header 'Content-Type: application/json' \
  --data '{
    "filters": {
      "op": "or",
      "conditions": [
        {
          "column": "linkedin_profile_urn",
          "type": "in",
          "value": ["ACwAAAVhcDEBbTdJtuc-KHsdYfPU1JAdBmHkh8I"]
        }
      ]
    },
    "offset": 0,
    "count": 100,
    "sorts": []
  }'
```

### Python Example
Here is an example of how to make the same request using Python:

```python
import requests
import json

url = "https://api.crustdata.com/data_lab/decision_makers/"
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Authorization': 'Token $auth_token',  # Replace with your actual token
    'Content-Type': 'application/json',
    'Origin': 'http://localhost:3000',
    'Referer': 'http://localhost:3000'
}

data = {
    "filters": {
        "op": "or",
        "conditions": [
            {
                "column": "linkedin_profile_urn",
                "type": "in",
                "value": ["ACwAAAVhcDEBbTdJtuc-KHsdYfPU1JAdBmHkh8I"]
            }
        ]
    },
    "offset": 0,
    "count": 100,
    "sorts": []
}

response = requests.post(url, headers=headers, json=json.dumps(data))
print(response.text)
```

## API Request for Employee Headcount and Follower Count

### Request Format
To get the employee headcount and follower count, use the following request format:

```bash
curl --request POST \
  --url https://api.crustdata.com/data_lab/headcount_timeseries/ \
  --header 'Accept: application/json, text/plain, */*' \
  --header 'Accept-Language: en-US,en;q=0.9' \
  --header 'Authorization: Token $auth_token' \
  --header 'Content-Type: application/json' \
  --data '{
    "filters": {
      "op": "or",
      "conditions": [
        {
          "column": "company_id",
          "type": "=",
          "value": 634995
        },
        {
          "column": "company_id",
          "type": "=",
          "value": 680992
        },
        {
          "column": "company_id",
          "type": "=",
          "value": 673947
        },
        {
          "column": "company_id",
          "type": "=",
          "value": 631811
        }
      ]
    },
    "offset": 0,
    "count": 100,
    "sorts": []
  }'
```

### Python Example
Here is an example of how to make the same request using Python:

```python
import requests
import json

url = "https://api.crustdata.com/data_lab/headcount_timeseries/"
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Authorization': 'Token $auth_token',  # Replace with your actual token
    'Content-Type': 'application/json',
    'Origin': 'https://crustdata.com',
    'Referer': 'https://crustdata.com'
}

json_data = {
    'filters': {
        'op': 'or',
        'conditions': [
            {
                'column': 'company_id',
                'type': '=',
                'value': 634995
            },
            {
                'column': 'company_id',
                'type': '=',
                'value': 680992
            },
            {
                'column': 'company_id',
                'type': '=',
                'value': 673947
            },
            {
                'column': 'company_id',
                'type': '=',
                'value': 631811
            }
        ]
    },
    'offset': 0,
    'count': 100,
    'sorts': []
}

response = requests.post(url, headers=headers, json=json_data)
print(response.text)
```

## Response Structure
The response from the API will typically include fields such as `company_id`, `company_website`, `linkedin_id`, `headcount_timeseries`, and `total_rows`. The data will be structured in a JSON format, which can be easily parsed and utilized in your application.

### Example Response
```json
{
  "fields": [
    {
      "type": "foreign_key",
      "api_name": "company_id",
      "hidden": false,
      "options": [],
      "summary": "",
      "local_metric": false,
      "display_name": "",
      "company_profile_name": "",
      "geocode": false
    },
    {
      "type": "string",
      "api_name": "company_website",
      "hidden": false,
      "options": [],
      "summary": "",
      "local_metric": false,
      "display_name": "",
      "company_profile_name": "",
      "geocode": false
    },
    ...
  ],
  "rows": [
    [
      631280,
      "https://www.lacework.com",
      "17932068",
      "lacework.com",
      [
        {
          "date": "2021-08-01T00:00:00+00:00",
          "employee_count": 643,
          "follower_count": null
        },
        ...
      ]
    ],
    ...
  ]
}
```

This structured response allows for easy access to the data you need for further processing or analysis.

# API Documentation Summary

## 1. Employee Headcount By Function

### Description
Use this request to get the headcount by function for the given company. You can provide either a list of Crustdata’s `company_id` or `company_website_domain` in the filters.

### cURL Example
```bash
curl --request POST \
  --url https://api.crustdata.com/data_lab/linkedin_headcount_by_facet/Table/ \
  --header 'Accept: application/json, text/plain, */*' \
  --header 'Accept-Language: en-US,en;q=0.9' \
  --header 'Authorization: Token $token' \
  --header 'Content-Type: application/json' \
  --header 'Origin: https://crustdata.com' \
  --data '{
    "tickers": [],
    "dataset": {
      "name": "linkedin_headcount_by_facet",
      "id": "linkedinheadcountbyfacet"
    },
    "filters": {
      "op": "and",
      "conditions": [
            {"column": "company_id", "type": "in", "value": [680992, 673947, 631280], "allow_null": false}
      ]
    },
    "groups": [],
    "aggregations": [],
    "functions": [],
    "offset": 0,
    "count": 100,
    "sorts": []
  }'
```

### Result Structure
```json
{
  "fields": [
    {
      "type": "string",
      "api_name": "linkedin_id",
      "hidden": true,
      ...
    },
    ...
  ],
  "rows": [
    [
      "35625249",
      "https://www.sketch.com/",
      "Sketch",
      "sketch.com",
      6,
      "2024-02-28T00:00:00Z",
      ...
    ],
    ...
  ]
}
```

## 2. Glassdoor Profile Metrics

### Description
Use this request to get the rating of a company on Glassdoor, number of reviews, business outlook, CEO approval rating, etc. You can provide either a list of Crustdata’s `company_id` or `company_website_domain` in the filters.

### cURL Example
```bash
curl --request POST \
  --url https://api.crustdata.com/data_lab/glassdoor_profile_metric/Table/ \
  --header 'Accept: application/json, text/plain, */*' \
  --header 'Accept-Language: en-US,en;q=0.9' \
  --header 'Authorization: Token $token' \
  --header 'Content-Type: application/json' \
  --header 'Origin: https://crustdata.com' \
  --data '{
    "tickers": [],
    "dataset": {
      "name": "glassdoor_profile_metric",
      "id": "glassdoorprofilemetric"
    },
    "filters": {
      "op": "and",
      "conditions": [
        {"column": "company_id", "type": "in", "value": [680992,673947,631280,636304,631811], "allow_null": false}
      ]
    },
    "groups": [],
    "aggregations": [],
    "functions": [],
    "offset": 0,
    "count": 100,
    "sorts": []
  }'
```

### Result Structure
```json
{
  "fields": [
    {
      "type": "string",
      "api_name": "linkedin_id",
      "hidden": true,
      ...
    },
    ...
  ],
  "rows": [
    [
      "3033823",
      "http://jumpcloud.com",
      "JumpCloud",
      "jumpcloud.com",
      "2024-01-07T00:00:00Z",
      3.45124,
      ...
    ],
    ...
  ]
}
```

## 3. G2 Profile Metrics

### Description
Use this request to get the rating of a company’s product on G2 and the number of reviews, etc.

### cURL Example
```bash
curl --request POST \
  --url http://api.crustdata.com/data_lab/g2_profile_metrics/Table/ \
  --header 'Accept: application/json, text/plain, */*' \
  --header 'Accept-Language: en-US,en;q=0.9' \
  --header 'Authorization: Token $token' \
  --header 'Content-Type: application/json' \
  --header 'Origin: https://crustdata.com' \
  --data '{
    "tickers": [],
    "dataset": {
      "name": "g2_profile_metrics",
      "id": "g2profilemetric"
    },
    "filters": {
      "op": "or",
      "conditions": [
        {"column": "company_website_domain", "type": "=", "value": "microstrategy.com", "allow_null": false},
        {"column": "company_website_domain", "type": "=", "value": "lacework.com", "allow_null": false},
        {"column": "company_website_domain", "type": "=", "value": "jumpcloud.com", "allow_null": false}
      ]
    },
    "groups": [],
    "aggregations": [],
    "functions": [],
    "offset": 0,
    "count": 100,
    "sorts": []
  }'
```

### Result Structure
```json
{
  "fields": [
    {
      "type": "string",
      "api_name": "linkedin_id",
      "hidden": true,
      ...
    },
    ...
  ],
  "rows": [
    [
      "3643",
      "http://www.microstrategy.com",
      "MicroStrategy",
      "microstrategy.com",
      "2023-07-28T00:00:00Z",
      464,
      ...
    ],
    ...
  ]
}
```

---

This documentation provides a structured overview of the API endpoints related to employee headcount, Glassdoor metrics, and G2 metrics, including example requests and expected response formats.

# API Documentation

## 8. Web Traffic

Use this request to get historical web-traffic of a company by domain.

### cURL Example

```bash
curl --request POST \
  --url 'https://api.crustdata.com/data_lab/webtraffic/' \
  --header 'Accept: */*' \
  --header 'Accept-Language: en-GB,en-US;q=0.9,en;q=0.8' \
  --header 'Authorization: Token $token' \
  --header 'Content-Type: application/json' \
  --data '{
    "filters": {
      "op": "or",
      "conditions": [
        {
          "column": "company_website",
          "type": "(.)",
          "value": "wefitanyfurniture.com"
        }
      ]
    },
    "offset": 0,
    "count": 100,
    "sorts": []
  }'
```

### Key Points:
- When querying a website, compute the domain (`$domain`) and then pass it in the `conditions` object of the payload.
  
```json
[
  {
    "column": "company_website",
    "type": "(.)",
    "value": "$domain"
  }
]
```

- If there is no data for the website, it will be auto-enriched in the next 24 hours. Just query again.
- For parsing the response, please follow the [response structure](https://www.notion.so/crustdata/Crustdata-Discovery-And-Enrichment-API-c66d5236e8ea40df8af114f6d447ab48?pvs=4#28de6e16940c4615b5872020a345766a).

## 9. Investor Portfolio

Retrieve portfolio details for a specified investor. Each investor, as returned in the company enrichment endpoint, has a unique identifier (UUID), name, and type. This API allows you to fetch the full portfolio of companies associated with an investor, using either the investor's `uuid` or `name` as an identifier.

### cURL Example

#### Example 1: Query by Investor UUID

```bash
curl 'https://api.crustdata.com/data_lab/investor_portfolio?investor_uuid=ce91bad7-b6d8-e56e-0f45-4763c6c5ca29' \
  --header 'Accept: application/json, text/plain, */*' \
  --header 'Accept-Language: en-US,en;q=0.9' \
  --header 'Authorization: Token $auth_token'
```

**Note:** UUID for an investor can be retrieved from `/screener/company` response. It is available in `funding_and_investment.crunchbase_investors_info_list[*].uuid` field.

#### Example 2: Query by Investor Name

```bash
curl 'https://api.crustdata.com/data_lab/investor_portfolio?investor_name=Sequoia Capital' \
  --header 'Accept: application/json, text/plain, */*' \
  --header 'Accept-Language: en-US,en;q=0.9' \
  --header 'Authorization: Token $auth_token'
```

**Note:** UUID for an investor can be retrieved from `/screener/company` response. It is available in `funding_and_investment.crunchbase_investors_info_list[*].uuid` field.

### Result
Full sample: [View Sample Response](https://jsonhero.io/j/hSEHVFgv68pz)

