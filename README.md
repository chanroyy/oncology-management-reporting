\# Oncology Management Reporting Dashboard

\## Technical Report



\[Read the full technical report (PDF)](report/Oncology\_Technical\_Report.pdf)

\## Project Overview



An end-to-end healthcare management reporting prototype

designed to demonstrate Python-based ETL, SQL data

management, operational KPI reporting, and interactive

data visualization in an oncology setting.



\## Objectives



\- Develop a reproducible Python ETL pipeline.

\- Validate and integrate structured appointment data.

\- Calculate operational KPIs using SQL.

\- Support management reporting through an interactive dashboard.

\- Ensure data quality through automated testing.



\## Technology Stack



\- Python

\- SQLite

\- SQL

\- pandas

\- Streamlit

\- unittest

\- Git and GitHub



\## System Architecture



Synthetic CSV Data

&#x20;   -> Python Extraction and Validation

&#x20;   -> SQLite Database

&#x20;   -> SQL Management Reporting

&#x20;   -> Streamlit Dashboard



\## Dataset



The project uses 500 synthetic oncology appointment records

across four departments:



\- Medical Oncology

\- Radiation Oncology

\- Hematology

\- Surgical Oncology



\## Reporting Results



| Key Performance Indicator | Result |

|---|---:|

| Total appointments | 500 |

| Completed appointments | 388 |

| Completion rate | 77.6% |

| Cancelled appointments | 61 |

| Cancellation rate | 12.2% |

| No-show appointments | 51 |

| No-show rate | 10.2% |



\## Dashboard Features



\- Interactive department filtering

\- Operational KPI cards

\- Appointment status visualization

\- Department-level activity reporting

\- Monthly appointment trends

\- Filtered CSV report export



\## Data Quality and Testing



The ETL pipeline validates appointment identifiers,

dates, department names, and appointment statuses.



Database upserts prevent duplicate appointment records

when the pipeline is executed repeatedly.



All four automated tests passed:



\- Synthetic data validation

\- Duplicate identifier rejection

\- Invalid status rejection

\- Idempotent database loading



\## Installation and Usage



Install dependencies:



&#x20;   python -m pip install -r requirements.txt



Generate synthetic data:



&#x20;   python generate\_data.py



Execute the ETL pipeline:



&#x20;   python etl\_pipeline.py



Generate SQL management reports:



&#x20;   python reporting.py



Run automated tests:



&#x20;   python -m unittest -v test\_etl.py



Launch the dashboard:



&#x20;   python -m streamlit run dashboard.py



\## Project Files



\- generate\_data.py: Synthetic dataset generation

\- etl\_pipeline.py: Data validation and database loading

\- reporting.py: SQL-based management reporting

\- dashboard.py: Interactive Streamlit dashboard

\- test\_etl.py: Automated ETL tests

\- requirements.txt: Python dependencies



\## Limitations and Future Development



This project is an educational reporting prototype.



Potential extensions include:



\- Microsoft SQL Server integration

\- Qlik Sense dashboard integration

\- Integration of multiple data sources

\- Expanded relational data modeling

\- Automated scheduled reporting

\- Role-based access controls



The November reporting period contains only one day

of possible appointment activity and should not be

compared directly with complete months.



\## Data Privacy



All appointment and patient identifiers are fictional.

No real patient information or confidential hospital

data is used.



This project is not intended for clinical use.



\## Author



Chandrae Roy



M.Sc. Data Science

TU Dortmund University, Germany

