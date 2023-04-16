import streamlit as st
import pandas as pd
import numpy as np
import os
import itertools
import math, random
random.seed = 42
from path import Path
import plotly.graph_objects as go
import plotly.express as px
import base64

# read the data
df = pd.read_csv("metadata_modelnet10.csv")

# function to read the off file
def read_off(file):
    if 'OFF' != file.readline().strip():
        raise('Not a valid OFF header')
    n_verts, n_faces, __ = tuple([int(s) for s in file.readline().strip().split(' ')])
    verts = [[float(s) for s in file.readline().strip().split(' ')] for i_vert in range(n_verts)]
    faces = [[int(s) for s in file.readline().strip().split(' ')][1:] for i_face in range(n_faces)]
    return verts, faces


def visualize_rotate(data):
    x_eye, y_eye, z_eye = 1.25, 1.25, 0.8
    frames=[]

    def rotate_z(x, y, z, theta):
        w = x+1j*y
        return np.real(np.exp(1j*theta)*w), np.imag(np.exp(1j*theta)*w), z

    for t in np.arange(0, 10.26, 0.1):
        xe, ye, ze = rotate_z(x_eye, y_eye, z_eye, -t)
        frames.append(dict(layout=dict(scene=dict(camera=dict(eye=dict(x=xe, y=ye, z=ze))))))
    fig = go.Figure(data=data,
        layout=go.Layout(
            updatemenus=[dict(type='buttons',
                showactive=False,
                y=1,
                x=0.8,
                xanchor='left',
                yanchor='bottom',
                pad=dict(t=45, r=10),
                buttons=[dict(label='Play',
                    method='animate',
                    args=[None, dict(frame=dict(duration=50, redraw=True),
                        transition=dict(duration=0),
                        fromcurrent=True,
                        mode='immediate'
                        )]
                    )
                ])]
        ),
        frames=frames
    )

    return fig
#------------------

def get_design_details(designs):
    des_results = []
    files = []
    for off in designs:
        with open(path/off, 'r') as f:
            verts, faces = read_off(f)

        i,j,k = np.array(faces).T
        x,y,z = np.array(verts).T
        len(x)
        diag = visualize_rotate([go.Mesh3d(x=x, y=y, z=z, color='skyblue', opacity=0.50, i=i,j=j,k=k)])
        des_results.append(diag)
        files.append(f)
    return des_results , files

#--------------------------
# create a download button for the file
def download_button():
    with open(file_path, "rb") as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:model/off;base64,{b64}" download="{file_path.name}">Download file</a>'
        st.markdown(href, unsafe_allow_html=True)

#--------------------------

if __name__ == '__main__':

    path = Path("ModelNet10")
    folders = [dir for dir in sorted(os.listdir(path)) if os.path.isdir(path/dir)]
    classes = {folder: i for i, folder in enumerate(folders)};
    placeholder_image_url = "https://www.pngall.com/wp-content/uploads/10/Drawing-PNG-Image-HD.png"

    # Create a text input for the search bar
    search_term = st.sidebar.text_input("Search for a item")
    all_items = ['bathtub', 'bed','chair','desk','dresser','monitor','night_stand','sofa','table','toilet']
    
    # Create a button for searching
    if st.sidebar.button("Search"):
        st.title("Here are your designs")
        try:
            designs = df[df.loc[:,'class' ] == search_term].iloc[:10, 3]
            # Perform the search
            item_design = get_design_details( designs)
            # Display the search results
            count = 0
            for des,file in zip(item_design[0],item_design[1]) :
                st.plotly_chart(des,use_container_width=True)

                # design text
                txt = path/designs.values[count]
                st.write(txt.split('/')[-1])
                # file_path = path/designs.values[count]
                count+=1
        except Exception as e:
            st.write( 'Item Not Found' )
    else:
        st.title("Hiee! Search an Autocad Design")
        st.image(placeholder_image_url, width=400)

    st.sidebar.write("# **Available items**")
    for itms in all_items:
        st.sidebar.write(itms)
