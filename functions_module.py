# -*- coding: utf-8 -*-
"""
              /|\         
            //  ||
       ____//___||____
     //   //   //    //
    //___//___//____//
         ||  //
         || // 
         \|/    DLR\deko_ge
         
Created on Sun Feb  8 16:55:17 2026 

-Plot functions for Pithan et al.

@author: deko_ge
"""

import os
import time
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

from matplotlib.collections import LineCollection
from matplotlib.colors import SymLogNorm

import cartopy.crs as ccrs
import cartopy.feature as cfeature

# %%
#Make color maps

def make_cmap():
    """
    Returns DLR linear segmented colormap
    
    """
    cdict={'red':  (( 0/15, 235/255, 235/255),
                ( 1/15, 153/255, 153/255),
                ( 2/15,  77/255,  77/255),
                ( 3/15,   0/255,   0/255),
                ( 4/15,   0/255,   0/255),
                ( 5/15,   0/255,   0/255),
                ( 6/15,  64/255,  64/255),
                ( 7/15, 194/255, 194/255),
                ( 8/15, 255/255, 255/255),
                ( 9/15, 255/255, 255/255),
                (10/15, 255/255, 255/255),
                (11/15, 255/255, 255/255),
                (12/15, 230/255, 230/255),
                (13/15, 191/255, 191/255),
                (14/15, 153/255, 153/255),
                (15/15,   0/255,   0/255)),
    'green':   (( 0/15, 235/255, 235/255),
                ( 1/15, 204/255, 204/255),
                ( 2/15, 102/255, 102/255),
                ( 3/15,  51/255,  51/255),
                ( 4/15, 128/255, 128/255),
                ( 5/15, 153/255, 153/255),
                ( 6/15, 179/255, 179/255),
                ( 7/15, 232/255, 232/255),
                ( 8/15, 255/255, 255/255),
                ( 9/15, 224/255, 224/255),
                (10/15, 168/255, 168/255),
                (11/15, 105/255, 105/255),
                (12/15,  38/255,  38/255),
                (13/15,   0/255,   0/255),
                (14/15,   0/255,   0/255),
                (15/15,   0/255,   0/255)),
    'blue':    (( 0/15, 255/255, 255/255),
                ( 1/15, 255/255, 255/255),
                ( 2/15, 255/255, 255/255),
                ( 3/15, 179/255, 179/255),
                ( 4/15, 115/255, 115/255),
                ( 5/15,   0/255,   0/255),
                ( 6/15,  64/255,  64/255),
                ( 7/15,  71/255,  71/255),
                ( 8/15,   0/255,   0/255),
                ( 9/15,   0/255,   0/255),
                (10/15,  77/255,  77/255),
                (11/15,  26/255,  26/255),
                (12/15,   0/255,   0/255),
                (13/15,   0/255,   0/255),
                (14/15,   0/255,   0/255),
                (15/15,   0/255,   0/255))}

    return mpl.colors.LinearSegmentedColormap('DLR_colormap',cdict,256)
# %%
#Generally used functions

def setup_axes_for_courtains(ax, w_time_s, lat, lon):
    date_formatter = mdates.DateFormatter('%H:%M')
    ax.xaxis.set_tick_params(reset=True)
    if len(w_time_s) < 1500:  #300 -> 5min 1500 -> 15 min
        ax.xaxis.set_major_locator(mdates.MinuteLocator([0,30]))
    else:
        ax.xaxis.set_major_locator(mdates.MinuteLocator([0]))
    ax.xaxis.set_major_formatter(date_formatter)
    
    ax.tick_params(which = 'major', direction='in', axis = 'y', length = 10, right=True, labelright=False)
    ax.minorticks_on()
    ax.tick_params(which = 'minor', direction='in', axis = 'y', length = 5, right=True, labelright=False, bottom = False)
    ax.xaxis.set_minor_locator(mdates.MinuteLocator(byminute=range(0, 60, 5)))
    
    axes1 = plt.gca()
    axes2 = axes1.twiny()
    axes3 = axes2.twiny()
    
    axes2.xaxis.set_ticks_position('bottom') 
    axes2.xaxis.set_label_position('bottom') 
    axes2.spines['bottom'].set_position(('outward', 60))
    
    axes3.xaxis.set_ticks_position('bottom') 
    axes3.xaxis.set_label_position('bottom') 
    axes3.spines['bottom'].set_position(('outward', 120))
    
    axes2.xaxis.set_major_locator(ticker.LinearLocator(numticks=None))
    axes2.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    axes3.xaxis.set_major_locator(ticker.LinearLocator(numticks=None))
    axes3.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    
    axes2.set_xlim(0, len(lat)-1)
    axes3.set_xlim(0, len(lon)-1)
    
    ticks2 = axes2.get_xticks()
    axes2.set_xticks(ticks2[:])
    ticks3 = axes3.get_xticks()
    axes3.set_xticks(ticks3[:])
    lat_label = []
    lon_label = []
    for i in ticks2:
        lat_label.append(lat[int(i)])
        lon_label.append(lon[int(i)])    
        
    axes2.set_xticklabels(np.round(lat_label,2))
    axes3.set_xticklabels(np.round(lon_label,2))
    
    axes2.set_xlabel("Latitude [°N]")
    axes3.set_xlabel("Longitude [°E]")
    
