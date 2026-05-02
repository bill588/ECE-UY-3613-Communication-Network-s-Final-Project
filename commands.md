# Reproduction Commands

All experiments use the same CloudLab profile and topology.

**Profile:** https://www.cloudlab.us/p/nyunetworks/education?refspec=refs/heads/tcp_congestion_control

**Topology:** romeo (sender) → router (bottleneck) → juliet (receiver)

---

## Initial Setup (one-time per session)

### On Juliet
```bash
sudo apt update
sudo apt -y install iperf3
```

### On Romeo
```bash
sudo apt update
sudo apt -y install iperf3 moreutils python3-pip libjpeg-dev
sudo python3 -m pip install pandas matplotlib
sudo sysctl -w net.ipv4.tcp_no_metrics_save=1
wget -O ss-output.sh https://raw.githubusercontent.com/ffund/tcp-ip-essentials/cloudlab/scripts/ss-output.sh
mkdir -p ~/results
```

### On Router
No installs needed. `tc` is built in.

---

## Experiment 1: RTT Sweep (Cubic Favorable)

**Fixed:** 100 Mbps, 0% loss, 1.5 MB buffer (limit 1000), 60s flows

### Per-run procedure

For each (algorithm, RTT) combination:

1. Router: apply tc shaping (see below)
2. Juliet: `iperf3 -s -1`
3. Romeo Terminal 1: `bash ss-output.sh 10.10.2.100`
4. Romeo Terminal 2: `iperf3 -c juliet -t 60 -C <reno|cubic> -J > ~/results/<run_name>.json`
5. Wait 60 seconds
6. Romeo Terminal 1: Ctrl+C, then `mv sender-ss.csv ~/results/<run_name>.csv`

### Router commands: 20ms RTT (10ms each side)
```bash
sudo tc qdisc del dev $iface_0 root
sudo tc qdisc del dev $iface_1 root

iface_0=$(ip route get 10.10.1.100 | grep -oP "(?<=dev )[^ ]+")
sudo tc qdisc add dev $iface_0 root handle 1: htb default 3
sudo tc class add dev $iface_0 parent 1: classid 1:3 htb rate 100mbit
sudo tc qdisc add dev $iface_0 parent 1:3 handle 3: netem limit 1000 delay 10ms loss 0%

iface_1=$(ip route get 10.10.2.100 | grep -oP "(?<=dev )[^ ]+")
sudo tc qdisc add dev $iface_1 root handle 1: htb default 3
sudo tc class add dev $iface_1 parent 1: classid 1:3 htb rate 100mbit
sudo tc qdisc add dev $iface_1 parent 1:3 handle 3: netem limit 1000 delay 10ms loss 0%
```

### Router commands: 100ms RTT (50ms each side)
Same as above, change `delay 10ms` to `delay 50ms` on both interfaces.

### Router commands: 200ms RTT, 1.5 MB buffer (100ms each side)
Same as above, change `delay 10ms` to `delay 100ms` on both interfaces.

### Router commands: 200ms RTT, 7.5 MB buffer (100ms each side)
Same as above, change `delay 10ms` to `delay 100ms` and `limit 1000` to `limit 5000` on both interfaces.

---

## Experiment 2: Random Loss Sweep (Cubic Unfavorable)

**Fixed:** 100 Mbps, 50ms RTT (25ms each side), 1.5 MB buffer (limit 1000), 60s flows

### Per-run procedure
Same as Experiment 1.

### Router commands: 0.5% loss
```bash
sudo tc qdisc del dev $iface_0 root
sudo tc qdisc del dev $iface_1 root

iface_0=$(ip route get 10.10.1.100 | grep -oP "(?<=dev )[^ ]+")
sudo tc qdisc add dev $iface_0 root handle 1: htb default 3
sudo tc class add dev $iface_0 parent 1: classid 1:3 htb rate 100mbit
sudo tc qdisc add dev $iface_0 parent 1:3 handle 3: netem limit 1000 delay 25ms loss 0.5%

iface_1=$(ip route get 10.10.2.100 | grep -oP "(?<=dev )[^ ]+")
sudo tc qdisc add dev $iface_1 root handle 1: htb default 3
sudo tc class add dev $iface_1 parent 1: classid 1:3 htb rate 100mbit
sudo tc qdisc add dev $iface_1 parent 1:3 handle 3: netem limit 1000 delay 25ms loss 0.5%
```

### Router commands: 1% loss
Same as above, change `loss 0.5%` to `loss 1%` on both interfaces.

### Router commands: 2% loss
Same as above, change `loss 0.5%` to `loss 2%` on both interfaces.

---

## Experiment 3: Fairness (Competing Flows)

**Fixed:** 100 Mbps, 0% loss, 60s flows, 2 simultaneous flows (1 Reno + 1 Cubic)

### Differences from Experiments 1 and 2
- 2 iperf3 servers on Juliet (ports 5201 and 5301)
- 2 iperf3 clients on Romeo running simultaneously
- 1 ss-output.sh session captures both flows (distinguished by source port)

### Per-run procedure

1. Router: apply tc shaping (see below)
2. Juliet Terminal 1: `iperf3 -s -1`
3. Juliet Terminal 2: `iperf3 -s -1 -p 5301`
4. Romeo Terminal 1: `bash ss-output.sh 10.10.2.100`
5. Romeo Terminal 2: paste Reno command (don't hit enter yet)
6. Romeo Terminal 3: paste Cubic command (don't hit enter yet)
7. Hit enter on Terminals 2 and 3 within 1 second of each other
8. Wait 60 seconds
9. Romeo Terminal 1: Ctrl+C, then `mv sender-ss.csv ~/results/<run_label>.csv`

### Client commands
```bash
# Romeo Terminal 2 (Reno flow, port 5201):
iperf3 -c juliet -t 60 -C reno -J > ~/results/<run_label>_reno.json

# Romeo Terminal 3 (Cubic flow, port 5301):
iperf3 -c juliet -t 60 -C cubic -p 5301 -J > ~/results/<run_label>_cubic.json
```

### Router commands: 3A — 20ms RTT, 1.5 MB buffer
```bash
sudo tc qdisc del dev $iface_0 root
sudo tc qdisc del dev $iface_1 root

iface_0=$(ip route get 10.10.1.100 | grep -oP "(?<=dev )[^ ]+")
sudo tc qdisc add dev $iface_0 root handle 1: htb default 3
sudo tc class add dev $iface_0 parent 1: classid 1:3 htb rate 100mbit
sudo tc qdisc add dev $iface_0 parent 1:3 handle 3: netem limit 1000 delay 10ms loss 0%

iface_1=$(ip route get 10.10.2.100 | grep -oP "(?<=dev )[^ ]+")
sudo tc qdisc add dev $iface_1 root handle 1: htb default 3
sudo tc class add dev $iface_1 parent 1: classid 1:3 htb rate 100mbit
sudo tc qdisc add dev $iface_1 parent 1:3 handle 3: netem limit 1000 delay 10ms loss 0%
```

### Router commands: 3B — 200ms RTT, 7.5 MB buffer
Same as above, change `delay 10ms` to `delay 100ms` and `limit 1000` to `limit 5000` on both interfaces.
