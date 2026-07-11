# Power BI setup on Windows 11

## 1. Generate the public dataset

Open PowerShell in the repository folder:

```powershell
py scripts\generate_synthetic_data.py
```

Confirm that `data` contains:

- `Dim_Client.csv`;
- `Dim_Date.csv`;
- `Fact_ClientMonthly.csv`.

## 2. Create the public PBIX

In Power BI Desktop, create a new `.pbix` file. Suggested name:

```text
Customer-Profitability-Synthetic.pbix
```

## 3. Import the synthetic tables

The safest approach is to create three new queries with **Get data > Text/CSV**.
Select the generated CSV files and choose **Transform Data**.

Set these data types in Power Query:

- IDs, categories, and flags: Text;
- dates: Date;
- counts: Whole Number;
- volumes, income, profitability: Fixed Decimal Number.

Rename the queries exactly `Dim_Client`, `Dim_Date`, and
`Fact_ClientMonthly`.

## 4. Recreate the relationships

In Model view, create:

1. `Dim_Client[client_version_id]` (1) to
   `Fact_ClientMonthly[client_version_id]` (*);
2. `Dim_Date[reference_date]` (1) to
   `Fact_ClientMonthly[reference_date]` (*).

Use single-direction filtering from dimension to fact.

Sort `Dim_Date[month_name]` by `Dim_Date[month_number]`.

## 5. Add the measures

Create the measures from `dax/measures.dax`. 
A dedicated empty table named `_Measures` is optional but helps keep the model organized.

## 6. Adapt the visuals

Replace old fields in each visual with fields from the public model.
Use these titles consistently:

- Total Customers;
- Customers Above Average Profitability;
- Average Monthly Profitability (RON);
- Above-Average Customers by County;
- Monthly Transactions;
- Digitally Active Customers by Month;
- Above-Average Customers by Gender;
- Above-Average Customers by Marital Status;
- Customers by Age Group.

