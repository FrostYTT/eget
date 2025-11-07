#!/usr/bin/env python3
class EmailFinder:
    def __init__(self, args):
        self.outputPath = args.target
        self.verbose = args.verbose

        # turn csv into 2D array
        with open(args.source, "r") as f:
            self.data = f.read().split("\n")
        # self.data = []
        # for line in data:
        #     self.data.append(line.strip().split(","))
        # input(self.data)
        self.contactExtensions = [
            "contact/",
            "contact-us/",
            "contactus/",
            "contact_us/",
            "contacts/",
            "support/",
            "help/",
            "about/contact/",
            "about-us/contact/",
            "company/contact/",
            "home/contact/",
            "en/contact/",
            "contact-form/",
            "connect/",
            "contact-page/",
            "contact-info/"
        ]


    def getBaseUrl(self, url):
        baseUrl = re.search(r'https?://[^/]+', url).group(0)+"/"
        return baseUrl

    def safeCurl(self, url):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            if "404" not in str(e):
                if self.verbose:
                    print(f"An error occurred: {e}")
                else:
                    print("Error")
            return None
    
    def emailRegex(self, content):
        # emails = re.findall(r'[\w\.\-]+@[\w\-]+\.\D+\.?\D+', content)
        emails = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', content)
        if emails:
            substrings = ["example", "domain", "wixpress", "filler", "sentry.io"]
            emails = [email.lower() for email in emails if not any(sub in email for sub in substrings)]
            # emails = [email for email in emails if "wixpress" not in email]
            return list(set(emails))
        return None

    def findEmail(self, url):
        content = self.safeCurl(url)
        if content:
            return self.emailRegex(content)
        return None

    def writeEmails(self, emails, url):
        with open(self.outputPath, "a") as f:
            for email in emails:
                print(f"Email found for {url}: {email}")
                f.write(f"{url},{email}\n")

    def startSearch(self):
        print("Starting Email Scraping...\n")
        # checks for presence of lines in the CSV file provided
        if len(self.data) == 0:
            # No lines
            print("Empty CSV file provided.")
            return
        # lines present
        # for each website in the csv make an array of urls to try
        for website in self.data:
            emails = self.findEmail(website)
            if emails:
                self.writeEmails(emails, website)
            else:
                urls = []
                baseUrl = self.getBaseUrl(website)
                for extension in self.contactExtensions:
                    urls.append(baseUrl+extension)
                urls.append(baseUrl)
                
                counter = 0
                found = False
                while counter < len(urls) and found == False:
                    url = urls[counter]
                    emails = self.findEmail(url)
                    if emails:
                        self.writeEmails(emails, url)
                        found = True
                    counter  += 1
                if not found:
                    if self.verbose:
                        print(f"No Emails found for {website}")

if __name__ == "__main__":
    import re, requests
    import argparse
    import time
    argParser = argparse.ArgumentParser(
        description="Scrape a websites for emails from a .csv")
    argParser.add_argument("source", default=None, help="Path to source file")
    argParser.add_argument("target", default=None, help="Path to target file")
    argParser.add_argument("-v", "--verbose", action="store_true", help="Show emails as they're being found")
    argParser.add_argument("-s", "--statistics", action="store_true", help="Show statistics at the end of the run")
    args = argParser.parse_args()
    emailFinder = EmailFinder(args)
    start = time.time()
    emailFinder.startSearch()
    end = time.time()
    if args.statistics:
        timeTaken = end - start
        with open(args.source, "r") as f:
            inputLines = len(f.readlines())
        with open(args.target, "r") as f:
            outputLines = len(f.readlines())
        print("\n\nSTATS\n")
        print(f"Time taken: {timeTaken}")
        print(f"Websites Input: {inputLines}")
        print(f"Emails found: {outputLines}")
        print(f"Average success rate: {(outputLines/inputLines)*100}")
        print(f"Average time per input website: {timeTaken/inputLines}")
        print(f"Average time per output email: {timeTaken/outputLines}")