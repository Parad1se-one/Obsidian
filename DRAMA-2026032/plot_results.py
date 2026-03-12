#!/usr/bin/env python3
"""
Generate comparison plots for DRAMA experiments.
Reads training_stats.json from results/{difficulty}/{algo}/ directories.
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

DRAMA_DIR = Path("/home/openclaw/.openclaw/DRAMA/DRAMA")
RESULTS_DIR = DRAMA_DIR / "results"

ALGO_LABELS = {
    "mappo":    "MAPPO (Baseline)",
    "mappo_rm": "MAPPO-RM (Ours)",
    "ippo":     "IPPO (Baseline)",
    "ippo_rm":  "IPPO-RM (Ours)",
    "dqn":      "DQN (Baseline)",
    "qmix":     "QMIX (Baseline)",
}

ALGO_COLORS = {
    "mappo":    "#1f77b4",
    "mappo_rm": "#d62728",
    "ippo":     "#2ca02c",
    "ippo_rm":  "#ff7f0e",
    "dqn":      "#9467bd",
    "qmix":     "#8c564b",
}

ALGO_STYLES = {
    "mappo":    "--",
    "mappo_rm": "-",
    "ippo":     "--",
    "ippo_rm":  "-",
    "dqn":      ":",
    "qmix":     ":",
}


def smooth(data, window=20):
    """Moving average smoothing."""
    if len(data) < window:
        return data
    kernel = np.ones(window) / window
    return np.convolve(data, kernel, mode='valid')


def plot_difficulty(difficulty, algos):
    """Generate completion ratio comparison plot for a difficulty level."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    for algo in algos:
        stats_path = RESULTS_DIR / difficulty / algo / "training_stats.json"
        if not stats_path.exists():
            print(f"  ⚠ Missing: {stats_path}")
            continue

        with open(stats_path) as f:
            stats = json.load(f)

        episodes = [s["episode"] for s in stats]
        crs = [s["completed_ratio"] for s in stats]

        smoothed = smooth(np.array(crs), window=20)
        x = episodes[19:]  # offset for smoothing window

        ax.plot(x, smoothed,
                label=ALGO_LABELS.get(algo, algo),
                color=ALGO_COLORS.get(algo, None),
                linestyle=ALGO_STYLES.get(algo, "-"),
                linewidth=2.0,
                alpha=0.9)

    ax.set_xlabel("Training Episode", fontsize=13)
    ax.set_ylabel("Task Completion Ratio", fontsize=13)
    ax.set_title(f"DRAMA — {difficulty.capitalize()} Difficulty: Task Completion Comparison", fontsize=14)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlim(0, 520)
    ax.legend(loc="lower right", fontsize=11, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.tick_params(labelsize=11)

    plt.tight_layout()
    out_path = RESULTS_DIR / difficulty / f"{difficulty}_completion_comparison.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  ✅ Saved: {out_path}")


def main():
    algos = ["mappo", "mappo_rm", "ippo", "ippo_rm", "dqn", "qmix"]

    print("Generating Easy comparison plot...")
    plot_difficulty("easy", algos)

    print("Generating Medium comparison plot...")
    plot_difficulty("medium", algos)

    # Print summary table
    print("\n" + "=" * 80)
    print("  SUMMARY TABLE")
    print("=" * 80)
    print(f"{'Algo':<12} {'Difficulty':<10} {'Best CR':<10} {'Final CR':<10} {'Success%':<10} {'Converge':<10}")
    print("-" * 80)

    for diff in ["easy", "medium"]:
        for algo in algos:
            metrics_path = RESULTS_DIR / diff / algo / "final_metrics.json"
            if not metrics_path.exists():
                continue
            with open(metrics_path) as f:
                m = json.load(f)
            conv = str(m.get("convergence_episode", "N/A"))
            print(f"{algo:<12} {diff:<10} {m['best_completed_ratio']:<10.3f} {m['final_completed_ratio']:<10.3f} {m['success_rate']*100:<10.1f} {conv:<10}")

    print("=" * 80)


if __name__ == "__main__":
    main()
