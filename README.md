# HETS
HDF5 Extraction Tool Set

The extractor is built in Python 3 with one outside package "H5py" that must be installed since this package interfaces with the HDF5 file format. 
To use the extractor:
1. Select the HDF5 file you wish to extract, answer y to extract additional files for a batch process, answer n when you are done adding files.
2. Select a save location for the resulting .dat file that can be imported into your favorite data analysis platform.
3. Select the type of process you wish to run, the spectrum extraction will sum the decay for each excitation wavelength, emission wavelength, and location in the file.  The decay extraction will sum over the sets in the groups of the above attributes and result in a decay histogram.  The specific decay will only sum the wavelength subset you wish to determine the properties of.

The extraction will run and let you know when the process is complete and enjoy your new spectral information.
