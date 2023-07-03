from pyannote.audio import Pipeline
import os

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1", use_auth_token = "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")

fldr_path = '/home/anuprabha/spkr_diarisation/June_27/diar/audio_files/'

for file in os.listdir(fldr_path):
    if file.endswith(".wav"):

        nm = os.path.join(fldr_path + file)
        print(nm)
        diarization = pipeline(nm, num_speakers = 2)

        nm = os.path.splitext(nm)[0]
        rttm_file = nm + '.rttm'
        print(rttm_file)
        with open( rttm_file, "w") as rttm:
            diarization.write_rttm(rttm)




