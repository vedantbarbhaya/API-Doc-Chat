# Crustdata Discovery And Enrichment API Documentation

## Overview
The Crustdata Discovery and Enrichment API provides access to a variety of data related to companies, including firmographics, revenue, employee headcount, and founder backgrounds.

---

## Company Data Dictionary

### Firmographics

| Column Name                     | Description                                                                 | Source     | Time Series Available |
|----------------------------------|-----------------------------------------------------------------------------|------------|-----------------------|
| company_name                    | Name of the company                                                         |            |                       |
| last_updated_date               | The timestamp when this information was last updated                       |            |                       |
| hq_country                      | The country where the company's headquarters is located                     |            |                       |
| largest_headcount_country        | The country with the most employees of the company                          |            |                       |
| last_funding_round_type         | The type of the company's last funding round                                |            |                       |
| company_website                 | The company's official website URL                                          |            |                       |
| company_website_domain          | The domain of the company's website                                         |            |                       |
| valuation_usd                   | The current valuation of the company in USD                                 |            |                       |
| valuation_date                  | The date when the current valuation was determined                          |            |                       |
| linkedin_categories              | The categories of the company on LinkedIn                                   |            |                       |
| linkedin_industries             | The industries in which the company operates, according to LinkedIn        |            |                       |
| crunchbase_investors            | The investors in the company, according to Crunchbase                      |            |                       |
| tracxn_investors                | The investors in the company, according to Tracxn                          |            |                       |

### Revenue

| Column Name                     | Description                                                                 | Source     | Time Series Available |
|----------------------------------|-----------------------------------------------------------------------------|------------|-----------------------|
| estimated_revenue_lower_bound_usd | Estimated revenue in USD lower limit                                       | LinkedIn   | Yes                   |
| estimated_revenue_higher_bound_usd | Estimated revenue in USD higher limit                                      | LinkedIn   | Yes                   |

### Employee Headcount

| Column Name                     | Description                                                                 | Source     | Time Series Available |
|----------------------------------|-----------------------------------------------------------------------------|------------|-----------------------|
| linkedin_headcount              | The total number of employees at the company, according to LinkedIn        | LinkedIn   | Yes                   |
| linkedin_followers              | The total number of followers of the company's LinkedIn profile            | LinkedIn   | Yes                   |
| linkedin_headcount_engineering   | The total number of engineering employees at the company, according to LinkedIn | LinkedIn | Yes                   |
| linkedin_headcount_sales         | The total number of sales employees at the company, according to LinkedIn  | LinkedIn   | Yes                   |
| linkedin_headcount_operations     | The total number of operations employees at the company, according to LinkedIn | LinkedIn | Yes                   |
| linkedin_headcount_human_resource | The total number of human resources employees at the company, according to LinkedIn | LinkedIn | Yes                   |
| linkedin_headcount_india         | The total number of employees based in India at the company, according to LinkedIn | LinkedIn | Yes                   |
| linkedin_headcount_usa           | The total number of employees based in USA at the company, according to LinkedIn | LinkedIn | Yes                   |

### Founder Background

| Column Name                     | Description                                                                 | Source     | Time Series Available |
|----------------------------------|-----------------------------------------------------------------------------|------------|-----------------------|
| founder_names_and_profile_urls   | Names and Linkedin profile URLs of the company's founders and decision makers | LinkedIn | Yes                   |
| founders_location                | Geographical location(s) of the company's and decision makers               | LinkedIn   | Yes                   |
| founders_education_institute     | Educational institutions attended by the company's founders                 | LinkedIn   | Yes                   |
| founders_degree_name             | Degree(s) held by the company's founders                                    | LinkedIn   | Yes                   |
| founders_previous_company        | Previous company(ies) where the company's founders have worked before      | LinkedIn   | Yes                   |

---

## Conclusion
This API provides a comprehensive set of data points that can be utilized for various analytical and enrichment purposes related to companies and their founders. The structured data format allows for easy integration into applications and services.

# API Documentation Summary

## Employee Metrics

