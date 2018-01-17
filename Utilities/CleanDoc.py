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


def clean_doc(text):
    regex = re.findall("htt.*:[\s+|\/][\s+|\/].*t.co.*\/\S+", text)
    text = text.strip()
    for value in regex:
        text = text.replace(value, '')

    regex = re.findall("https?:\s?\/\s?\/t\.c?o?", text)
    for value in regex:
        text = text.replace(value, '')

    return text


text = 'RT @yasmineryan: Sisi is worse than Netanyahu, &amp; the Egyptians are conspiring against us more than the Jews, #Gaza shopkeeper http: / /t.co'
print(clean_doc(text))
