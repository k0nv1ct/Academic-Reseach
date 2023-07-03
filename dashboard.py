import streamlit as st
import pandas as pd
import altair as alt
import random

st.set_page_config(layout='wide', initial_sidebar_state='expanded') # Set the page layout to wide

# Load the CSV data
df = pd.read_excel("prediction_dataset1.xlsx")

# Set up the sidebar
st.sidebar.title("Academic Dashboard")
user = st.sidebar.radio("Select User", ("Teacher", "Student","Subject-Wise"))

sr = df['Sr. No.']
# Define the semester ranges
semester_ranges = {
    '0':[0,0],
    '3': [1, 72],
    '3 total':[67,72],
    '4': [72, 146],
    '4 total':[140,146],
    '3 and 4': [146,151],
    '5': [151, 232],
    '5 total':[225,232],
    '6': [232, 319],
    '6 total':[312,319],
    '5 and 6': [319,324],
    '7': [324, 405],
    '7 total': [399,405],
    '8': [405, 579],
    '8 total': [473,479],
    '7 and 8': [479,489],
    'Grand Total': [484, 489]
}

subject_ranges = {
    'Applied Mathematics-I ': [1, 11],
    'Discrete Mathematical Structures ': [11, 21],
    'Advanced C Concepts ': [21, 34],
    'Digital Techniques ': [34, 48],
    'Computer Graphics ': [48, 58],
    'Lab-Visual Basic ': [58, 67],
    'Applied Mathematics-II ': [72, 82],
    'Theory of Computation ': [82, 92],
    'Microprocessors ': [92, 106],
    'Data Communication ': [106, 117],
    'Data Structures ': [117, 131],
    'Lab-Object Oriented Design & Programming Through C++ ': [131, 140],
    'Operating System Concepts ': [151, 165],
    'Computer Networks ': [165, 179],
    'System Programming ': [179, 189],
    'Design and Analysis of Algorithm ': [189, 199],
    'Computer Organization ': [199, 209],
    'Lab-Java Programming ': [209, 218],
    'Self Learning-I ': [218, 225],
    'Database Engineering ': [232, 246],
    'Compiler Construction ': [246, 256],
    'Unix Operating System ': [256, 266],
    'Mobile Computing ': [266, 276],
    'Software Engineering ': [276, 286],
    'Lab-Programming in C#.net ': [286, 295],
    'Mini Project ': [295, 304],
    'Self Learning -II ': [304, 312],
    'Advanced Computer Architecture ': [324, 334],
    'Distributed Systems ': [334, 344],
    'Modern Database Systems ': [344, 358],
    'Lab-I (Project Phase-I) ': [358, 367],
    'Lab-II (Python) ': [367, 373],
    'Vocational Training ': [373, 379],
    'Elective-I ': [379, 389],
    'Elective-II ': [389, 399],
    'Management Information System ': [405, 415],
    'Information & Cyber Security ': [415, 429],
    'Lab-I (Web Technology) ': [429, 438],
    'Lab-II (Project Phase-II) ': [438, 447],
    'Lab-III (Open Source Tehnology) ': [447, 453],
    'Elective-III ': [453, 463],
    'Elective-IV ': [463, 473],
}


# Set up the main app
st.title("Academic Dashboard")

