# Supermarket Sales Data Analysis & Visualization

## Repository Outline
README.md - Dokumentasi dan penjelasan umum project

Supermarket_Sales_DAG.py - DAG Airflow untuk ekstraksi, cleaning, dan load data

Supermarket_Sales_GX.ipynb - Notebook validasi data menggunakan Great Expectations

Supermarket_Sales_data_raw.csv - Dataset mentah hasil ekstraksi dari PostgreSQL

Supermarket_Sales_data_clean.csv - Dataset hasil proses cleaning


## Problem Background
Supermarket menghasilkan data transaksi setiap hari dalam jumlah besar, mulai dari informasi pelanggan, produk, hingga metode pembayaran. Tanpa pengelolaan dan analisis yang baik, data tersebut sulit dimanfaatkan untuk pengambilan keputusan bisnis. Oleh karena itu, dibutuhkan sebuah data pipeline yang mampu mengelola data secara terstruktur, memastikan kualitas data tetap terjaga, serta menyajikan insight yang mudah dipahami melalui visualisasi.

## Project Output
- **Data pipeline otomatis** menggunakan Apache Airflow
- **Validasi kualitas data** menggunakan Great Expectations
- **Dashboard visualisasi** pada Kibana untuk melihat insight penjualan supermarket
- Dataset yang telah melalui proses ekstraksi, pembersihan, dan validasi

## Data
Dataset yang digunakan adalah **Supermarket Sales**, yang berisi data transaksi penjualan supermarket.
Informasi data:
- Berisi informasi transaksi seperti invoice, branch, customer type, product line, quantity, total sales, payment method, dan rating
- Data bersifat tabular dan terstruktur
- Digunakan sebagai sumber utama untuk analisis penjualan dan perilaku pelanggan

Sumber data: dataset penjualan supermarket (public dataset).

## Method
Metode yang digunakan dalam project ini adalah data engineering dan data analytics pipeline, yang mencakup:
1. Ekstraksi data dari PostgreSQL
2. Validasi kualitas data menggunakan Great Expectations
3. Pembersihan dan standarisasi data
4. Load data ke Elasticsearch
5. Visualisasi data menggunakan Kibana

## Stacks
Tools dan teknologi yang digunakan dalam project ini antara lain:
- **Bahasa Pemrograman**: Python
- **Database**: PostgreSQL
- **Workflow Orchestration**: Apache Airflow
- **Data Validation**: Great Expectations
- **Search & Analytics Engine**: Elasticsearch
- **Visualization**: Kibana
- **Containerization**: Docker & Docker Compose
- **Library Python**: pandas, psycopg2, elasticsearch


## Reference
- Apache Airflow Documentation  
  https://airflow.apache.org/docs/
- Great Expectations Documentation  
  https://greatexpectations.io/docs/
- Elasticsearch & Kibana Documentation  
  https://www.elastic.co/guide/index.html
- Dataset Supermarket Sales (Public Dataset)  
  https://github.com/vnaumq/supermarket_sales/blob/main/supermarket_sales.csv