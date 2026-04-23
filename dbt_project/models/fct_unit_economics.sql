WITH sales_clean AS (
    SELECT
        CAST(date AS DATE) AS date,
        UPPER(vertical) AS vertical,
        SUM(orders) AS total_orders,
        SUM(revenue) AS revenue,
        SUM(rider_payouts) AS rider_payouts
    FROM raw.sales
    GROUP BY 1, 2
),

marketing_clean AS (
    SELECT
        CAST(campaign_date AS DATE) AS date,
        UPPER(business_vertical) AS vertical,
        SUM(direct_marketing_spend) AS direct_marketing_spend
    FROM raw.marketing
    GROUP BY 1, 2
),

logistics_clean AS (
    SELECT
        CAST(dt AS DATE) AS date,
        UPPER(vert) AS vertical,
        SUM(distance_km) AS distance_km,
        SUM(fuel_consumed_liters) AS fuel_consumed_liters
    FROM raw.logistics
    GROUP BY 1, 2
)

SELECT
    s.date,
    s.vertical,
    s.total_orders,
    s.revenue,
    s.rider_payouts,
    COALESCE(m.direct_marketing_spend, 0) AS direct_marketing_spend,
    COALESCE(l.distance_km, 0) AS distance_km,
    COALESCE(l.fuel_consumed_liters, 0) AS fuel_consumed_liters,
    -- Calculate net contribution margin
    s.revenue 
    - COALESCE(m.direct_marketing_spend, 0) 
    - s.rider_payouts 
    - (COALESCE(l.fuel_consumed_liters, 0) * 275) AS net_contribution_margin
FROM sales_clean s
LEFT JOIN marketing_clean m 
    ON s.date = m.date AND s.vertical = m.vertical
LEFT JOIN logistics_clean l 
    ON s.date = l.date AND s.vertical = l.vertical
