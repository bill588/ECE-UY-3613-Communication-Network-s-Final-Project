import json
import matplotlib.pyplot as plt

def get_mbps(filename):
    with open(filename) as f:
        d = json.load(f)
    return d["end"]["sum_received"]["bits_per_second"] / 1e6

# Small-buffer sweep (consistent across all three RTTs)
rtts = [20, 100, 200]
reno_small  = [get_mbps("exp1_reno_rtt20.json"),
               get_mbps("exp1_reno_rtt100.json"),
               get_mbps("exp1_reno_rtt200.json")]
cubic_small = [get_mbps("exp1_cubic_rtt20.json"),
               get_mbps("exp1_cubic_rtt100.json"),
               get_mbps("exp1_cubic_rtt200.json")]

# Large-buffer points at 200ms only
reno_large_200  = get_mbps("exp1_reno_rtt200_largebuf.json")
cubic_large_200 = get_mbps("exp1_cubic_rtt200_largebuf.json")

fig, ax = plt.subplots(figsize=(8, 5))

# Main sweep lines
ax.plot(rtts, reno_small,  marker='o', color='tab:blue',   label='Reno (1.5 MB buffer)')
ax.plot(rtts, cubic_small, marker='o', color='tab:orange', label='Cubic (1.5 MB buffer)')

# Large-buffer markers at 200ms
ax.plot(200, reno_large_200,  marker='s', markersize=10, color='tab:blue',
        markerfacecolor='white', markeredgewidth=2, linestyle='None',
        label='Reno (7.5 MB buffer)')
ax.plot(200, cubic_large_200, marker='s', markersize=10, color='tab:orange',
        markerfacecolor='white', markeredgewidth=2, linestyle='None',
        label='Cubic (7.5 MB buffer)')

# Annotate each point with its value
for x, y in zip(rtts, reno_small):
    ax.annotate(f"{y:.1f}", (x, y), textcoords="offset points", xytext=(8, -12), fontsize=9)
for x, y in zip(rtts, cubic_small):
    ax.annotate(f"{y:.1f}", (x, y), textcoords="offset points", xytext=(8, 6), fontsize=9)
ax.annotate(f"{reno_large_200:.1f}",  (200, reno_large_200),  textcoords="offset points", xytext=(8, -4),  fontsize=9)
ax.annotate(f"{cubic_large_200:.1f}", (200, cubic_large_200), textcoords="offset points", xytext=(8, -4),  fontsize=9)

ax.set_xlabel("RTT (ms)")
ax.set_ylabel("Throughput (Mbps)")
ax.set_title("Throughput vs RTT: Reno vs Cubic")
ax.set_xticks(rtts)
ax.set_ylim(0, 100)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(loc='lower left')
plt.tight_layout()
plt.savefig("exp1_throughput_vs_rtt.png", dpi=150)
plt.show()
