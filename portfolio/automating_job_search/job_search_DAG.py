from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

import requests
from datetime import datetime
from bs4 import BeautifulSoup
from random import randint
from time import sleep
import pandas as pd
from sqlalchemy import create_engine

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def search_url(position):
    template = 'https://uk.indeed.com/jobs?q={}&l=United+Kingdom&fromage=1'
    final_url = template.format(position)
    return (final_url)


def get_job(card, search_query):
    atag = card.h2.a
    job_title = atag.get('title')
    job_url = 'https://uk.indeed.com' + atag.get('href')
    company = card.find('span', 'company').text.strip()

    try:
        location = card.find('div', 'recJobLoc').get('data-rc-loc')
    except AttributeError:
        location = '-'

    try:
        job_summary = card.find('div', 'summary').text.strip().replace('\n', ' ')
    except AttributeError:
        job_summary = '-'

    posting_date = datetime.today().strftime('%Y-%m-%d')

    try:
        salary = card.find('span', 'salaryText').text.strip()
    except AttributeError:
        salary = '-'

    # Description. As to get description we have to follow a link:
    desc_template = 'https://www.indeed.com/viewjob?jk={}'

    desc_data_jk = card.get('data-jk')
    description_url = desc_template.format(desc_data_jk)
    response_desc = requests.get(description_url)
    soup_desc = BeautifulSoup(response_desc.text, 'html.parser')

    try:
        job_description = soup_desc.find('div', 'jobsearch-jobDescriptionText').text.strip().replace('\n', ' ')
    except AttributeError:
        job_description = '-'

    job = (job_title, company, location, job_summary, job_description, salary, job_url, posting_date, search_query)

    return (job)


def scraped_to_frame(scraped_jobs):
    job_title = []
    company = []
    location = []
    summary = []
    description = []
    salary = []
    job_url = []
    posting_date = []
    search_query = []

    titles = [job_title, company, location, summary, description, salary, job_url, posting_date, search_query]

    for Jobs in scraped_jobs:
        job_title.append(Jobs[0])
        company.append(Jobs[1])
        location.append(Jobs[2])
        summary.append(Jobs[3])
        description.append(Jobs[4])
        salary.append(Jobs[5])
        job_url.append(Jobs[6])
        posting_date.append(Jobs[7])
        search_query.append(Jobs[8])

    # Creating a Dictionary For all of the Saved Data
    Job_Data = {'job_title': job_title, 'company': company, 'location': location, 'summary': summary,
                'description': description, 'salary': salary, 'job_url': job_url, 'posting_date': posting_date,
                'search_query': search_query}

    return (pd.DataFrame(Job_Data))


def create_dataframe():
    column_names = ['job_title', 'company', 'location', 'summary', 'description',
                    'salary', 'job_url', 'posting_date', 'search_query']
    return (pd.DataFrame(columns=column_names))


# Main Scraper
def main(job_query):
    jobs = []
    # We create the url for the position we are looking for
    url = search_url(job_query)

    # Extracting the data
    while True:
        print(url)
        # Get the html data
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', 'jobsearch-SerpJobCard')

        for card in cards:
            job = get_job(card, job_query)
            jobs.append(job)

        try:
            url = 'https://uk.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
            delay = randint(10, 15)
            sleep(delay)
        except AttributeError:
            break

    job_frame = scraped_to_frame(jobs)

    return (job_frame)


# Scraping (excecute scraper) + removing duplicates
def scrape_and_clean(job_titles):
    general_dataframe = create_dataframe()
    for job in job_titles:
        general_dataframe = general_dataframe.append(main(job))
        general_dataframe.drop_duplicates(subset=['job_url'], inplace=True)
    return (general_dataframe)


def run_scrape_and_db():
    # Etablishing connection with the database
    engine = create_engine('postgresql://****@localhost:****/*****')
    con = engine.connect()

    # Scrape
    final_jobs = scrape_and_clean(['data scientist', 'data engineer', 'data analyst'])

    # Append to the database
    final_jobs.to_sql('jobs', engine, if_exists='append', index=False)

    # Close Connection
    con.close()

def extract_from_db():
    #define today's date to pull today's jobs from the database
    date = datetime.today().strftime('%Y-%m-%d')
    #define the connection to postgres
    engine = create_engine('postgresql://****@localhost:*****/*****')
    #define the query
    query = '''select * 
                from jobs 
                where posting_date = '{}' '''
    #import the data
    df = pd.read_sql_query(query.format(date),
                           con=engine)
    return(df)

def filter_job_descriptions(df):
    #Everthing gets lowercased
    df['description'] = df['description'].str.lower()
    #We filter for python, sql and ml as those are my interests
    python_filter = df['description'].str.contains(("python"))
    sql_filter = df['description'].str.contains(("sql"))
    ml_filter = sql_filter = df['description'].str.contains(("machine learning"))
    #Apply the filters defined above
    desc_filtered = df[(python_filter & sql_filter) | ml_filter]
    #Filter out senior roles
    title_filtered = desc_filtered[~desc_filtered['job_title'].str.contains("Manager|Senior|Lead|Principal")]
    #Final df to be sent will just contain the title, the company and the url
    final_df = title_filtered[['job_title','company','job_url']]
    return(final_df)

def email_filtered_jobs(final_df):
    date = datetime.today().strftime('%Y-%m-%d')
    EMAIL_ADDRESS = "********"
    EMAIL_PASSWORD = '**********'

    msg = MIMEMultipart()

    msg['Subject'] = "{} found jobs".format(date)
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = '*******'

    html = """Hi Adriano,\n\n
            Find attached the jobs found with your desired requirements \n\n
            <html>
              <head></head>
              <body>
                {}
              </body>
            </html>
            """.format(final_df.to_html(index=False))

    part1 = MIMEText(html, 'html')
    msg.attach(part1)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, '**********', msg.as_string())

def main_email_execute():
    df = extract_from_db()
    final_df = filter_job_descriptions(df)
    email_filtered_jobs(final_df)



default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 4, 13, 22, 00),
    'email': ['*******'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=15)
}

dag = DAG(
    dag_id='indeed_scraper_dag',
    default_args=default_args,
    description='Scraping indeed and inputting to database',
    schedule_interval="00 22 * * *",
    catchup=False
)

run_etl = PythonOperator(
    task_id='scrape_and_saveDB',
    python_callable=run_scrape_and_db,
    dag = dag
)

run_email = PythonOperator(
    task_id='load_db_filter_and_email',
    python_callable=main_email_execute,
    dag=dag
)

run_etl >> run_email
