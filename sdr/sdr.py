# SDR.PY
# A SAR System using SDR Radios


import numpy as np
import config
import sar_math
import uhd
import matplotlib.pylab as plt
from gnuradio import gr, analog



def build_signal(frequency, chirp_rate, pulse_duration):
    print("build_signal")
    t = np.linspace(0, pulse_duration, int(chirp_rate * pulse_duration), endpoint=False)
    signal = np.exp(1j * 2 * np.pi * frequency * t)
    return signal


def send_signal(signal, chirp_rate, tx_freq, tx_gain, tx_antenna, pulse_duration):
    print("send_signal")
    usrp = uhd.usrp.MultiUSRP("type=b200")
    usrp.set_tx_rate(chirp_rate)
    usrp.set_tx_freq(float(tx_freq))
    usrp.set_tx_gain(tx_gain)
    usrp.set_tx_antenna(tx_antenna)
    usrp.set_tx_subdev_spec(uhd.usrp.SubdevSpec("A:B"))
    
    usrp.send_waveform(signal, pulse_duration, tx_freq)
#    usrp.wait_send_metadata()


def receive_signal(rx_freq, rx_gain, rx_antenna, chirp_rate, pulse_duration):
    print("recieve_signal")
    usrp = uhd.usrp.MultiUSRP("type=b200")
    usrp.set_rx_rate(chirp_rate)
    usrp.set_rx_freq(float(rx_freq))
    usrp.set_rx_gain(rx_gain)
    usrp.set_rx_subdev_spec(uhd.usrp.SubdevSpec("A:B"))
    usrp.set_rx_antenna('TX/RX', 0)
    
    num_samples = int(chirp_rate * pulse_duration)
    samples = usrp.recv_num_samps(num_samples, rx_freq)
    return samples


def parse_signal(signal):
    print("parse_signal")
    processed_signal = signal  # Placeholder
    A=np.abs(processed_signal)
    Am=np.mean(A)
    As=np.std(np.abs(A))
    plt.figure(figsize=(4,4))
    plt.imshow(np.abs(A),cmap='gray',vmin=0,vmax=Am+As)
    plt.show()
    print(A)
    print(Am)
    print(As)
    return processed_signal


def main():
    # get Chirp Rate
    movement = 0
    while(True):
        cr = sar_math.calculate_chirp_rate(config.BW, config.PD)
        print("Chirp Rate is: ", cr)
        ssig = build_signal(config.CF, cr, config.PD)
        print("Signal is: ", ssig)
        send_signal(ssig, cr, config.CF, 20, config.TX_ANTENNA, config.PD)
        rsig = receive_signal(config.CF, 20, config.RX_ANTENNA, cr, config.PD)
        print("recieved signal: ", rsig)
        
        go = input("next signal? ")
        if go == "no":
            break
        movement += 1
        
    parse_signal(rsig)


main()
