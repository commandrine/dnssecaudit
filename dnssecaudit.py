import subprocess
import sys
import dns.resolver
import datetime

def check_prerequisites():
    try:
        import dns
    except ImportError:
        print("The required module 'dnspython' is not installed. Installing it now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "dnspython"])
        print("Installation complete. Please restart the script.")
        sys.exit()

def check_dnssec(domain):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['1.1.1.1']  # Use a reliable public DNS server
    try:
        answers = resolver.resolve(domain, 'DNSKEY')
        if answers:
            return True
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers, dns.exception.Timeout, dns.resolver.NoRootError):
        return False

def main():
    check_prerequisites()

    domains = []
    choice = input("Enter '1' to input a single domain or '2' to input a list of domains from a file: ").strip()

    if choice == '1':
        domain = input("Enter a domain name: ").strip()
        domains.append(domain)
    elif choice == '2':
        file_path = input("Enter the file path containing the list of domains: ").strip()
        try:
            with open(file_path, 'r') as file:
                domains = [line.strip() for line in file] #improved handling of whitespace in input file
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return
    else:
        print("Invalid choice. Please restart the script and enter '1' or '2'.")
        return

    results = []
    for domain in domains:
        if check_dnssec(domain):
            results.append(f"{domain}: DNSSEC enabled")
        else:
            results.append(f"{domain}: DNSSEC not enabled")

    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    report_filename = f"dnssecaudit-report-{date_str}.txt"

    try:
        with open(report_filename, 'w') as report_file: #Corrected section
            for result in results:
                print(result) # still print to console
                report_file.write(result + '\n')
        print(f"Report saved to {report_filename}") #Added confirmation message
    except Exception as e: #Catch potential errors during file writing.
        print(f"An error occurred while writing the report: {e}")

if __name__ == "__main__":
    main()