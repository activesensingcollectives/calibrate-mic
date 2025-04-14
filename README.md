Obtaining a sound-pressure-level (SPL) from non-calibration mics
================================================================
This module is useful when you have a sensitive mic (e.g. the SANKEN), and the calibration (e.g. GRAS) microphone isn't sensitive enough to pick up your signal.

*Warning 1* : While I suspect the SPL measurement written here works for any playback signal - for now it has only been tested with sweeps!

*Warning 2* : This is not a 'clone-and-run' module. There are intentional error messages in between so the user can check if certain relevant steps need to be implemented for your experiment.

## The substitution method
Here we'll first use the 'substitution' method:
The idea is to record the playback first with the calibration mic, and then record the same playback (at the same distance, room, height etc.) with the target microphone. The calibration mic gives you the sound-level spectrum in Pascals. 

Knowing the sound-presure over all the frequency bands then allows you to calculate the sensitivity of the target microphone because we *know* the input (sound-pressure-level over each frequency band), and the resulting 'output' (rms at each frequency band). Dividing the two gives us the sensitivity --> rms/Pascal of the target microphone. 


## I have a microphone sensitivity - what now?
From the sensitivity curve, you can then go on to two things:

	1. Calculate the overall sound-pressure-level of the sound (e.g. RMS)
 
	2. Compensate for microphone frequency response (i.e. 'flatten' the target microphone audio)

As of this commit, this module only implements overall SPL calculation for now. 

## Things to keep in mind
The example run-through shows a *very simple*, quick and dirty example just to show the kinds of inputs and outputs to expect. In your own case you will need to consider the following things below

### Matched-filtering is important
It is very hard to get clean recordings without reflections mixing in with the direct path of the recorded signal.Try to use matched filtering and obtain only the direct path wherever possible. The overlapping direct path and reflections can cause weird spikes in the sensitivity curves. Using only the direct path signal generates 'smooth' and consistent sensitivity curves.

### SNR is important 
Place the microphones at the same distance, location, height, etc. in such a way that the spectral signal-to-noise ratio is sufficient across all frequencies you are interested in. Overlay the spectra of the ambient sound (of the same duration as your playback signal) and compare it with your recorded audio. 


Author: Thejasvi Beleyur
Example data collected by: Lena de Framond, Thejasvi Beleyur
April 2025, Code released with an MIT license