def setup_axes_for_section_courtains(ax, secs_section, lat_section, lon_section):
    date_formatter = mdates.DateFormatter('%H:%M')
    ax.xaxis.set_tick_params(reset=True)
    if len(secs_section) < 300:  #300 -> 5min 1500 -> 15 min
        ax.xaxis.set_major_locator(mdates.MinuteLocator([0,5,10,15,20,25,30,35,40,45,50,55]))
    else:
        ax.xaxis.set_major_locator(mdates.MinuteLocator([0,15,30,45]))
    ax.xaxis.set_major_formatter(date_formatter)
    
    ax.tick_params(which = 'major', direction='in', axis = 'y', length = 10, right=True, labelright=False)
    ax.minorticks_on()
    ax.tick_params(which = 'minor', direction='in', axis = 'y', length = 5, right=True, labelright=False, bottom = False)
    ax.xaxis.set_minor_locator(mdates.MinuteLocator([5,10,15,20,25,30,35,40,45,50,55]))
    
    axes1 = plt.gca()
    axes2 = axes1.twiny()
    axes3 = axes2.twiny()
    
    axes2.xaxis.set_ticks_position('bottom') 
    axes2.xaxis.set_label_position('bottom') 
    axes2.spines['bottom'].set_position(('outward', 60))
    
    axes3.xaxis.set_ticks_position('bottom') 
    axes3.xaxis.set_label_position('bottom') 
    axes3.spines['bottom'].set_position(('outward', 120))
    
    axes2.xaxis.set_major_locator(ticker.LinearLocator(numticks=None))
    axes2.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    axes3.xaxis.set_major_locator(ticker.LinearLocator(numticks=None))
    axes3.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    
    axes2.set_xlim(0, len(lat_section)-1)
    axes3.set_xlim(0, len(lon_section)-1)
    
    ticks2 = axes2.get_xticks()
    axes2.set_xticks(ticks2[:])
    ticks3 = axes3.get_xticks()
    axes3.set_xticks(ticks3[:])
    lat_label = []
    lon_label = []
    for i in ticks2:
        lat_label.append(lat_section[int(i)])
        lon_label.append(lon_section[int(i)])    
        
    axes2.set_xticklabels(np.round(lat_label,2))
    axes3.set_xticklabels(np.round(lon_label,2))
    
    axes2.set_xlabel("Latitude [°N]")
    axes3.set_xlabel("Longitude [°E]")

def setup_map(ax, w_lat, w_lon):
    if max(w_lat)+5<90:
        ax.set_extent([min(w_lon)-5, max(w_lon)+5, min(w_lat)-5, max(w_lat)+5]
                      ,crs=ccrs.PlateCarree())
    elif max(w_lat)+5>90:
        ax.set_extent([min(w_lon)-5, max(w_lon)+5, min(w_lat)-5, 89]
                      ,crs=ccrs.PlateCarree())
    
    ax.coastlines(resolution='10m', color = 'dimgray', linewidth = 0.5)
    ax.add_feature(cfeature.BORDERS, edgecolor = 'dimgray', linewidth = 0.5)
    os.environ['CARTOPY_USER_BACKGROUNDS'] = 'C:/Users/deko_ge/Python/Backgrounds/' 
    ax.background_img(name='NaturalEarthRelief', resolution='low')
    ax.gridlines(zorder = 1)    

    
# %%
#Basic courtains

def H2Ocourtain(w_time_s, alt, data, full_date, file_name, lat, lon):
    secs = mdates.date2num(np.array(w_time_s, dtype='datetime64[s]'))
    
    bounds = np.logspace(0, 4, 30)  
    
    fig, ax = plt.subplots(figsize=(14, 4))
    

    plt.pcolormesh(secs, alt/1000, np.flipud(np.rot90(data,1)),
                   shading = 'auto', cmap = make_cmap(), norm=colors.LogNorm(vmin=1,vmax=10000))#,norm=colors.LogNorm())
    plt.ylabel("Altitude [km]")
    plt.xlabel("UTC Time [hh:mm]")
    plt.ylim((0,max(alt/1000)))
    cbar = plt.colorbar(extend = 'max', extendrect = True, boundaries = bounds, pad = 0.02)#, , format = mpl.ticker.LogFormatter(), ticks = mpl.ticker.LogLocator()) 
    cbar.ax.tick_params(which='minor', width=0, length=0, labelsize=0)
    cbar.ax.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%.0f'))
    plt.title('HALO-(AC)\u00b3'+' '+time.strftime("%d/%m/%Y", full_date)+
              ' Flight: '+file_name[-9:-5]+
              '\nwater vapor volume mixing ratio [ppmv]',
              fontsize=20, ha = 'center') 
    
    setup_axes_for_courtains(ax, w_time_s, lat, lon)
    
    plot_dir = '/users/fpithan/Documents/haloac3_paper/'
    pngfile = "{0}_wvmr.png".format(file_name)
    fig.savefig(plot_dir+pngfile, dpi = 300, bbox_inches = 'tight')
    plt.show()
    plt.close()
    
