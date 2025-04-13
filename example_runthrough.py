# -*- coding: utf-8 -*-
"""
Example run-through
===================
This IS NOT a complete run-through. The follow things need to implemented by the user
    * playback signal segmentation 
    * bandpass filtering / other cleaning
    * matched-filtering to remove reflections

Other things to remember
------------------------
The GRAS microphone and target microphone may or may not be recorded with the same
analog-digital-converter!! Be Very Aware of this while comparing the sensitivities 
between the two microphones!!

Experimental notes
------------------
* Remember to write down all the GAIN values in dB for every recording you make.

WARNING
-------
As of APRIL 2025 -  this is a prototype module only. 
See below for the steps you need to take to ensure everything makes sense.


Always double-check with a 'validation' signal
----------------------------------------------
Test your calibration outcomes with a second signal that wasn't used anywhere before
and also recorded by both the GRAs and target mic. 

Created on Sat Apr 12 07:35:50 2025

@author: theja
"""
import numpy as np 
import soundfile as sf
import matplotlib.pyplot as plt 
from utilities import *

#%%
# Load the substitution-calibration audio (calibration and target mic)
fs = sf.info('GRAS_playback_240819_0330.wav').samplerate
gras_pbk_audio, fs = sf.read('GRAS_playback_240819_0330.wav',
                         start=int(fs*16.870), stop=int(fs*16.874))
sennheiser_pbk_audio, fs = sf.read('SennheiserMKE_240819_0325.wav',
                               start=int(fs*14.593),  stop=int(fs*14.597))
sennheiser_pbk_audio = sennheiser_pbk_audio[:,0]
gras_pbk_audio = gras_pbk_audio[:,0]

# Load the 1 Pa reference tone 
gras_1Pa_tone, fs = sf.read('GRAS_1Pa_240819_0331.wav', start=int(fs*0.5),
                        stop=int(fs*1.5))
gras_1Pa_tone = gras_1Pa_tone[:,0]

# Gain compensate the audio (e.g. un-gain them all) to bring them to the 'same' 
# baseline level - not relevant for Ro-BAT
gras_pbk_gain = 56 # dB
gras_tone_gain = 36 
sennheiser_gain = 36 

gras_1Pa_tone *= db_to_linear(-gras_tone_gain)
gras_pbk_audio *= db_to_linear(-gras_pbk_gain)
sennheiser_pbk_audio *= db_to_linear(-sennheiser_gain)

#%%
# Do any bandpass filtering/cleaning here
raise NotImplementedError('Bandpass or audio cleaning steps not implemented')

#%%
# REMEMBER TO SEGMENT playback signal from calibration and target mic HERE -- THIS IS NOTT IMPLEMENTED!
raise NotImplementedError('Remember to segment your sound here - you should have ideally nothing else but your playback sound')

#%%
# REMEMBER TO MATCH-FILTER (NOT IMPLEMENTED HERE) and extract only the direct path
raise NotImplementedError('Matched filtering not implemented here - implement please')

#%%
# Check the SNR at the spectral level - use a silent audio clip from the above recordings
# to be sure that your measurements mean something useful. Remember garbage in, garbage out.

raise NotImplementedError('Check your SNR from the ambient sound!')
# snr_target = dB(bandwise_tgtmic/tgt_silence_bandwise)
# snr_gras = dB(bandwise_grasmic/gras_silence_bandwise)



#%%
# Calibration mic: Calculate the rms_Pascal of the 1 Pa calibration tone
rms_1Pa_tone = rms(gras_1Pa_tone)
print(f'The calibration mic has a sensitivity of {np.round(rms_1Pa_tone,3)}rms/Pa. RMS relevant only for this ADC!')

# Now measure mic RMS over all frequency bands
gras_centrefreqs, gras_freqrms = calc_native_freqwise_rms(gras_pbk_audio, fs)
# Convert from RMS to Pascals (rms equivalent) since we know the GRAS sensitivity
gras_freqParms = gras_freqrms/rms_1Pa_tone # now the levels of each freq band in Pa_rms
plt.figure()
a0 = plt.subplot(211)
plt.plot(gras_centrefreqs, gras_freqParms)
plt.ylabel('Pressure_rmseqv., Pa', fontsize=12)
plt.subplot(212, sharex=a0)
plt.plot(gras_centrefreqs, pascal_to_dbspl(gras_freqParms))
plt.xlabel('Frequencies, Hz', fontsize=12);
plt.ylabel('Sound pressure level,\n dBrms SPL re 20$\mu$Pa', fontsize=12)
plt.title('GRAS mic recording of playback')
#%%
# Target microphone. Here we'll cover the case where we only get an RMS/Pa
# sensitivity. The other option is to calculate a mV/Pa sensitivity - which allows
# you to use the mic aross different ADCs - but also needs more info on the ADC specs

