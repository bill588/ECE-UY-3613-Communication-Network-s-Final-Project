    import pandas as pd
import matplotlib.pyplot as plt

cols = ['time', 'sender', 'retx_unacked', 'retx_cum', 'cwnd', 'ssthresh', 'rtt']

def load_and_clean(filename):
    df = pd.read_csv(filename, names=cols)
    df = df[df.groupby("sender")['sender'].transform('size') > 100]
    df = df.copy()
    df['time'] = df['time'] - df['time'].min()
    return df

reno_20    = load_and_clean("exp1_reno_rtt20.csv")
cubic_20   = load_and_clean("exp1_cubic_rtt20.csv")
reno_100   = load_and_clean("exp1_reno_rtt100.csv")
cubic_100  = load_and_clean("exp1_cubic_rtt100.csv")
reno_200   = load_and_clean("exp1_reno_rtt200_largebuf.csv")
cubic_200  = load_and_clean("exp1_cubic_rtt200_largebuf.csv")

fig, axs = plt.subplots(1, 3, figsize=(15, 5))

axs[0].plot(reno_20['time'],  reno_20['cwnd'],  label='Reno',  color='tab:blue')
axs[0].plot(cubic_20['time'], cubic_20['cwnd'], label='Cubic', color='tab:orange')
axs[0].set_title("RTT = 20 ms")
axs[0].set_xlabel("Time (s)")
axs[0].set_ylabel("CWND (MSS)")
axs[0].legend()

axs[1].plot(reno_100['time'],  reno_100['cwnd'],  label='Reno',  color='tab:blue')
axs[1].plot(cubic_100['time'], cubic_100['cwnd'], label='Cubic', color='tab:orange')
axs[1].set_title("RTT = 100 ms")
axs[1].set_xlabel("Time (s)")
axs[1].legend()

axs[2].plot(reno_200['time'],  reno_200['cwnd'],  label='Reno',  color='tab:blue')
axs[2].plot(cubic_200['time'], cubic_200['cwnd'], label='Cubic', color='tab:orange')
axs[2].set_title("RTT = 200 ms (7.5 MB buffer)")
axs[2].set_xlabel("Time (s)")
axs[2].legend()

fig.suptitle("CWND Evolution: Reno vs Cubic Across RTT Sweep")
plt.tight_layout()
plt.savefig("exp1_cwnd_comparison.png", dpi=150)
plt.show()