def spec_humcourtain(w_time_s, alt, data, full_date, file_name, lat, lon):
    secs = mdates.date2num(np.array(w_time_s, dtype='datetime64[s]'))
    
    bounds = np.logspace(-3, 0.75, 30)
    norm = colors.BoundaryNorm(boundaries=bounds, ncolors=256)
    
    fig, ax = plt.subplots(figsize=(15, 5))
    

    plt.pcolormesh(secs, alt/1000, np.flipud(np.rot90(data,1)),
                   shading = 'auto', cmap = make_cmap(), norm=norm)#,norm=colors.LogNorm())
    plt.ylabel("Altitude [km]")
    plt.xlabel("UTC Time [hh:mm]")
    plt.ylim((0,max(alt/1000)))
    cbar = plt.colorbar(extend = 'max', extendrect = True, boundaries = bounds, pad = 0.02, label = 'g/kg')#, , format = mpl.ticker.LogFormatter(), ticks = mpl.ticker.LogLocator()) 
    cbar.ax.tick_params(which='minor', width=0, length=0, labelsize=0)
    cbar.ax.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%.3f'))
    plt.title('HALO-(AC)\u00b3'+' '+time.strftime("%d/%m/%Y", full_date)+
              ' Flight: '+file_name[-9:-5]+
              '\nSpecific Humidity',
              fontsize=20, ha = 'center') 
    
    setup_axes_for_courtains(ax, w_time_s, lat, lon)
    
    plot_dir = '/users/fpithan/Documents/haloac3_paper/'
    pngfile = "{0}_spechum.png".format(file_name)
    fig.savefig(plot_dir+pngfile, dpi = 300, bbox_inches = 'tight')
    plt.show()
    plt.close()
    
def spec_hum_anomcourtain(w_time_s, alt, data, full_date, file_name, lat, lon):
    secs = mdates.date2num(np.array(w_time_s, dtype='datetime64[s]'))
    
    
    fig, ax = plt.subplots(figsize=(15, 5))
    
    v = np.nanpercentile(np.abs(data), 95)
    norm = SymLogNorm(linthresh=0.02, linscale=1.0, vmin=-v, vmax=v, base=10)
    plt.pcolormesh(secs, alt/1000, np.flipud(np.rot90(data,1)),
                   shading = 'auto', cmap = "RdBu_r", norm = norm) #vmin=-v, vmax=v)
    plt.ylabel("Altitude [km]")
    plt.xlabel("UTC Time [hh:mm]")
    plt.ylim((0,max(alt/1000)))
    cbar = plt.colorbar(extend = 'both', pad = 0.02)#, , format = mpl.ticker.LogFormatter(), ticks = mpl.ticker.LogLocator()) 
    cbar.set_label(r"$q' \;\;[\mathrm{g\,kg^{-1}}]$")
    cbar.ax.axhline(0, color='k', linewidth=0.8)
    cbar.ax.tick_params(which='minor', width=0, length=0, labelsize=0)
    cbar.ax.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%.3f'))
    plt.title('HALO-(AC)\u00b3'+' '+time.strftime("%d/%m/%Y", full_date)+
              ' Flight: '+file_name[-9:-5]+
              '\nSpecific Humidity anomaly\n' +
    r"$q'(t,z)=q(t,z)-\overline{q}(z)$",
              fontsize=20, ha = 'center') 
    
    setup_axes_for_courtains(ax, w_time_s, lat, lon)
    
    plot_dir = '/users/fpithan/Documents/haloac3_paper/'
    pngfile = "{0}_spechum_anom.png".format(file_name)
    fig.savefig(plot_dir+pngfile, dpi = 300, bbox_inches = 'tight')
    plt.show()
    plt.close()
    