sennheiser_centrefreqs, sennheiser_freqrms = calc_native_freqwise_rms(sennheiser_pbk_audio, fs)
plt.figure()
plt.title('Sennheiser mic recording of playback')
a0 = plt.subplot(211)
plt.plot(sennheiser_centrefreqs, sennheiser_freqrms)
plt.ylabel('Pressure_rmseqv., Pa', fontsize=12)

plt.subplot(212, sharex=a0)
plt.plot(sennheiser_centrefreqs, dB(sennheiser_freqrms))
plt.xlabel('Frequencies, Hz', fontsize=12);
plt.ylabel('dBrms a.u.', fontsize=12)


#%%
# Now let's calculate the RMS/Pa sensitivity using the knowledge from the 
# calibration mic
sennheiser_sensitivity = np.array(sennheiser_freqrms)/np.array(gras_freqParms)

plt.figure()
a0 = plt.subplot(211)
plt.plot(sennheiser_centrefreqs, sennheiser_sensitivity)
plt.ylabel('a.u. RMS/Pa', fontsize=12)
plt.subplot(212, sharex=a0)
plt.plot(sennheiser_centrefreqs, dB(sennheiser_sensitivity))
plt.xlabel('Frequencies, Hz', fontsize=12);
plt.ylabel('dB a.u. rms/Pa', fontsize=12)
plt.ylim(-60,-10)

#%% 
# We now have the target mic sensitivity - how do we use it to calculate the
# actual dB SPL? 

# Here we load a separate 'recorded sound' 
recorded_sound, fs = sf.read('SennheiserMKE_240819_0325.wav',
                             start=int(fs*15.002), stop=int(fs*15.01))
recorded_sound = recorded_sound[:,0]
recorded_sound *= db_to_linear(-sennheiser_gain)


gras_rec, fs = sf.read('GRAS_playback_240819_0330.wav',
                         start=int(fs*17.278), stop=int(fs*17.286))
gras_rec = gras_rec[:,0]
gras_rec *= db_to_linear(-gras_pbk_gain)



#%% And finally let's check that the Sennheiser calibration makes sense
# using a sound that we didn't use to calculate the sensitivity
# If the length of the recorded target mic audio here is not the same as the calibration audio. 
#  then you'll need to interpolate the microphone sensitivity using interpolate_freq_response in the
# utilities.py module
recsound_centrefreqs, freqwise_rms = calc_native_freqwise_rms(recorded_sound, fs)
interp_sensitivity = interpolate_freq_response([sennheiser_centrefreqs, sennheiser_sensitivity],
                          recsound_centrefreqs)
freqwise_Parms = freqwise_rms/interp_sensitivity # go from rms to Pa(rmseq.)
freqwiese_dbspl = pascal_to_dbspl(freqwise_Parms)


gras_centrefreqs, gras_freqrms = calc_native_freqwise_rms(gras_rec, fs)
gras_Pa = gras_freqrms/rms_1Pa_tone
gras_dbspl = pascal_to_dbspl(gras_Pa)

plt.figure()
plt.plot(gras_dbspl, label='gras')
plt.plot(freqwiese_dbspl, label='sennheiser')
plt.legend()
#%%
# Now we know the sensitivity of the target mic - let's finally calculate
# the dB SPL of the recorded sound!
# We rely on combining the Pa rms of all relevant frequencies 
# e.g. see https://electronics.stackexchange.com/questions/642109/summing-rms-values-proof

frequency_band = [0.2e3, 15e3] # min, max frequency to do the compensation Hz

# Choose to calculate the dB SPL only for the frequency range of interest.
# Target mic
tgtmic_relevant_freqs = np.logical_and(recsound_centrefreqs>=frequency_band[0],
                                recsound_centrefreqs<=frequency_band[1])
total_rms_freqwise_Parms = np.sqrt(np.sum(freqwise_Parms[tgtmic_relevant_freqs]**2))

# Ground truth GRAS mic audio of the same sound
gras_relevant_freqs = np.logical_and(gras_centrefreqs>=frequency_band[0],
                                gras_centrefreqs<=frequency_band[1])
# This is one way to do it - use the RAW audio, and calculate its rms
# since we the overall flat sensitivity of the GRAS
gras_overallaudio_Parms = rms(gras_rec)/rms_1Pa_tone
# This is the other way to do it - like we did for the Sennheiser
gras_totalrms_Parms = np.sqrt(np.sum(gras_Pa[gras_relevant_freqs]**2))

print(f'GRAS dBrms SPL measures:{pascal_to_dbspl(gras_overallaudio_Parms)}, {pascal_to_dbspl(gras_totalrms_Parms)}')
print(f'Sennheiser dBrms SPL measure: {pascal_to_dbspl(total_rms_freqwise_Parms)}')


