import pandas as pd
import matplotlib.pyplot as plt

cols = ['time', 'sender', 'retx_unacked', 'retx_cum', 'cwnd', 'ssthresh', 'rtt']

def load_and_clean(filename):
    df = pd.read_csv(filename, names=cols)
    df = df[df.groupby("sender")['sender'].transform('size') > 100]
    df = df.copy()
    df['time'] = df['time'] - df['time'].min()
    return df

# Load all 6 runs
reno_05    = load_and_clean("exp2_reno_loss05.csv")
cubic_05   = load_and_clean("exp2_cubic_loss05.csv")
reno_1     = load_and_clean("exp2_reno_loss1.csv")
cubic_1    = load_and_clean("exp2_cubic_loss1.csv")
reno_2     = load_and_clean("exp2_reno_loss2.csv")
cubic_2    = load_and_clean("exp2_cubic_loss2.csv")

fig, axs = plt.subplots(1, 3, figsize=(15, 5))

axs[0].plot(reno_05['time'],  reno_05['cwnd'],  label='Reno',  color='tab:blue')
axs[0].plot(cubic_05['time'], cubic_05['cwnd'], label='Cubic', color='tab:orange')
axs[0].set_title("Loss = 0.5%")
axs[0].set_xlabel("Time (s)")
axs[0].set_ylabel("CWND (MSS)")
axs[0].legend()

axs[1].plot(reno_1['time'],  reno_1['cwnd'],  label='Reno',  color='tab:blue')
axs[1].plot(cubic_1['time'], cubic_1['cwnd'], label='Cubic', color='tab:orange')
axs[1].set_title("Loss = 1%")
axs[1].set_xlabel("Time (s)")
axs[1].legend()

axs[2].plot(reno_2['time'],  reno_2['cwnd'],  label='Reno',  color='tab:blue')
axs[2].plot(cubic_2['time'], cubic_2['cwnd'], label='Cubic', color='tab:orange')
axs[2].set_title("Loss = 2%")
axs[2].set_xlabel("Time (s)")
axs[2].legend()

fig.suptitle("CWND Evolution: Reno vs Cubic Under Random Loss (50ms RTT, 100 Mbps)")
plt.tight_layout()
plt.savefig("exp2_cwnd_comparison.png", dpi=150)
plt.show()