### Employee Headcount Growth Metrics

| Column Name                                           | Description                                                                 | Source   |
|------------------------------------------------------|-----------------------------------------------------------------------------|----------|
| `linkedin_headcount_sales_yoy_growth_pct`           | The one year growth percentage in Sales headcount, according to LinkedIn   | LinkedIn |
| `linkedin_headcount_operations_six_months_growth_pct` | The six months growth percentage in Sales headcount, according to LinkedIn | LinkedIn |
| `linkedin_headcount_operations_yoy_growth_pct`      | The one year growth percentage in Operations headcount, according to LinkedIn | LinkedIn |
| `linkedin_headcount_quality_assurance_six_months_growth_pct` | The six months growth percentage in Quality Assurance headcount, according to LinkedIn | LinkedIn |
| `linkedin_headcount_quality_assurance_yoy_growth_pct` | The one year growth percentage in Quality Assurance headcount, according to LinkedIn | LinkedIn |
| `linkedin_headcount_usa_six_months_growth_pct`     | The six months growth percentage in US headcount, according to LinkedIn    | LinkedIn |
| `linkedin_headcount_usa_yoy_growth_pct`             | The one year growth percentage in US headcount, according to LinkedIn      | LinkedIn |
| `linkedin_headcount_india_six_months_growth_pct`   | The six months growth percentage in India headcount, according to LinkedIn  | LinkedIn |
| `linkedin_headcount_india_yoy_growth_pct`           | The one year growth percentage in India headcount, according to LinkedIn    | LinkedIn |
| `linkedin_headcount_mexico_six_months_growth_pct`  | The six months growth percentage in Mexico headcount, according to LinkedIn | LinkedIn |
| `linkedin_headcount_mexico_yoy_growth_pct`          | The one year growth percentage in Mexico headcount, according to LinkedIn   | LinkedIn |

## Employee Skills

| Column Name                                           | Description                                                                 | Source   |
|------------------------------------------------------|-----------------------------------------------------------------------------|----------|
| `linkedin_all_employee_skill_names`                  | All skill names of employees at the company, according to LinkedIn        | LinkedIn |
| `linkedin_all_employee_skill_count`                  | Count of each skill among employees at the company, according to LinkedIn  | LinkedIn |
| `linkedin_employee_skills_0_to_10_pct`              | Percentage of employees with 0-10% proficiency in skills, according to LinkedIn | LinkedIn |
| `linkedin_employee_skills_11_to_30_pct`             | Percentage of employees with 11-30% proficiency in skills, according to LinkedIn | LinkedIn |
| `linkedin_employee_skills_31_to_50_pct`             | Percentage of employees with 31-50% proficiency in skills, according to LinkedIn | LinkedIn |
| `linkedin_employee_skills_51_to_70_pct`             | Percentage of employees with 51-70% proficiency in skills, according to LinkedIn | LinkedIn |
| `linkedin_employee_skills_71_to_100_pct`            | Percentage of employees with 71-100% proficiency in skills, according to LinkedIn | LinkedIn |

## Employee Review and Rating

| Column Name                                           | Description                                                                 | Source   |
|------------------------------------------------------|-----------------------------------------------------------------------------|----------|
| `glassdoor_overall_rating`                           | The company's overall rating on Glassdoor                                   | Glassdoor |
| `glassdoor_culture_rating`                           | The company's culture rating on Glassdoor                                   | Glassdoor |
| `glassdoor_diversity_rating`                         | The company's diversity rating on Glassdoor                                  | Glassdoor |
| `glassdoor_work_life_balance_rating`                 | The company's work-life balance rating on Glassdoor                          | Glassdoor |
| `glassdoor_senior_management_rating`                 | The company's senior management rating on Glassdoor                          | Glassdoor |
| `glassdoor_compensation_rating`                      | The company's compensation rating on Glassdoor                               | Glassdoor |
| `glassdoor_career_opportunities_rating`              | The company's career opportunities rating on Glassdoor                       | Glassdoor |
| `glassdoor_recommend_to_friend_pct`                  | The percentage of Glassdoor reviewers who would recommend the company to a friend | Glassdoor |
| `glassdoor_ceo_approval_pct`                         | The percentage of Glassdoor reviewers who approve of the CEO                | Glassdoor |
| `glassdoor_business_outlook_pct`                     | The percentage of Glassdoor reviewers who have a positive business outlook for the company | Glassdoor |
| `glassdoor_review_count`                             | The number of reviews of the company on Glassdoor                           | Glassdoor |

