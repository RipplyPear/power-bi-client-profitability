# Data model

## Relationships

| From | Column | To | Column | Cardinality |
|---|---|---|---|---|
| `Dim_Client` | `client_version_id` | `Fact_ClientMonthly` | `client_version_id` | One-to-many |
| `Dim_Date` | `reference_date` | `Fact_ClientMonthly` | `reference_date` | One-to-many |

## Grain

- `Fact_ClientMonthly`: one row per customer per reference month.
- `Dim_Client`: one row per version of a customer profile.
- `Dim_Date`: one row per month-end reference date.

## SCD Type 2 behavior

Some fictional customers receive a second profile version on 2024-07-01. The
fact table points to the version valid for each month through
`client_version_id`. This demonstrates historical dimensional modeling without
containing any real customer history.

## Key fields

| Field | Meaning |
|---|---|
| `client_id` | Stable fictional customer identifier |
| `client_version_id` | Unique identifier for a profile version |
| `reference_date` | Month-end observation date |
| `monthly_profitability` | Synthetic profit contribution in RON |
| `digitally_active_flag` | `Y` when the customer has at least two digital transactions |
| `product_count` | Number of selected banking products held that month |