def spec_hum_relanomcourtain(w_time_s, alt, data, full_date, file_name, lat, lon):
    secs = mdates.date2num(np.array(w_time_s, dtype='datetime64[s]'))
    
    fig, ax = plt.subplots(figsize=(15, 5))
    
    v = np.nanpercentile(np.abs(data), 95)
    norm = SymLogNorm(linthresh=0.1, linscale=1.0, vmin=-v, vmax=v, base=10)
    plt.pcolormesh(secs, alt/1000, np.flipud(np.rot90(data,1)),
                   shading = 'auto', cmap = "RdBu_r", norm = norm) #vmin=-v, vmax=v)
    plt.ylabel("Altitude [km]")
    plt.xlabel("UTC Time [hh:mm]")
    plt.ylim((0,max(alt/1000)))
    cbar = plt.colorbar(extend = 'both', pad = 0.02)#, , format = mpl.ticker.LogFormatter(), ticks = mpl.ticker.LogLocator()) 
    cbar.set_label(r"Relative anomaly $[\%]$")
    cbar.ax.axhline(0, color='k', linewidth=0.8)
    cbar.ax.tick_params(which='minor', width=0, length=0, labelsize=0)
    cbar.ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda x, pos: f"{100*x:.0f}"))
    plt.title("HALO-(AC)$^3$  " + time.strftime("%d/%m/%Y", full_date) +
    "  Flight: " + file_name[-9:-5] +
    "\nSpecific Humidity relative anomaly\n"
    r"$(q(t,z)-\overline{q}(z))\,/\,\overline{q}(z)$",
    fontsize=20)
    
    setup_axes_for_courtains(ax, w_time_s, lat, lon)
    
    plot_dir = '/users/fpithan/Documents/haloac3_paper/'
    pngfile = "{0}_spechum_relanom.png".format(file_name)
    fig.savefig(plot_dir+pngfile, dpi = 300, bbox_inches = 'tight')
    plt.show()
    plt.close()

# %%
#Make courtains for each flight segment

def plot_q_sections(w_lon, w_alt, q, sections, w_time_s, w_lat, full_date, file_name):
    secs = mdates.date2num(np.array(w_time_s, dtype='datetime64[s]'))

    bounds = np.logspace(-3, 0.75, 30)
    norm = colors.BoundaryNorm(boundaries=bounds, ncolors=256)
    

    for sec_name, sec_info in sections.items():
        start_idx = sec_info['start_idx']
        end_idx = sec_info['end_idx']
        
        # Slice the sections
        secs_section = secs[start_idx:end_idx+1]
        lat_section = w_lat[start_idx:end_idx+1]
        lon_section = w_lon[start_idx:end_idx+1]
        q_section = q[start_idx:end_idx+1, :]  
        
        
        fig, ax = plt.subplots(figsize=(15, 5))
        plt.pcolormesh(secs_section, w_alt/1000, np.flipud(np.rot90(q_section,1)),
                   shading = 'auto', cmap = make_cmap(), norm=norm)#,norm=colors.LogNorm())
                
        plt.ylabel("Altitude [km]")
        plt.xlabel("UTC Time [hh:mm]")
        plt.ylim((0,max(w_alt/1000)))
        cbar = plt.colorbar(extend = 'max', extendrect = True, boundaries = bounds, pad = 0.02, label = '[g kg$^{-1}$]')#, , format = mpl.ticker.LogFormatter(), ticks = mpl.ticker.LogLocator()) 
        cbar.ax.tick_params(which='minor', width=0, length=0, labelsize=0)
        cbar.ax.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%.3f'))
        plt.title('HALO-(AC)\u00b3'+' '+time.strftime("%d/%m/%Y", full_date)+
                  ' Flight: '+file_name[-9:-5]+ f" {sec_name}"+
                  '\nSpecific Humidity',
                  fontsize=20, ha = 'center') 
        
        setup_axes_for_section_courtains(ax, secs_section, lat_section, lon_section)
        
        plot_dir = '/Users/fpithan/halo-ac3_paper/'
        pngfile = "{0}_spechum_{1}.png".format(file_name, sec_name)
        fig.savefig(plot_dir+pngfile, dpi = 300, bbox_inches = 'tight')
        plt.show()
        plt.close()
        
