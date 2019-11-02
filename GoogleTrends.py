from pytrends.request import TrendReq
import pandas
import csv
import os
import csv
import time

#Get smartphone names list to be used as keywords
with open('keywords.csv') as csvfile:
    data = list(csv.reader(csvfile))

flat_list = []
for sublist in data:
    for item in sublist:
        flat_list.append(item)

flat_list = flat_list
print(flat_list)

# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend = TrendReq(hl='de-US', tz=360)

# Create and open csv file to store information. Two sorts of information stored for each phone... absolute data + data in relation to "book" search term
file = open(os.path.expanduser("GoogleTrends.csv"), "wb")             # Create .csv file
file_skipped = open(os.path.expanduser("GoogleTrendsSkipped.csv"), "wb")

# Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
skipped = []
for keyword in flat_list:
    #try:
        time.sleep(1)
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
        interest_over_time_df_abs = pandas.DataFrame(pytrend.interest_over_time()[keyword])
        interest_over_time_df_comp.columns = [keyword + " abs"]
        x = interest_over_time_df_abs.to_string(header=False, index=False, index_names=False).split('\n')
        vals = [','.join(ele.split()) for ele in x]
        str2 = ','.join(str(e) for e in vals)
        #print(interest_over_time_df_abs)
        JSON_data = "{\"Brand\":\"" + keyword + "\",\"Comp\":[" + str1 + "],\"Abs\":[" + str2 + "]}" + "\n"

        file.write(bytes(JSON_data, encoding="ascii", errors="ignore"))  # Write new data line to csv file
        print("Success")

    #except:
    #    print("Error occured and " + keyword + " had to be skipped")
    #    skipped.append(keyword)
    #    file_skipped.write(bytes(keyword + "\n",encoding="ascii", errors="ignore"))
    #    pass