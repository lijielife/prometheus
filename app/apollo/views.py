# from __future__ import print_function
import numpy as np
import pandas as pd
import app.apollo as ap

from pprint import pprint
from flask import Blueprint, render_template

apollo = Blueprint('apollo', __name__)


@apollo.route('/worth/<table>/')
def worth(table):
# 	list = ['prices', 'dividends', 'rates', 'commodities']
# 	dfs = []
#
# 	for item in list:
# 		result, keys, dtype, index = eval('ap.get_%s()' % item)
# 		values = ap.get_values(result, keys)
#
# 		if values:
# 			df = ap.make_df(values, dtype, index)
# 			df = ap.sort_df(df)
# 		else:
# 			df = ap.empty_df()
#
# 		dfs.append(df)

# 	currency_id = id_from_value(table, commodity)
	currency_id = 1
	result, keys = ap.get_transactions()
	data = ap.get_values(result, keys)
	myportfolio = ap.Portfolio(data, currency_id=currency_id)
# 	prices, dividends, rates, commodities = dfs[0], dfs[1], dfs[2], dfs[3]
# 	reinvestments, missing = ap.get_reinvestments(dividends, prices)
	values = myportfolio.calculate_value(prices, rates)
	data = myportfolio.convert_values(values)
	id = 'worth'
	title = 'Net Worth'
	chart_caption = 'Net Worth per Commodity in %s' % table

	if missing:
		chart_caption = '%s (some price data is missing)' % chart_caption
	elif myportfolio.transactions.empty:
		chart_caption = 'No transactions found. Please enter some events or prices.'

	heading = 'View your net worth'
	subheading = (
		'View the net worth of all ETF, Mutual Fund, and Stock '
		'holdings. Prices are taken from the Prices tab and a purchase of 100'
		' shares is assumed for each date a price is given.')

	category = 'Commodity'
	data_label = 'Value in %s' % table

	kwargs = {
		'id': id, 'title': title, 'heading': heading,
		'subheading': subheading, 'columns': data,
		'chart_caption': chart_caption, 'category': category,
		'data_label': data_label}

	return render_template('barchart.html', **kwargs)
