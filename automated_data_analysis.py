from weasyprint import HTML
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from jinja2 import Environment, FileSystemLoader, PackageLoader,select_autoescape
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("in", help="input of data")
parser.add_argument("out", help="output of data")
args = parser.parse_args()


df = pd.read_csv("/home/monika/Pulpit/Analiza ML Deep L/data092020.csv", low_memory=False)

columns = df.columns
new_columns_names={}

for column in columns:
    new_columns_names[column]=column.split()[-1].lower()

df=df.rename(columns=new_columns_names)

def drop_txt(value):
    try:
        return int(value)
    except:
        return None

values=df['value'].apply(drop_txt)
df['value'] = values

def get_month_from_date(var):
    try:
        return var.split("/")[1]
    except:
        return None

data_temp = df['date'].apply(get_month_from_date)
df['month']=data_temp
df['sales']=1

df=df.drop(columns=['street','city','zip','name', 'name', 'email', 'number'])
df=df.dropna()

condition =df['date'].str.endswith('19')
df_19=df[condition]
pt_sales = df_19.pivot_table(index='month', values =['sales', 'value'], aggfunc={'sales':'sum', 'value':'sum'})
pt_sales['value']/=100
plot = pt_sales.plot(title='Volume and sales revenue in 2019', kind='bar')
fig = plot.get_figure()
fig.savefig('/home/monika/Pulpit/Analiza ML Deep L/fig019.png', transparent = True)

condition_09 =df['date'].str.endswith('09/19')
df_09_19=df[condition_09]
# print(df_09_19.shape)
# print(df_09_19.isnull().sum())
# print(df_09_19.dropna())
pt_category_09 = df_09_19.pivot_table(index='category', values ='value', aggfunc='sum')
pt_category_09=pt_category_09.sort_values(by='value', ascending=False)
plot_cat =pt_category_09.plot(title='Sales volume in September 2019', kind='bar')
fig = plot_cat.get_figure()
fig.savefig('/home/monika/Pulpit/Analiza ML Deep L/fig192019.png')

templete_vars = {
    'pt_value': pt_sales.to_html(classes='data1'),
    'pt_category': pt_category_09.to_html(classes='data2'),
}
env = Environment(loader=FileSystemLoader("/home/monika/Pulpit/Analiza ML Deep L"))
template = env.get_template("template.html")
html_out=template.render(templete_vars)
HTML(string=html_out, base_url="/home/monika/Pulpit/Analiza ML Deep L").write_pdf(args.out)