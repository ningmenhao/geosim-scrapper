import gspread
from oauth2client.service_account import ServiceAccountCredentials
import praw

# use creds to create a client to interact with the praw Reddit API
reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit("geosim")

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Ning Screwing Around LOL").sheet1

# Figure out the last write to the document
last_update_utc = sheet.cell(2,1).value

# Write a set number of values from the most recent subreddit posts
#   to the Google Sheets, inserted at row 1 in descending order by time
line_count = 0
for submission in subreddit.new(limit=20):
    if submission.created_utc > float(last_update_utc):
        row = [str(submission.created_utc),str(submission.title.encode("utf-8")),str(submission.author.name.encode("utf-8"))
           ,str(submission.selftext.encode("utf-8"))]
        print(row[0:2])
        index = 2 + line_count
        line_count += 1
        sheet.insert_row(row,index)