def plot_q_anom_sec(w_lon, w_alt, data, sections, w_time_s, w_lat, full_date, file_name):
    secs = mdates.date2num(np.array(w_time_s, dtype='datetime64[s]'))
    v = np.nanpercentile(np.abs(data), 95)
    norm = SymLogNorm(linthresh=0.02, linscale=1.0, vmin=-v, vmax=v, base=10)
       
    for sec_name, sec_info in sections.items():
        fig, ax = plt.subplots(figsize=(15, 5))
        

        start_idx = sec_info['start_idx']
        end_idx = sec_info['end_idx']
        
        # Slice the sections
        secs_section = secs[start_idx:end_idx+1]
        lat_section = w_lat[start_idx:end_idx+1]
        lon_section = w_lon[start_idx:end_idx+1]
        data_section = data[start_idx:end_idx+1, :]  

        plt.pcolormesh(secs_section, w_alt/1000, np.flipud(np.rot90(data_section,1)),
                       shading = 'auto', cmap = "RdBu_r", norm = norm) #vmin=-v, vmax=v)
        plt.ylabel("Altitude [km]")
        plt.xlabel("UTC Time [hh:mm]")
        plt.ylim((0,max(w_alt/1000)))
        cbar = plt.colorbar(extend = 'both', pad = 0.02)#, , format = mpl.ticker.LogFormatter(), ticks = mpl.ticker.LogLocator()) 
        cbar.set_label(r"$q' \;\;[\mathrm{g\,kg^{-1}}]$")
        cbar.ax.axhline(0, color='k', linewidth=0.8)
        cbar.ax.tick_params(which='minor', width=0, length=0, labelsize=0)
        cbar.ax.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%.3f'))
        plt.title('HALO-(AC)\u00b3'+' '+time.strftime("%d/%m/%Y", full_date)+
                  ' Flight: '+file_name[-9:-5]+ f" {sec_name}"+
                  '\nSpecific Humidity anomaly\n' +
        r"$q'(t,z)=q(t,z)-\overline{q}(z)$",
                  fontsize=20, ha = 'center') 
        
        setup_axes_for_section_courtains(ax, secs_section, lat_section, lon_section)        

        plot_dir = '/users/fpithan/Documents/haloac3_paper/'
        pngfile = "{0}_spechum_anom_{1}.png".format(file_name, sec_name)
        fig.savefig(plot_dir+pngfile, dpi = 300, bbox_inches = 'tight')
        plt.show()
        plt.close()
    
def plot_q_relanom_sec(w_lon, w_alt, data, sections, w_time_s, w_lat, full_date, file_name):
    secs = mdates.date2num(np.array(w_time_s, dtype='datetime64[s]'))
    v = np.nanpercentile(np.abs(data), 95)
    norm = SymLogNorm(linthresh=0.1, linscale=1.0, vmin=-v, vmax=v, base=10)

    for sec_name, sec_info in sections.items():
        fig, ax = plt.subplots(figsize=(15, 5))
        
        start_idx = sec_info['start_idx']
        end_idx = sec_info['end_idx']
        
        # Slice the sections
        secs_section = secs[start_idx:end_idx+1]
        lat_section = w_lat[start_idx:end_idx+1]
        lon_section = w_lon[start_idx:end_idx+1]
        data_section = data[start_idx:end_idx+1, :]  

        plt.pcolormesh(secs_section, w_alt/1000, np.flipud(np.rot90(data_section,1)),
                       shading = 'auto', cmap = "RdBu_r", norm = norm) #vmin=-v, vmax=v)
        plt.ylabel("Altitude [km]")
        plt.xlabel("UTC Time [hh:mm]")
        plt.ylim((0,max(w_alt/1000)))
        cbar = plt.colorbar(extend = 'both', pad = 0.02)#, , format = mpl.ticker.LogFormatter(), ticks = mpl.ticker.LogLocator()) 
        cbar.set_label(r"Relative anomaly $[\%]$")
        cbar.ax.axhline(0, color='k', linewidth=0.8)
        cbar.ax.tick_params(which='minor', width=0, length=0, labelsize=0)
        cbar.ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda x, pos: f"{100*x:.0f}"))
        plt.title("HALO-(AC)$^3$  " + time.strftime("%d/%m/%Y", full_date) +
        "  Flight: " + file_name[-9:-5]+ f" {sec_name}"+
        "\nSpecific Humidity relative anomaly\n"
        r"$(q(t,z)-\overline{q}(z))\,/\,\overline{q}(z)$",
        fontsize=20)
        
        setup_axes_for_section_courtains(ax, secs_section, lat_section, lon_section)        

        plot_dir = '/users/fpithan/Documents/haloac3_paper/'
        pngfile = "{0}_spechum_relanom_{1}.png".format(file_name, sec_name)
        fig.savefig(plot_dir+pngfile, dpi = 300, bbox_inches = 'tight')
        plt.show()
        plt.close()    

# %%
#Make plots projected on map

def flight_track_w_wvmr(w_time_s, file_name, w_lat, w_lon, wvmr_means, full_date):
    

    fig= plt.figure(figsize=(10, 7))         
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.AzimuthalEquidistant())
    
    setup_map(ax, w_lat, w_lon)
    
    x = w_lon
    y = w_lat
    z = np.nan_to_num(wvmr_means, copy=True, nan=0.0,posinf=None,  neginf=None)  # first derivative
    
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-5], points[5:]], axis=1)
    
    norm = plt.Normalize(0, 1000000)
    lc = LineCollection(segments, cmap = make_cmap(), norm = norm, transform=ccrs.PlateCarree(), alpha = 1, zorder = 2)
    lc.set_array(z)
    lc.set_linewidth(2)
    line = ax.add_collection(lc)

    plt.title('HALO-(AC)$^3$  '+' '+time.strftime("%d/%m/%Y", full_date)+
              ' Flight: '+file_name[-9:-5]+'\nIntegrated wvmr [ppm]',
      fontsize=20, ha = 'center') 
    
    cbar = fig.colorbar(line, pad = 0.02)
    cbar.ax.tick_params(labelsize=8)
    cbar.set_label('wvmr [ppm]', fontsize=8)

    plot_dir = '/users/fpithan/Documents/haloac3_paper/'
    pngfile = "{0}_track_wvmr.png".format(file_name)
    fig.savefig(plot_dir+pngfile, dpi = 300, bbox_inches = 'tight')
    plt.show()
    plt.close()

