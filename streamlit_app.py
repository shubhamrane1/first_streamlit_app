




import streamlit

import pandas

import requests

import snowflake.connector

from urllib.error import URLError

streamlit.title('My Parents new healthy diner');

streamlit.header('Breakfast menu');

streamlit.text('🥣Omega 3 & Blueberry Oatmeal');

streamlit.text('🥗Kale, Spinach & Rocket Smoothie');

streamlit.text('🐔Hard-boiled Free-range Egg');

streamlit.text('🥑Avacade, 🍞Toast');

 

streamlit.header('🍌🥭Build your own smoothie🥝🍇');

my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt");

# Setting the default selection value to fruit

my_fruit_list = my_fruit_list.set_index('Fruit');

 

# Let's put a pick list here so they can pick the fruit they want to include

fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

fruits_to_show=my_fruit_list.loc[fruits_selected];

 

# Display the table on the page.

streamlit.dataframe(fruits_to_show);

 



def get_fruityvice_data(this_fruit_choice):

    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)

    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

    return fruityvice_normalized

 

 

# New section to display Fruityvice API response

streamlit.header("Fruityvice Fruit Advice!")

try:

   fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')

   if not fruit_choice:

     streamlit.error("Please select a fruit to get the information")

   else:

       back_from_function=get_fruityvice_data(fruit_choice)
       streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()
streamlit.write('The user entered ', fruit_choice)
 
# Normalizing the response
# Output it the screen as a table.
# Don't run anything past here while we troubleshoot
# streamlit.stop()
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT * FROM fruit_load_list")
# my_data_rows = my_cur.fetchall()
# button function
streamlit.header("View Your Fruit List")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("Select * from fruit_load_list")
         return my_cur.fetchall()
if streamlit.button('Get fruit list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()

    my_cnx.close()

    streamlit.dataframe(my_data_rows)

 

    


def insert_row_snowflake(new_fruit):

    with my_cnx.cursor() as my_cur:

         my_cur.execute("insert into fruit_load_list values ('guava')");

         my_cur.execute("insert into fruit_load_list values ('papaya')");

         my_cur.execute("insert into fruit_load_list values ('kiwi')");

         my_cur.execute("insert into fruit_load_list values ('jackfruit')");   

         return 'Thanks for adding ', new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to Add?','Jackfruit')

if streamlit.button('Add a fruit to the list'):

    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])

    back_from_function = insert_row_snowflake(add_my_fruit)

    streamlit.text(back_from_function)





