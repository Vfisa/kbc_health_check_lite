#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 13:14:11 2022

@author: ondrejsvoboda
"""

import streamlit as st
import plotly.express as px

def add_project_checkboxes(all_projects, projects_df, org_selected):
#    use checkboxes for quick filtering
    chboxes = []
    
    if st.session_state.get('last_org_selected', 'NA') != st.session_state['org_selected']:
        st.session_state.pop('projects_selected', None)
    
    if 'projects_selected' in st.session_state:
        for i, project in enumerate(set(all_projects)):
            # the project is selected
            if project in st.session_state['projects_selected']:
                chboxes.append((st.checkbox(project, value=True), project))
            else:
                chboxes.append((st.checkbox(project, value=False), project))
    else:
        for i, project in enumerate(set(all_projects)):
            chboxes.append((st.checkbox(project, value=True), project))
   
    projects_selected = []
    for box, project_name in chboxes:
        if box:
            projects_selected.append(project_name)
            
    print(f"projects_selected: {projects_selected}")
    selected_project_ids = list(projects_df.loc[projects_df.kbc_project.isin(projects_selected),].index)
    st.session_state['projects_selected'] = projects_selected

    st.session_state['selected_project_ids'] = selected_project_ids
    st.session_state['last_org_selected'] = org_selected
    return selected_project_ids

def breakdown_area_chart(df, x, y, color):
    #fig0 = px.area(df, x="date", y="project_consumption", color='Project')
    fig0 = px.area(df, x=x, y=y, color=color)

    fig0.update_layout(
    #    margin=dict(l=0, r=20, t=10, b=20),
        legend=dict(
        orientation="v",
        yanchor="top",
        xanchor="right",
        x=0.98,
        bgcolor='rgba(0,0,0,0)'
        ),
        width=1000 
    )

    # bold legend
    fig0.for_each_trace(lambda t: t.update(name = '<b>' + t.name +'</b>'))
    return fig0


def ecdf_chart(df, x, y, color):
    fig1 = px.ecdf(df, x=x, y=y, color=color, ecdfnorm=None)
    fig1.update_layout(
        legend=dict(
        orientation="v",
        yanchor="top",
        xanchor="right",
        x=0.98,
        bgcolor='rgba(0,0,0,0)'
        ),
        width=1000 
    )
    return fig1

def scatter_chart(df, x, y, color, trendline="lowess"):
    fig = px.scatter(df, x="date", y=x, color=color, trendline=trendline)

    fig.update_layout(
    #    margin=dict(l=0, r=20, t=10, b=20),
        legend=dict(
        orientation="v",
        yanchor="top",
        #y=1.02,
        xanchor="right",
        x=0.98,
        bgcolor='rgba(0,0,0,0)'
        ),
        width=1000 
        #marker=dict(
        #        size=5,
        #    )
    )
    # bold legend
    fig.for_each_trace(lambda t: t.update(name = '<b>' + t.name +'</b>'))



    # trendline width
    tr_line=[]
    for  k, trace  in enumerate(fig.data):
        if trace.mode is not None and trace.mode == 'lines':
            tr_line.append(k)

    for id in tr_line:
        fig.data[id].update(line_width=4)
        
    return fig