## Product Reviews

| Column Name                                           | Description                                                                 | Source   |
|------------------------------------------------------|-----------------------------------------------------------------------------|----------|
| `g2_review_count`                                    | The number of reviews of the company on G2                                  | G2       |
| `g2_average_rating`                                  | The company's average rating on G2                                         | G2       |

## Web Traffic

| Column Name                                           | Description                                                                 | Source   |
|------------------------------------------------------|-----------------------------------------------------------------------------|----------|
| `monthly_visitors`                                   | The number of monthly visitors to the company's site as recorded by Similarweb | Similarweb |
| `monthly_visitor_mom_pct`                           | The month-over-month percentage change in the number of monthly visitors to the company's site as recorded by Similarweb | Similarweb |
| `traffic_source_social_pct`                          | The percentage of the company's site traffic that comes from social media, as recorded by Similarweb | Similarweb |
| `traffic_source_search_pct`                          | The percentage of the company's site traffic that comes from search engines, as recorded by Similarweb | Similarweb |
| `traffic_source_direct_pct`                          | The percentage of the company's site traffic that comes directly, as recorded by Similarweb | Similarweb |
| `traffic_source_paid_referral_pct`                   | The percentage of the company's site traffic that comes from paid referrals, as recorded by Similarweb | Similarweb |
| `traffic_source_referral_pct`                        | The percentage of the company's site traffic that comes from non-paid referrals, as recorded by Similarweb | Similarweb |

## Job Listing Growth By Function

| Column Name                                           | Description                                                                 | Source   |
|------------------------------------------------------|-----------------------------------------------------------------------------|----------|
| `job_openings_accounting_qoq_pct`                   | Quarterly growth percentage of job openings in accounting                   | LinkedIn |
| `job_openings_accounting_six_months_growth_pct`     | Six months growth percentage of job openings in accounting                  | LinkedIn |
| `job_openings_art_and_design_qoq_pct`                | Quarterly growth percentage of job openings in art and design               | LinkedIn |
| `job_openings_art_and_design_six_months_growth_pct`  | Six months growth percentage of job openings in art and design              | LinkedIn |
| `job_openings_business_development_qoq_pct`          | Quarterly growth percentage of job openings in business development          | LinkedIn |
| `job_openings_business_development_six_months_growth_pct` | Six months growth percentage of job openings in business development        | LinkedIn |
| `job_openings_engineering_qoq_pct`                   | Quarterly growth percentage of job openings in engineering                  | LinkedIn |
| `job_openings_engineering_six_months_growth_pct`     | Six months growth percentage of job openings in engineering                 | LinkedIn |
| `job_openings_finance_qoq_pct`                       | Quarterly growth percentage of job openings in finance                      | LinkedIn |
| `job_openings_finance_six_months_growth_pct`         | Six months growth percentage of job openings in finance                     | LinkedIn |
| `job_openings_human_resource_qoq_pct`                | Quarterly growth percentage of job openings in human resources              | LinkedIn |
| `job_openings_human_resource_six_months_growth_pct`  | Six months growth percentage of job openings in human resources             | LinkedIn |
| `job_openings_information_technology_qoq_pct`        | Quarterly growth percentage of job openings in information technology       | LinkedIn |
| `job_openings_information_technology_six_months_growth_pct` | Six months growth percentage of job openings in information technology     | LinkedIn |
| `job_openings_marketing_qoq_pct`                     | Quarterly growth percentage of job openings in marketing                   | LinkedIn |
| `job_openings_marketing_six_months_growth_pct`       | Six months growth percentage of job openings in marketing                  | LinkedIn |
| `job_openings_media_and_communication_qoq_pct`       | Quarterly growth percentage of job openings in media and communication     | LinkedIn |
| `job_openings_media_and_communication_six_months_growth_pct` | Six months growth percentage of job openings in media and communication   | LinkedIn |
| `job_openings_operations_qoq_pct`                     | Quarterly growth percentage of job openings in operations                  | LinkedIn |
| `job_openings_operations_six_months_growth_pct`       | Six months growth percentage of job openings in operations                 | LinkedIn |
| `job_openings_research_qoq_pct`                       | Quarterly growth percentage of job openings in research                    | LinkedIn |
| `job_openings_research_six_months_growth_pct`         | Six months growth percentage of job openings in research                   | LinkedIn |

