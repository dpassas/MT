from pytrends.request import TrendReq
import pandas
import csv
import os
import csv
import time
from random import gauss

rangestart = 2700
rangeend = 3000

keywordsfile = "keywords.csv"
storedatafile = "GoogleTrends_" + str(rangestart) + "-" + str(rangeend) + ".csv"
skippeddatafile = "GoogleTrendsSkipped_v3"

google_username = "dpassasd@gmail.com"
google_password = "i31bC-kqrRhe1nfall"

#Get smartphone names list to be used as keywords
with open(keywordsfile) as csvfile:
    data = list(csv.reader(csvfile))

flat_list = []
for sublist in data:
    for item in sublist:
        flat_list.append(item)

flat_list = flat_list[rangestart:rangeend]

# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend = TrendReq(hl='en-US', tz=360)

# Create and open csv file to store information. Two sorts of information stored for each phone... absolute data + data in relation to "book" search term
file = open(os.path.expanduser(storedatafile), "wb")             # Create .csv file
file_skipped = open(os.path.expanduser(skippeddatafile), "wb")

# Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
skipped = []
num_stored = 0
num_skipped = 0
num_empty = 0
num_all = 0
for keyword in flat_list:
    try:
        time.sleep(abs(gauss(0, 1)))
        print("Getting data for " + keyword)

        # Google trends using book as a reference
        title_1 = keyword + " comp"
        pytrend.build_payload(kw_list=[keyword, 'book'])
        interest_over_time_df_comp = pandas.DataFrame(pytrend.interest_over_time()[keyword])
        interest_over_time_df_comp.columns = [keyword + " comp"]
        x = interest_over_time_df_comp.to_string(header=False, index=False, index_names=False).split('\n')
        vals = [','.join(ele.split()) for ele in x]
        str1 = ','.join(str(e) for e in vals)
        #print(interest_over_time_df_comp)


        # Google trends using only the smartphone keyword - absolute data
        title_2 = keyword + " abs"
        pytrend.build_payload(kw_list=[keyword])
        try:
            interest_over_time_df_abs = pandas.DataFrame(pytrend.interest_over_time()[keyword])
            interest_over_time_df_comp.columns = [keyword + " abs"]
            x = interest_over_time_df_abs.to_string(header=False, index=False, index_names=False).split('\n')
            vals = [','.join(ele.split()) for ele in x]
            str2 = ','.join(str(e) for e in vals)
            #print(interest_over_time_df_abs)


            # Google trends per region - absolute baseline
            title_3 = keyword + " abs" + " per region"
            interest_byregion_df = pandas.DataFrame(pytrend.interest_by_region())
            x = interest_byregion_df.to_string(header=False, index=False, index_names=False).split('\n')
            vals = [','.join(ele.split()) for ele in x]
            str3 = ','.join(str(e) for e in vals)
            #print(interest_byregion_df.index)


            #Concatenate data into JSON object
            JSON_data = "{\"Brand\":\"" + keyword + "\",\"Comparative\":[" + str1 + "],\"Absolute\":[" + str2 + "]" + ",\"Absolute_by_Country\":[" + str3 + "]}"  + "\n"

            #Write & store JSON object on csv
            file.write(bytes(JSON_data, encoding="ascii", errors="ignore"))  # Write new data line to csv file
            num_stored = num_stored + 1
            num_all = num_all + 1
            print("Success... data has been succesfully included to " + storedatafile + "(" + str(num_stored) + "," + str(num_empty) + "," + str(num_skipped) + "/" + str(num_all) + ")")

        except:
            JSON_data = "{\"Brand\":\"" + keyword + "\",\"Comparative\":[" + str1 + "],\"Absolute\":\"NA\"" + ",\"Absolute_by_Country\":\"NA\"}"  + "\n"
            num_empty = num_empty + 1
            num_all = num_all + 1
            print("Not enough data for this keyword... data has been succesfully included to " + storedatafile + "(" + str(num_stored) + "," + str(num_empty) + "," + str(num_skipped) + "/" + str(num_all) + ")")

    except:
        num_skipped = num_skipped + 1
        num_all = num_all + 1
        print("Error occured and " + keyword + " had to be skipped " + "(" + str(num_stored) + "," + str(num_empty) + "," + str(num_skipped) + "/" + str(num_all) + ")")
        skipped.append(keyword)
        file_skipped.write(bytes(keyword + "\n",encoding="ascii", errors="ignore"))

        pass
