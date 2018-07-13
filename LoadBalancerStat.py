import os, requests, re, time, datetime

"""
There's a good chance that this script is only useful for me. Our perimeter servers have a test page on them that will return a string with the name of the perimeter server you're connected to.
Given that, I use a regex check against the text that the GET request returns to determine what counter I should increase. If you have an app deployed in a similar fashion then this
script might also work for you. If not, I dunno.
"""


"""
Variable delcarations. Maybe if I can be bothered later I'll put these in seperate configuration files to be more user friendly.
"""

results_path = "C:\\YourFavoritePath"
filename = 'LoadBalancerStats' + str(datetime.datetime.now().strftime("%m_%d_%y-%H_%M")) + '.txt'

test_length = 30
per01_count = 0
per02_count = 0

perimeter_url = 'https://someperimeterserver.net/testpagefortestingthingsinatestingfashion.htm'
perimeter_page = requests.get(perimeter_url)

"""
Very ground-breaking regular expression used to determine which perimeter server the requests returned
"""

per01 = re.compile(r'01\b')
per02 = re.compile(r'02\b')



def check_perimeter(text):


    """
    This function takes the text returned from the GET to the configured perimeter server URL and checks it against regular expressions.
    Depending on which regex matches, we increase the counter for that respective perimeter server.
    """

    global per01_count
    global per02_count
    if per01.search(text):
        per01_count += 1
    if per02.search(text):
        per02_count += 1
    return per01_count, per02_count



def prepare_statistics(a):


    """
    This function gives us a percentage to report in the logs. It's very complicated.
    """

    ratio = a / test_length * 100
    return ratio



"""
Iterate X number of times according to the configured test length variable. If the current number of tests haven't yet matched the configured test length,
continue calling the testing function. When the test length is reached, gather statistics about the whole test and write them to a log file.
"""

for x in range(test_length + 1):
    if x == test_length:
        per01_result = prepare_statistics(per01_count)
        per02_result = prepare_statistics(per02_count)
        l = open(os.path.join(results_path, filename), 'w')
        l.write('Testing URL: {0}\n'.format(perimeter_url))
        l.write('Test Length: {0}\n'.format(test_length))
        l.write('\n----Per01 Results----\n')
        l.write('Connection Percentage: {0}%\n'.format(per01_result))
        l.write('{0} connections made / {1} total attempted connections for this test\n'.format(per01_count, test_length))
        l.write('\n----Per02 Results----\n')
        l.write('Connection Percentage: {0}%\n'.format(per02_result))
        l.write('{0} connections made / {1} total attempted connections for this test\n'.format(per02_count, test_length))
        l.close()
    else:
        time.sleep(60) #Trying not to DoS our production servers
        check_perimeter(perimeter_page.text)