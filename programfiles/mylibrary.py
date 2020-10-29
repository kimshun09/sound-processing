import wave
import numpy as np
import matplotlib.pyplot as plt

def read_wav(filename, fs=16000):
    w = wave.open(filename, 'r')
    buf = w.readframes(w.getnframes())
    data = np.frombuffer(buf, dtype='int16')
    x = np.linspace(0, len(data) // fs, num=len(data))
    return x, data

def save_wav(filename, data):
    data = data.astype(np.int16)
    w = wave.Wave_write(filename)
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(16000)
    w.writeframes(data)
    w.close()

def init_graph(xlabel='Time [s]', ylabel='Amplitude', xlim=None, ylim=None):
    plt.figure(num=None, figsize=(8, 4), dpi=80, facecolor='w', edgecolor='k')
    plt.clf()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if xlim != None:
        plt.xlim(xlim)
    if ylim != None:
        plt.ylim(ylim)
    plt.grid(True)

def get_logpowspct(y, fs=16000):
    fft = np.fft.fft(y)
    amp_spct = np.abs(fft)
    pow_spct = 20 * np.log10(amp_spct)
    x2 = np.linspace(0, fs, num=len(amp_spct))
    return x2, pow_spct

def hum(L):
    return 0.54 - 0.46 * np.cos(2 * np.pi * np.arange(L) / L)

def make_spct(filename, y, t, fs=16000, L=512, shift=128):
    hum = 0.54 - 0.46 * np.cos(2 * np.pi * np.arange(L) / L)

    list = []
    for s in range(0, len(y)-L, shift):
        yh = y[s: s + L] * hum
        fft = np.fft.fft(yh)
        pow_spct = 20 * np.log10(np.abs(fft))
        list.append(pow_spct)

    nplist = np.array(list)
    nplist = nplist.T

    fig = plt.figure(num=None, figsize=(8, 4), dpi=80, facecolor='w', edgecolor='k')
    fig.clf()
    ax1 = fig.add_subplot(1, 1, 1)
    xaxis = np.linspace(0, t, num=nplist.shape[1])
    yaxis = np.linspace(0, fs, num=nplist.shape[0])
    c = ax1.pcolorfast(xaxis, yaxis, nplist, cmap='jet', vmin=nplist.min(), vmax=nplist.max())
    ax1.axis([xaxis.min(), xaxis.max(), yaxis.min(), yaxis.max() // 2])
    # fig.colorbar(c, ax=ax1)
    plt.xlabel('Time [s]')
    plt.ylabel('Frequency [Hz]')
    fig.savefig(filename)
    fig.show()