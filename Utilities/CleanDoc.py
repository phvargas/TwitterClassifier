import re
"""
remove t.co regex --> https?:\\?\s?/\\?\s?/t.co\\?\s?/\S+
remove truncated t.co regex --> https?:\s?/\s?/t\.?
remove truncated --> https?:\s?/\s?$
remove truncated --> https?:\\/\\\S+$
remove retweet and its handle --> RT\s@\S+:
remove &amp; --> &amp;
remove \n --> \\n
replace handle for @ --> @\S+ -> @
remove all special characters but $,!,?,,@,# --> [^a-zA-Z0-9\.@#?'*%,=/:\(\)\s;_&-]
"""


def clean_doc(my_text):
    print(my_text.strip())
    regex = re.findall("htt.*:[\s+|\/][\s+|\/].*t.co.*\/\S+", my_text)
    my_text = my_text.strip()
    for value in regex:
        my_text = my_text.replace(value, '')

    regex = re.findall("https?:\s?\/\s?\/t\.c?o?\s/?", my_text)
    for value in regex:
        my_text = my_text.replace(value, '')

    regex = re.findall("@\S+", my_text)
    for value in regex:
        my_text = my_text.replace(value, '@hdl')

    regex = re.compile("['.]")
    my_text = regex.sub('', my_text)

    regex = re.compile("[();:-]")
    my_text = regex.sub(' ', my_text)

    regex = re.compile("[^a-zA-Z0-9@#*%\(\)\s_&]")
    my_text = regex.sub('', my_text.lower())

    return my_text


text = "RT @YasmineAlFarra: Edward Said on claims that #Palestine is the Jews' God Given Land http: / /t.co /wNRtRFaeni @georgegalloway"
print(clean_doc(text))
