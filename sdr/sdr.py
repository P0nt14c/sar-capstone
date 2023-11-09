# SDR.PY
# A SAR System using SDR Radios


import numpy as np
import config
import sar_math
from gnuradio import gr, analog



def build_signal(frequency, chirp_rate, pulse_duration):
    t = np.linspace(0, pulse_duration, int(chirp_rate * pulse_duration), endpoint=False)
    signal = np.exp(1j * 2 * np.pi * frequency * t)
    return signal


def send_signal(signal, chirp_rate, tx_freq, tx_gain, tx_antenna):
    usrp = uhd.usrp.MultiUSRP("type=b200")
    usrp.set_tx_rate(chirp_rate)
    usrp.set_tx_freq(tx_freq)
    usrp.set_tx_gain(tx_gain)
    usrp.set_tx_antenna(tx_antenna)
    usrp.set_tx_subdev_spec("A:0")
    
    usrp.send(signal, metadata=False)
    usrp.wait_send_metadata()


def receive_signal(rx_freq, rx_gain, rx_antenna, chirp_rate, pulse_duration):
    usrp = uhd.usrp.MultiUSRP("type=b200")
    usrp.set_rx_rate(chirp_rate)
    usrp.set_rx_freq(rx_freq)
    usrp.set_rx_gain(rx_gain)
    usrp.set_rx_antenna(rx_antenna)
    usrp.set_rx_subdev_spec("A:0")
    
    num_samples = int(chirp_rate * pulse_duration)
    samples = usrp.recv(num_samples, metadata=False)
    return samples


def parse_signal(signal):
    processed_signal = signal  # Placeholder
    return processed_signal


def main():
    # get Chirp Rate
    cr = sar_math.calculate_chirp_rate(config.BW, config.PD)
    sig = build_signal(config.CF, cr, config.PD)
    send_signal(sig)
    receive_signal()
    parse_signal()