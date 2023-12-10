# SDR.PY
# A SAR System using SDR Radios


import numpy as np
import config
import sar_math
import uhd
import matplotlib.pylab as plt
from gnuradio import gr, analog

noise_p = 0
signal_p = 0
recieved_p = 0

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
    print(":\n", A)
    plt.imshow(np.abs(A),cmap='gray',vmin=0,vmax=Am+As)
    plt.show()
    print(A)
    print(min(A[0]))
    print(max(A[0]))
    pass

def calculate_complex_power(signal):
    """Calculate the power of a complex signal."""
    power = np.mean(np.abs(signal)**2)
    return power

def calculate_snr(signal, noise):
    """Calculate the Signal to Noise Ratio (SNR)."""
    signal_power = calculate_complex_power(signal)
    noise_power = calculate_complex_power(noise)
    snr = 10 * np.log10(signal_power / noise_power)
    return snr

def main():
    # get Chirp Rate
    sig = []
    for i in range(28):
        cr = sar_math.calculate_chirp_rate(config.BW, config.PD)
        #print("Chirp Rate is: ", cr)
        ssig = build_signal(config.CF, cr, config.PD)
        #print("Signal is: ", ssig)
        noise = receive_signal(config.CF, 20, config.RX_ANTENNA, cr, config.PD)
        noise_p = calculate_complex_power(noise[0])
        print("Noise power: " + str(noise_p))
        send_signal(ssig, cr, config.CF, 20, config.TX_ANTENNA, config.PD)
        rsig = receive_signal(config.CF, 20, config.RX_ANTENNA, cr, config.PD)
        #print("recieved signal: ", rsig)
        magnitudes = np.abs(rsig[0])
        power = magnitudes ** 2
        peak_power = np.max(power)
        print('peak power: ' + str(peak_power))
        shape = np.shape(rsig)
        shape_0 = np.shape(rsig[0])
        #print("shape:", shape)
        #print("shape_0:", shape_0)
        #print("rsig[0]\n:", rsig[0])
        #print("rsig[0][0]\n:", rsig[0][0])
        #print("[rsig[0], rsig[0]]:\n", [rsig[0], rsig[0]])
        sig.append(rsig[0])
        #sig[1] = rsig[0]
        print("this is sig:\n", sig)
        print("SNR: " + str((peak_power-noise_p)/noise_p))
        
        go = input("next signal? ")
        if go == "no":
            break
        
    
    sig_real = np.ndarray((len(sig),56),dtype=np.complex64)
    for i in range(len(sig)):
        sig_real[i] = sig[i]
    print(sig)
    parse_signal(sig_real)


main()
