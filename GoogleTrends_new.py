from pytrends.request import TrendReq
import pandas
import csv
import os
import csv
import time
from random import gauss

rangestart = 0
rangeend = 200

keywordsfile = "keywords.csv"
storedatafile = "GoogleTrends_new_" + str(rangestart) + "-" + str(rangeend) + ".csv"

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

# Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
skipped = []
num_stored = 0
num_skipped = 0
num_empty = 0
num_all = 0
for keyword in flat_list:
    try:
        time.sleep(abs(gauss(0, 1)))

        # Identify if topic exists for the certain mobile phone
        suggs = pytrend.suggestions(keyword)
        TopicExists = "No Topic"

        if suggs:
            keywordTopic = suggs[0].get('mid')
            TopicExists = "Topic exists"
        else:
            keywordTopic = "NA"

        print("Getting data for " + keyword)

        # Google trends using book as a reference
        pytrend.build_payload(kw_list=[keyword, 'book'])
        interest_over_time_df_comp = pandas.DataFrame(pytrend.interest_over_time()[keyword])
        interest_over_time_df_comp.columns = [keyword + " comp"]
        x = interest_over_time_df_comp.to_string(header=False, index=False, index_names=False).split('\n')
        vals = [','.join(ele.split()) for ele in x]
        str1 = ','.join(str(e) for e in vals)
        #print(interest_over_time_df_comp)

        if(keywordTopic is not "NA"):
            pytrend.build_payload(kw_list=[keywordTopic, 'book'])
            interest_over_time_df_comp = pandas.DataFrame(pytrend.interest_over_time()[keywordTopic])
            interest_over_time_df_comp.columns = [keywordTopic + " comp"]
            x = interest_over_time_df_comp.to_string(header=False, index=False, index_names=False).split('\n')
            vals = [','.join(ele.split()) for ele in x]
            str1_Topic = ','.join(str(e) for e in vals)
        else:
            str1_Topic = "\"NA\""


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

            if(keywordTopic is not "NA"):
                interest_over_time_df_abs = pandas.DataFrame(pytrend.interest_over_time()[keywordTopic])
                interest_over_time_df_comp.columns = [keywordTopic + " abs"]
                x = interest_over_time_df_abs.to_string(header=False, index=False, index_names=False).split('\n')
                vals = [','.join(ele.split()) for ele in x]
                str2_Topic = ','.join(str(e) for e in vals)
            else:
                str2_Topic = "\"NA\""

            # Google trends per region - absolute baseline
            title_3 = keyword + " abs" + " per region"
            interest_byregion_df = pandas.DataFrame(pytrend.interest_by_region())
            x = interest_byregion_df.to_string(header=False, index=False, index_names=False).split('\n')
            vals = [','.join(ele.split()) for ele in x]
            str3 = ','.join(str(e) for e in vals)



            #Concatenate data into JSON object
            JSON_data = "{\"Brand\":\"" + keyword + "\",\"Comparative\":[" + str1 + "],\"Absolute\":[" + str2 + "]" + ",\"Absolute_by_Country\":[" + str3 + "]," +\
                        "\"TopicName\":\"" + keywordTopic+ "\"," +  "\"Comparative_Topic\":[" + str1_Topic + "],\"Absolute_Topic\":[" + str2_Topic + "]}" +"\n"


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
        pass
