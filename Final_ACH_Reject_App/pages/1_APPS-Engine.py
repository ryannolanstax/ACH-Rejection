#python3 -m streamlit run Carlos_App/pages/testing_5_16.py 

import pandas as pd
import streamlit as st
import base64
import openpyxl
from auth_utils import require_auth, get_user_info
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

if require_auth("Your Page Title"):
    # Your protected page content goes here
    user_info = get_user_info()

	
	
	def remove_suffix(column_name):
	    if column_name.endswith('_x'):
	        return column_name[:-2]
	    return column_name
	
	def merge_csv_files(engine_df, open_tickets_df, previous_day_df):
	
	    engine_df.drop(columns=['is_reattempted'], inplace=True)
	    engine_df_filtered = engine_df[engine_df['is_reattempt'] == False]
	    engine_df_filtered.rename(columns={'is_reattempted': 'is_reattempt'}, inplace=True)
	
	    engine_df_filtered = engine_df_filtered.add_suffix('_engine')
	    open_tickets_df = open_tickets_df.add_suffix('_tickets')
	    previous_day_df = previous_day_df.add_suffix('_previous_day')
	
	    merged_df = pd.merge(engine_df_filtered, open_tickets_df, left_on='merchant_id_engine', right_on='stax_id_tickets', how='left', suffixes=('_engine', '_tickets'))
	    merged_withsettlements = pd.merge(merged_df, previous_day_df, left_on='merchant_id_engine', right_on='merchant_id_previous_day', how='left')
	
	    merged_withsettlements['matched_id'] = 'No'
	    merged_withsettlements.loc[(merged_withsettlements['merchant_id_engine'] == merged_withsettlements['merchant_id_previous_day']), 'matched_id'] = 'Yes'
	
	    merged_withsettlements['matched_settlement'] = merged_withsettlements['settlement_id_engine'].isin(merged_withsettlements['settlement_id_previous_day']).map({True: 'Yes', False: 'No'})
	
	
	    #columns_to_drop = ['ticket_id_tickets', 'merchant_id_tickets', 'stax_id_tickets', 'merchant_id_previous_day', 'brand_name_previous_day', 'business_legal_name_previous_day', 'business_dba_previous_day', 'updated_at_previous_day', 'payout_id_previous_day', 'settlement_id_previous_day', 'type_previous_day', 'amount_previous_day', 'reference_number_previous_day', 'status_reason_previous_day', 'description_previous_day', 'company_state_previous_day', 'processor_name_previous_day', 'CONCAT("'",o.processor_mid)_previous_day', 'processor_ach_mid_previous_day', 'is_reattempt_previous_day', 'matched_id_previous_day', 'ticket_id_previous_day', 'settlement_match_previous_day', 'Risk Action_previous_day']
	    merged_withsettlements.drop(merged_withsettlements.columns[19:41], axis=1, inplace=True)
	
	    columns_to_drop = ['merchant_id_tickets']
	    merged_withsettlements.drop(columns=columns_to_drop, inplace=True)
	
	    merged_withsettlements.columns = merged_withsettlements.columns.str.replace('_engine', '')
	    merged_withsettlements.columns = merged_withsettlements.columns.str.replace('_tickets', '')
	
	    ticket_id_column = merged_withsettlements.pop('ticket_id')
	    merged_withsettlements.insert(merged_withsettlements.columns.get_loc('matched_id') + 1, 'ticket_id', ticket_id_column)
	
	    merged_withsettlements.drop_duplicates(inplace=True)
	
	#still working here
	 #   merged_withsettlements["processor_mid_concatenated"] = merged_withsettlements["o.processor_mid"].apply(lambda x: f"'{x}'")
	
	
	    final_columns = [
	    'merchant_id',
	    'brand_name',
	    'business_legal_name',
	    'business_dba',
	    'updated_at',
	    'payout_id',
	    'settlement_id',
	    'type',
	    'amount',
	    'reference_number',
	    'status_reason',
	    'description',
	    'company_state',
	    'processor_name',
	    "processor_mid_concatenated",
	    'processor_ach_mid',
	    'is_reattempt',
	    'matched_id_previous_day',
	    'ticket_id_previous_day',
	    'matched_settlement_previous_day',
	    'Risk Action_previous_day',
	    'matched_id',
	    'ticket_id',
	    'matched_settlement'
	]
	  
	    # Assuming merged_withsettlements is your DataFrame
	    merged_withsettlements = merged_withsettlements.loc[:, final_columns]
	
	
	    merged_withsettlements = merged_withsettlements.drop_duplicates()
	
	
	    #new line added 5 17
	    merged_withsettlements = merged_withsettlements.drop_duplicates(subset=['payout_id', 'settlement_id'], keep='last')
	
	
	
	
	
	
			
	
	
	
	    #drop duplicates
	
	
	
	
	
	   # 
	    #good through here
	
	 #   merged_withsettlements = pd.merge(merged_df, previous_day_df, left_on='merchant_id_x', right_on='merchant_id', how='outer')
	 #   merged_withsettlements['settlement_match'] = 'No'
	   # merged_withsettlements.loc[(merged_df['merchant_id_y'].notnull()) | (merged_df['payout_id_y'].notnull()), 'matched_id'] = 'Yes'
	   # merged_withsettlements.loc[merged_df['company_state'] == 'RISKHOLD', 'settlement_match'] = 'Yes'
	
	#previous day has merchant id
	
	
	
	
	
	    
	 #   merged_df.drop(['merchant_id_y', 'stax_id'], axis=1, inplace=True)
	
	 #   merged_df['settlement_match'] = 'No'
	
	 #   merged_df.loc[merged_df['company_state'] == 'RISKHOLD', 'settlement_match'] = 'Yes'
	 #   merged_df.loc[merged_df['company_state'] == 'RISKHOLD', 'matched_id'] = 'Yes'
	
	    
	
	 #   merged_withsettlements.loc[merged_withsettlements['brand_name_y'].notnull(), 'settlement_match'] = 'Yes'
	
	    return merged_withsettlements
	 #   return merged_df
	#    return previous_day_df
	
	
	
	def main():
	    st.title("Stax Engine Daily Report Builder")
	
	    st.header("Upload CSV Files")
	
	    st.write("Stax Engine Daily CSV Download  [link](https://app.mode.com/editor/fattmerchant/reports/2fcbf2f57767/queries/8cf6ab01968f)")
	    engine_df = st.file_uploader("Upload Daily Stax Engine CSV file", type=['csv'], key='StaxEngine')
	
	    st.write("Current Open Tickets CSV Download [link](https://app.mode.com/editor/fattmerchant/reports/c80539741d0e/queries/5a6857e8df40)")
	    open_tickets_df = st.file_uploader("Upload Current Tickets CSV File", type=['csv'], key='CurrentTicket')
	
	    st.write("Upload Previous Day CSV")
	    previous_day_files = st.file_uploader("Upload up to 10 Previous Day XLSX Files", accept_multiple_files=True, type=['xlsx'], key='PastTicket')
	
	    if engine_df is not None and open_tickets_df is not None and previous_day_files is not None:
	        engine_df = pd.read_csv(engine_df)
	        open_tickets_df = pd.read_csv(open_tickets_df)
	        
	        previous_day_df = pd.DataFrame()
	        for file in previous_day_files:
	            file_df = pd.read_excel(file)
	            previous_day_df = pd.concat([previous_day_df, file_df])
	
	        if st.button('Merge CSV Files'):
	            merged_data = merge_csv_files(engine_df, open_tickets_df, previous_day_df)
	            st.markdown(get_table_download_link(merged_data), unsafe_allow_html=True)
	
	def get_table_download_link(df):
	    csv = df.to_csv(index=False)
	    b64 = base64.b64encode(csv.encode()).decode()
	    href = f'<a href="data:file/csv;base64,{b64}" download="merged_data.csv">Download Merged CSV File</a>'
	    return href
	
	if __name__ == "__main__":
	    main()
