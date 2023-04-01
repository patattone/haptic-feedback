import numpy as np # useful library that does fancy math and matrix stuff
import simpleaudio as sa # audio input/output library!!
import keyboard

def createSignal(frequency: float, duration : float):
    '''
    Creates the signal with the given frequency in hertz
    and the given length in seconds and returns it as a numpy array
    '''

    assert frequency > 0, f"frequency should be greater than zero, it is {frequency}"
    assert duration > 0, f"duration should be greater than zero, it is {duration}"

    # calculate note frequencies
    freq = frequency # Hz
    T = duration # seconds
    sample_rate = 44100  # sample rate for the wave that we are going to generate for our signal

    t = np.linspace(0, T, int(T * sample_rate), False)

    signal = np.sin(freq * t * 2 * np.pi) # generate sine wave at the given frequency for the desired duration

    # normalize the signal 
    signal *= 32767 / np.max(np.abs(signal)) 
    # convert to 16-bit data
    signal = signal.astype(np.int16) # necessary for audio data to be processed as audio data
    return signal


def createComplexSignal(freqs: list, durations: list):
    """
    Create a more complicated signal using two lists that specify the signal characteristics.
    The frequencies will be played in the order they appear in the list.
    The first list determines the frequencies and the second list determines the duration for each frequency.
    The length of the two lists must be equal since there is a one to one correspondence between each entry.
    """

    assert len(freqs) == len(durations), f"The two inputs are not equal. freqs has length {len(freqs)} and durations as length {(len(durations))}"

    signals = []
    for freq, T in zip(freqs, durations): # loop through each of the lists simultaneously (freq is from the first, T is from the second)
        signal = createSignal(freq, T) # create a signal
        signals.append(signal) # add it to our list

    audio = np.hstack(signals) # combine the signals into a single object so that we can play them sequentially.
    return audio



def playSignal(signal : np.array):
    '''
    Given the signal, play it on the default audio channel
    '''

    assert signal.dtype == np.int16, f"the data type for the signal should be int16, it is {signal.dtype}"

    # Nyquist sampling rate for our ears 44000 Hz since the maximum frequency we can discern is 22000 Hz
    sample_rate = 44100

    # start playback, we are playing 16bit audio with single channel output
    play_obj = sa.play_buffer(signal, 1, 2, sample_rate) # play audio data!

    # wait for playback to finish before exiting
    play_obj.wait_done()


if __name__ == "__main__": # example of how to run this code
    A_freq = 440 # Hz
    T = 0.1 # seconds

    audio = createSignal(A_freq, T) # create signal here
    playSignal(audio)

    playSignal(createSignal(0.01, 2)) # play nothing (a very low signal) for 2 seconds

    Csh_freq = A_freq * 2 ** (4 / 12) # Hz (note ** is the exponent operator)
    E_freq = A_freq * 2 ** (7 / 12) # Hz

    freqs     = [A_freq, Csh_freq, E_freq] # the chosen frequencies
    durations = [0.5, 2.0, 3.0] # durations for each frequency

    audio = createComplexSignal(freqs, durations)
    playSignal(audio)

