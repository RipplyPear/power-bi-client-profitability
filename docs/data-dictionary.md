# Public data dictionary

All fields describe fictional entities and generated observations.

## Dim_Client

| Field                | Description                                             |
| -------------------- | ------------------------------------------------------- |
| `client_version_id`  | Unique identifier for a versioned client profile        |
| `client_id`          | Stable fictional client identifier                      |
| `gender`             | Generated gender category (`F` or `M`)                  |
| `age_bucket`         | Generated age interval                                  |
| `marital_status`     | Generated marital-status category                       |
| `education_level`    | Generated education category                            |
| `county`             | Fictional county assignment using Romanian county names |
| `onboarding_channel` | Digital or branch onboarding channel                    |
| `onboarding_method`  | Self-service or assisted onboarding method              |
| `customer_segment`   | Standard or Premium fictional segment                   |
| `registration_date`  | Generated client registration date                      |
| `valid_from_date`    | Start of the SCD Type 2 profile version                 |
| `valid_to_date`      | End of the SCD Type 2 profile version                   |

## Dim_Date

| Field            | Description               |
| ---------------- | ------------------------- |
| `reference_date` | Month-end reporting date  |
| `month_number`   | Calendar month number     |
| `month_name`     | English month name        |
| `quarter`        | Calendar quarter          |
| `year`           | Calendar year             |
| `year_month`     | Sortable year-month label |

## Fact_ClientMonthly

| Field                        | Description                                            |
| ---------------------------- | ------------------------------------------------------ |
| `client_id`                  | Stable fictional client identifier                     |
| `client_version_id`          | Link to the profile version valid that month           |
| `reference_date`             | Month-end observation date                             |
| `transaction_count`          | Generated monthly transaction count                    |
| `transaction_volume`         | Generated monthly transaction volume in RON            |
| `digital_transaction_count`  | Generated digital transaction count                    |
| `digital_transaction_volume` | Generated digital transaction volume in RON            |
| `mobile_app_login_count`     | Generated mobile-app login count                       |
| `credit_card_count`          | Generated credit-card count                            |
| `secured_loan_count`         | Generated secured-loan count                           |
| `unsecured_loan_count`       | Generated unsecured-loan count                         |
| `product_count`              | Number of selected fictional products held             |
| `new_customer_flag`          | Whether the client registered in the observation month |
| `digitally_active_flag`      | `Y` when at least two digital transactions occurred    |
| `credit_card_flag`           | Generated credit-card ownership flag                   |
| `loan_flag`                  | Generated loan ownership flag                          |
| `digital_loan_flag`          | Generated digital-loan flag                            |
| `monthly_income`             | Generated monthly income in RON                        |
| `monthly_profitability`      | Generated monthly profitability in RON                 |
| `deposit_flag`               | Generated deposit ownership flag                       |
| `insurance_flag`             | Generated insurance ownership flag                     |

