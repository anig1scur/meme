import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from scipy.stats import pearsonr
from datetime import datetime
import matplotlib.dates as mdates
from collections import Counter

# Set the style for all plots
plt.style.use("ggplot")
sns.set(style="whitegrid")


# Function to load and preprocess the data
def load_data(file_path):
    """Load meme data from JSON file and preprocess it"""
    df = pd.read_json(file_path)

    df["humor"] = df["emotion"].apply(lambda x: x[0] if isinstance(x, list) and len(x) >= 4 else None)
    df["sarcasm"] = df["emotion"].apply(lambda x: x[1] if isinstance(x, list) and len(x) >= 4 else None)
    df["offensive"] = df["emotion"].apply(lambda x: x[2] if isinstance(x, list) and len(x) >= 4 else None)
    df["motivation"] = df["emotion"].apply(lambda x: x[3] if isinstance(x, list) and len(x) >= 4 else None)

    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    df["peak_value"] = df["trend"].apply(lambda x: max(x) if isinstance(x, list) and len(x) > 0 else None)
    df["total_trend"] = df["trend"].apply(lambda x: sum(x) if isinstance(x, list) else None)

    threshold = 5
    df["lifespan"] = df["trend"].apply(lambda x: sum(1 for val in x if val > threshold) if isinstance(x, list) else None)

    df["type_list"] = df["type"].apply(lambda x: x.split(", ") if isinstance(x, str) else [])
    df["trend"] = df["trend"].apply(lambda x: x if isinstance(x, list) else [])

    return df

# ---------- INTRODUCTION: SETUP COUNTER-INTUITIVE HOOK ----------


def basic_statistics(df):
    """Calculate basic statistics for memes"""

    # Average lifespan
    avg_lifespan = df["lifespan"].mean()

    # Percentage surviving longer than average
    percent_above_avg = (df["lifespan"] > avg_lifespan).mean() * 100

    # Percentage surviving more than X months (adjust X as needed)
    x_months = 3
    percent_above_x = (df["lifespan"] > x_months).mean() * 100

    print(f"===== BASIC STATISTICS =====")
    print(f"Average meme lifespan: {avg_lifespan:.2f} months")
    print(f"Memes surviving longer than average: {percent_above_avg:.2f}%")
    print(f"Memes surviving longer than {x_months} months: {percent_above_x:.2f}%")

    # Create visualization
    plt.figure(figsize=(10, 6))
    plt.hist(df["lifespan"], bins=20, color="steelblue", edgecolor="black")
    plt.axvline(
        avg_lifespan,
        color="red",
        linestyle="--",
        label=f"Average ({avg_lifespan:.2f} months)",
    )
    plt.axvline(x_months, color="green", linestyle="--", label=f"{x_months} months")
    plt.title("Distribution of Meme Lifespans")
    plt.xlabel("Lifespan (months)")
    plt.ylabel("Number of Memes")
    plt.legend()
    plt.tight_layout()
    plt.savefig("meme_lifespan_distribution.png")
    plt.close()

    return avg_lifespan, percent_above_avg, percent_above_x


# ---------- CHAPTER 1: MEME MORTALITY ANALYSIS ----------


def survival_time_analysis(df):
    """Analyze meme survival times"""

    print(f"\n===== SURVIVAL TIME ANALYSIS =====")

    # Calculate survival statistics
    median_lifespan = df["lifespan"].median()
    max_lifespan = df["lifespan"].max()
    min_lifespan = df["lifespan"].min()

    print(f"Median meme lifespan: {median_lifespan:.2f} months")
    print(f"Maximum meme lifespan: {max_lifespan} months")
    print(f"Minimum meme lifespan: {min_lifespan} months")

    # Create survival curve
    plt.figure(figsize=(10, 6))

    # Sort lifespans in descending order
    sorted_lifespans = sorted(df["lifespan"], reverse=True)
    percentiles = np.arange(1, len(sorted_lifespans) + 1) / len(sorted_lifespans)

    plt.plot(sorted_lifespans, percentiles * 100)
    plt.title("Meme Survival Curve")
    plt.xlabel("Lifespan (months)")
    plt.ylabel("Percentage of Memes Surviving")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("meme_survival_curve.png")
    plt.close()

    return median_lifespan, max_lifespan, min_lifespan


def popularity_distribution_analysis(df):
    """Analyze the distribution of meme popularity"""

    print(f"\n===== POPULARITY DISTRIBUTION ANALYSIS =====")

    # Sort memes by total trend value
    df_sorted = df.sort_values(by="total_trend", ascending=False).reset_index(drop=True)

    # Calculate percentage of total trend for top X%
    top_percent = 10
    top_n = int(len(df_sorted) * top_percent / 100)

    top_trend_sum = df_sorted.iloc[:top_n]["total_trend"].sum()
    total_trend_sum = df_sorted["total_trend"].sum()

    top_percent_share = (top_trend_sum / total_trend_sum) * 100

    print(
        f"Top {top_percent}% of memes account for {top_percent_share:.2f}% of total popularity"
    )

    # Create visualization
    plt.figure(figsize=(12, 6))

    # Calculate cumulative percentage
    df_sorted["cum_percent"] = df_sorted["total_trend"].cumsum() / total_trend_sum * 100

    plt.plot(
        np.arange(1, len(df_sorted) + 1) / len(df_sorted) * 100,
        df_sorted["cum_percent"],
    )
    plt.title("Cumulative Distribution of Meme Popularity")
    plt.xlabel("Percentage of Memes (Sorted by Popularity)")
    plt.ylabel("Cumulative Percentage of Total Popularity")
    plt.axvline(
        x=top_percent,
        color="red",
        linestyle="--",
        label=f"Top {top_percent}%: {top_percent_share:.2f}% of total popularity",
    )
    plt.axhline(y=top_percent_share, color="red", linestyle="--")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("meme_popularity_distribution.png")
    plt.close()

    return top_percent_share