if user == "Teacher":
    st.write("Welcome Teacher!")
    chart_type = st.selectbox("Select Chart Type", ["Grades Distribution", "Marks Distribution", "Percentile Distribution", "Density Chart", "Heatmap Chart"])
    semester = st.selectbox("Select Semester", ['0', '3', '3 total' ,'4','4 total','3 and 4', '5','5 total', '6','6 total', '5 and 6','7','7 total', '8','8 total','7 and 8', 'Grand Total'], index=0)
    semester_range = semester_ranges[semester]
    filtered_df = df.iloc[:, semester_range[0]:semester_range[1]]
    non_numeric_columns = [col_name for col_name in filtered_df.columns if not pd.api.types.is_numeric_dtype(filtered_df[col_name])]
    numeric_columns = [col_name for col_name in filtered_df.columns if pd.api.types.is_numeric_dtype(filtered_df[col_name])]
    # Generate a column with numbers from 1 to 200
    y_values = list(range(1, 201))
    filtered_df['Roll No'] = y_values[:len(filtered_df)]
    if chart_type == "Grades Distribution":
        # Display donut chart of non-numeric columns
        for i, col_name in enumerate(non_numeric_columns):
            counts = filtered_df[col_name].value_counts()
            chart_data = pd.DataFrame({
                'index': counts.index,
                'count': counts.values
            })
            chart = alt.Chart(chart_data).mark_arc().encode(
                theta='count',
                color='index',
                tooltip=[alt.Tooltip('index'), alt.Tooltip('count')]
            ).properties(
                width=250,
                height=250,
                title=alt.TitleParams(text=col_name[:15], subtitle=[col_name[15:]], fontSize=12)
            )
            if i % 4 == 0:
                cols = st.columns(4)
            cols[i % 4].altair_chart(chart)

    elif chart_type == "Marks Distribution":
        # Display scatter plot of numeric columns
        #st.write(filtered_df)
        for i, col_name in enumerate(numeric_columns):
            #if col_name != "Grade":
            chart = alt.Chart(filtered_df).mark_circle(size=60).encode(
                x=col_name,
                y=alt.Y('Roll No:Q', scale=alt.Scale(domain=(1, 200)), title='Roll No'),
                tooltip=[alt.Tooltip(col_name), alt.Tooltip('Roll No')] # Update the Y-axis encoding to display the index
            ).properties(
                width=250,
                height=250,
                title=alt.TitleParams(text=col_name[:15], subtitle=[col_name[15:]], fontSize=12)
            )
            if i % 4 == 0:
                cols = st.columns(4)
            cols[i % 4].altair_chart(chart)

    elif chart_type == "Percentile Distribution":
        # Display box plot of numeric columns
        for i, col_name in enumerate(numeric_columns):
            if col_name != "Grade":
                chart = alt.Chart(filtered_df).mark_boxplot().encode(
                    y=col_name,
                    tooltip=[alt.Tooltip(col_name)]
                ).properties(
                    width=250,
                    height=250,
                    title=alt.TitleParams(text=col_name[:15], subtitle=[col_name[15:]], fontSize=12)
                )
                if i % 4 == 0:
                    cols = st.columns(4)
                cols[i % 4].altair_chart(chart)
    
    elif chart_type == "Density Chart":
        # Display density chart of numeric columns
        for i, col_name in enumerate(numeric_columns):
            if col_name != "Grade":
                chart_data = pd.DataFrame({
                    'value': filtered_df[col_name]
                })
                chart = alt.Chart(chart_data).mark_area().encode(
                    x=alt.X('value:Q', bin=alt.Bin(maxbins=50)),
                    y=alt.Y('count()', stack=None),
                    tooltip=[alt.Tooltip('value', format=".2f"), alt.Tooltip('count()', title='Count')]
                ).properties(
                    width=250,
                    height=250,
                    title=alt.TitleParams(text=col_name[:15], subtitle=[col_name[15:]], fontSize=12)
                )
                if i % 4 == 0:
                    cols = st.columns(4)
                    cols[i % 4].altair_chart(chart)

    elif chart_type == "Heatmap Chart":
        # Display heatmap chart of numeric columns
        heatmap_data = pd.melt(filtered_df, id_vars=['Roll No', numeric_columns[0]], value_vars=numeric_columns[1:], var_name='Measure')
        chart = alt.Chart(heatmap_data).mark_rect().encode(
            x=alt.X('Measure', title=None),
            y=alt.Y('Roll No:O', title="Roll No"),
            color=alt.Color('value', scale=alt.Scale(scheme='inferno')),
            tooltip=[alt.Tooltip('Roll No'), alt.Tooltip('Measure'), alt.Tooltip('value')]
        ).properties(
            width=1200,
            height=2500,
            title=alt.TitleParams(text="Heatmap Chart", fontSize=14)
        )
        st.altair_chart(chart)




