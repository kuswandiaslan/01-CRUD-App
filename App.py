
# Project ini adalah Aplikasi ToDo List (CRUD) berbasis Streamlit 
# yang memungkinkan user untuk melakukan operasi Create, Read, Update, 
# dan Delete pada data tugas.

# ============================================================
# CRUD TODO APP - MAIN FILE
# ============================================================

import streamlit as st
import pandas as pd 
from db_fxns2 import *  # ✅ PERBAIKAN: Nama file yang benar
import streamlit.components.v1 as stc

# Data Viz Pkgs
import plotly.express as px 
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use('Agg')

# Kegunaan: Memberikan tampilan header yang rapi dan profesional.
HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">ToDo List Application (CRUD)</h1>
    <p style="color:white;text-align:center;">Built with Streamlit</p>
    </div>
"""


# 1. Tampilkan HTML Banner
# 2. Buat sidebar menu dengan 5 pilihan
# 3. Panggil create_table() untuk membuat tabel database
# 4. Berdasarkan pilihan user, jalankan fungsi yang sesuai

def main():
    stc.html(HTML_BANNER)
    menu = ["Create", "Read", "Update", "Delete", "About"]
    choice = st.sidebar.selectbox("Menu", menu)
    create_table()  

    if choice == "Create":
        st.subheader("Add Item")
        col1, col2 = st.columns(2)
        
        with col1:
            task = st.text_area("Task To Do")

        with col2:
            task_status = st.selectbox("Status", ["ToDo", "Doing", "Done"])
            task_due_date = st.date_input("Due Date")

        if st.button("Add Task"):
            add_data(task, task_status, task_due_date)
            st.success(f"Added ::{task} ::To Task")

    elif choice == "Read":
        with st.expander("View All"):
            # memanggil view_all_data() untuk menampilkan semua data dari database
            result = view_all_data()
            # membuat DataFrame dari hasil query result dan mengatur nama kolom
            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
            # menampilkan data ke dalam DataFrame
            st.dataframe(clean_df)

        with st.expander("Task Status"):
            task_df = clean_df['Status'].value_counts().to_frame()
            task_df = task_df.reset_index()
            task_df.columns = ['Status', 'Count']
            st.dataframe(task_df)

            p1 = px.pie(task_df, names='Status', values='Count')
            st.plotly_chart(p1, use_container_width=True)

    elif choice == "Update":
        st.subheader("Edit Items")
        with st.expander("Current Data"):
            result = view_all_data()
            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
            st.dataframe(clean_df)

        list_of_tasks = [i[0] for i in view_all_task_names()]
        selected_task = st.selectbox("Task", list_of_tasks)
        task_result = get_task(selected_task)

        if task_result:
            task = task_result[0][0]
            task_status = task_result[0][1]
            task_due_date = task_result[0][2]

            col1, col2 = st.columns(2)
            
            with col1:
                new_task = st.text_area("Task To Do", task)

            with col2:
                status_options = ["ToDo", "Doing", "Done"]
                status_index = status_options.index(task_status) if task_status in status_options else 0
                new_task_status = st.selectbox("Status", status_options, index=status_index)
                new_task_due_date = st.date_input("Due Date", task_due_date)

            if st.button("Update Task"):
                edit_task_data(new_task, new_task_status, new_task_due_date,
                              task, task_status, task_due_date)
                st.success(f"Updated ::{task} ::To {new_task}")

            with st.expander("View Updated Data"):
                result = view_all_data()
                clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
                st.dataframe(clean_df)

    elif choice == "Delete":
        st.subheader("Delete")
        with st.expander("View Data"):
            result = view_all_data()
            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
            st.dataframe(clean_df)

        unique_list = [i[0] for i in view_all_task_names()]
        delete_by_task_name = st.selectbox("Select Task", unique_list)
        
        if st.button("Delete"):
            delete_data(delete_by_task_name)
            st.warning(f"Deleted: '{delete_by_task_name}'")

        with st.expander("Updated Data"):
            result = view_all_data()
            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
            st.dataframe(clean_df)

    else:
        st.subheader("About ToDo List App")
        st.info("Built with Streamlit")
        st.info("kuswandi14@gmail.com")
        st.info("Kuswandi Aslan")


if __name__ == '__main__':
    main()