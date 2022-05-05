FROM python:3.7
WORKDIR /usr/src/personalised_nudges
COPY ./app ./app
COPY company_A.json company_A.json
COPY company_B.csv company_B.csv
COPY company_A_products.csv company_A_products.csv
COPY company_B_subset.csv company_B_subset.csv
COPY company_A_products_subset.csv company_A_products_subset.csv
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt