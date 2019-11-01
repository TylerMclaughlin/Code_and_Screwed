import os
import subprocess
import numpy as np
from pydub import AudioSegment

# remove all spaces from file names
#cmd = '''for file in *.wav; do mv "$file" `echo $file | tr ' ' '_'` ; done'''

#subprocess.call(cmd, shell = True)

stem_parts = '''Adlibs_Stem.wav		FX_Stem.wav		Percussion_Stem.wav
BGV_1_Stem.wav		Guitars_Stem.wav	Pluck_Synth_Stem.wav
Claps_Stem.wav		Ld_Voc_Stem.wav		Synth_Stem.wav
Drum_Track_Stem.wav	Pads_Stem.wav		Whistle_Stem.wav'''.split()

tidal_parts = ''' dbv3 dbx dbp dbv2 dbg dbs1 dbc dbv1 dbs2 dbd dbpa dbw'''.split()


print(stem_parts)
print(tidal_parts)

# change to .duration_seconds
bpm = 87.5

ms_offset = 0 


# make sure wavs and tidal samples names have same length
assert len(stem_parts) == len(tidal_parts)
# make sure no duplicates in the wavs
assert len(stem_parts) == len(set(stem_parts))
# make sure no duplicates in the tidal parts 
assert len(tidal_parts) == len(set(tidal_parts))


wavs = []

for i, stem in enumerate(stem_parts):
    wavs.append(AudioSegment.from_wav(stem))

total_ms_song = 202971. #wavs[0].duration_seconds*1000.

ms_per_bar =  1./bpm*4*60*1000.

print(ms_per_bar)
print(total_ms_song)

bars= np.arange(ms_offset, total_ms_song + ms_per_bar, ms_per_bar) 

split_wavs_dir = "split_wavs"

if not os.path.exists(split_wavs_dir):
    os.makedirs(split_wavs_dir)


subwavs_per_bar = 4 

def write_subwav(audio, start, stop, part_name, number):
    # make a directory called "part_name" if it does not already exist
    subwav_dir = split_wavs_dir + '/' + part_name
    if not os.path.exists(subwav_dir):
        os.makedirs(subwav_dir)
    subwav = audio[start:stop]

    file_name = split_wavs_dir + '/' + part_name + '/' + str(number).zfill(3) + '.wav'
    #print(file_name)
    subwav.export(file_name, format="wav") #Exports to a wav file in the current path.

for i, stamp in enumerate(bars):
    if i == len(bars) -1:
        break
    len_bar = bars[i+1] - bars[i]
    # q is the length of the subwav
    q, r = divmod(len_bar, subwavs_per_bar)
    #print('the length of ' + part_name + ' is ' + str(q))
    print('bar number ' + str(i))
    for s in range(subwavs_per_bar):
        start = stamp + s*q
        stop = stamp + (s+1)*q  
        #print(start, stop)
        for index, wav in enumerate(wavs):
            write_subwav(audio = wav, start = start, stop = stop, part_name = tidal_parts[index], number = s+ i*subwavs_per_bar)

