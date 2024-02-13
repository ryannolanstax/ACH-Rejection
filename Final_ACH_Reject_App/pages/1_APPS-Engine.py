#python-test % python3 -m streamlit run Carlos_App/pages/test_streamlit.py 

#Combine up to 7 of the spreadsheets together at once
#for our initial merge make sure that there is a new collumn that says matched_settlement_id


#NEEDS TO BE PUSHED _X is Removed


import pandas as pd
import streamlit as st
import base64
import openpyxl

def remove_suffix(column_name):
    if column_name.endswith('_x'):
        return column_name[:-2]
    return column_name

def merge_csv_files(engine_df, open_tickets_df, previous_day_df):
  #  engine_df_filtered = engine_df[engine_df['is_reattempted'] == False]
    #drop column now as its junk
    engine_df.drop(columns=['is_reattempted'], inplace=True)
    engine_df_filtered = engine_df[engine_df['is_reattempt'] == False]
 #   engine_df_filtered.rename(columns={'is_reattempt': 'is_reattempted'}, inplace=True)
    engine_df_filtered.rename(columns={'is_reattempted': 'is_reattempt'}, inplace=True)

    engine_df_filtered['matched_id'] = 'No'

    merged_df = pd.merge(engine_df_filtered, open_tickets_df, left_on='merchant_id', right_on='stax_id', how='left')

    merged_df.loc[merged_df['merchant_id_y'].notnull(), 'matched_id'] = 'Yes'
    merged_df.drop(['merchant_id_y', 'stax_id'], axis=1, inplace=True)

    merged_df['settlement_match'] = 'No'

    merged_df.loc[merged_df['company_state'] == 'RISKHOLD', 'settlement_match'] = 'Yes'
    merged_df.loc[merged_df['company_state'] == 'RISKHOLD', 'matched_id'] = 'Yes'

    merged_withsettlements = pd.merge(merged_df, previous_day_df, left_on='settlement_id', right_on='settlement_id', how='left')

    merged_withsettlements.loc[merged_withsettlements['brand_name_y'].notnull(), 'settlement_match'] = 'Yes'


   

    specific_column_name = 'settlement_match'

    # Get the index of the specific column
    column_index = merged_withsettlements.columns.get_loc(specific_column_name)

    # Select columns up to the specific column and drop the rest to the right
    columns_to_drop = merged_withsettlements.columns[column_index + 1:]
    merged_withsettlements.drop(columns=columns_to_drop, inplace=True)


    # Select columns A-T
    merged_withsettlements = merged_withsettlements.iloc[:, :20]  # Assuming columns A-T are columns 0-19
    merged_withsettlements.drop_duplicates(inplace=True)


    # Rename columns by removing '_x' suffix and flipping them
    new_columns = [remove_suffix(col) for col in merged_withsettlements.columns]
    merged_withsettlements.columns = new_columns

    return merged_withsettlements # merged_withsettlements 


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



#merchant_id	brand_name	business_legal_name	business_dba	updated_at	payout_id	settlement_id	type	amount	reference_number	status_reason	description	company_state	processor_name	CONCAT("'",o.processor_mid)	processor_ach_mid	is_reattempted	matched id	ticket id	settlement match
#brand_name_x	business_legal_name_x	business_dba_x	updated_at_x	payout_id_x	settlement_id	type_x	amount_x	reference_number_x	status_reason_x	description_x	company_state_x	processor_name_x	CONCAT("'",o.processor_mid)_x	processor_ach_mid_x	is_reattempted_x	matched_id	ticket_id	settlement_match
