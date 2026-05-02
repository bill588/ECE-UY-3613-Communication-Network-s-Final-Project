\# TCP Reno vs Cubic: Performance Under Varying Network Conditions



Experiments comparing TCP Reno and TCP Cubic congestion control algorithms on CloudLab.



\## CloudLab Setup



Profile: https://www.cloudlab.us/p/nyunetworks/education?refspec=refs/heads/tcp\_congestion\_control



Topology: romeo (sender) → router (bottleneck) → juliet (receiver)



Tools: iperf3, tc/netem, ss-output.sh



\## Repository Structure



\- exp1/ — Experiment 1: RTT sweep (Cubic favorable)

\- exp2/ — Experiment 2: Random loss sweep (Cubic unfavorable)

\- exp3/ — Experiment 3: Fairness (competing flows)



Each experiment folder contains:

\- data/ — Raw CSV (CWND) and JSON (iperf3 output) files

\- plots/ — Generated figures/plots

\- scripts/ — Python plotting scripts



\## Experiments



\### Experiment 1: Cubic Favorable (RTT Sweep)

\- Fixed: 100 Mbps, 0% loss, 60s flows

\- Varied: RTT at 20ms, 100ms, 200ms

\- Additional test: 200ms with 7.5 MB buffer



\### Experiment 2: Cubic Unfavorable (Random Loss)

\- Fixed: 100 Mbps, 50ms RTT, 60s flows

\- Varied: Loss at 0.5%, 1%, 2%



\### Experiment 3: Fairness

\- 3A: 20ms RTT, 1 Reno + 1 Cubic flow (low BDP)

\- 3B: 200ms RTT, 1 Reno + 1 Cubic flow (high BDP)



\## References



\- Ha, Rhee, Xu (2008). CUBIC: A New TCP-Friendly High-Speed TCP Variant.

\- NYU Wireless Testbed Lab. TCP Congestion Control Basics.