def flight_track_w_wvmr_scat(w_time_s, file_name, w_lat, w_lon, wvmr_means, full_date):
    

    fig= plt.figure(figsize=(10, 7))         
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.AzimuthalEquidistant())
    
    setup_map(ax, w_lat, w_lon)
    
    plt.scatter(w_lon, w_lat, c=wvmr_means, cmap='viridis', s=25,
            transform=ccrs.PlateCarree(), zorder = 2)
    plt.title('HALO-(AC)$^3$  '+' '+time.strftime("%d/%m/%Y", full_date)+
              ' Flight: '+file_name[-9:-5]+'\nIntegrated wvmr [ppm]',
      fontsize=20, ha = 'center') 
    
    cbar = plt.colorbar(pad = 0.02)
    cbar.ax.tick_params(labelsize=8)
    cbar.set_label('wvmr [ppm]', fontsize=8)

    plot_dir = '/users/fpithan/Documents/haloac3_paper/'
    pngfile = "{0}_track_wvmr_scat.png".format(file_name)
    fig.savefig(plot_dir+pngfile, dpi = 300, bbox_inches = 'tight')
    plt.show()
    plt.close()
    
def flight_track_w_q(w_time_s, file_name, w_lat, w_lon, col_mean_q, full_date):
    

    #Import terrain data
    fig= plt.figure(figsize=(10, 7))         
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.AzimuthalEquidistant())
    
    setup_map(ax, w_lat, w_lon)
        
    x = w_lon
    y = w_lat
    z = np.nan_to_num(col_mean_q, copy=True, nan=0.0,posinf=None,  neginf=None)  # first derivative
    
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-5], points[5:]], axis=1)
    
    norm = plt.Normalize(0, 1)
    lc = LineCollection(segments, cmap = make_cmap(), norm = norm, transform=ccrs.PlateCarree(), alpha = 1, zorder = 2)
    lc.set_array(z)
    lc.set_linewidth(2)
    line = ax.add_collection(lc)

    plt.title('HALO-(AC)$^3$  '+' '+time.strftime("%d/%m/%Y", full_date)+
              ' Flight: '+file_name[-9:-5]+'\nColumn mean q [g/kg]',
      fontsize=20, ha = 'center') 
    
    cbar = fig.colorbar(line, pad = 0.02)
    cbar.ax.tick_params(labelsize=8)
    cbar.set_label('q [g/kg]', fontsize=8)

    plot_dir = '/users/fpithan/Documents/haloac3_paper/'
    pngfile = "{0}_track_q.png".format(file_name)
    fig.savefig(plot_dir+pngfile, dpi = 300, bbox_inches = 'tight')
    plt.show()
    plt.close()

def flight_track_w_q_anom(w_time_s, file_name, w_lat, w_lon, col_mean_q_anom, full_date):
    

    fig= plt.figure(figsize=(10, 7))         
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.AzimuthalEquidistant())
    
    setup_map(ax, w_lat, w_lon)
    
    x = w_lon
    y = w_lat
    z = np.nan_to_num(col_mean_q_anom, copy=True, nan=0.0,posinf=None,  neginf=None)  # first derivative
    
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-5], points[5:]], axis=1)
    
    #norm = plt.Normalize(0, 1)
    v = np.nanpercentile(np.abs(col_mean_q_anom), 95)
    norm = SymLogNorm(linthresh=0.02, linscale=1.0, vmin=-v, vmax=v, base=10)

    lc = LineCollection(segments, cmap = "RdBu_r", norm = norm, transform=ccrs.PlateCarree(), alpha = 1, zorder = 2)
    lc.set_array(z)
    lc.set_linewidth(2)
    line = ax.add_collection(lc)

    plt.title('HALO-(AC)$^3$  '+' '+time.strftime("%d/%m/%Y", full_date)+
              ' Flight: '+file_name[-9:-5]+'\nColumn mean q anomaly[g/kg]',
      fontsize=20, ha = 'center') 
    
    cbar = fig.colorbar(line, pad = 0.02)
    cbar.ax.tick_params(labelsize=8)
    cbar.set_label('q [g/kg]', fontsize=8)

    plot_dir = '/users/fpithan/Documents/haloac3_paper/'
    pngfile = "{0}_track_q_anom.png".format(file_name)
    fig.savefig(plot_dir+pngfile, dpi = 300, bbox_inches = 'tight')
    plt.show()
    plt.close()

