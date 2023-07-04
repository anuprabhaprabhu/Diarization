import scipy.io
import numpy as np
import os
import pydub 
from pydub import AudioSegment

#####################
#   Please pay attention to : 
#   1. fs
#   2. split / ramp
#####################


split = 0     # split =1 ,ramp =0

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
            wav_path = os.path.join(speaker_dir, f"{speaker}_{ind}.wav")
            scipy.io.wavfile.write(wav_path, fs, segment)
            wav_data[speaker].append(segment)


def ramp_samp(name):

    #### read files from spkr_splt folders #######
    speaker = ['SPEAKER_00', 'SPEAKER_01']
    for i in speaker:
        merge_data=[]
        split_dir = os.path.join(name+'_splt', i+'/')
        seg_dir = os.path.join(name+'_ramp',f"{i+'/'}")

        #########  create seg_dir for different speakers  #######
        if not os.path.isdir(seg_dir):
            os.mkdir(seg_dir)

        for entry in os.listdir(split_dir):
            ##### open file and read   #####
            split_dir_path = os.path.join(split_dir + entry)
            seg_path = os.path.join(seg_dir, f"{entry}")
            with open(split_dir_path, 'r') as f:
                ##### ramp up and down  ###3
                seg = AudioSegment.from_file(split_dir_path ) 
                seg = seg.fade_in(10)
                seg = seg.fade_out(10)
                
                seg_samples = seg.get_array_of_samples()
                seg.export(seg_path, format="wav")
                merge_data.append(seg_samples)
                
        #### to merge  ####
        merge_data = np.hstack(merge_data)
        wav_path = os.path.join(seg_dir, f"{i}_total.wav")
        scipy.io.wavfile.write(wav_path, fs, merge_data)
        #### ffmpeg conversion 
        wav_path2 = os.path.join(seg_dir, f"{i}_total_ff.wav")
        os.system(f"ffmpeg -hide_banner -loglevel error -i {wav_path} -c:a pcm_alaw {wav_path2}")
 

####################################

#######  main     #######
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
            print('fs',fs)
            #####   splits spkr parts and creats folder & merge ######
            split_audio(spkr_data, nm)
            print(f'Completed speaker splits on {file} ....')

        else:
            fs = 8000
            #####    ramp up and down   ########
            ramp_samp(nm)
            print(f'Completed ramp up and ramp down on {file}')