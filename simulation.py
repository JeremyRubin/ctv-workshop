import numpy as np
import matplotlib.pyplot as plt
PHASES = 500
PHASE_LENGTH = 1
SAMPLES = PHASE_LENGTH * PHASES
AVG_TX = 235
MAX_BLOCK_SIZE = 1e6
AVG_INTERVAL = 10.0*60.0
TXNS_PER_SEC = 0.5*MAX_BLOCK_SIZE/AVG_TX/AVG_INTERVAL
COMPRESSABLE = 0.50
BRANCHING_FACTOR = 4.0
EXTRA_WORK_MULTIPLIER = 1/(1-1.0/BRANCHING_FACTOR)
DAYS = np.array(range(SAMPLES))/144.0
DAYS_OFFSET = PHASES/144.0*PHASE_LENGTH

def show_legend(for_):
    plt.legend(for_, [l.get_label() for l in for_], loc='upper left')
def generate_rates(phase):
    if phase >= 20:
        return TXNS_PER_SEC
    elif phase > 10:
        return 1.25**(20 - phase) *TXNS_PER_SEC
    elif phase >= 5:
        return 1.25**(phase-5)*TXNS_PER_SEC
    else:
        return TXNS_PER_SEC
rates = [generate_rates(phase) for phase in range(PHASES//2)] + [generate_rates(phase)*2 for phase in range(PHASES//2)]
def get_rate(phase):
    return rates[phase]
rates = [np.random.poisson(7) for _ in range(PHASES//4)]  + [np.random.poisson(14) for _ in range(PHASES//4)] + [np.random.poisson(3) for _ in range(PHASES//2)]
def get_rate(phase):
    return rates[phase]

plt.subplot(3,1,1)
p = 100*COMPRESSABLE
plt.title("Transaction Compression Performance with %d%% Adoption During 2 Spikes"%p)
plt.ylabel("Txn/s")

p_full_block, = plt.plot([DAYS[0], DAYS[-1]],
        [MAX_BLOCK_SIZE/AVG_TX/AVG_INTERVAL]*2,
         label="Maximum Average Transactions Per Second")
T = np.array(range(0, SAMPLES, PHASE_LENGTH))/144.0
p5, = plt.plot(T, rates, "k-", label="Transactions Per Second")
show_legend([p5, p_full_block])
def compressed(compressable = COMPRESSABLE):
    backlog = 0
    postponed_backlog = 0
	# reserve space for results
    results_confirmed = [0]*SAMPLES
    results_unconfirmed = [0]*SAMPLES
    results_yet_to_spend = [0]*SAMPLES
    total_time = [0]*(SAMPLES)
    for phase in range(PHASES):
        for sample_idx in range(PHASE_LENGTH*phase, PHASE_LENGTH*(1+phase)):
			# Sample how much time until the next block
            total_time[sample_idx] = np.random.exponential(AVG_INTERVAL)
			# Random sample a number of transactions that occur in this block time period
            # Equivalent to the sum of one poisson per block time
            # I.E., \sum_1_n Pois(a) = Pois(a*n)
            txns = np.random.poisson(get_rate(phase)*total_time[sample_idx])
            postponed = txns * compressable
			# Add the non postponed transactions to the backlog as the available weight
            weight = (txns-postponed)*AVG_TX + backlog
			# Add the postponed to the postponed_backlog
            postponed_backlog += postponed*AVG_TX * EXTRA_WORK_MULTIPLIER # Total extra work

			# If we have more weight available than block space
            if weight > MAX_BLOCK_SIZE:
				# clear what we can -- 1 MAX_BLOCK_SIZE
                results_confirmed[sample_idx] += MAX_BLOCK_SIZE
                backlog = weight - MAX_BLOCK_SIZE
            else:
				# Otherwise, we have some space to spare for postponed backlog
                space = MAX_BLOCK_SIZE - weight
                postponed_backlog = max(postponed_backlog-space, 0)
                backlog = 0
			# record results in terms of transactions
            results_unconfirmed[sample_idx] = float(backlog)/AVG_TX
            results_yet_to_spend[sample_idx] = postponed_backlog/EXTRA_WORK_MULTIPLIER/AVG_TX

    return results_unconfirmed, results_yet_to_spend, np.cumsum(total_time)/(60*60*24.0)
compressed_txs, unspendable, blocktimes_c = compressed()
def normal():
    a,_,b = compressed(0)
    return a,b
normal_txs, blocktimes_n = normal()

plt.subplot(3,1,2)
plt.ylabel("Pending Txns")
p7, = plt.plot(blocktimes_c, unspendable,
			   label="Confirmed Congestion Control Pending")
show_legend([p7])

plt.subplot(3,1,3)
plt.ylabel("Mempool Txns")
p1, = plt.plot(blocktimes_n, normal_txs,
			   label="Unconfirmed Mempool without Congestion Control")
p3, = plt.plot(blocktimes_c, compressed_txs,
			   label="Unconfirmed Mempool with Congestion Control")
show_legend([p1, p3])

plt.xlabel("Block Days")
plt.savefig('simulation-%f-random.png'%COMPRESSABLE, dpi=300)