def flight_track_w_q_max(w_time_s, file_name, w_lat, w_lon, col_max_q, full_date):
    

    fig= plt.figure(figsize=(10, 7))         
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.AzimuthalEquidistant())
    
    setup_map(ax, w_lat, w_lon)

    x = w_lon
    y = w_lat
    z = np.nan_to_num(col_max_q, copy=True, nan=0.0,posinf=None,  neginf=None)  # first derivative
    
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-5], points[5:]], axis=1)
    
    norm = plt.Normalize(0, 5)
    lc = LineCollection(segments, cmap = make_cmap(), norm = norm, transform=ccrs.PlateCarree(), alpha = 1, zorder = 2)
    lc.set_array(z)
    lc.set_linewidth(2)
    line = ax.add_collection(lc)

    plt.title('HALO-(AC)$^3$  '+' '+time.strftime("%d/%m/%Y", full_date)+
              ' Flight: '+file_name[-9:-5]+'\nColumn max q [g/kg]',
      fontsize=20, ha = 'center') 
    
    cbar = fig.colorbar(line, pad = 0.02)
    cbar.ax.tick_params(labelsize=8)
    cbar.set_label('q [g/kg]', fontsize=8)

    plot_dir = '/users/fpithan/Documents/haloac3_paper/'
    pngfile = "{0}_track_q_max.png".format(file_name)
    fig.savefig(plot_dir+pngfile, dpi = 300, bbox_inches = 'tight')
    plt.show()
    plt.close()

# %%
def flight_track_w_wvmr_secs(w_time_s, file_name, w_lat, w_lon, wvmr_means, sections, full_date):
    for sec_name, sec_info in sections.items():
        start_idx = sec_info['start_idx']
        end_idx = sec_info['end_idx']
        
        # Slice the sections
        lat_section = w_lat[start_idx:end_idx+1]
        lon_section = w_lon[start_idx:end_idx+1]
        wvmr_means_section = wvmr_means[start_idx:end_idx+1]  

        

        fig= plt.figure(figsize=(10, 7))         
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.AzimuthalEquidistant())
            
        setup_map(ax, w_lat, w_lon)
        
        x = lon_section
        y = lat_section
        z = np.nan_to_num(wvmr_means_section, copy=True, nan=0.0,posinf=None,  neginf=None)  # first derivative
        
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-5], points[5:]], axis=1)
        
        norm = plt.Normalize(0, 1000000)
        lc = LineCollection(segments, cmap = make_cmap(), norm = norm, transform=ccrs.PlateCarree(), alpha = 1, zorder = 2)
        lc.set_array(z)
        lc.set_linewidth(2)
        line = ax.add_collection(lc)
    
        plt.title('HALO-(AC)\u00b3'+' '+time.strftime("%d/%m/%Y", full_date)+
                  ' Flight: '+file_name[-9:-5]+ f" {sec_name}"+
                  '\nIntegrated WV',
                  fontsize=20, ha = 'center') 
        
        cbar = fig.colorbar(line, pad = 0.02)
        cbar.ax.tick_params(labelsize=8)
        cbar.set_label('wvmr [ppm]', fontsize=8)
    
        plot_dir = '/users/fpithan/Documents/haloac3_paper/'
        pngfile = "{0}_track_wvmr_{1}.png".format(file_name, sec_name)
        fig.savefig(plot_dir+pngfile, dpi = 300, bbox_inches = 'tight')
        plt.show()
        plt.close()

def flight_track_w_q_secs(w_time_s, file_name, w_lat, w_lon, col_mean_q, sections, full_date):
    for sec_name, sec_info in sections.items():
        start_idx = sec_info['start_idx']
        end_idx = sec_info['end_idx']
        
        # Slice the sections
        lat_section = w_lat[start_idx:end_idx+1]
        lon_section = w_lon[start_idx:end_idx+1]
        col_mean_q_section = col_mean_q[start_idx:end_idx+1]  

        

        fig= plt.figure(figsize=(10, 7))         
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.AzimuthalEquidistant())
        
        setup_map(ax, w_lat, w_lon)
        
        x = lon_section
        y = lat_section
        z = np.nan_to_num(col_mean_q_section, copy=True, nan=0.0,posinf=None,  neginf=None)  # first derivative
        
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-5], points[5:]], axis=1)
        
        norm = plt.Normalize(0, 1)
        lc = LineCollection(segments, cmap = make_cmap(), norm = norm, transform=ccrs.PlateCarree(), alpha = 1, zorder = 2)
        lc.set_array(z)
        lc.set_linewidth(2)
        line = ax.add_collection(lc)
    
        plt.title('HALO-(AC)$^3$  '+' '+time.strftime("%d/%m/%Y", full_date)+
                  ' Flight: '+file_name[-9:-5]+ f" {sec_name}"+'\nColumn mean q [g/kg]',
          fontsize=20, ha = 'center') 
        
        cbar = fig.colorbar(line, pad = 0.02)
        cbar.ax.tick_params(labelsize=8)
        cbar.set_label('q [g/kg]', fontsize=8)
    
        plot_dir = '/users/fpithan/Documents/haloac3_paper/'
        pngfile = "{0}_track_q_{1}.png".format(file_name, sec_name)
        fig.savefig(plot_dir+pngfile, dpi = 300, bbox_inches = 'tight')
        plt.show()
        plt.close()

