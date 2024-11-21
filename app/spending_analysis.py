import boto3
import pandas as pd
import os

S3_BUCKET_NAME =os.environ['S3_BUCKET_NAME'] 
S3_FILE_KEY = os.environ['S3_FILE_KEY']

# Clean up amounts: removes the $ and converts to float
def clean_amount(amount):
    return float(amount.replace('$', '').replace(',', ''))

# Reads input data from S3
def read_file_from_s3(bucket_name, s3_key):
    try:
        response = s3.get_object(Bucket=bucket_name, Key=s3_key)
        print(f"File successfully read from S3: {s3_key}")
        return pd.read_csv(io.BytesIO(response['Body'].read()))
    except Exception as e:
        print(f"Error reading file from S3: {e}")
        exit(1)

# Uploads the result CSV file to S3
def upload_file_to_s3(local_path, bucket_name, s3_key):
    try:
        s3.upload_file(local_path, bucket_name, s3_key)
        print(f"File uploaded to S3: {local_path} -> {bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        exit(1)

def analyze_spending(dataframe):
    try:
        dataframe["amount"] = dataframe["amount"].apply(clean_amount)

        # Spending analysis by client
        client_summary = df.groupby("client_id")["amount"].agg(["sum", "mean", "count"]).reset_index()
        client_summary.columns = ["client_id", "total_spent", "average_transaction", "transaction_count"]
        print("\nClient-specific spending summary:")
        print(client_summary.head())

        # Spending analysis by Merchandising 
        merchant_summary = df.groupby("merchant_id")["amount"].agg(["sum", "mean", "count"]).reset_index()
        merchant_summary.columns = ["merchant_id", "total_spent", "average_transaction", "transaction_count"]
        print("\nMerchant-specific spending summary:")
        print(merchant_summary.head())

        # Save the client summary locally
        client_summary.to_csv("client_summary.csv", index=False)

        # Upload the result file to S3
        upload_file_to_s3("client_summary.csv", S3_BUCKET_NAME, "client_summary.csv")

        # Save the merchant summary locally
        merchant_summary.to_csv("merchant_summary.csv", index=False)

        # Upload the result file to S3
        upload_file_to_s3("merchant_summary.csv", S3_BUCKET_NAME, "merchant_summary.csv")

    except Exception as e:
        print(f"Error analyzing spending: {e}")
        exit(1)



# Main function to run the analysis
def main():
    dataframe = read_file_from_s3(S3_BUCKET_NAME, S3_FILE_KEY)

    analyze_spending(dataframe)

if __name__ == '__main__':
    main()
