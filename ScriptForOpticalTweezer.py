# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 12:53:52 2025

Requires prior installation of the pylake package from Lumicks.
The script is arranged in the form of code-blocks (each block is separated by #%%; visible on Spyder).                   
1) The first code block defines a function for selecting a range of data from a plot. 2) Code block-2
performs a linear fit on the data points selected. 3) Savitzky-Golay filter for distance data and identification of pause states.
                                                   
"""
#Code block 1

from matplotlib.widgets import SpanSelector
# fig, ax = plt.subplots()
k = 0 # file number to be selected from the list of H5 files
file = lk.File(fileList[k])

#file = lk.File(fileList[8])
#file.force1x.plot() # for plotting the force quickly
#For extracting the force1x and plotting the data against the time (not distance because there is no FD).
dist1 = file.distance1.data
dist1 = ((dist1-6.07)/(12.06-6.07))*17853
dist1 = dist1-dist1[0]
#f1x_timestamps = file.force1x.timestaC:\Users\prade\Dropbox (HMS)\Data\C-trap\2023\sPS42a_haloUb-gfp-MBP_tethered_Repeatmps # This is plotting actual time stamp from machine
time = file.distance1.seconds # This is for plotting time in seconds
fig, axs = plt.subplots(figsize=(8,6))
plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.2)
axs.set_xlabel('Time (s)', fontsize = 18)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
for spine in axs.spines.values():
    spine.set_linewidth(1.25)
axs.tick_params(width=1.25)
axs.set_ylabel('Distance (nt)',fontsize = 18)
axs.plot(time, dist1)
spans = []
window_data = []

def span_onselect(xmin, xmax):
    # Convert x-coordinate values to indices
    xmin_index = np.argmin(np.abs(time - xmin))
    xmax_index = np.argmin(np.abs(time - xmax))   
    # Extract data within the selected region using indices
    x_data = time[xmin_index:xmax_index]
    y_data = dist1[xmin_index:xmax_index]

    window_n = np.column_stack((x_data, y_data))
    window_data.append(window_n)
    
    print(window_n)

span = SpanSelector(axs,span_onselect,'horizontal', useblit=True, rectprops=dict(alpha=0.5, facecolor='green'))
plt.show()

#%% Code block 2. collecting spanselector data from all windows and plotting together
fitSlopes = []
fitIntercepts = []
fitr_Squared = []
# allFits = np.empty((0, 3))  # you need to start a variable called allFits
for j in np.arange(0, len(window_data)):
    temp_dist = window_data[j][:,1]
    temp_time = window_data[j][:,0]
    xseq = np.linspace(min(temp_time), max(temp_time), num=200)
    b, a = np.polyfit(temp_time, temp_dist, deg=1) #linear fitting
    fitSlopes = np.append(fitSlopes, b)
    fitIntercepts = np.append(fitIntercepts, a)
    y_extrapolated = a + b * xseq
    y_pred = b * temp_time + a
    ss_res = np.sum((temp_dist - y_pred) ** 2)
    ss_tot = np.sum((temp_dist - np.mean(temp_dist)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    fitr_Squared = np.append(fitr_Squared, r_squared)
    plt.plot(xseq, y_extrapolated, color="r", lw=2.5)
    loc = int(np.ceil(len(temp_dist)/2))
    plt.text(temp_time[loc], temp_dist[loc], '(%s) nt/s'%(round(b,3)) ,fontsize = 14) #printing the equation
fullData = np.column_stack((fitSlopes, fitIntercepts, fitr_Squared))
allFits = np.vstack((allFits, fullData)) # you need to start a variable called allFits

#%% Code block-3. Savitzky–Golay filtering of the distance data followed by 
#identification of paused states corresponding to instantaneous unwinding rate less than 2 nt/s

from scipy.signal import medfilt, savgol_filter

k = 0
file = lk.File(fileList[k])

#file = lk.File(fileList[8])
#file.force1x.plot() # for plotting the force quickly
#For extracting the force\ 1x and plotting the data against the time (not distance because there is no FD).
dist1 = file.distance1.data
dist1 = ((dist1-6.07)/(12.06-6.07))*17853 #converting to nt unwound
dist1 = dist1-dist1[0]
#f1x_timestamps = file.force1x.timestaC:\Users\prade\Dropbox (HMS)\Data\C-trap\2023\sPS42a_haloUb-gfp-MBP_tethered_Repeatmps # This is plotting actual time stamp from machine
time = file.distance1.seconds # This is for plotting time in seconds
fig, axs = plt.subplots(figsize=(8,6))
plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.2)
axs.set_xlabel('Time (s)', fontsize = 18)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
for spine in axs.spines.values():
    spine.set_linewidth(1.25)
axs.tick_params(width=1.25)
axs.set_ylabel('Distance (nt)',fontsize = 18)
axs.plot(time, dist1) #Final plot after extracting the data in previous statemnts


smoothed2 = savgol_filter(dist1, window_length=51, polyorder=2)

dt = np.diff(time)  # Assuming time is equally spaced
dy = np.diff(smoothed2)
slope = dy / dt  # Instantaneous ratecx
# Pad to match lengths
slope = np.concatenate([[0], slope])


flat_threshold = 2.0  # nt/s, adjust as needed
is_flat = np.abs(slope) < flat_threshold

distFlat = dist1[is_flat]
timeFlat= time[is_flat]
plt.plot(time,smoothed2, color='black' )
plt.scatter(timeFlat, distFlat, color='yellow', edgecolors='none', s=50, alpha=0.6, marker='o')
print('The fraction of trace that is paused is ',round(sum(is_flat)/len(is_flat) * 100, 2), '%')

