import csv

input_path = "data/live_signals_log.csv"
output_path = "data/live_signals_log_cleaned.csv"
log_path = "data/dropped_rows.csv"

EXPECTED_COLUMNS = 9

with open(input_path, "r", newline='', encoding="utf-8") as infile, \
     open(output_path, "w", newline='', encoding="utf-8") as outfile, \
     open(log_path, "w", newline='', encoding="utf-8") as logfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    drop_writer = csv.writer(logfile)

    header = next(reader)
    writer.writerow(header)
    drop_writer.writerow(header)

    for i, row in enumerate(reader, start=2):  # line numbers start after header
        if len(row) == EXPECTED_COLUMNS:
            writer.writerow(row)
        else:
            drop_writer.writerow(row)
            print(f"Dropped line {i}: {row}")

print(f"✅ Cleaned log saved to: {output_path}")
print(f"🗑️ Dropped rows saved to: {log_path}")