elif user == "Student":
    st.write("Welcome Student!")
    student_id = st.text_input("Enter Student ID")
    semester = st.selectbox("Select Semester", [None, '3', '3 total' ,'4','4 total','3 and 4', '5','5 total', '6','6 total', '5 and 6','7','7 total', '8','8 total','7 and 8', 'Grand Total'], index = 0)

    # Show the selected data
    chart_type = st.selectbox("Select Chart Type", ["Grades", "Marks", "Distribution","Distribution Histogram"])

    if chart_type == "Grades":
        if student_id and semester:
            student_id = int(student_id) # Convert student_id to integer
            semester_range = semester_ranges[semester]
            filtered_df = df[df['Sr. No.'] == student_id].iloc[:, semester_range[0]:semester_range[1]]
            st.write(f"Showing data for Student ID {student_id} and Semester {semester}")

            # Display non-numeric columns
            non_numeric_columns = [col_name for col_name in filtered_df.columns if not pd.api.types.is_numeric_dtype(filtered_df[col_name])]
            non_numeric_columns_chunked = [non_numeric_columns[i:i+4] for i in range(0, len(non_numeric_columns), 4)]
            for chunk in non_numeric_columns_chunked:
                row = st.columns(4)
                for i, col_name in enumerate(chunk):
                    row[i].write(f"<div style='border: 1px solid #e6e9ef; padding: 10px; margin: 5px;'>{filtered_df[col_name].values[0]}</div>", unsafe_allow_html=True)
                    row[i].markdown(f"<small>{col_name}</small>", unsafe_allow_html=True)

    elif chart_type == "Marks":
        if student_id and semester:
            student_id = int(student_id) # Convert student_id to integer
            semester_range = semester_ranges[semester]
            filtered_df = df[df['Sr. No.'] == student_id].iloc[:, semester_range[0]:semester_range[1]]
            st.write(f"Showing data for Student ID {student_id} and Semester {semester}")

            # Display numeric columns
            numeric_columns = [col_name for col_name in filtered_df.columns if pd.api.types.is_numeric_dtype(filtered_df[col_name])]
            chart_columns = st.columns(4)
            chart_index = 0
            for col_name in numeric_columns:
                mean_score = df[col_name].mean()
                random_color = '#' + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                chart_data = pd.DataFrame({
                    'contrast': ['Student Score', 'Average Score'],
                    'score': [filtered_df[col_name].values[0], mean_score]
                })
                chart = alt.Chart(chart_data).mark_bar().encode(
                    x=alt.X('contrast:N', title='Contrast', axis=alt.Axis(labelFontSize=10)),
                    y=alt.Y('score:Q', title='Score', axis=alt.Axis(labelFontSize=10)),
                    color=alt.Color('contrast:N', scale=alt.Scale(domain=['Student Score', 'Average Score'], range=['blue', 'red'])),
                    tooltip=['contrast:N', 'score:Q']
                ).properties(
                    width=250,
                    height=400,
                    title=alt.TitleParams(text=col_name[:15], subtitle=[col_name[15:]], fontSize=12)
                )

                chart_columns[chart_index % 4].altair_chart(chart)
                chart_index += 1

    elif chart_type == "Distribution":
        if semester:
            semester_range = semester_ranges[semester]
            filtered_df = df.iloc[:, semester_range[0]:semester_range[1]]
            st.write(f"Showing distribution of all rows for Semester {semester}")
        
            # Display box plots of numeric columns
            numeric_columns = [col_name for col_name in filtered_df.columns if pd.api.types.is_numeric_dtype(filtered_df[col_name])]
            chart_columns = st.columns(4)
            chart_index = 0
            for col_name in numeric_columns:
                chart_data = pd.DataFrame({
                    'value': filtered_df[col_name]
                })
                chart = alt.Chart(chart_data).mark_boxplot().encode(
                    y=alt.Y('value:Q', title='Score', axis=alt.Axis(labelFontSize=10))
                ).properties(
                    width=250,
                    height=400,
                    title=alt.TitleParams(text=col_name[:15], subtitle=[col_name[15:]], fontSize=12)
                )

                chart_columns[chart_index % 4].altair_chart(chart)
                chart_index += 1
    
    elif chart_type == "Distribution Histogram":
        if semester:
            semester_range = semester_ranges[semester]
            filtered_df = df.iloc[:, semester_range[0]:semester_range[1]]
            st.write(f"Showing distribution of all rows for Semester {semester}")

            # Display histograms of numeric columns
            numeric_columns = [col_name for col_name in filtered_df.columns if pd.api.types.is_numeric_dtype(filtered_df[col_name])]
            chart_columns = st.columns(4)
            chart_index = 0
            for col_name in numeric_columns:
                chart_data = pd.DataFrame({
                    'value': filtered_df[col_name]
                })
                chart = alt.Chart(chart_data).mark_bar().encode(
                    x=alt.X('value:Q', bin=alt.Bin(step=1), title='Score', axis=alt.Axis(labelFontSize=10)),
                    y=alt.Y('count()', title='Count', axis=alt.Axis(labelFontSize=10)),
                    tooltip=[alt.Tooltip('value:Q', title='Score', format='.2f'), alt.Tooltip('count()', title='Count')]
                ).properties(
                    width=250,
                    height=400,
                    title=alt.TitleParams(text=col_name[:15], subtitle=[col_name[15:]], fontSize=12)
                )

                chart_columns[chart_index % 4].altair_chart(chart)
                chart_index += 1

       
