from jql import jql, isint
from decimal import *

def formula(tick):
	Terminal_Growth = Decimal(0.03)
	Risk_free = Decimal(0.032)
	Historical_market = Decimal(0.0846)
	Ke = Risk_free + jql('get','day','beta') * (Historical_market - Risk_free)
	max_is_col = jql('maxcol','income_statement') - 1
	max_is_col_bal = jql('maxcol','balance_sheet') - 1
	rsmc = jql('get','yql_real','smc')
	Debt_level = jql('get','balance_sheet','CurrLTDebt',max_is_col) + jql('balance_sheet','LTDebt',max_is_col_bal)
	Kd = jql('get','income_statement','IntExp',max_is_col) / Debt_level
	TotalDE = Debt_level - jql('get','balance_sheet','Cash',max_is_col_bal) + rsmc

#market cap  = [yql_real(smc)]
#Bottoms up growth rate
	Running_Avg_Total = Decimal(0)
	Running_Avg_Total1 = Decimal(0) 
	Running_Avg_Total2 = Decimal(0) 
	Running_Avg_Total3 = Decimal(0) 
	Running_Avg_Total4 = Decimal(0)  
	Running_Avg_Total5 = Decimal(0) 
	incomeq = jql('gets','income_statement', ['IncTax', 'EBT','COGS','Rev','RnDExp','SGnAExp','Depr','Inv'])
	cashflowq = jql('gets', 'cash_flow', ['ChangePPE'])
	for i in range (0, max_is_col):
		Running_Avg_Total = Running_Avg_Total + incomeq['IncTax'][i] + incomeq['EBT'][i]
		Running_Avg_Total1 = Running_Avg_Total1 + incomeq['COGS'][i] + incomeq['Rev'][i]
		Running_Avg_Total2 = Running_Avg_Total2 + incomeq['RnDExp'][i] + incomeq['Rev'][i]
		Running_Avg_Total3 = Running_Avg_Total3 + incomeq['SGnAExp'][i] + incomeq['Rev'][i]
		Running_Avg_Total4 = Running_Avg_Total4 + incomeq['Depr'][i] + incomeq['Rev'][i]
		Running_Avg_Total5 = Running_Avg_Total5 + cashflowq['ChangePPE'][i] + incomeq['Rev'][i]
	
	Tax_rate = Running_Avg_Total / (max_is_col + 1)
	COGS_perc = Running_Avg_Total1 / (max_is_col + 1)
	RnDExp_perc = Running_Avg_Total2 / (max_is_col + 1)
	SGnAExp_perc = Running_Avg_Total3 / (max_is_col + 1)
	Depr_perc = Running_Avg_Total4 / (max_is_col + 1)
	PPE_perc = Running_Avg_Total / (max_is_col + 1)
	wacc = rsmc/TotalDE * Ke + (Debt_level - balanceq['Cash'][max_is_col_bal])/TotalDE * Kd * (1 - Tax_rate)
	waccq = pow(1+wacc,Decimal(1/4)) - 1


#AP and inventory might have to be as a percentage of COGS
	Running_Avg_Total = Decimal(0) 
	Running_Avg_Total1 = Decimal(0)

	balanceq = jql('gets','balance_sheet', ['Cash','MarketSecur','AR','RawMat','WIP','FinishedG','AP'])
	for i in range (0, max_is_col-1):
		Running_Avg_Total = Running_Avg_Total  + incomeq['Rev'][i]/incomeq['Rev'][i] - 1
		NWC = balanceq['Cash'][i+1] + balanceq['MarketSecur'][i+1] + balanceq['AR'][i+1] + balanceq['Inv'][i+1] + balanceq['RawMat'][i+1] + balanceq['WIP'][i+1] + balanceq['FinishedG'][i+1]-balanceq['AP'][i+1]
		NWC1 = balanceq['Cash'][i] + balanceq['MarketSecur'][i] + balanceq['AR'][i] + balanceq['Inv'][i] + balanceq['RawMat'][i] + balanceq['WIP'][i] + balanceq['FinishedG'][i] - balanceq['AP'][i]
		Running_Avg_Total1 = Running_Avg_Total1 + NWC - NWC1
	BU_GrowthRate = Running_Avg_Total / (max_is_col + 1)
	NWC_perc = Running_Avg_Total1 / (max_is_col + 1)



	PV_FCF = Decimal(0)
#
#	PROBLEM HERE
#
	for i in range (0, max_is_col): # or do you actually want 8?
		Revenue = incomeq['Rev'][max_is_col]*pow((1+BU_GrowthRate),Decimal(i+1))
		Expense = Revenue * (COGS_perc + RnDExp_perc + SGnAExp_perc)
		FCF = (Revenue - Expense) * (1-Tax_rate) + Revenue * (Depr_perc - NWC_perc - PPE_perc)
		PV_FCF = PV_FCF + FCF * pow((1 + waccq), Decimal(-i-1))
	
	Terminal_Val = FCF * (1+ Terminal_Growth)/ (waccq - Terminal_Growth) * pow(1+waccq, Decimal(-8))
	EnterpriseValue = PV_FCF + Terminal_Val
	EquityValue = EnterpriseValue - Debt_level + balanceq['Cash'][max_is_col_bal]
	Num_Share = jql('get','highlight','Rev')/jql('get','highlight','RevPerShare')
	Share_price = EquityValue/Num_Share

	ask_price = jql('get', 'yql_real','ask')

	if ask_price > Share_price:
		print ("TRUE")
#	return True
	else:
#	return False
		print ("False")