def cluster_and_visualize(df, n_clusters=4):
    """Cluster memes based on their trend patterns and visualize the clusters"""

    print(f"\n===== CLUSTER ANALYSIS =====")

    # Get trend data as a matrix for clustering
    # First, ensure all trend arrays have the same length
    max_length = max(len(trend) for trend in df["trend"] if isinstance(trend, list))

    # Pad shorter arrays with zeros
    trend_matrix = np.array(
        [trend + [0] * (max_length - len(trend)) for trend in df["trend"]]
    )

    # Normalize trends for clustering
    row_sums = trend_matrix.sum(axis=1, keepdims=True)
    # Avoid division by zero
    row_sums[row_sums == 0] = 1.0
    normalized_matrix = trend_matrix / row_sums

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(normalized_matrix)

    # Add cluster labels to dataframe
    df["cluster"] = clusters

    # Calculate cluster statistics
    cluster_stats = (
        df.groupby("cluster")
        .agg(
            {
                "lifespan": "mean",
                "peak_value": "mean",
                "total_trend": "mean",
                "name": "count",
            }
        )
        .rename(columns={"name": "count"})
    )

    print("Cluster Statistics:")
    print(cluster_stats)

    # Visualize the typical trend pattern for each cluster
    plt.figure(figsize=(14, 8))

    for i in range(n_clusters):
        cluster_trends = normalized_matrix[clusters == i]
        mean_trend = cluster_trends.mean(axis=0)
        plt.plot(mean_trend, label=f"Cluster {i} (n={sum(clusters == i)})")

    plt.title("Average Trend Patterns by Cluster")
    plt.xlabel("Months")
    plt.ylabel("Normalized Trend Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("meme_cluster_patterns.png")
    plt.close()

    # Find an example meme from each cluster
    example_memes = []
    for i in range(n_clusters):
        cluster_memes = df[df["cluster"] == i]
        # Find the meme closest to the cluster centroid
        if len(cluster_memes) > 0:
            idx = cluster_memes.index[0]
            example_memes.append(df.loc[idx, "name"])

    print("Example memes from each cluster:")
    for i, meme in enumerate(example_memes):
        print(f"Cluster {i}: {meme}")

    return df


# ---------- CHAPTER 2: EMOTIONAL ANATOMY ANALYSIS ----------


def emotion_lifecycle_correlation(df):
    """Analyze correlation between emotional dimensions and lifecycle characteristics"""

    print(f"\n===== EMOTION & LIFECYCLE CORRELATION =====")

    # Calculate correlations
    emotions = ["humor", "sarcasm", "offensive", "motivation"]
    lifecycle_metrics = ["lifespan", "peak_value", "total_trend"]

    correlation_results = {}

    for emotion in emotions:
        correlation_results[emotion] = {}
        for metric in lifecycle_metrics:
            corr, p_value = pearsonr(df[emotion], df[metric])
            correlation_results[emotion][metric] = (corr, p_value)
            sig = "significant" if p_value < 0.05 else "not significant"
            print(
                f"Correlation between {emotion} and {metric}: {corr:.3f} ({sig}, p={p_value:.3f})"
            )

    # Create correlation heatmap
    corr_data = pd.DataFrame(
        {
            metric: [correlation_results[emotion][metric][0] for emotion in emotions]
            for metric in lifecycle_metrics
        },
        index=emotions
    ).astype(float)

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_data, annot=True, cmap="coolwarm", vmin=-1, vmax=1, center=0)
    plt.title("Correlation between Emotional Dimensions and Lifecycle Metrics")
    plt.tight_layout()
    plt.savefig("emotion_lifecycle_correlation.png")
    plt.close()

    # Visualize relationship between sarcasm and lifespan
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="sarcasm", y="lifespan", data=df, alpha=0.7)

    # Add trend line
# Drop rows with NaN values in sarcasm or lifespan
    valid = df[["sarcasm", "lifespan"]].dropna()
    x = valid["sarcasm"]
    y = valid["lifespan"]

    if len(x) >= 2:
        m, b = np.polyfit(x, y, 1)
        plt.plot(x, m * x + b, color="red", linestyle="--")


    plt.title("Relationship between Sarcasm and Meme Lifespan")
    plt.xlabel("Sarcasm Level (0-5)")
    plt.ylabel("Lifespan (months)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("sarcasm_lifespan_relationship.png")
    plt.close()

    return correlation_results


def emotion_popularity_analysis(df):
    """Analyze relationship between emotional dimensions and popularity metrics"""

    print(f"\n===== EMOTION & POPULARITY ANALYSIS =====")

    emotions = ["humor", "sarcasm", "offensive", "motivation"]

    # Create a grid of scatter plots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()

    for i, emotion in enumerate(emotions):
        ax = axes[i]
        sns.scatterplot(x=emotion, y="total_trend", data=df, alpha=0.7, ax=ax)

        # Add trend line
        valid = df[[emotion, "total_trend"]].dropna()
        x = valid[emotion]
        y = valid["total_trend"]

        if len(x) >= 2:
            m, b = np.polyfit(x, y, 1)
            ax.plot(x, m * x + b, color="red", linestyle="--")

        ax.set_title(f"{emotion.capitalize()} vs Total Popularity")
        ax.set_xlabel(f"{emotion.capitalize()} Level (0-5)")
        ax.set_ylabel("Total Trend Value")
        ax.grid(True)

    plt.tight_layout()
    plt.savefig("emotion_popularity_relationship.png")
    plt.close()

    # Focus on offensive content and popularity
    corr, p_value = pearsonr(df["offensive"], df["total_trend"])
    print(
        f"Correlation between offensive content and total popularity: {corr:.3f} (p={p_value:.3f})"
    )

    # Create scatter plot for offensive content
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="offensive", y="total_trend", data=df, alpha=0.7)

    # Add trend line
    valid = df[["offensive", "total_trend"]].dropna()
    x = valid["offensive"]
    y = valid["total_trend"]

    if len(x) >= 2:
        m, b = np.polyfit(x, y, 1)
        plt.plot(x, m * x + b, color="red", linestyle="--")

    plt.title("Relationship between Offensive Content and Popularity")
    plt.xlabel("Offensive Level (0-5)")
    plt.ylabel("Total Popularity")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("offensive_popularity_relationship.png")
    plt.close()

    return corr, p_value