# API Documentation Summary

## Job Openings

### Job Openings Metrics

| Column Name                                          | Description                                               | Source   |
|-----------------------------------------------------|-----------------------------------------------------------|----------|
| `job_openings_sales_qoq_pct`                        | Quarterly growth percentage of job openings in sales      | LinkedIn |
| `job_openings_sales_six_months_growth_pct`         | Six months growth percentage of job openings in sales      | LinkedIn |
| `job_openings_product_management_qoq_pct`           | Quarterly growth percentage of job openings in product management | LinkedIn |
| `job_openings_product_management_six_months_growth_pct` | Six months growth percentage of job openings in product management | LinkedIn |
| `job_openings_overall_qoq_pct`                      | Quarterly growth percentage of overall job openings        | LinkedIn |
| `job_openings_overall_six_months_growth_pct`       | Six months growth percentage of overall job openings       | LinkedIn |

## Total Job Listings

| Column Name                | Description                                               | Source   |
|----------------------------|-----------------------------------------------------------|----------|
| `job_openings_title`       | Current job opening titles at the company                 | LinkedIn |
| `job_openings_count`       | The total count of current job openings at the company     | LinkedIn |
| `job_openings_count_mom_pct` | The percentage change in the number of job openings at the company on a month-over-month basis | LinkedIn |
| `job_openings_count_qoq_pct` | The percentage change in the number of job openings at the company on a quarter-over-quarter basis | LinkedIn |
| `job_openings_count_yoy_pct` | The percentage change in the number of job openings at the company on a year-over-year basis | LinkedIn |

## Ads

| Column Name                | Description                                               | Source   |
|----------------------------|-----------------------------------------------------------|----------|
| `meta_total_ads`           | Total Ads during the lifetime of the company              | Meta     |
| `meta_active_ads`          | Currently active Ads by the company                        | LinkedIn |
| `meta_ad_url`              | URL of company’s page on Meta Ads Library                 | LinkedIn |
| `monthly_paid_clicks`      | Estimated number of clicks on website from Google Ads     | Spyfu    |
| `monthly_organic_clicks`   | Estimated number of clicks on website from organic search results | Spyfu    |
| `average_ad_rank`          | Average position of all the company domain’s ad           | Spyfu    |
| `total_organic_results`     | Number of keywords for which the company domain appears in organic search result | Spyfu    |

## SEO and Google Search Ranking

| Column Name                | Description                                               | Source   |
|----------------------------|-----------------------------------------------------------|----------|
| `average_organic_rank`     | Average rank of company domain on keywords for which it ranks in top 100 results | Spyfu    |
| `monthly_google_ads_budget` | Monthly budget in USD of google ads campaigns             | Spyfu    |
| `num_of_impressions`       | Number of times company is searched on Google            | Google   |
| `num_of_impressions_mom_growth` | Monthly growth of number of times company is searched on Google | Google   |
| `num_of_impressions_qoq_growth` | Quarterly growth of number of times company is searched on Google | Google   |
| `num_of_impressions_yoy_growth` | Yearly growth of number of times company is searched on Google | Google   |

## Twitter Followers

