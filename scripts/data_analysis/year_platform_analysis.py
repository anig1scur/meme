import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

import os

BASE = os.path.join(os.path.dirname(__file__), "../../public")
json_file = os.path.join(BASE, "meme_stats.json")



def load_data(file_path):
    """从JSON文件加载meme数据"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"加载数据时出错: {e}")
        return []


def calculate_trend_metrics(trend_data):
    """计算trend数据的关键指标"""
    if not trend_data or len(trend_data) == 0 or all(x is None for x in trend_data):
        return None, None, None, None

    # 过滤None值
    valid_trend = [x if x is not None else 0 for x in trend_data]

    # 计算四个关键指标
    peak_value = max(valid_trend)
    area = sum(valid_trend)

    return peak_value, area


def preprocess_data(data):
    """预处理数据，创建分析用的DataFrame"""
    processed_data = []

    for meme in data:
        name = meme.get("name")
        year = meme.get("year")
        origin = meme.get("origin")
        emotion = meme.get("emotion")
        trend = meme.get("trend")

        # 跳过缺少必要数据的meme
        if not name or not year or not origin or not emotion or not trend:
            continue

        # 确保emotion包含4个维度
        if len(emotion) != 4:
            continue

        # 转换年份为整数
        try:
            year = int(year)
        except (ValueError, TypeError):
            continue

        # 计算trend指标
        trend_metrics = calculate_trend_metrics(trend)
        if trend_metrics is None:
            peak_value, area = None, None
        else:
            peak_value, area = trend_metrics

        # 添加到处理后的数据
        processed_data.append(
            {
                "name": name,
                "year": year,
                "origin": origin,
                "humor": emotion[0],
                "sarcasm": emotion[1],
                "offensive": emotion[2],
                "motivation": emotion[3],
                "peak_value": peak_value,
                "total_area": area,
            }
        )

    # 转换为DataFrame
    df = pd.DataFrame(processed_data)

    return df


def analyze_year_trends(df):
    """分析不同年份的情绪结构趋势"""
    if df.empty:
        print("没有足够的数据进行年份分析")
        return

    # 按年份分组计算平均情绪值
    year_emotions = df.groupby("year")[
        ["humor", "sarcasm", "offensive", "motivation"]
    ].mean()

    # 确保年份是排序的
    year_emotions = year_emotions.sort_index()

    # 可视化年份情绪趋势
    plt.figure(figsize=(15, 10))

    # 1. 情绪随时间的变化趋势线
    plt.subplot(2, 1, 1)
    for emotion in ["humor", "sarcasm", "offensive", "motivation"]:
        plt.plot(
            year_emotions.index,
            year_emotions[emotion],
            marker="o",
            linewidth=2,
            label=emotion,
        )

    plt.xlabel("年份")
    plt.ylabel("平均情绪强度")
    plt.title("Meme情绪随年份的变化趋势")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)

    # 2. 每个年份的情绪雷达图
    # 每行最多4个雷达图
    years = sorted(year_emotions.index.tolist())
    rows = (len(years) + 3) // 4

    plt.figure(figsize=(20, 5 * rows))

    for i, year in enumerate(years):
        plt.subplot(rows, 4, i + 1, polar=True)

        # 获取年份的情绪值
        values = year_emotions.loc[year].tolist()
        # 闭合雷达图
        values += values[:1]

        # 情绪类别
        categories = ["humor", "sarcasm", "offensive", "motivation"]
        # 计算角度
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        # 闭合
        angles += angles[:1]
        categories += categories[:1]

        # 绘制雷达图
        plt.polar(angles, values)
        plt.fill(angles, values, alpha=0.25)

        # 添加标签
        plt.xticks(angles, categories)
        plt.title(f"{year}年 ({len(df[df.year == year])} memes)")

    plt.tight_layout()
    plt.savefig("year_emotion_analysis.png")
    plt.close()

    # 3. 情绪和趋势指标随年份的热力图
    if "peak_value" in df.columns and "total_area" in df.columns:
        year_metrics = df.groupby("year")[
            ["humor", "sarcasm", "offensive", "motivation", "peak_value", "total_area"]
        ].mean()

        plt.figure(figsize=(12, 8))
        sns.heatmap(year_metrics, cmap="YlGnBu", annot=True, fmt=".2f")
        plt.title("年份与情绪/趋势指标的关系热力图")
        plt.tight_layout()
        plt.savefig("year_metrics_heatmap.png")
        plt.close()

    return year_emotions


def analyze_platform_trends(df):
    """分析不同平台的情绪结构和趋势"""
    if df.empty:
        print("没有足够的数据进行平台分析")
        return

    # 处理缺失的平台数据
    df["origin"] = df["origin"].fillna("Unknown")

    # 统计各平台的meme数量
    platform_counts = df["origin"].value_counts()

    # 计算各平台的平均情绪值
    platform_emotions = df.groupby("origin")[
        ["humor", "sarcasm", "offensive", "motivation"]
    ].mean()

    # 可视化
    plt.figure(figsize=(15, 12))

    # 1. 平台分布饼图
    plt.subplot(2, 2, 1)
    plt.pie(
        platform_counts, labels=platform_counts.index, autopct="%1.1f%%", startangle=90
    )
    plt.axis("equal")
    plt.title("各平台meme数量分布")

    # 2. 各平台的情绪柱状图
    plt.subplot(2, 2, 2)
    platform_emotions.plot(kind="bar", figsize=(10, 6), ax=plt.gca())
    plt.title("各平台meme的平均情绪强度")
    plt.xlabel("平台")
    plt.ylabel("平均情绪强度")
    plt.legend(loc="best")

    # 3. 各平台的情绪雷达图
    platforms = platform_emotions.index.tolist()
    rows = (len(platforms) + 1) // 2

    plt.figure(figsize=(15, 5 * rows))

    for i, platform in enumerate(platforms):
        plt.subplot(rows, 2, i + 1, polar=True)

        # 获取平台的情绪值
        values = platform_emotions.loc[platform].tolist()
        # 闭合雷达图
        values += values[:1]

        # 情绪类别
        categories = ["humor", "sarcasm", "offensive", "motivation"]
        # 计算角度
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        # 闭合
        angles += angles[:1]
        categories += categories[:1]

        # 绘制雷达图
        plt.polar(angles, values)
        plt.fill(angles, values, alpha=0.25)

        # 添加标签
        plt.xticks(angles, categories)
        plt.title(f"{platform} ({platform_counts.get(platform, 0)} memes)")

    plt.tight_layout()
    plt.savefig("platform_emotion_analysis.png")
    plt.close()

    # 4. 各平台的情绪与趋势指标热力图
    if "peak_value" in df.columns and "total_area" in df.columns:
        platform_metrics = df.groupby("origin")[
            ["humor", "sarcasm", "offensive", "motivation", "peak_value", "total_area"]
        ].mean()

        plt.figure(figsize=(12, 8))
        sns.heatmap(platform_metrics, cmap="YlGnBu", annot=True, fmt=".2f")
        plt.title("平台与情绪/趋势指标的关系热力图")
        plt.tight_layout()
        plt.savefig("platform_metrics_heatmap.png")
        plt.close()

    return platform_emotions


def analyze_platform_by_year(df):
    """分析平台随时间的演变趋势"""
    if df.empty:
        print("没有足够的数据进行平台年份联合分析")
        return

    # 处理缺失值
    df["origin"] = df["origin"].fillna("Unknown")

    # 统计每年各平台的meme数量
    platform_year_counts = df.groupby(["year", "origin"]).size().unstack(fill_value=0)

    # 可视化
    plt.figure(figsize=(15, 8))
    platform_year_counts.plot(kind="bar", stacked=True)
    plt.title("各平台meme数量随年份的变化")
    plt.xlabel("年份")
    plt.ylabel("meme数量")
    plt.legend(title="平台")
    plt.tight_layout()
    plt.savefig("platform_year_distribution.png")
    plt.close()

    # 计算每年各平台的平均情绪
    emotions = ["humor", "sarcasm", "offensive", "motivation"]

    # 检查数据量是否足够
    if len(df) > 10:
        # 选择主要平台（数据量最多的3个）
        main_platforms = df["origin"].value_counts().nlargest(3).index.tolist()

        # 为每种情绪创建一个趋势图
        plt.figure(figsize=(20, 15))

        for i, emotion in enumerate(emotions):
            plt.subplot(2, 2, i + 1)

            for platform in main_platforms:
                platform_data = df[df["origin"] == platform]
                yearly_emotion = platform_data.groupby("year")[emotion].mean()

                if not yearly_emotion.empty:
                    plt.plot(
                        yearly_emotion.index,
                        yearly_emotion.values,
                        marker="o",
                        linewidth=2,
                        label=platform,
                    )

            plt.xlabel("年份")
            plt.ylabel(f"{emotion} 强度")
            plt.title(f"{emotion} 强度随年份和平台的变化")
            plt.legend(title="平台")
            plt.grid(True, linestyle="--", alpha=0.7)

        plt.tight_layout()
        plt.savefig("platform_year_emotion_trends.png")
        plt.close()

    return platform_year_counts


def year_platform_analysis(data):
    """执行年份和平台分析"""
    # 预处理数据
    df = preprocess_data(data)

    if df.empty:
        print("没有足够的有效数据进行分析")
        return

    print(f"有效数据: {len(df)} 个meme")

    # 年份分析
    year_emotions = analyze_year_trends(df)

    # 平台分析
    platform_emotions = analyze_platform_trends(df)


def year_platform_analysis(data):
    """执行年份和平台分析"""
    # 预处理数据
    df = preprocess_data(data)

    if df.empty:
        print("没有足够的有效数据进行分析")
        return

    print(f"有效数据: {len(df)} 个meme")

    # 年份分析
    year_emotions = analyze_year_trends(df)

    # 平台分析
    platform_emotions = analyze_platform_trends(df)

    # 平台年份联合分析
    platform_year_data = analyze_platform_by_year(df)

    # 输出一些统计信息
    print("\n年份分布:")
    print(df["year"].value_counts().sort_index())

    print("\n平台分布:")
    print(df["origin"].value_counts())

    print("\n各年份的平均情绪强度:")
    if year_emotions is not None:
        print(year_emotions)

    print("\n各平台的平均情绪强度:")
    if platform_emotions is not None:
        print(platform_emotions)

    # 额外分析：情绪结构随时间的变化趋势
    if not df.empty and len(df) > 10:
        # 按年代分组（2000-2009, 2010-2019等）
        df["decade"] = (df["year"] // 10) * 10
        decade_emotions = df.groupby("decade")[
            ["humor", "sarcasm", "offensive", "motivation"]
        ].mean()

        print("\n按年代的平均情绪强度:")
        print(decade_emotions)

        # 可视化年代情绪变化
        plt.figure(figsize=(12, 8))
        decade_emotions.plot(kind="bar")
        plt.title("Meme情绪结构随年代的变化")
        plt.xlabel("年代")
        plt.ylabel("平均情绪强度")
        plt.legend(title="情绪维度")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.savefig("decade_emotion_trends.png")
        plt.close()

    return df


if __name__ == "__main__":
    # 从JSON文件加载数据
    data = load_data(json_file)

    if not data:
        print("无法加载数据或数据为空")
    else:
        print(f"成功加载 {len(data)} 个meme数据")
        # 执行年份和平台分析
        analysis_df = year_platform_analysis(data)

        if analysis_df is not None:
            # 保存处理后的数据
            analysis_df.to_csv("meme_year_platform_analysis.csv", index=False)
            print("分析结果已保存到 meme_year_platform_analysis.csv")
