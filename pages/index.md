---
title: Unit Economics
description: "Executive summary of unit economics and performance across all verticals."
---

```sql aggregated_data
SELECT 
    sum(revenue) as total_revenue,
    sum(net_contribution_margin) as total_net_margin,
    sum(net_contribution_margin) / nullif(sum(revenue), 0) as net_profit_margin,
    sum(rider_payouts) as total_rider_payouts,
    sum(direct_marketing_spend) as total_marketing_spend
FROM analytics.unit_economics
```

<Grid cols=3>
    <BigValue 
        data={aggregated_data} 
        value=total_revenue 
        fmt=usd
        title="Total Revenue" 
    />
    <BigValue 
        data={aggregated_data} 
        value=net_profit_margin 
        fmt=pct
        title="Net Profit Margin" 
    />
    <BigValue 
        data={aggregated_data} 
        value=total_net_margin 
        fmt=usd
        title="Net Contribution Margin" 
    />
</Grid>

---

### Vertical Performance Analysis
The contribution margin varies significantly across our business units. The chart below breaks down the profitability profile of each vertical after accounting for direct marketing, rider payouts, and fuel costs.

```sql vertical_margin
SELECT 
    vertical,
    sum(revenue) as revenue,
    sum(net_contribution_margin) as contribution_margin,
    sum(net_contribution_margin) / nullif(sum(revenue), 0) as margin_pct
FROM analytics.unit_economics
GROUP BY vertical
ORDER BY contribution_margin DESC
```

<Grid cols=2>
    <BarChart
        data={vertical_margin}
        x=vertical
        y=contribution_margin
        yFmt=usd
        title="Contribution Margin by Vertical"
        seriesColors={{ "contribution_margin": "#4F46E5" }}
    />
    <BarChart
        data={vertical_margin}
        x=vertical
        y=margin_pct
        yFmt=pct
        title="Margin Percentage (%)"
        seriesColors={{ "margin_pct": "#10B981" }}
    />
</Grid>

---

### Logistics & Fuel Efficiency
Fuel consumption directly impacts the logistics vertical. Tracking Liters per 100km allows us to isolate operational efficiency from fluctuating revenue metrics.

```sql fuel_trend
SELECT 
    date_trunc('week', date) as week,
    sum(fuel_consumed_liters) / nullif(sum(distance_km), 0) * 100 as fuel_efficiency_l_per_100km
FROM analytics.unit_economics
GROUP BY 1
ORDER BY 1
```

<LineChart
    data={fuel_trend}
    x=week
    y=fuel_efficiency_l_per_100km
    yAxisTitle="Liters per 100km"
    title="Weekly Fuel Efficiency Trend"
    lineColor="#F59E0B"
/>
