import streamlit as st
import streamlit as st
import openai
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime
from streamlit_chat import message as st_message
import io  
import base64



# Add this line of code to display an image in the sidebar
st.sidebar.image("/home/user/Dataeaze/text2sql_streamlit/dataease-logo.png", width=200)  # Replace "your_image_path.jpg" with the actual image path

# st.markdown('<h1 style="color: blue;">DZ Data Assistant</h1>', unsafe_allow_html=True)

st.title("DZ Data Assistant")

# Set your OpenAI API key here
openai.api_key = "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"



# Replace 'your_database.db' with the path to your SQLite database file
conn = sqlite3.connect('chat.db')
cursor = conn.cursor()

# Set the table name directly
table_name = 'orders'
 
    
def generate_sql_query(schema, question, table_name):
    prompt = f"Generate a SQL query using the following schema:\n{schema}\nQuestion: {question}\nTable:{table_name}\n, SQL Query format : select ....; "
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the chat model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        # prompt = prompt,
        max_tokens = 500,
        stop = None,
    )
    print(response)  # Print the response to inspect its structure
    return response.choices[0].message["content"].strip()


def execute_sql_query(sql_query):
    cursor.execute(sql_query)
    result_df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    return result_df

def generate_summary(result_df):
    result_csv_text = result_df.to_csv(index=False)
    # prompt = f"Generate a summary of a data in result_df"
    # prompt = f"Summarize the sales data:\n{result_csv_text}"

    
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",  # Use the chat model
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": prompt},
    #     ],
    #     max_tokens=100,  # Adjust this value for the desired length of the summary
    #     stop=None  # You can specify stop words to control the summary
    # )
    
    # return response.choices[0].message["content"].strip()
    prompt = f"Perform a comprehensive business analysis on the provided CSV data. Extract meaningful insights, identify trends, and make data-driven recommendations etc that can enhance business performance, response in maximum 20-50 words\n{result_csv_text} "

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", # Use the chat model
    messages=[
    {"role": "system", "content": "You are business analyst give anslysis on csv data"},
    {"role": "user", "content": prompt},
    ],
    max_tokens=100, # Adjust this value for the desired length of the summary
    stop=None # You can specify stop words to control the summary
    )

    return response.choices[0].message["content"].strip()


def run(question):
    try:
        # Get the schema of the selected table
        cursor.execute(f"PRAGMA table_info({table_name})")
        schema = cursor.fetchall()
        schema = [column[1] for column in schema]

        # # Generate SQL Query
        # sql_query = generate_sql_query(schema, question, table_name)
        # # st.subheader("Generated SQL Query:")
        # # st.code(sql_query, language='sql')

        # # Execute the SQL query on the selected table
        # result_df = execute_sql_query(sql_query)

        # st.session_state.result_df = result_df


        # # Store the result DataFrame in session state
        # st.session_state.result_df = result_df
        # # st.session_state.table = table

        # # Store the result DataFrame in tabular format
        # result_csv = result_df.to_csv(index=False)

        # st.session_state.history.append({"message": question, "is_user": True})
        # st.session_state.history.append({"message": sql_query, "is_user": False})
        # st.session_state.history.append(
        #     {"message": result_csv, "is_user": False, "is_table": True})  # Store the CSV in tabular format
        
        # Generate SQL Query
        new_response = generate_sql_query(schema, question, table_name)

        if new_response:
            sql_query = new_response
            for i in range(4):
                print('########################################Attempt', i, '#################################')
                try:
                    print(sql_query)
                    result_df = execute_sql_query(sql_query)  # Replace some_order_id with the actual value
                    break
                except  Exception as e:
                    if i == 3:
                        response = "Could not create SQL query for this."
                        break
                    else:
                        prompt = "SQL query : " + sql_query + ' ' + str(
                            e) + ", give query only dont give other description " + 'table schema is : ' + str(
                            schema) + " response format must be : SELECT ..... ;  "
                        # Ask OpenAI for an SQL query
                        print('########response##########\n', prompt)
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",  # Use the chat model
                            messages=[
                                {"role": "system",
                                 "content": "Provide correct sql quesry for asked question , response format: select ... ;"},
                                {"role": "user", "content": prompt},
                            ],
                            # prompt = prompt,
                            max_tokens=500,
                            stop=None,
                        )

                        new_response = response.choices[0].message["content"].strip()

                        print('#########formatted_response#########\n', new_response)

                        # Set the raw_query to the formatted response
                        sql_query = new_response

        # Store the result DataFrame in session state

        st.session_state.result_df = result_df

        # Store the result DataFrame in tabular format
        result_csv = result_df.to_csv(index=False)

        st.session_state.history.append({"message": question, "is_user": True})
        st.session_state.history.append({"message": new_response, "is_user": False})
        st.session_state.history.append(
            {"message": result_csv, "is_user": False, "is_table": True})
        
    except Exception as e:
       # Handle the error and call generate_sql_query again with the error message
        # st.error(f"An error occurred: {str(e)}")
        st.session_state.history.append({"message": question, "is_user": True})
        st.session_state.history.append({"message": f"cannot find ans please reframe your question","is_user": False})

        # st.session_state.history.append({"message": f"Error: {str(e)}", "is_user": False})
        # sql_query = generate_sql_query([], f"Error: {str(e)}", table_name)
     
