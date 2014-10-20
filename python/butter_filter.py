from scipy.signal import butter, lfilter, lfilter_zi


def butter_lowpass(lowcut, fs, order=2):
    nyq = 0.5 * fs
    low = lowcut / nyq
    b, a = butter(order, low)
    return b, a


def butter_lowpass_filter(data, lowcut, fs, order=5):
    b, a = butter_lowpass(lowcut, fs, order=order)
    zi=lfilter_zi(b,a)
    y,zo = lfilter(b, a, data,zi=zi*data[0])
    return y