| Column Name                | Description                                               | Source   |
|----------------------------|-----------------------------------------------------------|----------|
| `followers`                | Number of followers on company’s Twitter handle          | Twitter  |
| `followers_mom_growth`     | Monthly growth of Twitter followers                       | Twitter  |
| `followers_qoq_growth`     | Quarterly growth of Twitter followers                     | Twitter  |
| `followers_yoy_growth`     | Yearly growth of Twitter followers                        | Twitter  |

## Twitter Posts

| Column Name                | Description                                               | Source   |
|----------------------------|-----------------------------------------------------------|----------|
| `post_content`             | Content of the post on Twitter by the Company            | Twitter  |
| `date_posted`             | Date of the Twitter post                                  | Twitter  |
| `likes`                    | Number of likes of the post                               | Twitter  |
| `retweets`                 | Number of retweets of the post                            | Twitter  |
| `comments`                 | Number of comments on the post                            | Twitter  |

## News Articles

| Column Name                | Description                                               | Source   |
|----------------------------|-----------------------------------------------------------|----------|
| `title`                    | Title of article                                         | News Publisher |
| `article_link`            | Website link of the article                              | News Publisher |
| `date_published`          | Date the article was first published by the news publisher | News Publisher |
| `one_line_description`     | One line description of the content of the article       | News Publisher |

## Form D Filings

| Column Name                | Description                                               | Source   |
|----------------------------|-----------------------------------------------------------|----------|
| `total_amount`             | Total offering amount in USD                             | SEC EDGAR |
| `date_filed`               | Date FORM D was filed                                    | SEC EDGAR |
| `accession_no`             | SEC Accession No                                         | SEC EDGAR |
| `file_no`                  | SEC File No                                             | SEC EDGAR |
| `date_of_first_sale`       | Date of sale of the security                             | SEC EDGAR |

## People

### Profile and Background

| Column Name                | Description                                               | Source   |
|----------------------------|-----------------------------------------------------------|----------|
| `linkedin_profile_url`     | LinkedIn profile url of the person                       | LinkedIn |
| `linkedin_flagship_url`    | LinkedIn profile url in readable format                  | LinkedIn |

# API Documentation Overview

This document provides a detailed overview of the API functions, including their parameters and descriptions. Below are the relevant tables extracted from the HTML content.

## API Functions and Parameters

### User Information

| Parameter                     | Description                                               | Example      |
|-------------------------------|-----------------------------------------------------------|--------------|
| `name`                        | Name of the person                                        | John Doe     |
| `email`                       | Email of the person                                      | john@example.com |
| `title`                       | Title of the person at the current job                   | Software Engineer |
| `headline`                    | Headline of the person on their LinkedIn profile         | Tech Enthusiast |
| `summary`                     | Summary of the person on their LinkedIn profile          | Experienced software developer with a passion for AI. |
| `num_of_connections`          | Number of connections the person has on their LinkedIn profile | 500+        |
| `skills`                      | All the skills the person has listed on their LinkedIn profile | Python, Java, SQL |
| `twitter_handle`              | Twitter handle shared by the person on their LinkedIn profile | @johndoe   |
| `languages`                   | The languages the person speaks as listed on their LinkedIn profile | English, Spanish |
| `all_employers`              | List of all employers the person has worked for          | Company A, Company B |
| `all_employers_company_id`    | Crustdata company IDs corresponding to each employer      | 123, 456    |
| `all_titles`                  | List of all job titles the person has held               | Developer, Manager |
| `all_schools`                 | List of all schools the person attended                   | University A, College B |
| `all_degrees`                 | List of all degrees obtained by the person                | BSc in Computer Science |
  
### Example Code Snippet

```python
# Example of how to use the API to get user information
import requests

def get_user_info(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

user_info = get_user_info("12345")
print(user_info)
```

### Notes
- Ensure to replace `https://api.example.com` with the actual API endpoint.
- The `user_id` should be a valid identifier for the user you wish to retrieve information for.

This documentation provides a comprehensive overview of the API's capabilities regarding user information retrieval. For further details, please refer to the specific API endpoint documentation.

