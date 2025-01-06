# Crustdata Discovery And Enrichment API Documentation

## Introduction
The Crustdata API provides programmatic access to firmographic and growth metrics data for companies worldwide from over 16 datasets (LinkedIn headcount, Glassdoor, Instagram, G2, Web Traffic, Apple App Store reviews, Google Play Store, News, among others). This documentation describes various available API calls and the schema of the response.

## Getting Started
To get started with the Crustdata API, you need to obtain an authorization token (API key). Reach out to [abhilash@crustdata.com](mailto:abhilash@crustdata.com) to get your token.

## Data Dictionary
For detailed information about the data fields available in the API, refer to the [Crustdata Data Dictionary](https://api.crustdata.com).

## Company Endpoints

### Enrichment: Company Data API
**Overview:** This endpoint enriches company data by retrieving detailed information about one or multiple companies using either their domain, name, or ID.

**Required:** Authentication token `auth_token` for authorization.

#### Request Parameters
- **company_domain**: `string` (comma-separated list, up to 25 domains)
  - **Description:** The domain(s) of the company(ies) you want to retrieve data for.
  - **Example:** 
    ```plaintext
    company_domain=hubspot.com,google.com
    ```

- **company_name**: `string` (comma-separated list, up to 25 names; use double quotes if names contain commas)
  - **Description:** The name(s) of the company(ies) you want to retrieve data for.
  - **Example:** 
    ```plaintext
    company_name="Acme, Inc.","Widget Co"
    ```

- **company_linkedin_url**: `string` (comma-separated list, up to 25 URLs)
  - **Description:** The LinkedIn URL(s) of the company(ies).
  - **Example:** 
    ```plaintext
    company_linkedin_url=https://linkedin.com/company/hubspot,https://linkedin.com/company/clay-hq
    ```

- **company_id**: `integer` (comma-separated list, up to 25 IDs)
  - **Description:** The unique ID(s) of the company(ies) you want to retrieve data for.
  - **Example:** 
    ```plaintext
    company_id=12345,67890
    ```

- **fields**: `string` (comma-separated list of fields)
  - **Description:** Specifies the fields you want to include in the response. Supports nested fields up to a certain level.
  - **Example:** 
    ```plaintext
    fields=company_name,company_domain,glassdoor.glassdoor_review_count
    ```

- **enrich_realtime**: `boolean` (False by default)
  - **Description:** When True and the requested company is not present in Crustdata’s database, the company is enriched within 10 minutes of the request.

### Example Requests
#### Request by Company Domain
**Use Case:** Ideal for users who have one or more company website domains and need to fetch detailed profiles.

**Note:** You can provide up to 25 domains in a comma-separated list.

**Request:**
```bash
curl 'https://api.crustdata.com/screener/company?company_domain=hubspot.com,google.com' \
  --header 'Accept: application/json, text/plain, */*' \
  --header 'Accept-Language: en-US,en;q=0.9' \
  --header 'Authorization: Token $token'
```

#### Request by Company Name
**Use Case:** Suitable for users who have one or more company names and need to retrieve detailed profiles.

**Note:** You can provide up to 25 names in a comma-separated list. If a company name contains a comma, enclose the name in double quotes.

**Request:**
```bash
curl 'https://api.crustdata.com/screener/company?company_name="HubSpot","Google, Inc."' \
  --header 'Accept: application/json, text/plain, */*' \
  --header 'Accept-Language: en-US,en;q=0.9' \
  --header 'Authorization: Token $token'
```

#### Request by Company LinkedIn URL
**Use Case:** Suitable for users who have one or more company LinkedIn URLs and need to retrieve detailed profiles.

**Request:**
```bash
curl 'https://api.crustdata.com/screener/company?company_linkedin_url=https://linkedin.com/company/hubspot,https://linkedin.com/company/clay-hq' \
  --header 'Accept: application/json, text/plain, */*' \
  --header 'Accept-Language: en-US,en;q=0.9' \
  --header 'Authorization: Token $token'
```

#### Request by Company ID
**Use Case:** Suitable for users who have ingested one or more companies from Crustdata already and want to enrich their data by Crustdata’s `company_id`.

**Request:**
```bash
curl 'https://api.crustdata.com/screener/company?company_id=631480,789001' \
  --header 'Accept: application/json, text/plain, */*' \
  --header 'Accept-Language: en-US,en;q=0.9' \
  --header 'Authorization: Token $token'
```

### Response Includes
- **company_name**: The name of the company.
- **company_website_domain**: The website domain of the company.
- **glassdoor**: Includes fields like `glassdoor_overall_rating` and `glassdoor_review_count`.
- **decision_makers**: Full array of decision-maker profiles.
- **founders**: Full array of founder profiles.

### Important Notes
- **Nested Fields:** You can specify nested fields up to the levels defined in the response structure. Fields nested beyond the allowed levels or within lists (arrays) cannot be individually accessed.
- **User Permissions:** Access to certain fields may be restricted based on your user permissions. If you request fields you do not have access to, the API will return an error indicating unauthorized access.

This concludes the overview of the Crustdata Discovery And Enrichment API. For further details, please refer to the complete documentation or contact support.

# API Documentation Summary

## Error Response
When an error occurs, the API will return a JSON object with an error message. Below is an example of the error response format:

```json
{
  "error": "Unauthorized access to field(s): headcount"
}
```

## Request with Realtime Enrichment
### Use Case
For companies not tracked by Crustdata, you want to enrich them within 10 minutes of the request.

### Example Request
To make a request with real-time enrichment, you can use the following `curl` command:

```bash
curl --location 'https://api.crustdata.com/screener/company?company_linkedin_url=https://www.linkedin.com/company/usebramble&enrich_realtime=True' \
--header 'Accept: application/json, text/plain, */*' \
--header 'Accept-Language: en-US,en;q=0.9' \
--header 'Authorization: Token $token'
```

## Response Structure
The response is a JSON array containing company objects. Below is the structure of the response up to the levels where you can filter using the `fields` parameter.

### Top-Level Fields
- **company_id**: *integer*
- **company_name**: *string*
- **linkedin_profile_url**: *string*
- **linkedin_id**: *string*
- **linkedin_logo_url**: *string*
- **company_twitter_url**: *string*
- **company_website_domain**: *string*
- **hq_country**: *string*
- **headquarters**: *string*
- **largest_headcount_country**: *string*
- **hq_street_address**: *string*
- **company_website**: *string*
- **year_founded**: *string* (ISO 8601 date)
- **fiscal_year_end**: *string*
- **estimated_revenue_lower_bound_usd**: *integer*
- **estimated_revenue_higher_bound_usd**: *integer*
- **employee_count_range**: *string*
- **company_type**: *string*
- **linkedin_company_description**: *string*
- **acquisition_status**: *string* or *null*
- **ceo_location**: *string*

### Nested Objects
You can filter up to the following nested levels:

#### all_office_addresses
- *array of strings*

#### markets
- *array of strings*

#### stock_symbols
- *array of strings*

#### headcount
- **headcount**: *object*
  - **linkedin_headcount**: *integer*
  - **linkedin_headcount_total_growth_percent**: *object*
    - **mom**: *float*
    - **qoq**: *float*
    - **yoy**: *float*
  - **linkedin_headcount_by_role_absolute**: *object*
  - **linkedin_headcount_by_role_percent**: *object*
  - **linkedin_headcount_by_role_six_months_growth_percent**: *object*
  - **linkedin_headcount_by_role_yoy_growth_percent**: *object*
  - **linkedin_headcount_by_region_absolute**: *object*
  - **linkedin_headcount_by_region_percent**: *object*
  - **linkedin_headcount_by_skill_absolute**: *object*
  - **linkedin_headcount_by_skill_percent**: *object*

#### web_traffic
- **monthly_visitors**: *integer*
- **monthly_visitor_mom_pct**: *float*
- **monthly_visitor_qoq_pct**: *float*
- **traffic_source_social_pct**: *float*
- **traffic_source_search_pct**: *float*
- **traffic_source_direct_pct**: *float*
- **traffic_source_paid_referral_pct**: *float*
- **traffic_source_referral_pct**: *float*

#### glassdoor
- **glassdoor_overall_rating**: *float*
- **glassdoor_ceo_approval_pct**: *integer*
- **glassdoor_review_count**: *integer*
- **glassdoor_senior_management_rating**: *float*
- **glassdoor_compensation_rating**: *float*
- **glassdoor_career_opportunities_rating**: *float*
- **glassdoor_work_life_balance_rating**: *float*
- **glassdoor_diversity_rating**: *float* or *null*

#### g2
- **g2_review_count**: *integer*
- **g2_average_rating**: *float*
- **g2_review_count_mom_pct**: *float*
- **g2_review_count_qoq_pct**: *float*

This documentation provides a comprehensive overview of the API's functionality, including error handling, request examples, and response structures.

# Company Discovery: Screening API Documentation

## Overview
The Company Screening API allows you to screen and filter companies based on various growth and firmographic criteria. 

### Required Authentication
You need an authentication token (`auth_token`) for authorization.

## API Functions

### Metrics
- **linkedin_followers_qoq_percent**: `float`
- **linkedin_followers_six_months_growth_percent**: `float`
- **linkedin_followers_yoy_percent**: `float`

### Funding and Investment
- **crunchbase_total_investment_usd**: `integer`
- **days_since_last_fundraise**: `integer`
- **last_funding_round_type**: `string`
- **crunchbase_investors**: `array of strings`
- **last_funding_round_investment_usd**: `integer`
- **funding_milestones_timeseries**: `array of objects` (Cannot filter within this array)

### Job Openings
- **recent_job_openings_title**: `string` or `null`
- **job_openings_count**: `integer` or `null`
- **job_openings_count_growth_percent**: `float`
- **mom**: `float` or `null`
- **qoq**: `float` or `null`
- **yoy**: `float` or `null`
- **job_openings_by_function_qoq_pct**: `object`
- **job_openings_by_function_six_months_growth_pct**: `object`
- **open_jobs_timeseries**: `array of objects` (Cannot filter within this array)
- **recent_job_openings**: `array of objects` (Cannot filter within this array)

### SEO
- **average_seo_organic_rank**: `integer`
- **monthly_paid_clicks**: `integer`
- **monthly_organic_clicks**: `integer`
- **average_ad_rank**: `integer`
- **total_organic_results**: `integer` or `float`
- **monthly_google_ads_budget**: `integer` or `float`
- **monthly_organic_value**: `integer`
- **total_ads_purchased**: `integer`
- **lost_ranked_seo_keywords**: `integer`
- **gained_ranked_seo_keywords**: `integer`
- **newly_ranked_seo_keywords**: `integer`

### Founders
- **founders_locations**: `array of strings`
- **founders_education_institute**: `array of strings`
- **founders_degree_name**: `array of strings`
- **founders_previous_companies**: `array of strings`
- **founders_previous_titles**: `array of strings`
- **profiles**: `array of objects` (Cannot filter within this array)

### Decision Makers
- **decision_makers**: `array of objects` (Cannot filter within this array)

### News Articles
- **news_articles**: `array of objects` (Cannot filter within this array)

## Request Example
To get companies that meet specific criteria, you can use the following cURL command:

```bash
curl 'https://api.crustdata.com/screener/company?company_id=123' \
  --header 'Authorization: Token $token' \
  --header 'Accept: application/json'
```

## Request Body Overview
The request body is a JSON object that contains the following parameters:

### Parameters Table

| Parameter | Description | Required |
|-----------|-------------|----------|
| metrics   | An array of metric objects containing the metric name. Value should always be `[{"metric_name": "linkedin_headcount_and_glassdoor_ceo_approval_and_g2"}]` | Yes |
| filters   | An object containing the filter conditions. | Yes |
| offset    | The starting point of the result set. Default value is 0. | Yes |
| count     | The number of results to return in a single request. Maximum value is 100. Default value is 100. | Yes |
| sorts     | An array of sorting criteria. | No |

### Example Request Body
```json
{
  "metrics": [
    {
      "metric_name": "linkedin_headcount_and_glassdoor_ceo_approval_and_g2"
    }
  ],
  "filters": {
    "op": "and",
    "conditions": [
      {
        "column": "crunchbase_total_investment_usd",
        "type": ">",
        "value": 5000000,
        "allow_null": false
      },
      {
        "column": "linkedin_headcount",
        "type": ">",
        "value": 50,
        "allow_null": false
      },
      {
        "column": "largest_headcount_country",
        "type": "(.)",
        "value": "USA",
        "allow_null": false
      }
    ]
  },
  "hidden_columns": [],
  "offset": 0,
  "count": 100,
  "sorts": []
}
```

## Filters Object
The filters object contains the following parameters:

### Filters Table

| Parameter | Description | Required |
|-----------|-------------|----------|
| op        | The operator to apply on the conditions. The value can be "and" or "or". | Yes |
| conditions| An array of complex filter objects or basic filter objects. | Yes |

### Basic Filter Object Example
```json
{
  "column": "linkedin_headcount",
  "type": ">",
  "value": "50"
}
```

## Limitations on Nested Fields
- **Maximum Nesting Level**: You can specify nested fields only up to the levels defined above.
- **Default Exclusion of Certain Fields**: Even if you have access to fields like `decision_makers` and `founders.profiles`, they will not be included in the response by default when the `fields` parameter is not provided. You must explicitly request these fields using the `fields` parameter.

### Example cURL Command to Include Fields
```bash
curl 'https://api.crustdata.com/screener/company?company_id=123&fields=decision_makers,founders.profiles' \
  --header 'Authorization: Token $token' \
  --header 'Accept: application/json'
```

## Response
The response provides a comprehensive profile of the company, including firmographic details, social media links, headcount data, and growth metrics. For a detailed response data structure, refer to this JSON [JSON Hero](https://jsonhero.io/j/QN8Qj7dg8MbW).

# Crustdata API Documentation

## Company Identification API

### Overview
Given a company’s name, website, or LinkedIn profile, you can identify the company in Crustdata’s database with the Company Identification API.

### Request Example
```bash
curl 'https://api.crustdata.com/screener/identify/' \
    --header 'Accept: application/json, text/plain, */*' \
    --header 'Accept-Language: en-US,en;q=0.9' \
    --header 'Authorization: Token $api_token' \
    --header 'Connection: keep-alive' \
    --header 'Content-Type: application/json' \
    --header 'Origin: https://crustdata.com' \
    --data '{"query_company_website": "serverobotics.com", "count": 1}'
```

### Payload Fields (at least one of the query fields required):
- `query_company_name`: Name of the company
- `query_company_website`: Website of the company
- `query_company_linkedin_url`: LinkedIn profile URL of the company
- `count`: Maximum number of results. Default is 10.

### Result
Each item in the result corresponds to a company record in Crustdata’s database. The records are ranked by the matching score, highest first. The score is maximum when all the query fields are provided and their values exactly match the value of the corresponding company in Crustdata’s database.

### Result Fields
Each result record contains the following fields for the company:
- `company_id`: A unique identifier for the company in Crustdata’s database.
- `company_name`: Name of the company in Crustdata’s database.
- `company_website_domain`: Website domain of the company as mentioned on its LinkedIn page.
- `company_website`: Website of the company.
- `linkedin_profile_url`: LinkedIn profile URL for the company.
- `linkedin_headcount`: Latest headcount of the company in Crustdata’s database.
- `acquisition_status`: Either `acquired` or `null`.
- `score`: A relative score based on the query parameters provided and how well they match the company fields in Crustdata’s database.

## Filter Dictionary for Company Search

### Filter Types and Descriptions

| Filter Type                     | Description                                                  | Properties | Value/Sub-filter |
|----------------------------------|--------------------------------------------------------------|------------|------------------|
| `COMPANY_HEADCOUNT`             | Specifies the size of the company based on the number of employees. | types: [in] | "1-10", "11-50", "51-200", "201-500", "501-1,000", "1,001-5,000", "5,001-10,000", "10,001+" |
| `REGION`                        | Specifies the geographical region of the company.           | types: [in, not in] | [region_values](https://crustdata-docs-region-json.s3.us-east-2.amazonaws.com/updated_regions.json) |
| `INDUSTRY`                      | Specifies the industry of the company.                       | types: [in, not in] | [industry_values](https://crustdata-docs-region-json.s3.us-east-2.amazonaws.com/industry_values.json) |
| `NUM_OF_FOLLOWERS`              | Specifies the number of followers a company has.            | types: [in] | "1-50", "51-100", "101-1000", "1001-5000", "5001+" |
| `ACCOUNT_ACTIVITIES`            | Specifies recent account activities, such as leadership changes or funding events. | types: [in] | "Senior leadership changes in last 3 months", "Funding events in past 12 months" |
| `JOB_OPPORTUNITIES`             | Specifies job opportunities available at the company.       | types: [in] | "Hiring on LinkedIn" |
| `COMPANY_HEADCOUNT_GROWTH`      | Specifies the growth of the company's headcount.            | types: [between] | N/A |
| `ANNUAL_REVENUE`                | Specifies the annual revenue of the company.                | types: [between] | "USD", "AED", "AUD", "BRL", "CAD", "CNY", "DKK", "EUR", "GBP", "HKD", "IDR", "ILS", "INR", "JPY", "NOK", "NZD", "RUB", "SEK", "SGD", "THB", "TRY", "TWD" |
| `DEPARTMENT_HEADCOUNT`          | Specifies the headcount of specific departments within the company. | types: [between] | "Accounting", "Administrative", "Arts and Design", "Business Development", "Community and Social Services", "Consulting", "Education", "Engineering", "Entrepreneurship", "Finance", "Healthcare Services", "Human Resources", "Information Technology", "Legal", "Marketing", "Media and Communication", "Military and Protective Services", "Operations", "Product Management", "Program and Project Management", "Purchasing", "Quality Assurance", "Real Estate", "Research", "Sales", "Customer Success and Support" |
| `DEPARTMENT_HEADCOUNT_GROWTH`   | Specifies the growth of headcount in specific departments.   | types: [between] | N/A |
| `KEYWORD`                       | Filters based on specific keywords related to the company.   | types: [in] | List of strings (max length 1) |

### Example of a Text Filter
```json
{
  "filter_type": "COMPANY_HEADCOUNT",
  "type": "in",
  "value": ["10,001+", "1,001-5,000"]
}
```

### Example of a Range Filter
```json
{
  "filter_type": "ANNUAL_REVENUE",
  "type": "between",
  "value": {"min": 1, "max": 500},
  "sub_filter": "USD"
}
```

### Example of a Boolean Filter
```json
{
  "filter_type": "IN_THE_NEWS"
}
```

This documentation provides a comprehensive overview of the Crustdata API, including request examples, payload fields, and filter types. For further details, please refer to the respective sections.

# API Documentation Overview

## Filter Dictionary for Person Search

### Filter Types

| Filter Type                | Description                                           | Properties | Value/Sub-filter |
|----------------------------|-------------------------------------------------------|------------|------------------|
| `CURRENT_COMPANY`          | Specifies the current company of the person.         | types: [in, not in] | List of strings. You can specify names, domains or LinkedIn URL of the companies. Example: `"Serve Robotics"`, `"serverobotics.com"`, `"https://www.linkedin.com/company/serverobotics"` |
| `CURRENT_TITLE`            | Specifies the current title of the person.           | types: [in, not in] | List of strings. Case insensitive contains matching for each of the strings. Example: `["ceo", "founder", "director"]` will match all profiles with any current job title(s) having any of the 3 strings. |
| `PAST_TITLE`               | Specifies the past titles held by the person.        | types: [in, not in] | List of strings. Example: `["ceo", "founder", "director"]` will match all profiles with any past job title(s) having any of the 3 strings. |
| `COMPANY_HEADQUARTERS`     | Specifies the headquarters of the person's company.  | types: [in, not in] | List of strings. |
| `COMPANY_HEADCOUNT`        | Specifies the size of the company based on the number of employees. | types: [in] | Example: `"Self-employed"`, `"1-10"`, `"11-50"`, `"51-200"`, `"201-500"`, `"501-1,000"`, `"1,001-5,000"`, `"5,001-10,000"`, `"10,001+"` |
| `REGION`                   | Specifies the geographical region of the person.     | types: [in, not in] | List of strings. |
| `INDUSTRY`                 | Specifies the industry of the person's company.      | types: [in, not in] | List of strings. |
| `PROFILE_LANGUAGE`         | Specifies the language of the person's profile.      | types: [in] | Example: `"Arabic"`, `"English"`, `"Spanish"`, etc. |
| `SENIORITY_LEVEL`          | Specifies the seniority level of the person.         | types: [in, not in] | Example: `"Owner / Partner"`, `"CXO"`, `"Vice President"`, etc. |
| `YEARS_AT_CURRENT_COMPANY` | Specifies the number of years the person has been at their current company. | types: [in] | Example: `"Less than 1 year"`, `"1 to 2 years"`, etc. |
| `YEARS_IN_CURRENT_POSITION` | Specifies the number of years the person has been in their current position. | types: [in] | Example: `"Less than 1 year"`, `"1 to 2 years"`, etc. |
| `YEARS_OF_EXPERIENCE`      | Specifies the total years of experience the person has. | types: [in] | Example: `"Less than 1 year"`, `"1 to 2 years"`, etc. |
| `FIRST_NAME`               | Specifies the first name of the person.              | types: [in] | List of strings (max length 1) |
| `LAST_NAME`                | Specifies the last name of the person.               | types: [in] | List of strings (max length 1) |
| `FUNCTION`                 | Specifies the function or role of the person.        | types: [in, not in] | Example: `"Accounting"`, `"Administrative"`, etc. |
| `POSTED_ON_LINKEDIN`      | Specifies if the person has posted on LinkedIn.      | N/A | N/A |
| `RECENTLY_CHANGED_JOBS`    | Specifies if the person has recently changed jobs.    | N/A | N/A |
| `IN_THE_NEWS`              | Specifies if the person has been mentioned in the news. | N/A | N/A |
| `KEYWORD`                  | Filters based on specific keywords related to the company. | types: [in] | List of strings (max length 1). Supports boolean filters. Example: `"'sales' or 'gtm' or 'marketer'"` will match any of these 3 words across the full LinkedIn profile of the person. |

## Making Requests

### Request Body

The request body can have the following keys (at least one of them is required):

- `linkedin_sales_navigator_search_url` (optional): URL of the Sales Navigator Accounts search from the browser.
- `filters` (optional): JSON dictionary defining the search criteria as laid out by the [Crustdata filter schema](#).
  
### Example Request

```bash
curl --location 'https://api.crustdata.com/screener/company/search' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json, text/plain, */*' \
--header 'Accept-Language: en-US,en;q=0.9' \
--header 'Authorization: Token $auth_token' \
--data '{
    "linkedin_sales_navigator_search_url": "https://www.linkedin.com/sales/search/company?query=(filters%3AList((type%3ACOMPANY_HEADCOUNT%2Cvalues%3AList((id%3AD%2Ctext%3A51-200%2CselectionType%3AINCLUDED)))%2C(type%3AREGION%2Cvalues%3AList((id%3A103323778%2Ctext%3AMexico%2CselectionType%3AINCLUDED)))%2C(type%3AINDUSTRY%2Cvalues%3AList((id%3A25%2Ctext%3AManufacturing%2CselectionType%3AINCLUDED)))))&sessionId=8TR8HMz%2BTVOYaeivK9p%2Bpg%3D%3D&viewAllFilters=true"
}'
```

### Example Request with Custom Search Filters

```bash
curl --location 'https://api.crustdata.com/screener/company/search' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json, text/plain, */*' \
--header 'Accept-Language: en-US,en;q=0.9' \
--header 'Authorization: Token $token' \
--data '{
    "filters": [
        {
            "filter_type": "COMPANY_HEADCOUNT",
            "type": "in",
            "value": ["10,001+", "1,001-5,000"]
        },
        {
            "filter_type": "ANNUAL_REVENUE",
            "type": "between",
            "value": {"min": 1, "max": 500},
            "sub_filter": "USD"
        },
        {
            "filter_type": "REGION",
            "type": "not in",
            "value": ["United States"]
        }
    ],
    "page": 2
}'
```

## Key Points

- Each page request costs 25 credits.
- The data is fetched in real-time from LinkedIn, and the latency for this endpoint is between 10 to 30 seconds.
- Because the data is fetched in real-time, the response schema may differ from the company data enrichment endpoint. However, all results will be added to Crustdata’s database within 60 minutes of your query, and the data for a specific company profile can be enriched via the company enrichment endpoint.

## LinkedIn Posts by Company API (real-time)

### Overview

This endpoint retrieves recent LinkedIn posts and related engagement metrics for a specified company.

### Example Request

```bash
curl --location 'https://api.crustdata.com/screener/company/posts' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json, text/plain, */*' \
--header 'Authorization: Token $auth_token' \
--data '{
    "company_name": "Example Company",
    "page": 1,
    "limit": 5
}'
```

### Request Parameters

- `company_name` (optional): Company name.
- `company_domain` (optional): Company domain.
- `company_id` (optional): Company ID.
- `company_linkedin_url` (optional): Company LinkedIn URL.
- `page` (optional, default: 1): Page number for pagination.
- `limit` (optional, default: 5): Limit the number of posts in a page.
- `post_types` (optional, default: repost, original): Specify the types of posts to retrieve.

### Note

Provide only one of the company identifiers.

# LinkedIn Posts API Documentation

## Overview
This API endpoint retrieves LinkedIn posts containing specified keywords along with related engagement metrics.

## Key Points
- **Credits**: 
  - Without reactors (default): Each successful page request costs 5 credits.
  - With reactors: Each successful page request costs 25 credits.
- **Pagination**: 
  - Increment the value of `page` query param to fetch the next set of posts.
  - Most recent posts will be in the first page and then so on.
  - Currently, you can only fetch up to 20 pages of the latest posts. For more, contact the Crustdata team at [info@crustdata.com](mailto:info@crustdata.com).
- **Latency**: 
  - The data is fetched in real-time from LinkedIn, with a latency of 30 to 60 seconds depending on the number of reactions for all the posts on the page.

## Request

### Request Body Overview
The request body is a JSON object that contains the following parameters:

| Parameter | Description | Default | Required |
|-----------|-------------|---------|----------|
| `keyword` | The keyword or phrase to search for in LinkedIn posts. | - | Yes |
| `page` | Page number for pagination. | 1 | Yes |
| `limit` | Limit the number of posts in a page. | 5 | No |
| `sort_by` | Defines the sorting order of the results. Can be either "relevance" or "date_posted". | "date_posted" | No |
| `date_posted` | Filters posts by the date they were posted. Can be "past-24h", "past-week", "past-month", "past-quarter", or "past-year". | "past-24h" | No |

### Example Request
```bash
curl 'https://api.crustdata.com/screener/linkedin_posts/keyword_search/' \
-H 'Accept: application/json, text/plain, */*' \
-H 'Accept-Language: en-US,en;q=0.9' \
-H 'Authorization: Token $auth_token' \
-H 'Connection: keep-alive' \
-H 'Content-Type: application/json' \
-H 'Origin: https://crustdata.com' \
--data-raw '{
   "keyword":"LLM Evaluation",
   "page":1,
   "sort_by":"relevance",
   "date_posted":"past-quarter"
}' --compressed
```

## Response
The response provides a list of recent LinkedIn posts for the specified company, including post content, engagement metrics, and information about users who interacted with the posts.

### Response Structure
```json
{
  "posts": [
    {
      "backend_urn": "urn:li:activity:7236812027275419648",
      "share_urn": "urn:li:share:7236812026038083584",
      "share_url": "https://www.linkedin.com/posts/crustdata_y-combinators-most-popular-startups-from-activity-7236812027275419648-4fyw?utm_source=combined_share_message&utm_medium=member_desktop",
      "text": "Y Combinator’s most popular startups...",
      "actor_name": "Crustdata",
      "date_posted": "2024-09-03",
      "hyperlinks": {
        "company_linkedin_urls": [],
        "person_linkedin_urls": [
          "https://www.linkedin.com/in/ACoAAAKoldoBqSsiXY_DHsXdSk1slibabeTvDDY"
        ],
        "other_urls": []
      },
      "total_reactions": 37,
      "total_comments": 7,
      "reactions_by_type": {
        "LIKE": 28,
        "EMPATHY": 4,
        "PRAISE": 4,
        "INTEREST": 1
      },
      "num_shares": 5,
      "is_repost_without_thoughts": false,
      "reactors": [
        {
          "name": "Courtney May",
          "linkedin_profile_url": "https://www.linkedin.com/in/ACwAACkMyzkBYncrCuM2rzhc06iz6oj741NL-98",
          "reaction_type": "LIKE",
          "profile_image_url": "https://media.licdn.com/dms/image/v2/D5603AQF-8vL_c5H9Zg/profile-displayphoto-shrink_100_100/profile-displayphoto-shrink_100_100/0/1690558480623?e=1730937600&v=beta&t=Lm2hHLTFiEVlHWdTt-Vh3vDYevK8U8SlPqaFdNu3R6A",
          "title": "GTM @ Arc (YC W22)",
          "additional_info": "3rd+",
          "location": "San Francisco, California, United States",
          "linkedin_profile_urn": "ACwAACkMyzkBYncrCuM2rzhc06iz6oj741NL-98",
          "default_position_title": "GTM @ Arc (YC W22)",
          "default_position_company_linkedin_id": "74725230",
          "default_position_is_decision_maker": false,
          "flagship_profile_url": "https://www.linkedin.com/in/courtney-may-8a178b172",
          "profile_picture_url": "https://media.licdn.com/dms/image/v2/D5603AQF-8vL_c5H9Zg/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1690558480623?e=1730937600&v=beta&t=vHg233746zA00m3q2vHKSFcthL3YKiagTtVEZt1qqJI",
          "headline": "GTM @ Arc (YC W22)",
          "summary": null,
          "num_of_connections": 786,
          "related_colleague_company_id": 74725230,
          "skills": [
            "Marketing Strategy",
            "Product Support",
            "SOC 2"
          ]
        }
      ]
    }
  ]
}
```

### Each item in the `posts` array contains the following fields:
- `backend_urn` (string): Unique identifier for the post in LinkedIn's backend system.
- `share_urn` (string): Unique identifier for the shared content.
- `share_url` (string): Direct URL to the post on LinkedIn.
- `text` (string): The full content of the post.
- `actor_name` (string): Name of the company or person who created the post.
- `date_posted` (string): Date when the post was published, in "YYYY-MM-DD" format.
- `hyperlinks` (object): Contains the external links and Company/Person LinkedIn URLs mentioned in the post.
- `total_reactions` (integer): Total number of reactions on the post.
- `total_comments` (integer): Total number of comments on the post.
- `reactions_by_type` (object): Breakdown of reactions by type.
- `num_shares` (integer): Number of times the post has been shared.
- `is_repost_without_thoughts` (boolean): Indicates if the post is a repost without additional thoughts.
- `reactors` (array): List of users who reacted to the post.

### Reactor Object Fields:
- `name` (string): Full name of the person who reacted.
- `linkedin_profile_url` (string): URL to the reactor's LinkedIn profile.
- `reaction_type` (string): Type of reaction given (e.g., "LIKE", "EMPATHY").
- `profile_image_url` (string): URL to the reactor's profile image (100x100 size).
- `title` (string): Current professional title of the reactor.
- `additional_info` (string): Additional information, often indicating connection degree.
- `location` (string): Geographic location of the reactor.
- `linkedin_profile_urn` (string): Unique identifier for the reactor's LinkedIn profile.
- `default_position_title` (string): Primary job title.
- `default_position_company_linkedin_id` (string): LinkedIn ID of the reactor's primary company.
- `default_position_is_decision_maker` (boolean): Indicates if the reactor is in a decision-making role.
- `flagship_profile_url` (string): Another form of the reactor's LinkedIn profile URL.
- `profile_picture_url` (string): URL to a larger version of the profile picture (400x400 size).
- `headline` (string): Professional headline from the reactor's LinkedIn profile.
- `summary` (string or null): Brief professional summary, if available.
- `num_of_connections` (integer): Number of LinkedIn connections the reactor has.
- `related_colleague_company_id` (integer): LinkedIn ID of a related company, possibly current employer.
- `skills` (array of strings): List of professional skills listed on the reactor's profile.

# Crustdata API Documentation

## Overview
The Crustdata API provides endpoints for enriching data related to individuals using LinkedIn profiles or business email addresses. This documentation outlines the key features, request formats, and response structures for the API.

---

## People Endpoints

### Enrichment: People Profile(s) API

#### Overview
Enrich data for one or more individuals using LinkedIn profile URLs or business email addresses. This API allows you to retrieve enriched person data from Crustdata’s database or perform a real-time search from the web if the data is not available.

#### Key Features
- Enrich data using LinkedIn profile URLs or business email addresses (3 credits per profile/email).
- Option to perform a real-time search if data is not present in the database (5 credits per profile/email).
- Retrieve data for up to 25 profiles or emails in a single request.

#### Required Authentication
- An authentication token (`auth_token`) is required for authorization.

---

### Request Format

#### Query Parameters
- `linkedin_profile_url` (optional): Comma-separated list of LinkedIn profile URLs.
- `business_email` (optional): Person's business email address (only one allowed per request).
- `enrich_realtime` (optional): Boolean (True or False). If set to True, performs a real-time search from the web if data is not found in the database. Default is False.
- `fields` (optional): Comma-separated list of fields to include in the response.
- `page` (optional): Page number for pagination (used only with `filters`).
- `preview` (optional): Boolean field to get the preview of profiles.

#### Example Request with LinkedIn Profile URLs
```bash
curl 'https://api.crustdata.com/screener/person/enrich?linkedin_profile_url=https://www.linkedin.com/in/johndoe/,https://www.linkedin.com/in/janedoe/' \
  --header 'Accept: application/json, text/plain, */*' \
  --header 'Accept-Language: en-US,en;q=0.9' \
  --header 'Authorization: Token $auth_token'
```

#### Example Request with Business Email
```bash
curl 'https://api.crustdata.com/screener/person/enrich?business_email=john.doe@example.com' \
  --header 'Accept: application/json, text/plain, */*' \
  --header 'Accept-Language: en-US,en;q=0.9' \
  --header 'Authorization: Token $auth_token'
```

#### Example Request with Real-Time Enrichment
```bash
curl 'https://api.crustdata.com/screener/person/enrich?linkedin_profile_url=https://www.linkedin.com/in/johndoe/&enrich_realtime=True' \
  --header 'Accept: application/json, text/plain, */*' \
  --header 'Accept-Language: en-US,en;q=0.9' \
  --header 'Authorization: Token $auth_token'
```

---

### Response Format
- When LinkedIn profiles are present in Crustdata’s database, the response will include the enriched data for each profile.
- If profiles are not found and `enrich_realtime` is set to False, an empty response is returned for those entries, and they will be auto-enriched in the background. Query again after at least 60 minutes to retrieve the data.

#### Example Response
```json
{
  "profiles": [
    {
      "linkedin_profile_url": "https://www.linkedin.com/in/johndoe/",
      "name": "John Doe",
      "location": "New York, USA",
      "email": "john.doe@example.com",
      "title": "Software Engineer",
      "skills": ["Python", "JavaScript", "React"]
    },
    {
      "linkedin_profile_url": "https://www.linkedin.com/in/janedoe/",
      "name": "Jane Doe",
      "location": "San Francisco, USA",
      "email": "jane.doe@example.com",
      "title": "Product Manager",
      "skills": ["Product Management", "Agile", "Scrum"]
    }
  ]
}
```

---

### Key Points
- Each successful page request costs 5 credits.
- Increment the value of `page` query param to fetch the next set of posts. Each page has 5 posts.
- The `limit` can not exceed 5 when `page` is provided in the payload. To retrieve posts in bulk, use the `limit` parameter (with value over 5 allowed here) without the `page` parameter.
- Latency for this endpoint is between 5 to 10 seconds depending on the number of posts fetched in a request.

---

### Constraints
- Ensure all LinkedIn URLs and email addresses are correctly formatted.
- Invalid inputs result in validation errors.
- Do not include both `linkedin_profile_url` and `business_email` in the same request.

---

### Credits
- Database Enrichment: 3 credits per LinkedIn profile or email.
- Real-Time Enrichment (enrich_realtime=True): 5 credits per LinkedIn profile or email.

--- 

This documentation provides a comprehensive overview of the Crustdata API for enriching LinkedIn profiles. For further details, please refer to the official API documentation or contact support.

# API Documentation Overview

## People Search API

### Description
This API allows you to retrieve people working at specific companies (e.g., Google, Microsoft) while excluding certain job titles (e.g., Software Engineer, Data Scientist). It focuses on individuals based in the United States or Canada and from specific industries.

### Example Request
To perform a search, you can use the following `curl` command:

```bash
curl --location 'https://api.crustdata.com/screener/person/search' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json, text/plain, */*' \
--header 'Accept-Language: en-US,en;q=0.9' \
--header 'Authorization: Token $token' \
--data '{
    "filters": [
        {
            "filter_type": "CURRENT_COMPANY",
            "type": "in",
            "value": ["Google", "Microsoft"]
        },
        {
            "filter_type": "CURRENT_TITLE",
            "type": "not in",
            "value": ["Software Engineer", "Data Scientist"]
        },
        {
            "filter_type": "COMPANY_HEADQUARTERS",
            "type": "in",
            "value": ["United States", "Canada"]
        },
        {
            "filter_type": "INDUSTRY",
            "type": "in",
            "value": ["Software Development", "Hospitals and Health Care"]
        },
        {
            "filter_type": "REGION",
            "type": "not in",
            "value": ["California, United States", "New York, United States"]
        }
    ],
    "page": 1
}'
```

### More Examples

#### 1. People with Specific First Name from a Specific Company Given Company’s Domain
```bash
curl --location 'https://api.crustdata.com/screener/person/search' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json, text/plain, */*' \
--header 'Accept-Language: en-US,en;q=0.9' \
--header 'Authorization: Token $token' \
--data '{
    "filters": [
        {
            "filter_type": "FIRST_NAME",
            "type": "in",
            "value": ["steve"]
        },
        {
            "filter_type": "CURRENT_COMPANY",
            "type": "in",
            "value": ["buzzbold.com"]
        }
    ],
    "page": 1
}'
```

#### 2. People with Specific First Name from a Specific Company Given Company’s LinkedIn URL
```bash
curl --location 'https://api.crustdata.com/screener/person/search' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json, text/plain, */*' \
--header 'Authorization: Token $token' \
--data '{
    "filters": [
        {
            "filter_type": "FIRST_NAME",
            "type": "in",
            "value": ["Ali"]
        },
        {
            "filter_type": "CURRENT_COMPANY",
            "type": "in",
            "value": ["https://www.linkedin.com/company/serverobotics"]
        }
    ],
    "page": 1
}'
```

#### 3. Preview List of People Given Filter Criteria
```bash
curl --location 'https://api.crustdata.com/screener/person/search' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token $token' \
--data '{
    "filters": [
        {
            "filter_type": "CURRENT_COMPANY",
            "type": "in",
            "value": ["serverobotics.com"]
        },
        {
            "filter_type": "REGION",
            "type": "in",
            "value": ["United States"]
        }
    ],
    "preview": true
}'
```

### Response
The response will include a list of people matching the criteria, with details such as their names, job titles, and LinkedIn profiles.

### Key Points
- Each successful page request costs 25 credits. With `preview`, a successful request costs 5 credits.
- The API fetches data in real-time from LinkedIn, with a latency of 10 to 30 seconds.
- The response schema may vary as data is fetched in real-time.

## LinkedIn Posts by Person API (Real-Time)

### Overview
This endpoint retrieves recent LinkedIn posts and related engagement metrics for a specified person.

### Example Request
```bash
curl --location 'https://api.crustdata.com/screener/person/posts' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token $token' \
--data '{
    "person_linkedin_url": "https://linkedin.com/in/abhilash-chowdhary",
    "page": 1
}'
```

### Response Structure
The response provides a list of recent LinkedIn posts for the specified person, including post content, engagement metrics, and information about users who interacted with the posts.

### Response Example
```json
{
  "posts": [
    {
      "backend_urn": "urn:li:activity:7236812027275419648",
      "share_urn": "urn:li:share:7236812026038083584",
      "share_url": "https://www.linkedin.com/posts/crustdata_y-combinators-most-popular-startups-from-activity-7236812027275419648-4fyw?utm_source=combined_share_message&utm_medium=member_desktop",
      "text": "Y Combinator’s most popular startups...",
      "actor_name": "Crustdata",
      "date_posted": "2024-09-03",
      "total_reactions": 37,
      "total_comments": 7,
      "reactors": [
        {
          "name": "Courtney May",
          "linkedin_profile_url": "https://www.linkedin.com/in/ACwAACkMyzkBYncrCuM2rzhc06iz6oj741NL-98",
          "reaction_type": "LIKE"
        }
      ]
    }
  ]
}
```

### Required Parameters
- `person_linkedin_url`: LinkedIn profile URL of the person (required).

### Optional Parameters
- `page`: Page number for pagination (default: 1).
- `limit`: Limit the number of posts in a page (default: 5).
- `fields`: Comma-separated list of fields to include in the response.

### Response Fields
- `posts`: Array containing post details.
- Each post includes fields like `backend_urn`, `share_url`, `text`, `actor_name`, `date_posted`, `total_reactions`, `total_comments`, and `reactors`.

This documentation provides a comprehensive overview of the API's capabilities, usage examples, and response structures.

# API Documentation Summary

## Data Fields

### Reactor Information
- **num_of_connections** (integer): Number of LinkedIn connections the reactor has.
- **related_colleague_company_id** (integer): LinkedIn ID of a related company, possibly current employer.
- **skills** (array of strings): List of professional skills listed on the reactor's profile.

### Employment History
- **employer** (array of objects): Employment history, each containing:
  - **title** (string): Job title.
  - **company_name** (string): Name of the employer.
  - **company_linkedin_id** (string or null): LinkedIn ID of the company.
  - **start_date** (string): Start date of employment in ISO format.
  - **end_date** (string or null): End date of employment in ISO format, or null if current.
  - **description** (string or null): Job description, if available.
  - **location** (string or null): Job location.
  - **rich_media** (array): Currently empty, may contain media related to the job.

### Educational Background
- **education_background** (array of objects): Educational history, each containing:
  - **degree_name** (string): Type of degree obtained.
  - **institute_name** (string): Name of the educational institution.
  - **field_of_study** (string): Area of study.
  - **start_date** (string): Start date of education in ISO format.
  - **end_date** (string): End date of education in ISO format.

### Contact Information
- **emails** (array of strings): Known email addresses associated with the reactor.
- **websites** (array): Currently empty, may contain personal or professional websites.
- **twitter_handle** (string or null): Twitter username, if available.
- **languages** (array): Currently empty, may contain languages spoken.
- **pronoun** (string or null): Preferred pronouns, if specified.
- **current_title** (string): Current job title, often identical to `default_position_title`.

## API Usage Endpoints

### Get Remaining Credits
- **Request**: A plain GET request without any query params.
- **Required**: Authentication token `auth_token` for user identification.

#### Example Request
```bash
curl --location 'https://api.crustdata.com/user/credits' \
--header 'Accept: application/json, text/plain, */*' \
--header 'Accept-Language: en-US,en;q=0.9' \
--header 'Authorization: Token $auth_token' \
--header 'Content-Type: application/json'
```

#### Example Response
```json
{
    "credits": 1000000
}
```

## Key Points
- **Credits**: 
  - Without reactors (default): Each successful page request costs 5 credits.
  - With reactors: Each successful page request costs 25 credits.
  
- **Pagination**: Increment the value of `page` query param to fetch the next set of posts. Most recent posts will be in the first page and then so on. Currently, you can only fetch up to 20 pages of latest posts. In case you want to fetch more, contact Crustdata team at [info@crustdata.com](mailto:info@crustdata.com).

- **Latency**: The data is fetched in real-time from LinkedIn and the latency for this endpoint is between 30 to 60 seconds depending on the number of reactions for all the posts in the page.

