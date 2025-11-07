#!/usr/bin/env python3
# initialising eget class
class Eget:
    def __init__(self, args):
        self.outputPath = args.target
        self.verbose = args.verbose
        self.url = args.url

        # turn CSV into 2D array
        with open(args.source, "r") as f:
            self.data = f.read().split("\n")
        
        # define a list of common contact page extensions
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

    # function to isolate the base URL of any link
    def getBaseUrl(self, url):
        try:
            baseUrl = re.search(r'https?://[^/]+', url).group(0)+"/"
            return baseUrl
        except Exception as e:
            if self.verbose:
                print(f"Invalid URL: {url}")
            return None

    # function to get HTML from a URL with error checking
    def safeGetRequest(self, url):
        try:
            # get HTML data, 5s timeout
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            # return HTML
            return response.text
        # Error
        except requests.exceptions.RequestException as e:
            # print error type only with verbose flag
            if self.verbose:
                print(f"An error occurred: {e}")
            # return nothing on error
            return None
    
    # function to search through HTML content for email matches
    def emailRegex(self, content):
        try:
            # regex search
            emails = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', content)
            # if any emails were found
            if emails:
                # ignore emails with following substrings present (useless)
                substrings = ["example", "domain", "wixpress", "filler", "sentry.io", ".png", ".jpeg", ".jpg", ".webp", ".gov."]
                emails = [email.lower() for email in emails if not any(sub in email for sub in substrings)]
                # return email list (removed duplicates)
                return list(set(emails))
            return None
        except Exception as e:
            if self.verbose:
                print(f"An error occurred: {e}")

    # function to find an email in HTML content
    def findEmail(self, url):
        # fetch content from url
        content = self.safeGetRequest(url)
        if content:
            # return emails if existent
            return self.emailRegex(content)
        # no HTML, return nothing
        return None

    # function to write found emails to the output .csv file
    def writeEmails(self, emails, url):
        with open(self.outputPath, "a") as f:
            for email in emails:
                # logging
                print(f"Email found for {url}: {email}")
                # writing the email
                if self.url:
                    f.write(f"{url},{email}\n")
                else:
                    f.write(f"{email}\n")

    # function to search for emails in all the provided websites
    def startSearch(self):
        # logging
        print("Starting Email Scraping...\n")
        # checks for presence of lines in the csv file provided
        if len(self.data) == 0:
            # No lines
            print("Empty CSV file provided.")
            # kill program
            sys.exit(1)
        # lines present
        # try the provided url for each website
        for website in self.data:
            print(f"Searching for email for {website}")
            emails = self.findEmail(website)
            if emails:
                # emails found in the provided url
                self.writeEmails(emails, website)
            else:
                # no emails found in the provided url, searching in commonly used contact urls
                urls = []
                # get base url to then append contact extensions
                baseUrl = self.getBaseUrl(website)
                if not baseUrl:
                    continue
                for extension in self.contactExtensions:
                    # append contact extensions to base url
                    urls.append(baseUrl+extension)
                # append base url to array just in case
                urls.append(baseUrl)
                
                # I dont like breaks so im doing a while loop. forgive me
                i = 0
                found = False
                while i < len(urls) and found == False:
                    # choose url from the loop
                    url = urls[i]
                    # fetch emails for this url
                    emails = self.findEmail(url)
                    if emails:
                        # emails found
                        self.writeEmails(emails, url)
                        found = True
                    i  += 1
                # if a url has not been found (and verbose flag is selected), log.
                if not found:
                    print(f"No Emails found for {website}")

if __name__ == "__main__":
    # import modules
    import re, requests, sys, argparse, time
    # argparser for convenient argument parsing
    argParser = argparse.ArgumentParser(
        description="Scrape a websites for emails from a .csv")
    argParser.add_argument("source", default=None, help="Path to source file")
    argParser.add_argument("target", default=None, help="Path to target file")
    argParser.add_argument("-v", "--verbose", action="store_true", help="Show emails as they're being found")
    argParser.add_argument("-s", "--statistics", action="store_true", help="Show statistics at the end of the run")
    argParser.add_argument("-u", "--url", action="store_true", help="Include the URL in the output file")
    # parse args
    args = argParser.parse_args()
    # init class
    eget = Eget(args)
    # start timer for statistics
    start = time.time()
    # start email scraping
    eget.startSearch()
    # end timer for statistics
    end = time.time()
    # only run statistics if the statistics option is selected
    if args.statistics:
        # self explanatory
        timeTaken = end - start
        with open(args.source, "r") as f:
            inputLines = len(f.readlines())
        with open(args.target, "r") as f:
            outputLines = len(f.readlines())
        print(f"""\n-----Statistics-----

Time taken: {timeTaken}
Websites Input: {inputLines}
Emails found: {outputLines}
Average success rate: {(outputLines/inputLines)*100}
Average time per input website: {timeTaken/inputLines}
Average time per output email: {timeTaken/outputLines}
""")