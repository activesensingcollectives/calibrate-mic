Obtaining a sound-pressure-level (SPL) from non-calibration mics
================================================================
This module is useful when you have a sensitive mic (e.g. the SANKEN), and the calibration (e.g. GRAS) microphone isn't sensitive enough to pick up your signal.

*Warning* : While I suspect the SPL measurement written here works for any playback signal - for now it has only been tested with sweeps!

## The substitution method
Here we'll first use the 'substitution' method:
The idea is to record the playback first with the calibration mic (in a way that there's enough SNR), and then record the same playback (at the same distance, location etc.) with the sensitive microphone. The calibration mic gives you the sound-level spectrum in Pascals (because we have the 1 Pa calibration for reference). 

Knowing the sound-presure over all the frequency bands then allows you to calculate the sensitivity of the target microphone because we *know* the input (sound-pressure-level over each frequency band), and the resulting 'output' (rms at each frequency band). Dividing the two gives us the sensitivity --> rms/Pascal. 

## Matched-filtering is important
If you have the actual playback signal - then try to use it to matched filter and obtain only the direct path. 
Using the direct path generates 'smooth' sensitivity curves that don't need further processing.

## I have a microphone sensitivity - what now?
From the sensitivity curve, you can then go on to two things:

	1. Calculate the overall sound-pressure-level of the sound (e.g. RMS)
 
	2. Compensate for microphone frequency response (i.e. 'flatten' the target microphone audio)

As of this commit, this module only implements overall SPL calculation for now. 





April 2025, Code released with an MIT license
