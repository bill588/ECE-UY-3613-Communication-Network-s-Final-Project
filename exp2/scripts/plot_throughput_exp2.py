import json
import matplotlib.pyplot as plt

def get_mbps(filename):
    with open(filename) as f:
        d = json.load(f)
    return d["end"]["sum_received"]["bits_per_second"] / 1e6

losses = [0.5, 1, 2]
reno  = [get_mbps("exp2_reno_loss05.json"),
         get_mbps("exp2_reno_loss1.json"),
         get_mbps("exp2_reno_loss2.json")]
cubic = [get_mbps("exp2_cubic_loss05.json"),
         get_mbps("exp2_cubic_loss1.json"),
         get_mbps("exp2_cubic_loss2.json")]

fig, ax = plt.subplots(figsize=(8, 5))

# Reference line: no-loss baseline (from Exp 1, 20ms RTT)
ax.axhline(y=91.5, color='gray', linestyle=':', linewidth=1, label='No-loss baseline (~91.5 Mbps)')

# Main lines
ax.plot(losses, reno,  marker='o', color='tab:blue',   label='Reno')
ax.plot(losses, cubic, marker='o', color='tab:orange', label='Cubic')

# Annotate each point
for x, y in zip(losses, reno):
    ax.annotate(f"{y:.2f}", (x, y), textcoords="offset points", xytext=(8, -12), fontsize=9)
for x, y in zip(losses, cubic):
    ax.annotate(f"{y:.2f}", (x, y), textcoords="offset points", xytext=(8, 6), fontsize=9)

ax.set_xlabel("Random Loss Rate (%)")
ax.set_ylabel("Throughput (Mbps)")
ax.set_title("Throughput vs Random Loss Rate: Reno vs Cubic\n(50ms RTT, 100 Mbps, 1.5MB buffer)")
ax.set_xticks(losses)
ax.set_ylim(0, 100)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig("exp2_throughput_vs_loss.png", dpi=150)
plt.show()
