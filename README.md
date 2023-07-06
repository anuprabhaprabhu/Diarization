#####           SPEAKER DIARIZATION         ######


step 1 : ".wav"  convertion

		ffmpeg -i Zaid.mpga -acodec pcm_alaw -sample_fmt s16 -ar 8000 Zaid.wav


step 2 : generate ".rttm" (takes time)

		use "diar.py"


step 3 : split speakers 

		use "split_ramp.py" --> set split=1, creates speaker_00 & speaker_01 folders in ***_split folder

		manually check for overlaps, noise etc., and discard files if necessary.


step 4 : Ramp up and down

		use "split_ramp.py" --> set split=0, creates speaker_00 & speaker_01 folders in ***_ramp folder

		and also creates "speaker_00_total.wav" and "speaker_00_total_ff.wav" 
		
step 5 : Final check

		soxi speaker_00_total_ff.wav   --> check for A-law, 8k etc.,

		check for ramp up and down(transients should not be there).
