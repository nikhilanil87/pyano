import argparse
import array
from collections import Counter

import numpy as np
import scipy
from pydub import AudioSegment
from pydub.utils import get_array_type

# ----------------------------------------------------------
# Note frequencies (only one octave, will fold all into this)
# ----------------------------------------------------------
NOTES = {
    "A": 440,
    "A#": 466.1637615180899,
    "B": 493.8833012561241,
    "C": 523.2511306011972,
    "C#": 554.3652619537442,
    "D": 587.3295358348151,
    "D#": 622.2539674441618,
    "E": 659.2551138257398,
    "F": 698.4564628660078,
    "F#": 739.9888454232688,
    "G": 783.9908719634985,
    "G#": 830.6093951598903,
}


# ----------------------------------------------------------
# FFT frequency spectrum
# ----------------------------------------------------------
def frequency_spectrum(sample, max_frequency=800):
    bit_depth = sample.sample_width * 8
    array_type = get_array_type(bit_depth)
    raw_audio_data = array.array(array_type, sample._data)
    n = len(raw_audio_data)

    freq_array = np.arange(n) * (float(sample.frame_rate) / n)
    freq_array = freq_array[: (n // 2)]

    raw_audio_data = raw_audio_data - np.average(raw_audio_data)
    freq_magnitude = scipy.fft(raw_audio_data)
    freq_magnitude = freq_magnitude[: (n // 2)]

    if max_frequency:
        max_index = int(max_frequency * n / sample.frame_rate) + 1
        freq_array = freq_array[:max_index]
        freq_magnitude = freq_magnitude[:max_index]

    freq_magnitude = abs(freq_magnitude)
    freq_magnitude = freq_magnitude / np.sum(freq_magnitude)
    return freq_array, freq_magnitude


# ----------------------------------------------------------
# Note classification
# ----------------------------------------------------------
def classify_note_attempt_3(freq_array, freq_magnitude):
    min_freq = 82
    note_counter = Counter()
    for i in range(len(freq_magnitude)):
        if freq_magnitude[i] < 0.01:
            continue

        for freq_multiplier, credit_multiplier in [
            (1, 1),
            (1 / 3, 3 / 4),
            (1 / 5, 1 / 2),
            (1 / 6, 1 / 2),
            (1 / 7, 1 / 2),
        ]:
            freq = freq_array[i] * freq_multiplier
            if freq < min_freq:
                continue
            note = get_note_for_freq(freq)
            if note:
                note_counter[note] += freq_magnitude[i] * credit_multiplier

    if len(note_counter) == 0:
        return None
    return note_counter.most_common(1)[0][0]


def get_note_for_freq(f, tolerance=33):
    tolerance_multiplier = 2 ** (tolerance / 1200)
    note_ranges = {
        k: (v / tolerance_multiplier, v * tolerance_multiplier) for (k, v) in NOTES.items()
    }

    range_min = note_ranges["A"][0]
    range_max = note_ranges["G#"][1]
    if f < range_min:
        while f < range_min:
            f *= 2
    else:
        while f > range_max:
            f /= 2

    for (note, note_range) in note_ranges.items():
        if f > note_range[0] and f < note_range[1]:
            return note
    return None


# ----------------------------------------------------------
# Detect note starts
# ----------------------------------------------------------
def predict_note_starts(song):
    SEGMENT_MS = 50
    VOLUME_THRESHOLD = -35
    EDGE_THRESHOLD = 5
    MIN_MS_BETWEEN = 100

    song = song.high_pass_filter(80)  # fixed: removed 'order'
    volume = [segment.dBFS for segment in song[::SEGMENT_MS]]

    predicted_starts = []
    for i in range(1, len(volume)):
        if volume[i] > VOLUME_THRESHOLD and volume[i] - volume[i - 1] > EDGE_THRESHOLD:
            ms = i * SEGMENT_MS
            if len(predicted_starts) == 0 or ms - predicted_starts[-1] >= MIN_MS_BETWEEN:
                predicted_starts.append(ms)
    return predicted_starts


# ----------------------------------------------------------
# Predict notes for each detected start
# ----------------------------------------------------------
def predict_notes(song, starts):
    results = []
    for i, start in enumerate(starts):
        sample_from = start + 50
        sample_to = start + 550
        if i < len(starts) - 1:
            sample_to = min(starts[i + 1], sample_to)
        segment = song[sample_from:sample_to]
        freqs, freq_magnitudes = frequency_spectrum(segment)
        predicted = classify_note_attempt_3(freqs, freq_magnitudes) or "U"
        results.append((start / 1000.0, predicted))  # seconds + note
    return results


# ----------------------------------------------------------
# Main
# ----------------------------------------------------------
def main(file):
    song = AudioSegment.from_file(file)
    song = song.high_pass_filter(80)  # fixed: removed 'order'

    starts = predict_note_starts(song)
    notes = predict_notes(song, starts)

    for t, n in notes:
        print(f"{t:.2f}s: {n}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Input .wav file")
    args = parser.parse_args()
    main(args.file)
