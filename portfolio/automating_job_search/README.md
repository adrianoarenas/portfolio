# Automating my job search
---

This project was inspired by the hours spent looking through job search pages searching for jobs I could apply to with my skills.

This project consists first, on an ETL process, where job searching pages are scraped for Data Scientist, Data Analyst and Data Engineer jobs. 
As of right now, just Indeed is scraped for proof of concept.  Now that the pipeline works correctly I plan on scaling to more pages.  LinkedIn seems to be the page where most jobs are posted on a daily basis, however, ToS forbid scrapping, which can lead to a banned account, so I will skip LinkedIn.

The scraper retrieves Job Title, Company, Location, Job Description, Salary and the Job URL.  All this data is then stored in a PostgresSQL Database hosted in my own computer.  Although the data could be read and analysed on the fly, I store it as I plan on doing further analysis based on the job description and the salary in the future. The file for the scraper and the connection to the database for storage can be found [here](https://github.com/adrianoarenas/portfolio/blob/main/job_search/Scraper.ipynb) (Scraper.ipynb file).

To avoid duplicates, the URLs for the scraper just scrape jobs posted in the last 24 hours.  This was also done so I could apply to the jobs on the same day they were posted.

Once the jobs are scraped, the next step is to analyse its description.  One of the steps that takes the most time while job searching is reading through all the job description and figuring out you dont have the necessary skills to apply.  For this reason, I decided to filter jobs based on some keywords of skills I have (e.g. SQL, Python, Machine Learning, discarding Senior roles, etc).

Once the jobs have been filtered, the program emails a list of the selected jobs (The title, the company and the job URL) to my personal email. The code for this second step can be found [here](https://github.com/adrianoarenas/portfolio/blob/main/job_search/Analyse_jobs_and_email.ipynb) (Analyse_jobs_and_email.ipynb file).

This whole process is executed once a day by Apache Airflow.  The code is scheduled to run at 10pm.  As we scrape jobs posted on the last 24 hours, I am theoretically getting all the jobs posted on that day.

![image](https://user-images.githubusercontent.com/24966827/118402672-d5814080-b662-11eb-949a-c2fe1689556c.png)

The DAG file for Airflow can be found [here](https://github.com/adrianoarenas/portfolio/blob/main/job_search/job_search_DAG.py).

Finally here is an example of how the final job list is received to my email:

![image](https://user-images.githubusercontent.com/24966827/118402743-28f38e80-b663-11eb-9463-ffaa87e693be.png)