else: 
    st.write("Subject-wise Visualizations")
    student_id = st.text_input("Enter Student ID between 0-199")
    subject = st.selectbox("Select Subject", [None,
    'Applied Mathematics-I ',
    'Discrete Mathematical Structures ',
    'Advanced C Concepts ',
    'Digital Techniques ',
    'Computer Graphics ',
    'Lab-Visual Basic ',
    'Applied Mathematics-II ',
    'Theory of Computation ',
    'Microprocessors ',
    'Data Communication ',
    'Data Structures ',
    'Lab-Object Oriented Design & Programming Through C++ ',
    'Operating System Concepts ',
    'Computer Networks ',
    'System Programming ',
    'Design and Analysis of Algorithm ',
    'Computer Organization ',
    'Lab-Java Programming ',
    'Self Learning-I ',
    'Database Engineering ',
    'Compiler Construction ',
    'Unix Operating System ',
    'Mobile Computing ',
    'Software Engineering ',
    'Lab-Programming in C#.net ',
    'Mini Project ',
    'Self Learning -II ',
    'Advanced Computer Architecture ',
    'Distributed Systems ',
    'Modern Database Systems ',
    'Lab-I (Project Phase-I) ',
    'Lab-II (Python) ',
    'Vocational Training ',
    'Elective-I ',
    'Elective-II ',
    'Management Information System ',
    'Information & Cyber Security ',
    'Lab-I (Web Technology) ',
    'Lab-II (Project Phase-II) ',
    'Lab-III (Open Source Tehnology) ',
    'Elective-III ',
    'Elective-IV '], index = 0)

    # Show the selected data
    chart_type = st.selectbox("Select Chart Type", ["Grades", "Marks", "Distribution","Distribution Line","Distribution Swarm","Distribution Histogram"])

    if chart_type == "Grades":
        if student_id and subject:
            student_id = int(student_id) # Convert student_id to integer
            subject_range = subject_ranges[subject]
            filtered_df = df[df['Sr. No.'] == student_id].iloc[:, subject_range[0]:subject_range[1]]
            st.write(f"Showing data for Student ID {student_id} and Subject {subject}")

            # Display non-numeric columns
            non_numeric_columns = [col_name for col_name in filtered_df.columns if not pd.api.types.is_numeric_dtype(filtered_df[col_name])]
            non_numeric_columns_chunked = [non_numeric_columns[i:i+4] for i in range(0, len(non_numeric_columns), 4)]
            for chunk in non_numeric_columns_chunked:
                row = st.columns(4)
                for i, col_name in enumerate(chunk):
                    row[i].write(f"<div style='border: 1px solid #e6e9ef; padding: 10px; margin: 5px;'>{filtered_df[col_name].values[0]}</div>", unsafe_allow_html=True)
                    row[i].markdown(f"<small>{col_name}</small>", unsafe_allow_html=True)

    elif chart_type == "Marks":
        if student_id and subject:
            student_id = int(student_id) # Convert student_id to integer
            subject_range = subject_ranges[subject]
            filtered_df = df[df['Sr. No.'] == student_id].iloc[:, subject_range[0]:subject_range[1]]
            st.write(f"Showing data for Student ID {student_id} and Subject {subject}")

            # Display numeric columns
            numeric_columns = [col_name for col_name in filtered_df.columns if pd.api.types.is_numeric_dtype(filtered_df[col_name])]
            chart_columns = st.columns(4)
            chart_index = 0
            for col_name in numeric_columns:
                mean_score = df[col_name].mean()
                random_color = '#' + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                chart_data = pd.DataFrame({
                    'contrast': ['Student Score', 'Average Score'],
                    'score': [filtered_df[col_name].values[0], mean_score]
                })
                chart = alt.Chart(chart_data).mark_bar().encode(
                    x=alt.X('contrast:N', title='Contrast', axis=alt.Axis(labelFontSize=10)),
                    y=alt.Y('score:Q', title='Score', axis=alt.Axis(labelFontSize=10)),
                    color=alt.Color('contrast:N', scale=alt.Scale(domain=['Student Score', 'Average Score'], range=['blue', 'red'])),
                    tooltip=['contrast:N', 'score:Q']
                ).properties(
                    width=250,
                    height=400,
                    title=alt.TitleParams(text=col_name[:15], subtitle=[col_name[15:]], fontSize=12)
                )

                chart_columns[chart_index % 4].altair_chart(chart)
                chart_index += 1

    elif chart_type == "Distribution":
        if subject:
            subject_range = subject_ranges[subject]
            filtered_df = df.iloc[:, subject_range[0]:subject_range[1]]
            st.write(f"Showing distribution of all rows for Subject {subject}")
        
            # Display box plots of numeric columns
            numeric_columns = [col_name for col_name in filtered_df.columns if pd.api.types.is_numeric_dtype(filtered_df[col_name])]
            chart_columns = st.columns(4)
            chart_index = 0
            for col_name in numeric_columns:
                chart_data = pd.DataFrame({
                    'value': filtered_df[col_name]
                })
                chart = alt.Chart(chart_data).mark_boxplot().encode(
                    y=alt.Y('value:Q', title='Score', axis=alt.Axis(labelFontSize=10))
                ).properties(
                    width=250,
                    height=400,
                    title=alt.TitleParams(text=col_name[:15], subtitle=[col_name[15:]], fontSize=12)
                )

                chart_columns[chart_index % 4].altair_chart(chart)
                chart_index += 1

    elif chart_type == "Distribution Line":
            if subject:
                subject_range = subject_ranges[subject]
                filtered_df = df.iloc[:, subject_range[0]:subject_range[1]]
                st.write(f"Showing distribution of all rows for Subject {subject}")

                # Display line graphs of numeric columns
                numeric_columns = [col_name for col_name in filtered_df.columns if pd.api.types.is_numeric_dtype(filtered_df[col_name])]
                chart_columns = st.columns(4)
                chart_index = 0
                for col_name in numeric_columns:
                    chart_data = pd.DataFrame({
                        'index': filtered_df.index,
                        'value': filtered_df[col_name]
                    })
                    chart = alt.Chart(chart_data).mark_line().encode(
                        x=alt.X('index:Q', title='Index', axis=alt.Axis(labelFontSize=10)),
                        y=alt.Y('value:Q', title='Score', axis=alt.Axis(labelFontSize=10)),
                        tooltip=[alt.Tooltip('index:Q', title='Index'), alt.Tooltip('value:Q', title='Score', format='.2f')]
                    ).properties(
                        width=250,
                        height=400,
                        title=alt.TitleParams(text=col_name[:15], subtitle=[col_name[15:]], fontSize=12)
                    )

                    chart_columns[chart_index % 4].altair_chart(chart)
                    chart_index += 1

    elif chart_type == "Distribution Swarm":
        if subject:
            subject_range = subject_ranges[subject]
            filtered_df = df.iloc[:, subject_range[0]:subject_range[1]]
            st.write(f"Showing distribution of all rows for Subject {subject}")

            # Display swarm charts of numeric columns
            numeric_columns = [col_name for col_name in filtered_df.columns if pd.api.types.is_numeric_dtype(filtered_df[col_name])]
            chart_columns = st.columns(4)
            chart_index = 0
            for col_name in numeric_columns:
                chart_data = pd.DataFrame({
                    'index': filtered_df.index,
                    'value': filtered_df[col_name]
                })
                chart = alt.Chart(chart_data).mark_circle(size=20, opacity=0.7, stroke='black').encode(
                    x=alt.X('index:Q', title='Index', axis=alt.Axis(labelFontSize=10)),
                    y=alt.Y('value:Q', title='Score', axis=alt.Axis(labelFontSize=10)),
                    color=alt.Color('value:Q', scale=alt.Scale(scheme='viridis')),
                    tooltip=[alt.Tooltip('index:Q', title='Index'), alt.Tooltip('value:Q', title='Score')]
                ).properties(
                    width=250,
                    height=400,
                    title=alt.TitleParams(text=col_name[:15], subtitle=[col_name[15:]], fontSize=12)
                ).interactive()

                chart_columns[chart_index % 4].altair_chart(chart)
                chart_index += 1

    elif chart_type == "Distribution Histogram":
        if subject:
            subject_range = subject_ranges[subject]
            filtered_df = df.iloc[:, subject_range[0]:subject_range[1]]
            st.write(f"Showing distribution of all rows for Subject {subject}")

            # Display histograms of numeric columns
            numeric_columns = [col_name for col_name in filtered_df.columns if pd.api.types.is_numeric_dtype(filtered_df[col_name])]
            chart_columns = st.columns(4)
            chart_index = 0
            for col_name in numeric_columns:
                chart_data = pd.DataFrame({
                    'value': filtered_df[col_name]
                })
                chart = alt.Chart(chart_data).mark_bar().encode(
                    x=alt.X('value:Q', bin=alt.Bin(step=1), title='Score', axis=alt.Axis(labelFontSize=10)),
                    y=alt.Y('count()', title='Count', axis=alt.Axis(labelFontSize=10)),
                    tooltip=[alt.Tooltip('value:Q', title='Score', format='.2f'), alt.Tooltip('count()', title='Count')]
                ).properties(
                    width=250,
                    height=400,
                    title=alt.TitleParams(text=col_name[:15], subtitle=[col_name[15:]], fontSize=12)
                )

                chart_columns[chart_index % 4].altair_chart(chart)
                chart_index += 1


