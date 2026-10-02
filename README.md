# Log Analyzer

Python tool that detects SSH brute force attempts in auth logs.

> **Disclaimer:** Educational purposes only. The sample log file contains
> fake data and reserved documentation IP addresses.

## Features

- Parses SSH auth logs (`Failed password` lines)
- Counts failed logins per IP address
- Raises an alert when an IP reaches a configurable threshold
- Saves the report to a file
- No external dependencies (standard library only)

## Requirements

- Python 3.8+

## Usage

    python analyzer.py -f sample_auth.log
    python analyzer.py -f sample_auth.log -t 3
    python analyzer.py -f sample_auth.log -o report.txt

## Options

| Option | Description | Default |
|--------|-------------|---------|
| -f, --file | Path to the log file (required) | - |
| -t, --threshold | Failed attempts before an alert | 5 |
| -o, --output | Save the report to a file | - |

## Example output

    Failed logins per IP:
      203.0.113.50: 6
      198.51.100.77: 3
      192.0.2.10: 1

    Brute force detection (threshold = 5):
      [ALERT] 203.0.113.50 - 6 failed attempts

## How it works

1. Reads the log file line by line
2. Extracts the source IP with a regex
3. Counts failed attempts per IP using `collections.Counter`
4. Flags every IP at or above the threshold

## What I learned

- Regular expressions (`re`)
- Counting and aggregating data with `Counter`
- Building a CLI with `argparse`
- Basics of SOC log analysis and brute force detection

## Roadmap

- [ ] Detect attempts within a time window
- [ ] Support more log formats
- [ ] Export report as CSV or JSON

## License

MIT
