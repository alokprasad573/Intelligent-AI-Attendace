import streamlit as st
from src.databases.db import get_attendance_records
from datetime import datetime
import pandas as pd

def attendance_records():
      
    st.header("Attendance Records")
    teacher_id = st.session_state.get('teacher_data', {}).get('id')
    if not teacher_id:
        st.error("Please login first.")
        return
    
    attendance_data = get_attendance_records(teacher_id)
    if not attendance_data:
        st.error("No attendance records found.")
        return
    
    data = []
    
    for records in attendance_data:
        ts = records.get('timestamp')
        
        data.append({
            "Timestamp Group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
            "Subject Code" : records['subjects']['code'] if records.get('subjects') else "N/A",
            "Subject" : records['subjects']['name'].title() if records.get('subjects') else "N/A",
            "Attendance": records.get('is_present', False)
        })
        
    df = pd.DataFrame(data)
    
    # Group by the session (Timestamp Group) to get attendance stats
    summary = (
        df.groupby(["Timestamp Group", "Time", "Subject Code", "Subject"])
        .agg(
            Present_Count=('Attendance', 'sum'),
            Total_Count=('Attendance', 'count')
        )
        .reset_index()
    )
    
    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(int).astype(str) + " / "
        + summary['Total_Count'].astype(str) + ' Students'
    )

    display_df = (summary.sort_values(by='Timestamp Group', ascending=False)
                  [['Time', 'Subject', 'Subject Code', 'Attendance Stats']])
    
    st.dataframe(display_df, width='stretch', hide_index=True)
