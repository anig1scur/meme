import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
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

    # 首次大于阈值的月份 (使用peak的20%作为阈值)
    threshold = peak_value * 0.2
    first_significant_month = next(
        (i for i, v in enumerate(valid_trend) if v >= threshold), len(valid_trend)
    )

    # 活跃期（有意义的trend值的月数）
    active_months = sum(1 for v in valid_trend if v >= threshold)

    # 总面积（总trend值）
    total_area = sum(valid_trend)

    return peak_value, first_significant_month, active_months, total_area


def emotion_trend_analysis(data):
    """分析情绪与trend特征的关系"""
    # 准备数据结构
    analysis_data = []

    emotion_labels = ["humor", "sarcasm", "offensive", "motivation"]

    for meme in data:
        name = meme.get("name")
        trend_data = meme.get("trend")
        emotion_data = meme.get("emotion")

        # 跳过缺少必要数据的meme
        if not name or not trend_data or not emotion_data:
            continue

        # 确保情绪数据包含4个维度
        if len(emotion_data) != 4:
            continue

        # 计算trend指标
        metrics = calculate_trend_metrics(trend_data)
        if metrics is None:
            continue

        peak_value, first_significant_month, active_months, total_area = metrics

        # 添加到分析数据集
        analysis_data.append(
            {
                "name": name,
                "humor": emotion_data[0],
                "sarcasm": emotion_data[1],
                "offensive": emotion_data[2],
                "motivation": emotion_data[3],
                "peak_value": peak_value,
                "first_significant_month": first_significant_month,
                "active_months": active_months,
                "total_area": total_area,
            }
        )

    # 转换为DataFrame以便分析
    df = pd.DataFrame(analysis_data)

    if df.empty:
        print("没有足够的有效数据进行分析")
        return

    # 计算相关性矩阵
    trend_features = [
        "peak_value",
        "first_significant_month",
        "active_months",
        "total_area",
    ]
    correlation_matrix = pd.DataFrame(index=emotion_labels, columns=trend_features)

    for emotion in emotion_labels:
        for feature in trend_features:
            if emotion in df.columns and feature in df.columns:
                # 过滤有效数据
                valid_data = df[[emotion, feature]].dropna()
                if len(valid_data) > 1:  # 需要至少两个点来计算相关性
                    corr, _ = pearsonr(valid_data[emotion], valid_data[feature])
                    correlation_matrix.loc[emotion, feature] = corr
                else:
                    correlation_matrix.loc[emotion, feature] = np.nan

    # 输出相关性矩阵
    print("情绪维度与趋势特征之间的相关性矩阵:")
    print(correlation_matrix)

    # ⚠️ 这里加一行确保数据类型正确
    correlation_matrix = correlation_matrix.astype(float)

    # 可视化
    plt.figure(figsize=(15, 10))
    emotion_colors = {
        "humor": "blue",
        "sarcasm": "green",
        "offensive": "red",
        "motivation": "purple",
    }
    # 1. 热力图
    plt.figure(figsize=(6, 5))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1, center=0)
    plt.title("情绪与趋势特征相关性热力图")
    plt.tight_layout()
    plt.savefig("correlation_heatmap.png")
    plt.close()

    # 2. 各趋势特征的散点图
    plt.figure(figsize=(15, 10))
    for i, feature in enumerate(trend_features):
        plt.subplot(2, 2, i + 1)  # ✅ 从 1 到 4

        for emotion in emotion_labels:
            if emotion in df.columns and feature in df.columns:
                plt.scatter(
                    df[emotion],
                    df[feature],
                    alpha=0.6,
                    label=emotion,
                    color=emotion_colors[emotion],
                )

        plt.xlabel("情绪强度")
        plt.ylabel(feature)
        plt.title(f"{feature}与情绪关系")
        plt.legend()

    plt.tight_layout()
    plt.savefig("emotion_trend_scatter.png")
    plt.close()


    # 创建单独的散点图，每个情绪维度一个图
    plt.figure(figsize=(20, 15))

    for i, emotion in enumerate(emotion_labels):
        plt.subplot(2, 2, i + 1)

        for j, feature in enumerate(trend_features):
            if emotion in df.columns and feature in df.columns:
                feature_normalized = (df[feature] - df[feature].min()) / (
                    df[feature].max() - df[feature].min() + 1e-10
                )
                plt.scatter(df[emotion], feature_normalized, alpha=0.6, label=feature)

        plt.xlabel(f"{emotion} 强度")
        plt.ylabel("归一化趋势特征值")
        plt.title(f"{emotion}与各趋势特征关系")
        plt.legend()

    plt.tight_layout()
    plt.savefig("emotion_specific_analysis.png")
    plt.close()

    return df


if __name__ == "__main__":
    # 从JSON文件加载数据
    data = load_data(json_file)

    if not data:
        print("无法加载数据或数据为空")
    else:
        print(f"成功加载 {len(data)} 个meme数据")
        analysis_df = emotion_trend_analysis(data)
