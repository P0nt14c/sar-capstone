import numpy as np
import uhd

def generate_noise_segment(center_freq, bandwidth, segment_duration, tx_gain, usrp):
    # Generate random noise for a segment
    num_samples = int(bandwidth * segment_duration)
    noise_signal = np.random.normal(size=num_samples) + 1j * np.random.normal(size=num_samples)

    # Transmit noise segment
    usrp.send_waveform(noise_signal, segment_duration, center_freq)

def generate_continuous_noise(center_freq, bandwidth, total_duration, tx_gain):
    usrp = uhd.usrp.MultiUSRP("type=b200")
    usrp.set_tx_rate(bandwidth)
    usrp.set_tx_freq(float(center_freq))
    usrp.set_tx_gain(tx_gain)

    segment_duration = 0.1  # Duration of each noise segment in seconds
    num_segments = int(total_duration / segment_duration)

    for _ in range(num_segments):
        generate_noise_segment(center_freq, bandwidth, segment_duration, tx_gain, usrp)

# Example call for 5 seconds of noise jamming
generate_continuous_noise(5935000000, 56, 5, 20)
