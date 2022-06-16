# Data science portfolio by Adriano Arenas
---

This portfolio contains a few notebooks I have created for data analysis and exploration of machine learning algorithms.

You can also find my Tableau portfolio [here](https://public.tableau.com/profile/adrianoarenas#!/)

## Tender classification based on its text - NLP

Tender categories were analysed based on its title.  Two methods were tried out, classic RNNs (e.g. LSTM, GRU) and BERT, a transformer-based state of the art NLP developed by Google. The notebook can be found [here](https://github.com/adrianoarenas/portfolio/blob/0b707ab622e9d7c50dfb560ff95eba68d07c553c/notebooks/NLP%20-%20Tender%20Classification.ipynb).

## Automating my job search

An ETL process is performed by scraping the internet for jobs of my interest (Data Scientist, Data Analyst and Data Engineer).  Once these jobs have been found, they are saved into a Postgres database hosted in my computer (this data is saved as I will perform further analysis in the future).  Next, the description of the jobs are filtered based on the skills I have and the final filtered dataframe is emailed to me. This process is scheduled to execute daily with Apache Airflow. A more in depth description of this project can be found [here](https://github.com/adrianoarenas/portfolio/tree/main/automating_job_search).

## Churn prediction

EDA is performed to see what attributes seem to affect customer churn the most.  Random Forest Classifier was applied to try predict the churn probability per customer. The notebook with the code can be found [here](https://github.com/adrianoarenas/portfolio/blob/eabc350545763dcc9d0adc0b949d258dbf54ec3a/notebooks/Customer%20Churn.ipynb). An interactive app/dashboard is done where you can manually input the attributes you wish and see how it affects churn in an interactive way found [here](http://adrianoarenas.pythonanywhere.com/dash/). 

## Power Plant Emissions prediction

Exploratory data analysis is performed on data from a power plant.  Classic machine learning algorithm -Random Forest Regression- is applied to predict CO and NOx emissions based on the turbine's parameters and ambient conditions. Feature Importance is extracted from the Random Forest and a new model with the most important features is fit to compare performance. The notebook can be found [here](https://github.com/adrianoarenas/portfolio/blob/c48e5a5ff66efbaf867f67b3a8b16fe545d5fea5/notebooks/Power%20Plant%20-%20Gas%20Emissions%20Prediction.ipynb).
A small dashboard prototype was done with Streamlit to see how the turbine conditions affect the emissions. It can be found [here](https://github.com/adrianoarenas/portfolio/tree/main/notebooks/emissions_pred_dashboard).