def flight_track_w_q_anom_secs(w_time_s, file_name, w_lat, w_lon, col_mean_q_anom, sections, full_date):
    v = np.nanpercentile(np.abs(col_mean_q_anom), 95)
    norm = SymLogNorm(linthresh=0.02, linscale=1.0, vmin=-v, vmax=v, base=10)

    for sec_name, sec_info in sections.items():
        start_idx = sec_info['start_idx']
        end_idx = sec_info['end_idx']
        
        # Slice the sections
        lat_section = w_lat[start_idx:end_idx+1]
        lon_section = w_lon[start_idx:end_idx+1]
        col_mean_q_anom_section = col_mean_q_anom[start_idx:end_idx+1]  

        

        fig= plt.figure(figsize=(10, 7))         
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.AzimuthalEquidistant())
        
        setup_map(ax, w_lat, w_lon)
        
        x = lon_section
        y = lat_section
        z = np.nan_to_num(col_mean_q_anom_section, copy=True, nan=0.0,posinf=None,  neginf=None)  # first derivative
        
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-5], points[5:]], axis=1)
        
        lc = LineCollection(segments, cmap = "RdBu_r", norm = norm, transform=ccrs.PlateCarree(), alpha = 1, zorder = 2)
        lc.set_array(z)
        lc.set_linewidth(2)
        line = ax.add_collection(lc)
    
        plt.title('HALO-(AC)$^3$  '+' '+time.strftime("%d/%m/%Y", full_date)+
                  ' Flight: '+file_name[-9:-5]+ f" {sec_name}"+'\nColumn mean q anomaly[g/kg]',
          fontsize=20, ha = 'center') 
        
        cbar = fig.colorbar(line, pad = 0.02)
        cbar.ax.tick_params(labelsize=8)
        cbar.set_label('q [g/kg]', fontsize=8)
    
        plot_dir = '/users/fpithan/Documents/haloac3_paper/'
        pngfile = "{0}_track_q_anom_{1}.png".format(file_name, sec_name)
        fig.savefig(plot_dir+pngfile, dpi = 300, bbox_inches = 'tight')
        plt.show()
        plt.close()

def flight_track_w_q_max_secs(w_time_s, file_name, w_lat, w_lon, col_max_q, sections, full_date):
    for sec_name, sec_info in sections.items():
        start_idx = sec_info['start_idx']
        end_idx = sec_info['end_idx']
        
        # Slice the sections
        lat_section = w_lat[start_idx:end_idx+1]
        lon_section = w_lon[start_idx:end_idx+1]
        col_max_q_section = col_max_q[start_idx:end_idx+1]  

        

        fig= plt.figure(figsize=(10, 7))         
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.AzimuthalEquidistant())
        
        setup_map(ax, w_lat, w_lon)
        
        x = lon_section
        y = lat_section
        z = np.nan_to_num(col_max_q_section, copy=True, nan=0.0,posinf=None,  neginf=None)  # first derivative
        
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-5], points[5:]], axis=1)
        
        norm = plt.Normalize(0, 5)
        lc = LineCollection(segments, cmap = make_cmap(), norm = norm, transform=ccrs.PlateCarree(), alpha = 1, zorder = 2)
        lc.set_array(z)
        lc.set_linewidth(2)
        line = ax.add_collection(lc)
    
        plt.title('HALO-(AC)$^3$  '+' '+time.strftime("%d/%m/%Y", full_date)+
                  ' Flight: '+file_name[-9:-5]+ f" {sec_name}"+'\nColumn max q [g/kg]',
          fontsize=20, ha = 'center') 
        
        cbar = fig.colorbar(line, pad = 0.02)
        cbar.ax.tick_params(labelsize=8)
        cbar.set_label('q [g/kg]', fontsize=8)
    
        plot_dir = '/users/fpithan/Documents/haloac3_paper/'
        pngfile = "{0}_track_q_max_{1}.png".format(file_name, sec_name)
        fig.savefig(plot_dir+pngfile, dpi = 300, bbox_inches = 'tight')
        plt.show()
        plt.close()