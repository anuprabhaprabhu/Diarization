import scipy.io
import numpy as np
import os
import pydub 
from pydub import AudioSegment

file_path = "june30.rttm"

with open(file_path, 'r') as f:
    lines = f.readlines()

speaker_data = {}

for line in lines:
    line = line.split()
    st_time, duration, speaker = float(line[3]), float(line[4]), line[7]
    if not speaker in speaker_data:
        speaker_data[speaker] = []
    speaker_data[speaker].append((st_time, st_time + duration))

file_path = "june30.wav"
out_dir = "ndata"
out_dir_1 = 'ramp'

if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

if not os.path.isdir(out_dir_1):
    os.mkdir(out_dir_1)   

fs, wav = scipy.io.wavfile.read(file_path)
print(fs, wav, wav.shape[0] / fs, wav.shape)

wav_data = {}

for speaker in speaker_data:
    print(speaker)
    wav_data[speaker] = []
    speaker_dir = os.path.join(out_dir, speaker)
    seg_dir = os.path.join(out_dir_1, speaker)
    os.mkdir(speaker_dir)
    os.mkdir(seg_dir)
    for ind, (st_time, end_time) in enumerate(speaker_data[speaker]):
        st_time, end_time = int(st_time * fs), int(end_time * fs)
        segment = wav[st_time: end_time]
        # # ramp up
        # segment = AudioSegment.from_file(segment)
        # segment = segment.fade_in(1000)
        # #ramp down
        # segment = segment.fade_out(1000)
        # #save
        # wav_data[speaker].append(segment)
        wav_path = os.path.join(speaker_dir, f"{speaker}_{ind}.wav")
        scipy.io.wavfile.write(wav_path, fs, segment)
        print('wav_path',wav_path)
        
        seg = AudioSegment.from_file(wav_path,  format="wav")
        seg = seg.fade_in(10)
        seg = seg.fade_out(10)

        seg_path = os.path.join(seg_dir, f"{speaker}_{ind}.wav")
        seg_samples = seg.get_array_of_samples()
        print('seg_path',seg_path)
        print('type of seg',type(seg))
        print(' type seg_samples',type(seg_samples))
      
        seg.export(seg_path, format="wav")
        wav_data[speaker].append(seg_samples)
        
        
   

    wav_data[speaker] = np.hstack(wav_data[speaker])
    wav_path = os.path.join(speaker_dir, f"{speaker}_total.wav")
    scipy.io.wavfile.write(wav_path, fs, wav_data[speaker])
    wav_path2 = os.path.join(out_dir, f"{speaker}.wav")
    os.system(f"ffmpeg -hide_banner -loglevel error -i {wav_path} -c:a pcm_alaw {wav_path2}")
