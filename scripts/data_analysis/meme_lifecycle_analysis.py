import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from tslearn.clustering import TimeSeriesKMeans
from tslearn.utils import to_time_series_dataset

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


def preprocess_trend_data(data):
    """预处理trend数据，准备用于聚类"""
    valid_memes = []
    trend_series = []
    meme_names = []
    emotion_data = []

    for meme in data:
        name = meme.get("name")
        trend = meme.get("trend", [])
        emotion = meme.get("emotion", [])

        # 跳过缺少必要数据的meme
        if not name or not trend or not emotion or len(emotion) != 4:
            continue

        # 处理trend中的None值
        trend_cleaned = np.array([x if x is not None else 0 for x in trend])

        # 只考虑有实际趋势的meme (至少有一个非零值)
        if np.max(trend_cleaned) > 0:
            valid_memes.append(meme)
            trend_series.append(trend_cleaned)
            meme_names.append(name)
            emotion_data.append(emotion)

    if not trend_series:
        return None, None, None, None

    # 统一时间序列长度 (使用最短的序列长度)
    min_length = min(len(ts) for ts in trend_series)
    trend_series = [ts[:min_length] for ts in trend_series]

    return np.array(trend_series), meme_names, emotion_data, valid_memes


def normalize_time_series(trend_series):
    """归一化时间序列，便于比较形状"""
    normalized_series = []

    for ts in trend_series:
        # 避免除以零
        max_val = np.max(ts)
        if max_val > 0:
            normalized_series.append(ts / max_val)
        else:
            normalized_series.append(ts)

    return np.array(normalized_series)


def perform_kmeans_clustering(normalized_series, n_clusters=3):
    """使用K-means进行聚类"""
    # 准备数据
    X = normalized_series.reshape(normalized_series.shape[0], -1)

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # K-means聚类
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)

    return clusters


def perform_dtw_clustering(normalized_series, n_clusters=3):
    """使用DTW（Dynamic Time Warping）进行基于形状的聚类"""
    # 转换为tslearn格式
    ts_dataset = to_time_series_dataset(normalized_series)

    # 使用DTW距离的K-means
    model = TimeSeriesKMeans(n_clusters=n_clusters, metric="dtw", random_state=42)
    clusters = model.fit_predict(ts_dataset)

    return clusters, model


def analyze_meme_lifecycle(data):
    """分析meme生命周期模式"""
    # 预处理数据
    trend_series, meme_names, emotion_data, valid_memes = preprocess_trend_data(data)

    if trend_series is None:
        print("没有足够的有效数据进行聚类分析")
        return

    # 归一化序列
    normalized_series = normalize_time_series(trend_series)

    # 确定最佳聚类数 (silhouette score 或 elbow method)
    # 简化起见，这里直接使用3个聚类
    n_clusters = 3

    # 使用DTW进行聚类
    dtw_clusters, dtw_model = perform_dtw_clustering(normalized_series, n_clusters)

    # 创建结果DataFrame
    results = pd.DataFrame({"name": meme_names, "cluster": dtw_clusters})

    # 添加情绪数据
    emotion_df = pd.DataFrame(
        emotion_data, columns=["humor", "sarcasm", "offensive", "motivation"]
    )
    results = pd.concat([results, emotion_df], axis=1)

    # 分析每个聚类的情绪特征
    cluster_emotions = results.groupby("cluster")[
        ["humor", "sarcasm", "offensive", "motivation"]
    ].mean()
    print("每个生命周期聚类的平均情绪特征:")
    print(cluster_emotions)

    # 可视化聚类结果
    plt.figure(figsize=(20, 15))

    # 1. 绘制各聚类的代表性曲线
    plt.subplot(2, 2, 1)
    cluster_centers = dtw_model.cluster_centers_
    for i in range(n_clusters):
        plt.plot(cluster_centers[i, :, 0], label=f"Cluster {i}")
    plt.title("各生命周期类型的代表曲线")
    plt.xlabel("时间 (月)")
    plt.ylabel("归一化趋势值")
    plt.legend()

    # 2. 绘制每个聚类的所有曲线
    for i in range(n_clusters):
        plt.subplot(2, 2, i + 2)
        cluster_indices = np.where(dtw_clusters == i)[0]

        for idx in cluster_indices:
            plt.plot(normalized_series[idx], alpha=0.3, color=f"C{i}")

        # 加粗显示聚类中心
        plt.plot(
            cluster_centers[i, :, 0], linewidth=3, color="black", label="Cluster Center"
        )

        plt.title(f"Cluster {i}: {len(cluster_indices)} memes")
        plt.xlabel("时间 (月)")
        plt.ylabel("归一化趋势值")

    plt.tight_layout()
    plt.savefig("meme_lifecycle_clusters.png")
    plt.close()

    # 3. 绘制每个聚类的情绪雷达图
    emotion_categories = ["humor", "sarcasm", "offensive", "motivation"]

    plt.figure(figsize=(15, 5 * n_clusters))
    for i in range(n_clusters):
        plt.subplot(n_clusters, 1, i + 1, polar=True)

        # 获取聚类的平均情绪值
        values = cluster_emotions.iloc[i].values.tolist()
        # 闭合雷达图
        values += values[:1]

        # 计算角度
        angles = np.linspace(
            0, 2 * np.pi, len(emotion_categories), endpoint=False
        ).tolist()
        # 闭合
        angles += angles[:1]

        # 绘制雷达图
        plt.polar(angles, values)
        plt.fill(angles, values, alpha=0.25)

        # 添加标签
        plt.xticks(angles[:-1], emotion_categories)
        plt.title(f"Cluster {i} 情绪特征 ({len(results[results.cluster == i])} memes)")

    plt.tight_layout()
    plt.savefig("meme_lifecycle_emotions.png")
    plt.close()

    # 4. 绘制一些随机样例meme的生命周期
    samples_per_cluster = min(3, min(np.bincount(dtw_clusters)))

    plt.figure(figsize=(15, 5 * n_clusters))
    for i in range(n_clusters):
        cluster_indices = np.where(dtw_clusters == i)[0]
        if len(cluster_indices) == 0:
            continue

        # 随机选择样例
        sample_indices = np.random.choice(
            cluster_indices, samples_per_cluster, replace=False
        )

        plt.subplot(n_clusters, 1, i + 1)
        for idx in sample_indices:
            plt.plot(trend_series[idx], label=meme_names[idx])

        plt.title(f"Cluster {i} 示例")
        plt.xlabel("时间 (月)")
        plt.ylabel("趋势值")
        plt.legend()

    plt.tight_layout()
    plt.savefig("meme_lifecycle_examples.png")
    plt.close()

    return results


if __name__ == "__main__":
    # 从JSON文件加载数据
    data = load_data(json_file)

    if not data:
        print("无法加载数据或数据为空")
    else:
        print(f"成功加载 {len(data)} 个meme数据")

        # 执行生命周期分析
        lifecycle_results = analyze_meme_lifecycle(data)

        if lifecycle_results is not None:
            # 保存结果
            lifecycle_results.to_csv("meme_lifecycle_clusters.csv", index=False)
            print("分析结果已保存到 meme_lifecycle_clusters.csv")
