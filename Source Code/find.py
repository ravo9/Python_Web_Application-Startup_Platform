from flask import Flask
import json
import data
import sqlite3


def find_all_matching(phrase, min_investment, max_investment):
  conn = sqlite3.connect('data/data.db')
  c = conn.cursor()
  results = []
  phrase = '%' + phrase + '%'
  c.execute('select * from circles where (desc like ? or title like ?) and (investment_value between ? and ?)',(phrase, phrase, min_investment, max_investment,))
  for row in c:
    results.append(row)
  conn.close()
  if results == None:
    results = []
  return results


