import numpy as np
import uhd
import time

def generate_and_transmit_noise(usrp, center_freq, bandwidth, tx_gain, segment_duration):
    # Generate random noise for a segment
    num_samples = int(bandwidth * segment_duration)
    noise_signal = np.random.normal(size=num_samples) + 1j * np.random.normal(size=num_samples)

    # Transmit noise segment
    usrp.send_waveform(noise_signal, segment_duration, center_freq)

def continuous_noise_transmission(center_freq, bandwidth, total_duration, tx_gain, segment_duration):
    usrp = uhd.usrp.MultiUSRP("type=b200")
    usrp.set_tx_rate(bandwidth)
    usrp.set_tx_freq(float(center_freq))
    usrp.set_tx_gain(tx_gain)

    end_time = time.time() + total_duration
    while time.time() < end_time:
        generate_and_transmit_noise(usrp, center_freq, bandwidth, tx_gain, segment_duration)

# Parameters
center_freq = 5935000000  # 5.935 GHz
bandwidth = 56e6  # 56 MHz
tx_gain = 20
total_duration = 5  # 5 seconds
segment_duration = 0.1  # 100 milliseconds

# Start continuous noise transmission
continuous_noise_transmission(center_freq, bandwidth, total_duration, tx_gain, segment_duration)
