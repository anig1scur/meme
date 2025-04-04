import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# 导入各个分析模块
# 假设上面三个脚本已保存为独立的.py文件
from emotion_trend_analysis import emotion_trend_analysis, load_data as load_data_1
from meme_lifecycle_analysis import analyze_meme_lifecycle, load_data as load_data_2
from year_platform_analysis import year_platform_analysis, load_data as load_data_3


def ensure_dir(directory):
    """确保输出目录存在"""
    if not os.path.exists(directory):
        os.makedirs(directory)


def main(data_file="meme_data.json", output_dir="meme_analysis_results"):
    """运行所有meme分析任务"""
    print("=" * 50)
    print("开始Meme数据分析...")
    print("=" * 50)

    # 确保输出目录存在
    ensure_dir(output_dir)

    # 设置全局图表参数
    plt.rcParams["font.size"] = 12
    plt.rcParams["axes.titlesize"] = 14
    plt.rcParams["axes.labelsize"] = 12
    plt.rcParams["xtick.labelsize"] = 10
    plt.rcParams["ytick.labelsize"] = 10

    # 加载数据
    try:
        data = load_data_1(data_file)
        if not data:
            print("数据加载失败，请检查文件路径和格式")
            return

        print(f"成功加载 {len(data)} 个meme数据")
    except Exception as e:
        print(f"数据加载错误: {e}")
        return

    # 1. 情绪标签与趋势的关系分析
    print("\n1. 执行情绪标签与趋势的关系分析...")
    try:
        emotion_df = emotion_trend_analysis(data)
        if emotion_df is not None:
            emotion_df.to_csv(f"{output_dir}/emotion_trend_analysis.csv", index=False)
            print("  情绪与趋势分析完成，结果已保存")
    except Exception as e:
        print(f"  情绪与趋势分析出错: {e}")

    # 2. Meme生命周期分析
    print("\n2. 执行Meme生命周期分析...")
    try:
        lifecycle_df = analyze_meme_lifecycle(data)
        if lifecycle_df is not None:
            lifecycle_df.to_csv(
                f"{output_dir}/meme_lifecycle_clusters.csv", index=False
            )
            print("  生命周期分析完成，结果已保存")
    except Exception as e:
        print(f"  生命周期分析出错: {e}")

    # 3. 年份与平台分析
    print("\n3. 执行年份与平台分析...")
    try:
        year_platform_df = year_platform_analysis(data)
        if year_platform_df is not None:
            year_platform_df.to_csv(
                f"{output_dir}/meme_year_platform_analysis.csv", index=False
            )
            print("  年份与平台分析完成，结果已保存")
    except Exception as e:
        print(f"  年份与平台分析出错: {e}")

    # 生成分析报告
    generate_report(output_dir)

    print("\n" + "=" * 50)
    print("Meme分析完成!")
    print(f"所有结果已保存到 {output_dir} 目录")
    print("=" * 50)


def generate_report(output_dir):
    """生成分析报告"""
    report_file = f"{output_dir}/meme_analysis_report.md"

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("# Meme数据分析报告\n\n")
        f.write(f"生成日期: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # 分析结果摘要
        f.write("## 分析结果摘要\n\n")

        # 1. 情绪与趋势分析
        f.write("### 1. 情绪标签与趋势的关系\n\n")
        f.write(
            "本部分分析了meme的四种情绪维度（幽默、讽刺、冒犯、激励）与其流行趋势特征（峰值、首次大于阈值的月份、活跃期、总面积）之间的相关性。\n\n"
        )
        f.write("关键发现:\n")
        f.write("- 情绪与趋势特征的相关性热力图可见: `emotion_trend_analysis.png`\n")
        f.write(
            "- 各情绪维度与趋势特征的散点图可见: `emotion_specific_analysis.png`\n\n"
        )

        # 2. 生命周期分析
        f.write("### 2. Meme生命周期分析\n\n")
        f.write(
            "本部分对meme的趋势曲线进行了形态聚类，识别不同的生命周期模式，并分析了各类meme的情绪特征。\n\n"
        )
        f.write("关键发现:\n")
        f.write("- 不同生命周期类型的代表曲线可见: `meme_lifecycle_clusters.png`\n")
        f.write("- 各生命周期类型的情绪雷达图可见: `meme_lifecycle_emotions.png`\n")
        f.write("- 各类型示例meme可见: `meme_lifecycle_examples.png`\n\n")

        # 3. 年份与平台分析
        f.write("### 3. 年份与平台分析\n\n")
        f.write("本部分分析了不同年份和平台上meme的情绪结构差异与演变趋势。\n\n")
        f.write("关键发现:\n")
        f.write("- 年份情绪趋势分析可见: `year_emotion_analysis.png`\n")
        f.write("- 平台情绪分析可见: `platform_emotion_analysis.png`\n")
        f.write(
            "- 平台与年份的联合分析可见: `platform_year_distribution.png` 和 `platform_year_emotion_trends.png`\n"
        )
        f.write("- 情绪结构随年代的变化可见: `decade_emotion_trends.png`\n\n")

        # 分析方法说明
        f.write("## 分析方法说明\n\n")

        f.write("### 1. 情绪与趋势关系分析\n")
        f.write(
            "- 计算每个meme的趋势特征指标（峰值大小、首次显著月份、活跃月数、总面积）\n"
        )
        f.write("- 分析这些指标与情绪维度之间的皮尔逊相关系数\n")
        f.write("- 通过散点图和热力图可视化相关关系\n\n")

        f.write("### 2. 生命周期分析\n")
        f.write("- 对趋势曲线进行归一化处理以突出形状特征\n")
        f.write("- 使用动态时间规整(DTW)度量和时间序列K-means聚类\n")
        f.write("- 分析各类meme的代表曲线和情绪特征\n\n")

        f.write("### 3. 年份与平台分析\n")
        f.write("- 按年份和平台分组计算平均情绪值\n")
        f.write("- 通过雷达图和趋势线可视化情绪结构随时间和平台的变化\n")
        f.write("- 分析不同平台meme的分布和情绪差异\n")

        # 报告脚注
        f.write("\n\n---\n")
        f.write("注: 所有图表和CSV文件可在同一目录下找到。")

    print(f"分析报告已生成: {report_file}")


import os

BASE = os.path.join(os.path.dirname(__file__), "../../public")
json_file = os.path.join(BASE, "meme_stats.json")


if __name__ == "__main__":
    main(json_file)
