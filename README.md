Scripts to analyze obtain distance data from Optical tweezer measurements, convert to bp-unwound and identify pause states during unwinding activity.
Requires prior installation of the pylake package from Lumicks.
The script is arranged in the form of code-blocks (each block is separated by #%%; visible on Spyder).                   
1) The first code block defines a function for selecting a range of data from a plot. 2) Code block-2
performs a linear fit on the data points selected. 3) Savitzky-Golay filter for distance data and identification of pause states.