def emotion_combination_analysis(df):
    """Compare lifecycle characteristics for different emotion combinations"""

    print(f"\n===== EMOTION COMBINATION ANALYSIS =====")

    # Create emotion combination categories
    df["high_sarcasm"] = df["sarcasm"] >= 3
    df["high_offensive"] = df["offensive"] >= 3
    df["high_humor"] = df["humor"] >= 3
    df["high_motivation"] = df["motivation"] >= 3

    # Define interesting combinations
    combinations = [
        ("High Sarcasm, Low Offensive", (df["high_sarcasm"]) & (~df["high_offensive"])),
        ("Low Sarcasm, High Offensive", (~df["high_sarcasm"]) & (df["high_offensive"])),
        ("High Humor, High Sarcasm", (df["high_humor"]) & (df["high_sarcasm"])),
        ("High Humor, High Motivation", (df["high_humor"]) & (df["high_motivation"])),
    ]

    # Calculate statistics for each combination
    stats = []
    for name, mask in combinations:
        subset = df[mask]
        if len(subset) > 0:
            stats.append(
                {
                    "Combination": name,
                    "Count": len(subset),
                    "Avg Lifespan": subset["lifespan"].mean(),
                    "Avg Peak": subset["peak_value"].mean(),
                    "Avg Total": subset["total_trend"].mean(),
                }
            )

    stats_df = pd.DataFrame(stats)
    print("Statistics by emotion combination:")
    print(stats_df)

    # Visualize average lifespan by combination
    plt.figure(figsize=(12, 6))
    sns.barplot(x="Combination", y="Avg Lifespan", data=stats_df)
    plt.title("Average Lifespan by Emotion Combination")
    plt.xlabel("")
    plt.ylabel("Average Lifespan (months)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("emotion_combination_lifespan.png")
    plt.close()

    # Visualize average total popularity by combination
    plt.figure(figsize=(12, 6))
    sns.barplot(x="Combination", y="Avg Total", data=stats_df)
    plt.title("Average Total Popularity by Emotion Combination")
    plt.xlabel("")
    plt.ylabel("Average Total Trend Value")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("emotion_combination_popularity.png")
    plt.close()

    return stats_df


# ---------- CHAPTER 3: MEME REFLECTING THE WORLD ANALYSIS ----------


def historical_event_analysis(df, events):
    """Analyze meme trends in relationship to historical events"""

    print(f"\n===== HISTORICAL EVENT ANALYSIS =====")

    # Skip if no trend data available
    if "trend" not in df.columns or df["trend"].apply(len).max() == 0:
        print("No valid trend data available for historical event analysis.")
        return pd.DataFrame()

    start_date = datetime(2004, 1, 1)
    months = df["trend"].apply(len).max()

    # Generate date range safely
    date_range = [
        start_date.replace(
            month=((start_date.month - 1 + i) % 12) + 1,
            year=start_date.year + ((start_date.month - 1 + i) // 12),
        )
        for i in range(months)
    ]

    if not date_range:
        print("Date range could not be generated.")
        return pd.DataFrame()

    # Calculate total trend by month
    total_trend_by_month = np.zeros(months)
    for trend in df["trend"]:
        # Ensure the trend array is the right length
        padded_trend = trend + [0] * (months - len(trend))
        total_trend_by_month += padded_trend[:months]

    # Create a DataFrame for time series analysis
    time_df = pd.DataFrame({"date": date_range, "total_trend": total_trend_by_month})

    # Visualize total trend with event markers
    plt.figure(figsize=(16, 8))
    plt.plot(time_df["date"], time_df["total_trend"], color="steelblue")

    # Add event markers
    for event_name, event_date, event_desc in events:
        event_dt = datetime.strptime(event_date, "%Y-%m-%d")
        if event_dt >= start_date and event_dt <= date_range[-1]:
            plt.axvline(x=event_dt, color="red", linestyle="--", alpha=0.7)
            plt.text(
                event_dt,
                max(total_trend_by_month) * 0.9,
                event_name,
                rotation=90,
                verticalalignment="top",
            )

    plt.title("Total Meme Trend Over Time with Historical Events")
    plt.xlabel("Date")
    plt.ylabel("Total Trend Value")
    plt.grid(True)

    # Format x-axis to show years
    years = mdates.YearLocator()
    plt.gca().xaxis.set_major_locator(years)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    plt.tight_layout()
    plt.savefig("meme_trend_with_events.png")
    plt.close()

    # Analyze meme creation around events
    event_analysis = []
    for event_name, event_date, event_desc in events:
        event_dt = datetime.strptime(event_date, "%Y-%m-%d")
        event_year = event_dt.year

        # Count memes created in the event year
        memes_in_year = df[df["year"] == event_year]["name"].count()

        # Calculate average lifespan of memes created in event year
        if memes_in_year > 0:
            avg_lifespan = df[df["year"] == event_year]["lifespan"].mean()
        else:
            avg_lifespan = 0

        event_analysis.append(
            {
                "Event": event_name,
                "Year": event_year,
                "Memes Created": memes_in_year,
                "Avg Lifespan": avg_lifespan,
            }
        )

    event_df = pd.DataFrame(event_analysis)
    print("Event Analysis:")
    print(event_df)

    return event_df


def keyword_matching_analysis(df, keywords):
    """Find memes related to specific keywords and analyze their characteristics"""

    print(f"\n===== KEYWORD MATCHING ANALYSIS =====")

    results = []
    for keyword in keywords:
        # Find memes containing the keyword in name
        matches = df[df["name"].str.lower().str.contains(keyword.lower())]
        match_count = len(matches)

        if match_count > 0:
            avg_lifespan = matches["lifespan"].mean()
            avg_total = matches["total_trend"].mean()
            most_popular = (
                matches.loc[matches["total_trend"].idxmax(), "name"]
                if match_count > 0
                else "None"
            )
        else:
            avg_lifespan = 0
            avg_total = 0
            most_popular = "None"

        results.append(
            {
                "Keyword": keyword,
                "Match Count": match_count,
                "Avg Lifespan": avg_lifespan,
                "Avg Total Trend": avg_total,
                "Most Popular": most_popular,
            }
        )

    keyword_df = pd.DataFrame(results)
    print("Keyword Analysis:")
    print(keyword_df)

    # Visualize keyword match counts
    plt.figure(figsize=(12, 6))
    sns.barplot(x="Keyword", y="Match Count", data=keyword_df)
    plt.title("Meme Count by Keyword")
    plt.xlabel("Keyword")
    plt.ylabel("Number of Matches")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("keyword_match_counts.png")
    plt.close()

    # Visualize average lifespan by keyword
    plt.figure(figsize=(12, 6))
    sns.barplot(x="Keyword", y="Avg Lifespan", data=keyword_df)
    plt.title("Average Lifespan by Keyword")
    plt.xlabel("Keyword")
    plt.ylabel("Average Lifespan (months)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("keyword_avg_lifespan.png")
    plt.close()

    return keyword_df


def trend_peak_analysis(df):
    """Analyze clustering of trend peaks over time"""

    print(f"\n===== TREND PEAK ANALYSIS =====")

    # Find the month of peak trend for each meme
    peak_months = []
    for i, row in df.iterrows():
        trend = row["trend"]
        if len(trend) > 0 and max(trend) > 0:
            peak_month = trend.index(max(trend))
            peak_date = datetime(2004, 1, 1).replace(
                month=((0 + peak_month) % 12) + 1, year=2004 + ((0 + peak_month) // 12)
            )
            peak_months.append((peak_date, row["name"], max(trend)))

    # Create a DataFrame with peak information
    peak_df = pd.DataFrame(peak_months, columns=["Peak Date", "Meme", "Peak Value"])
    peak_df["Year"] = peak_df["Peak Date"].dt.year
    peak_df["Month"] = peak_df["Peak Date"].dt.month

    # Count peaks by year-month
    peak_count = (
        peak_df.groupby(["Year", "Month"]).size().reset_index(name="Peak Count")
    )

    # Create a date column for plotting
    peak_count["Date"] = peak_count.apply(
        lambda x: datetime(int(x["Year"]), int(x["Month"]), 1), axis=1
    )

    # Visualize peak distribution over time
    plt.figure(figsize=(16, 8))
    plt.bar(peak_count["Date"], peak_count["Peak Count"], width=30)
    plt.title("Distribution of Meme Peak Trends Over Time")
    plt.xlabel("Date")
    plt.ylabel("Number of Memes Peaking")
    plt.grid(True, axis="y")

    # Format x-axis to show years
    years = mdates.YearLocator()
    plt.gca().xaxis.set_major_locator(years)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    plt.tight_layout()
    plt.savefig("meme_peak_distribution.png")
    plt.close()

    # Find months with unusually high numbers of peaking memes
    mean_peaks = peak_count["Peak Count"].mean()
    std_peaks = peak_count["Peak Count"].std()
    threshold = mean_peaks + 2 * std_peaks

    hot_months = peak_count[peak_count["Peak Count"] > threshold]
    print(f"Average number of peaking memes per month: {mean_peaks:.2f}")
    print(f"Months with unusually high numbers of peaking memes (>{threshold:.2f}):")
    for _, row in hot_months.iterrows():
        print(f"{row['Date'].strftime('%B %Y')}: {row['Peak Count']} peaks")

    # Create heatmap of peak counts by year and month
    heatmap_data = peak_count.pivot_table(
        index="Month", columns="Year", values="Peak Count", fill_value=0
    )

    plt.figure(figsize=(16, 8))
    sns.heatmap(heatmap_data, cmap="YlOrRd", annot=True, fmt=".0f")
    plt.title("Heatmap of Meme Peak Counts by Year and Month")
    plt.xlabel("Year")
    plt.ylabel("Month")
    plt.tight_layout()
    plt.savefig("meme_peak_heatmap.png")
    plt.close()

    return peak_count, hot_months


# ---------- CHAPTER 4: MEME TYPE EVOLUTION ANALYSIS ----------


def type_evolution_analysis(df):
    """Analyze how meme types have evolved over time"""

    print(f"\n===== MEME TYPE EVOLUTION ANALYSIS =====")

    # Extract all unique types
    all_types = set()
    for type_list in df["type_list"]:
        all_types.update(type_list)

    # Count memes by type and year
    type_year_counts = {}
    for year in sorted(df["year"].unique()):
        type_year_counts[year] = {type_name: 0 for type_name in all_types}

        year_memes = df[df["year"] == year]
        for types in year_memes["type_list"]:
            for type_name in types:
                type_year_counts[year][type_name] += 1

    # Convert to DataFrame for plotting
    type_evolution_df = pd.DataFrame(type_year_counts).T

    # Get top N types by total count
    top_n = 10
    top_types = type_evolution_df.sum().nlargest(top_n).index.tolist()

    # Plot evolution of top types
    plt.figure(figsize=(16, 10))

    # Convert years to numeric for proper plotting
    type_evolution_df.index = pd.to_numeric(type_evolution_df.index)
    type_evolution_df = type_evolution_df.sort_index()

    # Plot lines for each top type
    for type_name in top_types:
        plt.plot(
            type_evolution_df.index,
            type_evolution_df[type_name],
            marker="o",
            linewidth=2,
            label=type_name,
        )

    plt.title(f"Evolution of Top {top_n} Meme Types Over Time")
    plt.xlabel("Year")
    plt.ylabel("Number of Memes")
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig("meme_type_evolution.png")
    plt.close()

    # Create stacked area chart
    plt.figure(figsize=(16, 10))
    type_evolution_df[top_types].plot.area(stacked=True, alpha=0.7, figsize=(16, 10))
    plt.title(f"Stacked Area Chart of Top {top_n} Meme Types")
    plt.xlabel("Year")
    plt.ylabel("Number of Memes")
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig("meme_type_stacked_area.png")
    plt.close()

    return type_evolution_df


def platform_evolution_analysis(df):
    """Analyze how meme origins have evolved over time"""

    print(f"\n===== PLATFORM EVOLUTION ANALYSIS =====")

    # Count memes by origin and year
    origin_counts = df.groupby(["year", "origin"]).size().unstack(fill_value=0)

    # Convert years to numeric for proper plotting
    origin_counts.index = pd.to_numeric(origin_counts.index)
    origin_counts = origin_counts.sort_index()

    # Calculate percentage by platform for each year
    origin_percentages = origin_counts.div(origin_counts.sum(axis=1), axis=0) * 100

    # Get top platforms by total count
    top_n = 8
    top_platforms = origin_counts.sum().nlargest(top_n).index.tolist()

    # Plot evolution of top platforms (absolute counts)
    plt.figure(figsize=(16, 10))

    for platform in top_platforms:
        if platform in origin_counts.columns:
            plt.plot(
                origin_counts.index,
                origin_counts[platform],
                marker="o",
                linewidth=2,
                label=platform,
            )

    plt.title(f"Evolution of Top {top_n} Meme Platforms Over Time")
    plt.xlabel("Year")
    plt.ylabel("Number of Memes")
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig("platform_evolution_absolute.png")
    plt.close()

    # Plot evolution
# Plot evolution of top platforms (percentage shares)
    plt.figure(figsize=(16, 10))
    
    for platform in top_platforms:
        if platform in origin_percentages.columns:
            plt.plot(origin_percentages.index, origin_percentages[platform], 
                     marker='o', linewidth=2, label=platform)
    
    plt.title(f'Percentage Share of Top {top_n} Meme Platforms Over Time')
    plt.xlabel('Year')
    plt.ylabel('Percentage of Memes')
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('platform_evolution_percentage.png')
    plt.close()
    
    # Create stacked area chart for platforms
    plt.figure(figsize=(16, 10))
    origin_percentages[top_platforms].plot.area(stacked=True, alpha=0.7, figsize=(16, 10))
    plt.title(f'Stacked Area Chart of Top {top_n} Meme Platforms')
    plt.xlabel('Year')
    plt.ylabel('Percentage of Memes')
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('platform_stacked_area.png')
    plt.close()
    
    # Find platform with most growth
    platform_growth = {}
    for platform in top_platforms:
        if platform in origin_counts.columns and len(origin_counts) > 1:
            earliest_year = origin_counts.index.min()
            latest_year = origin_counts.index.max()
            
            if earliest_year in origin_counts.index and latest_year in origin_counts.index:
                early_count = origin_counts.loc[earliest_year, platform]
                late_count = origin_counts.loc[latest_year, platform]
                
                # Calculate growth factor
                if early_count > 0:
                    growth = late_count / early_count
                else:
                    growth = late_count if late_count > 0 else 0
                
                platform_growth[platform] = growth
    
    # Sort platforms by growth
    sorted_growth = sorted(platform_growth.items(), key=lambda x: x[1], reverse=True)
    print("Platform growth factors (latest year / earliest year):")
    for platform, growth in sorted_growth:
        print(f"{platform}: {growth:.2f}x")
    
    return origin_counts, origin_percentages, platform_growth

def cross_platform_comparison(df):
    """Compare characteristics of memes from different platforms"""
    
    print(f"\n===== CROSS-PLATFORM COMPARISON =====")
    
    # Get platforms with enough memes for analysis
    platform_counts = df['origin'].value_counts()
    valid_platforms = platform_counts[platform_counts >= 5].index.tolist()
    
    # Prepare data for comparisons
    platform_stats = []
    for platform in valid_platforms:
        platform_memes = df[df['origin'] == platform]
        
        stats = {
            'Platform': platform,
            'Count': len(platform_memes),
            'Avg Lifespan': platform_memes['lifespan'].mean(),
            'Avg Peak Value': platform_memes['peak_value'].mean(),
            'Avg Total Trend': platform_memes['total_trend'].mean(),
            'Avg Humor': platform_memes['humor'].mean(),
            'Avg Sarcasm': platform_memes['sarcasm'].mean(),
            'Avg Offensive': platform_memes['offensive'].mean(),
            'Avg Motivation': platform_memes['motivation'].mean()
        }
        platform_stats.append(stats)
    
    platform_df = pd.DataFrame(platform_stats)
    print("Platform Statistics:")
    print(platform_df)
    
    # Create visualization comparing lifespan across platforms
    plt.figure(figsize=(14, 7))
    sns.barplot(x='Platform', y='Avg Lifespan', data=platform_df, order=platform_df.sort_values('Avg Lifespan', ascending=False)['Platform'])
    plt.title('Average Meme Lifespan by Platform')
    plt.xlabel('')
    plt.ylabel('Average Lifespan (months)')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig('platform_lifespan_comparison.png')
    plt.close()
    
    # Create visualization comparing popularity across platforms
    plt.figure(figsize=(14, 7))
    sns.barplot(x='Platform', y='Avg Total Trend', data=platform_df, order=platform_df.sort_values('Avg Total Trend', ascending=False)['Platform'])
    plt.title('Average Meme Popularity by Platform')
    plt.xlabel('')
    plt.ylabel('Average Total Trend Value')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig('platform_popularity_comparison.png')
    plt.close()
    
    # Create radar chart for emotional profile by platform
    top_platforms = platform_df.nlargest(5, 'Count')['Platform'].tolist()
    
    emotion_dims = ['Avg Humor', 'Avg Sarcasm', 'Avg Offensive', 'Avg Motivation']
    
    # Create radar chart
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, polar=True)
    
    # Number of variables
    N = len(emotion_dims)
    
    # What will be the angle of each axis in the plot
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Draw the polygons for each platform
    for i, platform in enumerate(top_platforms):
        platform_data = platform_df[platform_df['Platform'] == platform][emotion_dims].values.flatten().tolist()
        platform_data += platform_data[:1]  # Close the loop
        
        ax.plot(angles, platform_data, linewidth=2, linestyle='solid', label=platform)
        ax.fill(angles, platform_data, alpha=0.1)
    
    # Fix axis to go in the right order and start at 12 o'clock
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([dim.replace('Avg ', '') for dim in emotion_dims])
    
    # Draw axis lines for each angle and label
    ax.set_rlabel_position(0)
    plt.yticks([1, 2, 3, 4, 5], color="grey", size=8)
    plt.ylim(0, 5)
    
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.title('Emotional Profile by Platform', size=15, y=1.1)
    plt.tight_layout()
    plt.savefig('platform_emotion_radar.png')
    plt.close()
    
    return platform_df

# ---------- CONCLUSION: WHAT MAKES MEMES ENDURE ----------

def correlation_index_development(df):
    """Develop a relevance index based on various meme characteristics"""
    
    print(f"\n===== RELEVANCE INDEX DEVELOPMENT =====")
    
    # Create relevance index components
    # 1. Normalized lifespan (0-1)
    max_lifespan = df['lifespan'].max()
    df['norm_lifespan'] = df['lifespan'] / max_lifespan if max_lifespan > 0 else 0
    
    # 2. Normalized peak value (0-1)
    max_peak = df['peak_value'].max()
    df['norm_peak'] = df['peak_value'] / max_peak if max_peak > 0 else 0
    
    # 3. Normalized total trend (0-1)
    max_total = df['total_trend'].max()
    df['norm_total'] = df['total_trend'] / max_total if max_total > 0 else 0
    
    # 4. Calculate "renaissance" factor (recurring peaks)
    df['renaissance_factor'] = df['trend'].apply(lambda x: 
        sum(1 for i in range(1, len(x)-1) if x[i] > x[i-1] and x[i] > x[i+1] and x[i] > 5)
    )
    max_renaissance = df['renaissance_factor'].max()
    df['norm_renaissance'] = df['renaissance_factor'] / max_renaissance if max_renaissance > 0 else 0
    
    # Combine into relevance index (weights can be adjusted)
    df['relevance_index'] = (
        0.3 * df['norm_lifespan'] +
        0.3 * df['norm_total'] +
        0.2 * df['norm_peak'] +
        0.2 * df['norm_renaissance']
    )
    
    # Analyze top memes by relevance index
    top_memes = df.nlargest(20, 'relevance_index')
    print("Top 20 memes by relevance index:")
    for i, (idx, row) in enumerate(top_memes.iterrows(), 1):
        print(f"{i}. {row['name']} (Index: {row['relevance_index']:.3f})")
    
    # Correlation between index components
    corr_matrix = df[['norm_lifespan', 'norm_peak', 'norm_total', 'norm_renaissance', 'relevance_index']].corr()
    print("\nCorrelation between index components:")
    print(corr_matrix)
    
    # Correlation with emotional dimensions
    emotion_corr = {}
    for emotion in ['humor', 'sarcasm', 'offensive', 'motivation']:
        corr, p_value = pearsonr(df[emotion], df['relevance_index'])
        emotion_corr[emotion] = (corr, p_value)
        sig = "significant" if p_value < 0.05 else "not significant"
        print(f"Correlation between {emotion} and relevance index: {corr:.3f} ({sig}, p={p_value:.3f})")
    
    # Visualize relevance index distribution
    plt.figure(figsize=(12, 6))
    sns.histplot(df['relevance_index'], bins=20, kde=True)
    plt.title('Distribution of Meme Relevance Index')
    plt.xlabel('Relevance Index')
    plt.ylabel('Count')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('relevance_index_distribution.png')
    plt.close()
    
    # Create scatter plot of lifespan vs. total trend with relevance index as color
    plt.figure(figsize=(12, 10))
    scatter = plt.scatter(df['norm_total'], df['norm_lifespan'], 
                c=df['relevance_index'], cmap='viridis', alpha=0.7, s=100)
    
    # Add colorbar
    cbar = plt.colorbar(scatter)
    cbar.set_label('Relevance Index')
    
    # Annotate some top memes
    for i, (idx, row) in enumerate(top_memes.head(10).iterrows()):
        plt.annotate(row['name'], 
                    (row['norm_total'], row['norm_lifespan']),
                    xytext=(5, 5), textcoords='offset points',
                    fontsize=8)
    
    plt.title('Meme Popularity vs. Lifespan with Relevance Index')
    plt.xlabel('Normalized Total Trend')
    plt.ylabel('Normalized Lifespan')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('relevance_index_scatter.png')
    plt.close()
    
    return df, emotion_corr

def successful_case_analysis(df):
    """Analyze the most successful long-lasting memes"""
    
    print(f"\n===== SUCCESSFUL CASE ANALYSIS =====")
    
    # Get top 10 memes by relevance index
    top_memes = df.nlargest(10, 'relevance_index').copy()
    
    # Add normalized emotion values
    for emotion in ['humor', 'sarcasm', 'offensive', 'motivation']:
        top_memes[f'norm_{emotion}'] = top_memes[emotion] / 5
    
    print("Analysis of top 10 most successful memes:")
    for i, (idx, row) in enumerate(top_memes.iterrows(), 1):
        print(f"\n{i}. {row['name']} (Origin: {row['origin']}, Year: {row['year']})")
        print(f"   Lifespan: {row['lifespan']} months, Peak Value: {row['peak_value']}")
        print(f"   Emotional profile: Humor={row['humor']}, Sarcasm={row['sarcasm']}, " +
              f"Offensive={row['offensive']}, Motivation={row['motivation']}")
    
    # Create emotional profile radar chart for top memes
    emotion_dims = ['norm_humor', 'norm_sarcasm', 'norm_offensive', 'norm_motivation']
    
    # Create radar chart
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, polar=True)
    
    # Number of variables
    N = len(emotion_dims)
    
    # What will be the angle of each axis in the plot
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Draw the polygons for each top meme
    for i, (idx, row) in enumerate(top_memes.head(5).iterrows()):
        values = [row[dim] for dim in emotion_dims]
        values += values[:1]  # Close the loop
        
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=row['name'])
        ax.fill(angles, values, alpha=0.1)
    
    # Fix axis to go in the right order and start at 12 o'clock
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([dim.replace('norm_', '') for dim in emotion_dims])
    
    # Draw axis lines for each angle and label
    ax.set_rlabel_position(0)
    plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0], color="grey", size=8)
    plt.ylim(0, 1)
    
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.title('Emotional Profile of Top 5 Most Successful Memes', size=15, y=1.1)
    plt.tight_layout()
    plt.savefig('top_memes_emotion_radar.png')
    plt.close()
    
    # Create aggregated emotion profile for successful memes
    avg_profile = top_memes[['humor', 'sarcasm', 'offensive', 'motivation']].mean()
    avg_profile_norm = avg_profile / 5
    
    avg_all = df[['humor', 'sarcasm', 'offensive', 'motivation']].mean()
    avg_all_norm = avg_all / 5
    
    # Create comparison bar chart
    plt.figure(figsize=(12, 6))
    
    x = np.arange(4)
    width = 0.35
    
    emotions = ['Humor', 'Sarcasm', 'Offensive', 'Motivation']
    
    plt.bar(x - width/2, avg_profile, width, label='Top 10 Memes')
    plt.bar(x + width/2, avg_all, width, label='All Memes')
    
    plt.title('Emotional Profile: Top Memes vs All Memes')
    plt.xticks(x, emotions)
    plt.ylabel('Average Score (0-5)')
    plt.legend()
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig('top_vs_all_emotion_profile.png')
    plt.close()
    
    # Extract common features
    common_features = {
        'origin': Counter(top_memes['origin']).most_common(),
        'year': Counter(top_memes['year']).most_common(),
        'type': Counter([t for sublist in top_memes['type_list'] for t in sublist]).most_common()
    }
    
    print("\nCommon features among top memes:")
    for feature, counts in common_features.items():
        print(f"\nMost common {feature}:")
        for item, count in counts[:5]:
            print(f"  {item}: {count} occurrences")
    
    return top_memes, common_features

