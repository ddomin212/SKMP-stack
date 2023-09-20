### Description
I wanted to do something a bit more advanced in terms of data then just to read csv files like a monkey, so here it is. The workflow is as follows:
1. A kafka producer sends simulated real-time data, in this case I am just calling the OpenWeatherMap API every 2 second for one of 5 cities.
2. This is sent to the kafka broker, and a kafka consumer parses this data and saves it into a MySQL database.
3. Apache Superset visualizes this data in a pretty looking dashboard, or you can use the streamlit web app, much easier.
Since this would require multiple VMS, Lambda and RDB to run, I just chose to do a local docker-compose, because I'm cheap. The compose takes up about 1GB of RAM, and Superset itself takes about 2GB.
### Instructions
1. Specify the names of the cities you want to show in the dashboard by modifying the `CITIES` variable in `.env` for the `/kafka producer` folder.
2. Run the docker-compose on stack.yml ``` docker-compose -f stack.yml -d ```
3. Using Apache Superset
    * Run superset locally as advised on [their website](https://superset.apache.org/docs/installation/installing-superset-using-docker-compose/#database-dependencies)
    * Click on dashboards, then in the upper right corner "Import Dashboard"
    * Import "superset_dashboard.zip". A new dashboard with the name "Weather Dashboard" should appear.
    * Click on the dashboard, and you should see the data right away if everything is set up correctly.
4. Using Streamlit
    * Go to (localhost:8501)[http://localhost:8501]
    * See dashboard, live life.
### Takeaways
Open-source proves itself once again, Superset is good, but the functionality is not on par with likes of PowerBI or Tableau (although Tableau looks like it's a Windows 7 app).
Installing Spark on docker and trying to connect it to other services is a pain in the a**, so not parallel processing as of yet.
### Issues
* Spark would be nice but I literally cant get it to work because of jar dependencies. I seem to be installing the MySQL connector for jdbc but it just refuses to work, therefore we are regressed back to native python. Spark code is still present inside `spark_processing.py` but it is not used.