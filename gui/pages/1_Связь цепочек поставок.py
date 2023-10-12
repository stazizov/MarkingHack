import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from supply_chain import create_supply_chains
from utils import empty_page
import os
import json


with open("interface.json") as f:
    config = json.load(f)

def page1_gui():
    def basic_layer(data):
        return pdk.Layer(
                "ArcLayer",
                data=data,
                get_source_position=["lon", "lat"],
                get_target_position=["lon2", "lat2"],
                get_source_color=[255, 0, 0, 100],
                get_target_color=[0, 0, 255, 100],
                auto_highlight=True,
                width_scale=0.0001,
                get_width="outbound",
                width_min_pixels=3,
                width_max_pixels=30,
            )

    def update_map():
        # try:
        min_value_b = st.session_state.min_threshold_slider
        max_value_b = st.session_state.max_threshold_slider
        # inn = st.session_state.inn_input

        min_value = min(min_value_b, max_value_b)
        max_value = max(min_value_b, max_value_b)

        geodata = create_supply_chains(
            '', 
            min_value,
            max_value,
            )
         
        layers = [basic_layer(geodata)] 

        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={
                    "latitude": 55.7558,
                    "longitude": 37.6173,
                    "zoom": 5,
                    "pitch": 50,
                },
                layers=layers,
            )
        )

        # except:
        #     print("Error")

    st.set_page_config(page_title=config["mappage_title"], page_icon="🌍")

    st.title(config["mappage_title"])
    st.sidebar.header(config["mappage_title"])


    st.sidebar.slider(
        config["max_threshold_sidebar_text"], 
        max_value=12, 
        min_value=2,
        value=12, 
        key="max_threshold_slider",
        )

    st.sidebar.slider(
        config["min_threshold_sidebar_text"], 
        max_value=12, 
        min_value=2,
        value=2, 
        key="min_threshold_slider",
        )
    
    # st.sidebar.text_input("валидировать по ИНН", key="inn_input")
    # st.sidebar.button("Отобразить", key="process_button", on_click=update_map)

    update_map()
    # geodata = create_supply_chains('', min_threshold, max_threshold)

    # avg_latitude = ((geodata.lat + geodata.lat2)/2).sum() / len(geodata)
    # avg_longtitude = ((geodata.lon + geodata.lon2)/2).sum() / len(geodata)

    # geodata = pd.DataFrame({
    #     "lon": [],
    #     "lat": [],
    #     "lon2": [],
    #     "lat2": []
    # })

    
    # st.pydeck_chart(
    #     pdk.Deck(
    #         map_style="mapbox://styles/mapbox/light-v9",
    #         initial_view_state={
    #                 "latitude": avg_latitude,
    #                 "longitude": avg_longtitude,
    #                 "zoom": 5,
    #                 "pitch": 50,
    #             },
    #         layers=basic_layer(geodata),
    #         )
    #     )
    


if os.path.exists(os.path.join(config["download_folder"], config["geochain_filename"])):
    page1_gui()
else:
    empty_page()
 