def predictive_model_analysis(df):
    """Create a simple model to predict meme lifespan and identify key predictors"""
    
    print(f"\n===== PREDICTIVE MODEL ANALYSIS =====")
    
    # Prepare features for prediction
# Prepare features
    features = ['humor', 'sarcasm', 'offensive', 'motivation', 'year']
    X = pd.get_dummies(df[features], columns=['year'], drop_first=True)
    y = df['lifespan']

    # Drop rows with NaNs in either X or y
    Xy = pd.concat([X, y], axis=1).dropna()
    X = Xy[X.columns]
    y = Xy['lifespan']

    
    # Calculate correlation between each feature and lifespan
    correlations = {}
    for col in X.columns:
        corr, p_value = pearsonr(X[col], y)
        correlations[col] = (corr, p_value)
    
    # Sort correlations by absolute value
    sorted_correlations = sorted(correlations.items(), key=lambda x: abs(x[1][0]), reverse=True)
    
    print("Feature correlations with lifespan:")
    for feature, (corr, p_value) in sorted_correlations:
        sig = "significant" if p_value < 0.05 else "not significant"
        print(f"{feature}: {corr:.3f} ({sig}, p={p_value:.3f})")
    
    # Create a simple linear regression model to identify key predictors
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import StandardScaler
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train linear regression model
    model = LinearRegression()
    model.fit(X_scaled, y)
    
    # Get feature importance
    feature_importance = list(zip(X.columns, model.coef_))
    feature_importance.sort(key=lambda x: abs(x[1]), reverse=True)
    
    print("\nFeature importance in predicting lifespan:")
    for feature, importance in feature_importance:
        print(f"{feature}: {importance:.3f}")
    
    # Visualize top predictors
    top_n_predictors = 10
    top_features = [f[0] for f in feature_importance[:top_n_predictors]]
    importances = [abs(f[1]) for f in feature_importance[:top_n_predictors]]
    
    plt.figure(figsize=(12, 8))
    bars = plt.barh(top_features, importances, color='steelblue')
    plt.title(f'Top {top_n_predictors} Features for Predicting Meme Lifespan')
    plt.xlabel('Absolute Importance')
    plt.grid(True, axis='x')
    plt.tight_layout()
    plt.savefig('predictive_model_features.png')
    plt.close()
    
    # Visualize combined effects of top emotional predictors
    top_emotion_predictors = [f for f in feature_importance if f[0] in ['humor', 'sarcasm', 'offensive', 'motivation']]
    
    if len(top_emotion_predictors) >= 2:
        top_emotions = [f[0] for f in top_emotion_predictors[:2]]
        
        plt.figure(figsize=(10, 8))
        sns.scatterplot(x=top_emotions[0], y=top_emotions[1], size='lifespan', 
                     hue='lifespan', palette='viridis', data=df, sizes=(20, 200))
        plt.title(f'Combined Effect of Top Emotional Predictors on Lifespan')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('top_emotion_predictors_scatter.png')
        plt.close()
    
    return correlations, feature_importance

