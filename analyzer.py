import re
import argparse
from collections import Counter

PATTERN = re.compile(r"Failed password .* from (\d+\.\d+\.\d+\.\d+)")


def count_failed_logins(log_file):
    failed_ips = Counter()
    with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            match = PATTERN.search(line)
            if match:
                failed_ips[match.group(1)] += 1
    return failed_ips


def main():
    parser = argparse.ArgumentParser(
        description="Detect SSH brute force attempts in auth logs (educational use only)"
    )
    parser.add_argument("-f", "--file", required=True,
                        help="Path to the log file (ex: sample_auth.log)")
    parser.add_argument("-t", "--threshold", type=int, default=5,
                        help="Failed attempts before raising an alert (default: 5)")
    parser.add_argument("-o", "--output",
                        help="Save the report to a file (ex: report.txt)")
    args = parser.parse_args()

    try:
        failed_ips = count_failed_logins(args.file)
    except FileNotFoundError:
        print(f"Error: file '{args.file}' not found.")
        return

    lines = ["Failed logins per IP:"]
    for ip, count in failed_ips.most_common():
        lines.append(f"  {ip}: {count}")

    lines.append("")
    lines.append(f"Brute force detection (threshold = {args.threshold}):")
    suspects = [ip for ip, count in failed_ips.items() if count >= args.threshold]

    if suspects:
        for ip in suspects:
            lines.append(f"  [ALERT] {ip} - {failed_ips[ip]} failed attempts")
    else:
        lines.append("  No suspicious activity detected.")

    for line in lines:
        print(line)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"\nReport saved to {args.output}")


if __name__ == "__main__":
    main()