import streamlit as st
from src.databases.db import get_attendance_records
import datetime
import pandas as pd

def attendance_records():
      
    st.header("Attendance Records")
    teacher_id = st.session_state.get('teacher_data', {}).get('id')
    if not teacher_id:
        st.error("Please login first.")
        return
    
    if 'attendance_images' not in st.session_state:
        st.session_state['attendance_images'] = []
        
    attendance_records = get_attendance_records(teacher_id)
    if not attendance_records:
        st.error("No attendance records found.")
        return
    
    data = []
    
    for records in attendance_records:
        ts = records.get('timestamp')
        
        data.append({
            "Timestamp Group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
            "Subject Code" : records['subjects']['code'] if records.get('subjects') else "N/A",
            "Subject " : records['subjects']['name'] if records.get('subjects') else "N/A",
            "Attendance": records.get('is_present', False)
        })
        
    df = pd.Dataframe(data)
    
    summary = {
        df.groupby(["Timestamp Group", "Time", "Subject Code", "Subject", "Attendance"])
        .agg(
            Present_Count = ('is_present', 'sum'),
            Total_Count = ('is_present', 'count')
        )
        .reset_index()
    }
    
    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + " /"
        + summary['Total_Count'].astype(str) + ' Students'
    )

    display_df = ( summary.sort_values(by='Timestamp Group' ,ascending=False)
                  [['Time', 'Subject', 'Subject Code', 'Attendance Stats']]
                  )
    
    st.dataframe(display_df, width='stretch', hide_index=True)
