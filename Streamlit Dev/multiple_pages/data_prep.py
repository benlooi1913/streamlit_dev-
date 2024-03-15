import streamlit as st
import pandas as pd


def preprocess_data(df):
    # Remove rows with missing values in specific columns
    columns_to_check = ['int_param_vl', 'dbl_param_vl', 'vchar_param_vl']
    df = df.dropna(subset=columns_to_check)

    # Convert data types if needed
    # For example, converting a column to datetime
    # df['date_column'] = pd.to_datetime(df['date_column'])

    # Perform operations on columns
    try:
        df['dbl_param_vl'] = df['int_param_vl'] + df['dbl_param_vl'].apply(lambda x: round(x, 3))
        df['dbl_param_vl'] = df['dbl_param_vl'].astype(str) + df['vchar_param_vl'].astype(str)
    except (TypeError, ValueError) as e:
        print(f"Error in performing operations: {e}")

    # Pivot table
    try:
        transposed_df = df.pivot_table(index='pen_id', columns='param_dn', values='dbl_param_vl', aggfunc='first')
        transposed_df = transposed_df.reset_index().merge(df[['pen_id', 'inkfill_nest', 'status']], on='pen_id', how='left')
        transposed_df.set_index('pen_id', inplace=True)
        transposed_df = transposed_df.groupby(level=0).first()
    except KeyError as e:
        print(f"Error in pivot table creation: {e}")

    # Apply shortcuts
    shortcut = {
        'G5M5_Z3-INK-1INKFILL-P1': 'P1',
        'G5M5_Z3-INK-1INKFILL-P2': 'P2',
        'G5M5_Z3-INK-1INKFILL-P3': 'P3',
        'G5M5_Z3-INK-1INKFILL-P4': 'P4'
    }
    transposed_df['inkfill_nest'] = transposed_df['inkfill_nest'].replace(shortcut)

    # Select columns
    columns_to_include = [
        "FoamHeight",
        "FB1 Volume",
        "FB1 Avg Height",
        "FB1 Avg Weight",
        "POM Ave Height",
        "D-Datum Avg Height",
        "Hopper A Degas Value",
        "Hopper B Degas Value",
        "Vacuum delta actual (nose - body) InHg",
        "inkfill_nest",
        "status"
    ]
    df_selected = transposed_df[columns_to_include]

    # Drop columns with low unique counts
    unique_counts = df_selected.drop('status', axis=1).nunique()
    columns_to_drop = unique_counts[unique_counts <= 3].index.tolist()
    if 'status' in columns_to_drop:
        columns_to_drop.remove('status')
    df_merged_filtered = df_selected.drop(columns=columns_to_drop)

    # Generate labels and bin numerical columns
    num_bins = 3  # Number of bins for binning numerical columns
    generate_labels = lambda: ['low', 'medium', 'high']
    columns_and_labels = {
        "FoamHeight": generate_labels(),
        "FB1 Volume": generate_labels(),
        "FB1 Avg Height": generate_labels(),
        "FB1 Avg Weight": generate_labels(),
        "POM Ave Height": generate_labels(),
        "D-Datum Avg Height": generate_labels(),
        "Hopper A Degas Value": generate_labels(),
        "Hopper B Degas Value": generate_labels(),
        "Vacuum delta actual (nose - body) InHg": generate_labels(),
    }

    for column, labels in columns_and_labels.items():
        try:
            df_merged_filtered[column] = pd.cut(df_merged_filtered[column].astype(float), num_bins, labels=labels)
        except ValueError as e:
            print(f"Error in binning {column}: {e}")

    return df_merged_filtered



# Streamlit app
def main():
    st.title('CSV Preprocessing')

    st.write('This interface is intended to pre-processe and transform the data into binning as the data comes in as a raw data format would not be any meaningful for analysis.')

    # Upload CSV file
    st.header('Upload CSV File')
    uploaded_file = st.file_uploader('Choose a CSV file', type=['csv'])

    if uploaded_file is not None:
        # Read CSV file
        df = pd.read_csv(uploaded_file)

        # Display the raw data
        st.subheader('Raw Data')
        st.write(df)

        # Preprocess the data
        processed_df = preprocess_data(df)

        # Display the processed data
        st.subheader('Processed Data')
        st.write(processed_df)

        # Download processed CSV file
        st.header('Download Processed CSV File')
        st.write('Click below to download the processed CSV file')
        st.download_button(
            label='Download CSV',
            data=processed_df.to_csv(index=False),
            file_name='processed_data.csv',
            mime='text/csv'
        )

if __name__ == '__main__':
    main()
