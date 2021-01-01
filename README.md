# CustomerClassification_RFM_python
Simple RFM model used to do customer classification which is developed with Python.

## Procedures

1. We accept customer investment data, including customer ID, investment timestamp and amount.
2. Calculate for each customer the last investment date (`recency`), total investment counts (`frequency`) and amount (`monetary`).
3. Bin these three variables above according to their sample mean respectively (tag 1 if the value is higher or equal to the sample mean, tag 0 otherwise), and categorize customers by the following table:

    | recency | frequency | monitory | comment         | importance rank |
    |---------|-----------|----------|-----------------|-----------------|
    | 1       | 1         | 1        | 1. VIP          | 1               |
    | 0       | 1         | 1        | 2. IP           | 2               |
    | 1       | 0         | 1        | 3. Low Activity | 3               |
    | 0       | 0         | 1        | 4. Low Loyalty  | 4               |
    | 1       | 1         | 0        | 5. General      | 5               |
    | 0       | 1         | 0        | 6. Growth       | 6               |
    | 1       | 0         | 0        | 7. Primary Plus | 7               |
    | 0       | 0         | 0        | 8. Primary      | 8               |

4. Customer listing with categories
5. Summary by categories
6. Output the customer classification table and the pie chart
