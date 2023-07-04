import scipy.io
import numpy as np
import os
import pydub 
from pydub import AudioSegment



#### split / ramp 

split = 1
# ramp = 0

#### folder path

fldr_path = '/home/anuprabha/spkr_diarisation/June_27/diar/audio_files/'



def read_rttm(path):

    ### speakers split
    with open(path, 'r') as f:
        lines = f.readlines()

    speaker_data = {}
    for line in lines:
        line = line.split()
        st_time, duration, speaker = float(line[3]), float(line[4]), line[7]
        if not speaker in speaker_data:
            speaker_data[speaker] = []
        speaker_data[speaker].append((st_time, st_time + duration))
    return speaker_data    

def create_fldr(name):
    if not os.path.isdir(name+'_splt'):
        os.mkdir(name+'_splt')

    if not os.path.isdir(name+'_ramp'):
        os.mkdir(name+'_ramp')  


def split_audio(data, name):
    wav_data = {}
    for speaker in data:
        wav_data[speaker] = []
        speaker_dir = os.path.join(name+'_splt', speaker)

        if not os.path.isdir(speaker_dir):
            os.mkdir(speaker_dir)
        
        for ind, (st_time, end_time) in enumerate(data[speaker]):
            st_time, end_time = int(st_time * fs), int(end_time * fs)
            segment = wav[st_time: end_time]
            wav_path = os.path.join(speaker_dir, f"{spkr}_{ind}.wav")
            scipy.io.wavfile.write(wav_path, fs, segment)
            print('wav_path',wav_path)
            wav_data[speaker].append(segment)

    

#######  

def ramp_samp(data, name):
    wav_data = {}
    for speaker in data:
        wav_data[speaker] = []
        speaker_dir = os.path.join(name+'_ramp', speaker)

        if not os.path.isdir(speaker_dir):
            os.mkdir(speaker_dir)
        
        for ind, (st_time, end_time) in enumerate(data[speaker]):
            st_time, end_time = int(st_time * fs), int(end_time * fs)
            segment = wav[st_time: end_time]
            wav_path = os.path.join(speaker_dir, f"{spkr}_{ind}.wav")
            scipy.io.wavfile.write(wav_path, fs, segment)
            print('wav_path',wav_path)
            wav_data[speaker].append(segment)

    wav_data[speaker] = np.hstack(wav_data[speaker])
    wav_path = os.path.join(speaker_dir, f"{speaker}_total.wav")
    scipy.io.wavfile.write(wav_path, fs, wav_data[speaker])
    wav_path2 = os.path.join(out_dir, f"{speaker}.wav")
    os.system(f"ffmpeg -hide_banner -loglevel error -i {wav_path} -c:a pcm_alaw {wav_path2}")
    #### to merge  ####

    # wav_data[speaker] = np.hstack(wav_data[speaker])
    # wav_path = os.path.join(speaker_dir, f"{speaker}_total.wav")
    # scipy.io.wavfile.write(wav_path, fs, wav_data[speaker])
    # wav_path2 = os.path.join(out_dir, f"{speaker}.wav")
    # os.system(f"ffmpeg -hide_banner -loglevel error -i {wav_path} -c:a pcm_alaw {wav_path2}")
    print('Completed ramp up  and ramp down')

####################################

######  Read rttm files ######
#######  main +++++++++ 
for file in os.listdir(fldr_path):
    if file.endswith(".rttm"):
        print(file)
        file_path = os.path.join(fldr_path + file)

        ##### create folders #####
        nm = os.path.splitext(file_path)[0]
        create_fldr(nm)
                
        ### read rttm file #####
        spkr_data = read_rttm(file_path)
        
        if split == 1:
            #####  read audio   #######
            fs, wav = scipy.io.wavfile.read(nm+'.wav')
            # print(fs, wav, wav.shape[0] / fs, wav.shape)

            #####   splits spkr parts and creats folder & merge ######
            split_audio(spkr_data, nm)
            print('Completed speaker splits....')

        else:
            #####    ramp up and down   ########
            # ramp_samp()
            print('write for ramp!!!!!!!!!!!!')