if "history" not in st.session_state:
        st.session_state.history = []
    
if "questions" not in st.session_state:
    st.session_state.questions = []
    
# # Ask a new question and append it to the list
# if prompt := st.chat_input("Ask me a question"):
#     st.session_state.questions.append(prompt)
#     run(prompt)
   

# # Display the list of questions in the sidebar
# st.sidebar.title("Questions Asked")
# selected_question_index = st.sidebar.radio("Select a question to view in history:", st.session_state.questions, index=0)
  

# Initialize a list to store user-generated questions
user_questions = []

# Ask a new question and append it to the list
if prompt := st.chat_input("Ask me a question"):
    st.session_state.questions.append(prompt)
    run(prompt)
    user_questions.append(prompt)  # Add the user's question to the list

# Display the list of questions in the sidebar as hyperlinks
st.sidebar.subheader("Questions Asked")
for i, question in enumerate(st.session_state.questions):
    # Generate a hyperlink for each user-generated question
    question_link = f'<a href="#question_{i}">{question}</a>'
    st.sidebar.write(question_link, unsafe_allow_html=True)

  
if hasattr(st.session_state, 'history') and len(st.session_state.history) > 0:
        # Iterate through the chat history
        for i, chat in enumerate(st.session_state.history):
            if chat.get("is_table"):
                # Display the CSV table as a table
                table = pd.read_csv(io.StringIO(chat["message"]))  # Use io.StringIO
                st.write(table)
                
                download_key = f"Download Table{i}"
                csv_data = st.session_state.result_df.to_csv(index=False).encode()
                st.download_button(
                label="Download CSV",
                data=csv_data,
                key=download_key,
                file_name="result.csv",
                mime="text/csv",
                )


                col1, col2 = st.columns(2)
                selectbox_key = f"selectbox_{i}"

                # Select X parameter
                x_param = col1.selectbox("Select X Parameter", table.columns, key=selectbox_key)

                if len(table.columns) > 0:
                    # Select Y parameters with a default value
                    default_y_param = table.columns[0]  # Select the first column as the default
                    multiselect_key = f"multiselect_{i}"
                    y_params = col2.multiselect("Select Y Parameters", table.columns, default=[default_y_param],
                                                key=multiselect_key)

                    chart_type_key = f"chart_type_{i}"
                    chart_type = st.selectbox("Select Chart Type", ["Line Chart", "Bar Chart", "Scatter Plot"],
                                            key=chart_type_key)
                    if chart_type == "Bar Chart":
                        chart_function = st.bar_chart
                    elif chart_type == "Scatter Plot":
                        chart_function = st.scatter_chart
                    else:
                        chart_function = st.line_chart
                    
                    
                    # Visualize Data without the need to press a button
                    chart_function(table, x=x_param, y=y_params)

                else:
                    st.warning("No columns available for visualization.")
                # generate = f"generate{i}"
                # if st.button("Generate Summary", key=generate):
                if hasattr(st.session_state, 'result_df'):
                        # Generate a summary of the chart
                        result_summary = generate_summary(st.session_state.result_df)

                        # Display the chart summary
                        st.write("Summary:")
                        st.write(result_summary)
                else:
                        st.warning("No data available to generate a summary.")
            else:
                st_message(**chat, key=str(i))  # unpacking
            
             
        