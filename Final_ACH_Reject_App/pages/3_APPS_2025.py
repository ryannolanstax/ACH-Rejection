import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

st.set_page_config(page_title="APPS Rejects Formatter", page_icon="🛍️")

# Title and Instructions
st.title("Days Processing Calculator")
st.write("Upload your APPS and MCC files, and select the month to calculate days processing based on account opening date.")

# File upload for APPS and MCC Sheets
st.write("Accounting Email File (Manual Mode Here:)  [link](https://app.mode.com/fattmerchant/reports/ff1ddaec56d2/runs/9f41f0a13c40)")
accounting_file = st.file_uploader("Upload Accounting Sheet", type=['csv', 'xlsx'])

st.write("APPS Merchants  [link](https://app.mode.com/editor/fattmerchant/reports/44a3ce0e8222/queries/b00942edce21)")
appsos_values_file = st.file_uploader("Upload APPS Merchant Sheet", type=['csv', 'xlsx'])


# Processing data when both files are uploaded
if accounting_file and appsos_values_file:

    output = BytesIO()
    # Load DataFrames
    df = pd.read_excel(accounting_file) if accounting_file.name.endswith('.xlsx') else pd.read_csv(accounting_file)
    appsos_values = pd.read_excel(appsos_values_file) if appsos_values_file.name.endswith('.xlsx') else pd.read_csv(appsos_values_file)



    df2 = df[df['CompanyName'] == 'BANKCRD'].copy()

    df2['TranAmount'] = np.where(df2['DebitCredit'] == 'Credit', df2['TranAmount'] * -1, df2['TranAmount'])

    #CorrectedData if this is not null we need to make a new sheet and remove from normal
    df_corrected_data = df2[df2['CorrectedData'].notna()]
    df3 = df2[df2['CorrectedData'].isnull()]

    df4 = df3.drop(columns=['CompanyID', 'ReturnFlag', 'EDIFlag', 'EffectiveEntryDate', 'SettlementDate', 'OriginatingFileName', 'FileCreationDateTime', 'CompanyName', 'CompanyDiscretionaryData', 'StandardEntryClassCode', 'CompanyDescriptiveDate', 'OriginatorStatusCode', 'OriginatingDFIIdentification', 'ReceivingDFIIdentification', 'CheckDigit', 'CheckSerialNumber', 'DiscretionaryData', 'TraceNumber', 'PaymentTypeCode', 'PaymentRelatedInformation', 'ItemTypeIndicator', 'CardTransactionTypeCode', 'TerminalCity', 'TerminalState', 'CardExpirationDate', 'DocumentReferenceNumber', 'IndividualCardAccountNumber', 'ProcessControlField', 'ItemResearchNumber', 'AddendaTypeCode', 'TransactionDescription', 'NetworkIdentificationCode', 'TerminalIdentificationCode', 'TransactionSerialNumber', 'TransactionDate', 'TransactionTime', 'TerminalLocation', 'ReferenceInformation1', 'ReferenceInformation2', 'TraceNumber_7', 'AuthorizationCodeOrCardExpirationDate', 'TransactionTypeCode', 'ForeignReceivingDFIIdentification', 'ForeignPaymentAmount', 'ForeignTraceNumber', 'ForeignReceiversAccountNumber', 'ChangeCode', 'OriginalReceivingDFIIdentification', 'CorrectedData'])

    def company_description(value):
      if value == 'MERCH DEP':
        return 'MERCH DEP'
      elif value == 'CR CD DEP':
        return 'MERCH DEP'
      elif value == 'DLY FEE S':
        return 'MERCH DEP'
      elif value == 'CCDISCOUNT':
        return 'Month End Fee'
      else:
        return value

    df4['CompanyEntryDescription'] = df4['CompanyEntryDescription'].apply(company_description)

    df4['IdentificationNumber'] = df4['IdentificationNumber'].apply(lambda x: f'6{x}' if pd.notna(x) else x)

    df4['OriginalEntryTraceNumber'] = df4['OriginalEntryTraceNumber'].apply(lambda x: f'0{x}' if pd.notna(x) else x)

    df4 = df4.sort_values(by=['AccountNumber', 'ReceiverName'])

    df5 = pd.merge(df4, appsos_values, left_on='IdentificationNumber', right_on='merchant_id', how='left')

    df6 = df5.drop(columns=['merchant_id'])

    df6['OriginalEntryTraceNumber'] = df6['OriginalEntryTraceNumber'].astype(str)

    my_ordering = ['AccountNumber', 'TranAmount', 'TranCode', 'DebitCredit', 'CompanyEntryDescription', 'IdentificationNumber', 'ReceiverName', 'OriginalEntryTraceNumber', 'ReturnReasonCode', 'ReasonDescription', 'business_name', 'status', 'sales_office', 'sales_agent', 'IAT_GatewayOperatorOfacScreeningIndicator', 'IAT_SecondaryOFACScreeningIndicator', 'IAT_OriginatorName', 'IAT_OriginatorStreetAddress', 'IAT_OriginatorCity_State_Province', 'IAT_OriginatorCountry_PostalCode', 'IAT_OriginatingDFIName', 'IAT_OriginatingDFIIdentificationNumberQualifier', 'IAT_OriginatingDFIIdentification_Addenda4', 'IAT_OriginatingDFIBranchCountryCode', 'IAT_ReceivingDFIName', 'IAT_ReceivingDFIIdentificationNumberQualifier', 'IAT_ReceivingDFIIdentification_Addenda5', 'IAT_ReceivingDFIBranchCountryCode', 'IAT_ReceiverIdentificationNumber', 'IAT_ReceiverStreetAddress', 'IAT_ReceiverCity_State_Province', 'IAT_ReceiverCountry_PostalCode', 'IAT_PaymentRelatedInformation1', 'IAT_PaymentRelatedInformation2', 'IAT_ForeignCorrespondentBankName1', 'IAT_ForeignCorrespondentBankIdentificationNumberQualifier1', 'IAT_ForeignCorrespondentBankIdentificationNumber1', 'IAT_ForeignCorrespondentBankBranchCountryCode1', 'IAT_ForeignCorrespondentBankName2', 'IAT_ForeignCorrespondentBankIdentificationNumberQualifier2', 'IAT_ForeignCorrespondentBankIdentificationNumber2', 'IAT_ForeignCorrespondentBankBranchCountryCode2', 'IAT_ForeignCorrespondentBankName3', 'IAT_ForeignCorrespondentBankIdentificationNumberQualifier3', 'IAT_ForeignCorrespondentBankIdentificationNumber3', 'IAT_ForeignCorrespondentBankBranchCountryCode3', 'IAT_ForeignCorrespondentBankName4', 'IAT_ForeignCorrespondentBankIdentificationNumberQualifier4', 'IAT_ForeignCorrespondentBankIdentificationNumber4', 'IAT_ForeignCorrespondentBankBranchCountryCode4', 'IAT_ForeignCorrespondentBankName5', 'IAT_ForeignCorrespondentBankIdentificationNumberQualifier5', 'IAT_ForeignCorrespondentBankIdentificationNumber5', 'IAT_ForeignCorrespondentBankBranchCountryCode5', 'ImportDatetime']

    final_df = df6[my_ordering]

    file_name = "v2_ACH_Reject_and_Corrected_Data_1_31_test.xlsx"

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
      final_df.to_excel(writer, sheet_name='ACH Reject Data', index=False)
      df_corrected_data.to_excel(writer, sheet_name='Corrected Data', index=False)
      writer.close()

    # Save processed file
    st.write("Download the processed data:")

    st.download_button(
        label="Download APPS Exposure Data",
        data=output.getvalue(),  # Read data from BytesIO
        file_name="processed_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
