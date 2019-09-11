# Content:
# ---------------------
# multiple_replace
# sub_digits
# fix_date_strings
# sort_word_count
# isolate_symbols



import re
import operator

def multiple_replace(mapping, text):
    """
    :param 
        mapping: dictionary which maps search_pattern:substitution
		text: the text where patterns in mapping should be substituted
    :return: 
        text: text with substitution for each search pattern (if pattern was found)
    """
    # Create a regular expression from all of the dictionary keys
    regex = re.compile("|".join(map(re.escape, mapping.keys( ))))
    
    # For each match, look up the corresponding value in the dictionary
    text = regex.sub(lambda match: f' {mapping[match.group(0)]}', text) # ein match in sub ist wohl der jeweils gefundene String
    return text
    
   
def sub_digits(text, start, to):
    '''
    usage:
        data.txt.apply(lambda x: sub_digits(x, 2, 8))
    
    param:
        text:
        start:
        to:
    return:
        text: text where Number from start to 'to' digits are replaced with DIGn
        
    example: 
        65 --> DIG2 
        678 --> DIG3
    '''
    regex = {}
    for i in range(start, to+1):
        sub = f"DIG{i}"
        regex[sub] = re.compile(rf"\b\d{{{i}}}\b") # Merke: Curly Braces werden durch Curly Braces escaped
        #https://stackoverflow.com/questions/5466451/how-can-i-print-literal-curly-brace-characters-in-python-string-and-also-use-fo
    
    for substitution, reg in regex.items():
        text = reg.sub(substitution, text)
    
    return text

    
def fix_date_strings(text):
    '''
    
    example: 
        '20170103000821' --> TIMESTR
    '''
    RE_DATE = re.compile(r"\b20\d{12}\b")
    text = RE_DATE.sub("TIMESTR", text)
    return text
    
    
def sort_word_count(dictionary):
    sorted_vocab = sorted(dictionary.items(), key=operator.itemgetter(1))
    return sorted_vocab
    
    
def replace_symbols(text, mapping):
    '''
    ToDo: Transfer it into a separate function, maybe

    param:
        text: the text, where symbols should be replaced
        mapping: a dictionary which maps the unicode code of a char to its replacement value (ord(c):replacement_string)
    '''
    mapping = {ord(s):replacement for s, replacement in mapping.items()}
    #text = text.translate(self.unknown_symbols)
    #text = text.translate(self.known_dict)
    text = text.translate(mapping)
    return text
    
    
def isolate_symbols(text, symbols=None):
    '''
    Isolates symbols by whitespaces
    
    param:
        symbols: string of symbols (chars with len==1)
        text: strings where symbols should be replaced
    '''
    if symbols == None:
        symbols = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~“”’\'\r\t\n'
    
    mapping = {ord(s):f' {s} ' for s in symbols}
    text = text.translate(mapping)
    return text
    
def mask_tokens(text, token_len):
    RE_DIGN = re.compile(rf"\b\d{{{token_len}}}\b")
    tokens = RE_DIGN.findall(text)
    if tokens: # if list is not empty
        for token in tokens:
            masked_token = token[:5] + 'xxxxx'
            text = text.replace(token, masked_token)
    return text
    

def fix_conf_alert_type(text):
    # e.g 005056b9111f1ed6bd8fc084ecf43f26
    RE_CONF_ALERT_TYPE = re.compile("005056\w{26}")
    text = RE_CONF_ALERT_TYPE.sub('CONFALERTTYPE', text)
    return text