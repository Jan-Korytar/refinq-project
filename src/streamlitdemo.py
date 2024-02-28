import streamlit as st
from streamlit_image_comparison import image_comparison
import glob
import rasterio as rs
import os
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image


st.write("Current working directory:", os.getcwd())
# loading the data and saving it in session_state
if 'maps_loaded' not in st.session_state:
    band1 = []
    band2 = []
    band3 = []

    for file in glob.glob('data/*.tiff'):
        with rs.open(file) as src:
            img = src.read(1)
            band1.append(img)
            band2.append(src.read(2))
            band3.append(src.read(3))

    st.session_state['band1'] = band1
    st.session_state['band2'] = band2
    st.session_state['band3'] = band3
    st.session_state.maps_loaded = True
else:
    band1 = st.session_state['band1']
    band2 = st.session_state['band2']
    band3 = st.session_state['band3']


st.title('Refinq Project')
st.markdown('This is a Refinq coding challenge interview project created by Jan Korytář')
st.subheader('The given data')
st.markdown('We are given three geoTIFF files containing three bands of NVDI index of a Naturpark Karwende taken at '
            'different times.')

year_to_index = {0:2019, 1:2023, 2:2024}
year = st.select_slider(label='Select a year', options=[0, 1, 2], format_func=lambda x: year_to_index.get(x))

if 'plot_1' not in st.session_state or year != st.session_state['year']:
    print('run')
    fig, axes = plt.subplots(3, 1, )
    a = axes[0].imshow(band1[year], cmap='winter')
    axes[0].set_title('Band 1')
    axes[1].imshow(band2[year], cmap='winter')
    axes[1].set_title('Band 2')
    axes[2].imshow(band3[year], cmap='winter')
    axes[2].set_title('Band 3')
    fig.tight_layout(h_pad=1, w_pad=1)
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    fig.colorbar(a, cax=cbar_ax, label='NVDI')
    st.session_state['year'] = year
    st.session_state['plot_1'] = fig
else:
    fig = st.session_state['plot_1']
st.pyplot(fig)

st.title("Exploratory analysis of change of the NVDI index")
col1, col2, col3 = st.columns(3)
with col1:
    st.selectbox(label='Select a year for the first image', options=[0, 1, 2], format_func=lambda x: year_to_index.get(x))
with col2:
    st.selectbox(label='Select a year for the second image', options=[0, 1, 2], format_func=lambda x: year_to_index.get(x))
with col3:
    st.selectbox(label='Select the band', options=[1, 2, 3])

image_comparison(Image.fromarray(band1[0]), Image.fromarray(band2[1]))