# ---------- MAIN ANALYSIS FUNCTION ----------

def run_meme_analysis(file_path, historical_events, keywords):
    """Run comprehensive meme analysis"""
    
    print("Starting meme analysis...\n")
    
    # Load data
    df = load_data(file_path)
    print(f"Loaded {len(df)} memes for analysis\n")
    
    # Introduction
    avg_lifespan, percent_above_avg, percent_above_x = basic_statistics(df)
    
    # Chapter 1: Mortality Analysis
    median_lifespan, max_lifespan, min_lifespan = survival_time_analysis(df)
    top_percent_share = popularity_distribution_analysis(df)
    df = cluster_and_visualize(df)
    
    # Chapter 2: Emotion Analysis
    emotion_correlations = emotion_lifecycle_correlation(df)
    offensive_corr, offensive_p = emotion_popularity_analysis(df)
    emotion_stats = emotion_combination_analysis(df)
    
    # Chapter 3: World Reflection Analysis
    if historical_events:
        event_df = historical_event_analysis(df, historical_events)
    if keywords:
        keyword_df = keyword_matching_analysis(df, keywords)
    peak_count, hot_months = trend_peak_analysis(df)
    
    # Chapter 4: Type Evolution Analysis
    type_evolution_df = type_evolution_analysis(df)
    origin_counts, origin_percentages, platform_growth = platform_evolution_analysis(df)
    platform_df = cross_platform_comparison(df)
    
    # Conclusion: What Makes Memes Endure
    df, emotion_corr = correlation_index_development(df)
    top_memes, common_features = successful_case_analysis(df)
    correlations, feature_importance = predictive_model_analysis(df)
    
    print("\nMeme analysis complete!")
    return df

# ---------- EXAMPLE USAGE ----------
import os

BASE = os.path.join(os.path.dirname(__file__), "../../public")
json_file = os.path.join(BASE, "meme_stats.json")

if __name__ == "__main__":
    # Example file path - replace with your actual file path
    file_path =json_file
    
    # Example historical events
    historical_events = [
        ("2008 Financial Crisis", "2008-09-15", "Lehman Brothers bankruptcy"),
        ("US Election 2016", "2016-11-08", "Trump elected president"),
        ("COVID-19 Pandemic", "2020-03-11", "WHO declares pandemic"),
        ("ChatGPT Release", "2022-11-30", "OpenAI releases ChatGPT")
    ]
    
    # Example keywords to search
    keywords = ["cat", "dog", "Trump", "COVID", "AI", "election", "challenge"]
    
    # Run the analysis
    df = run_meme_analysis(file_path, historical_events, keywords)