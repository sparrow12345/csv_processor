import argparse
from processor import process_csv
from tabulate import tabulate


def main():
    parser = argparse.ArgumentParser(description="CSV Processor")
    parser.add_argument("--file", help="Path to CSV file")
    parser.add_argument("--where", help="Filter condition, e.g. price>500")
    parser.add_argument("--aggregate", help="Aggregation function, e.g. mean:price or max:rating")
    parser.add_argument('--order-by', help='Order rows by column (e.g. price:asc or rating:desc)')

    args = parser.parse_args()

    try:
        result = process_csv(args.file, args.where, args.aggregate, args.order_by)
        print(tabulate(result, headers="keys", tablefmt="grid"))
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
