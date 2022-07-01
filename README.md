# EEG Firebase
This repo contains a simple script for pushing data from the EEG ganglion sensor to a firebase real-time database. The pushed data looks something like this : 

![firebase](https://user-images.githubusercontent.com/22594650/176925570-9e37a6cb-557a-4dd1-b03f-2e0512ced606.png)


In this EEG setup, the electrodes are placed in a way similar to the Muse EEG headset. You can read more about the Muse headset [here](https://choosemuse.com/). You can also read about the 10-20 system of electrode placement [here](https://info.tmsi.com/blog/the-10-20-system-for-eeg). The [Brainflow](https://brainflow.org/) python library is used to stream data from the BLE dongle of the [OpenBCI Ganglion Board](https://docs.openbci.com/Ganglion/GanglionLanding/). 

## Reference Tutorials 
1. https://firebase.google.com/docs/reference/admin/python/
2. https://www.freecodecamp.org/news/how-to-get-started-with-firebase-using-python/
3. https://ahnaafk.medium.com/creating-a-neurofeedback-program-with-python-c6153022a4e7
