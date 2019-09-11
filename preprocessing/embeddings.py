from tqdm import tqdm
import operator
import string

# definiere eine Liste von 'regulären' Buchstaben (keine Symbole, wie z.B. Smilies)
latin_similar = "’'‘ÆÐƎƏƐƔĲŊŒẞÞǷȜæðǝəɛɣĳŋœĸſßþƿȝĄƁÇĐƊĘĦĮƘŁØƠŞȘŢȚŦŲƯY̨Ƴąɓçđɗęħįƙłøơşșţțŧųưy̨ƴÁÀÂÄǍĂĀÃÅǺĄÆǼǢƁĆĊĈČÇĎḌĐƊÐÉÈĖÊËĚĔĒĘẸƎƏƐĠĜǦĞĢƔáàâäǎăāãåǻąæǽǣɓćċĉčçďḍđɗðéèėêëěĕēęẹǝəɛġĝǧğģɣĤḤĦIÍÌİÎÏǏĬĪĨĮỊĲĴĶƘĹĻŁĽĿʼNŃN̈ŇÑŅŊÓÒÔÖǑŎŌÕŐỌØǾƠŒĥḥħıíìiîïǐĭīĩįịĳĵķƙĸĺļłľŀŉńn̈ňñņŋóòôöǒŏōõőọøǿơœŔŘŖŚŜŠŞȘṢẞŤŢṬŦÞÚÙÛÜǓŬŪŨŰŮŲỤƯẂẀŴẄǷÝỲŶŸȲỸƳŹŻŽẒŕřŗſśŝšşșṣßťţṭŧþúùûüǔŭūũűůųụưẃẁŵẅƿýỳŷÿȳỹƴźżžẓ"
white_list = string.ascii_letters + string.digits + latin_similar + ' '
white_list += "'"

def build_vocab(token_lists, verbose =  True):
    """
	Creates a Dictionary of existing words and their word count from a list of tokens
	
    :param 
		token_lists: list of list of words
    :return: 
		dictionary of words and their count 
    """
    vocab = {}
    for token_list in tqdm(token_lists, disable = (not verbose)):
        for word in token_list:
            try: # wenn Wort bereits in Dict existiert, zähle es hoch
                vocab[word] += 1
            except KeyError: # wenn nicht, lege es an und setze Count auf 1
                vocab[word] = 1
    return vocab
	

def check_coverage(vocab, embeddings_index):
    """
	Checks if words from vocab exists in embeddings_index (this is the given (pre-trained) embedding)
	Returns a sorted dictionary of unknown words and their word count
	
	vocab can be calculated by 'build_vocab' function
	
    :param 
        vocab: dictionary of words and their count 
        embeddings_index: dict with mapping word:embedding_vector
    :return: dictionary of words not in embedding and their count (sorted from 
    """
    known_words = {}
    unknown_words = {}
    nb_known_words = 0
    nb_unknown_words = 0
    for word in vocab.keys():
        try:
            known_words[word] = embeddings_index[word]
            nb_known_words += vocab[word]
        except:
            unknown_words[word] = vocab[word]
            nb_unknown_words += vocab[word]
            pass

    print('Found embeddings for {:.3%} of vocab'.format(len(known_words) / len(vocab)))
    print('Found embeddings for  {:.3%} of all text'.format(nb_known_words / (nb_known_words + nb_unknown_words)))
    unknown_words = sorted(unknown_words.items(), key=operator.itemgetter(1))[::-1]

    return unknown_words
	
def check_punct(embeddings_index): 
    """
	For a given pre-trained embedding, this function checks, if there is an embedding vector
	for a given punctuation
	
    :param 
        embeddings_index: dict with mapping word:embedding_vector
    :return: 
        known_punct: list of punctuations found in embeddings_index
        unkown_punct: list of punctuations not found in embeddings_index
    """
    punct = "/-'?!.,#$%\'()*+-/:;<=>@[\\]^_`{|}~" + '""“”’' + '∞θ÷α•à−β∅³π‘₹´°£€\×™√²—–&'
    known_punct = []
    unknown_punct = []

    for p in punct:
        try:
            embeddings_index[p] # prüfe, ob Wort in Embedding vorhanden ist
            known_punct.append(p)
        except:
            unknown_punct.append(p)
        
    return known_punct, unknown_punct
    
    # Attributes
    # regular_characters
    # embeddings_chars
    # embeddings_symbols
    # text_chars
    # text_symbols
    # symbols_to_delete
    # symbols_to_isolate
	
def check_symbols(text, embeddings_index): 
    """
    Checks if symbols from vocab are known in embeddings_index
	
    :param 
        text: list of raw strings e.g. ['this is my house', 'the quick brown fox ;)']
        embeddings_index: dict with mapping word:embedding_vector
    :return: 
        known_punct: list of punctuations found in embeddings_index
        unkown_punct: list of punctuations not found in embeddings_index
    """
    # definiere eine Liste von 'regulären' Buchstaben (keine Symbole, wie z.B. Smilies)
    latin_similar = "’'‘ÆÐƎƏƐƔĲŊŒẞÞǷȜæðǝəɛɣĳŋœĸſßþƿȝĄƁÇĐƊĘĦĮƘŁØƠŞȘŢȚŦŲƯY̨Ƴąɓçđɗęħįƙłøơşșţțŧųưy̨ƴÁÀÂÄǍĂĀÃÅǺĄÆǼǢƁĆĊĈČÇĎḌĐƊÐÉÈĖÊËĚĔĒĘẸƎƏƐĠĜǦĞĢƔáàâäǎăāãåǻąæǽǣɓćċĉčçďḍđɗðéèėêëěĕēęẹǝəɛġĝǧğģɣĤḤĦIÍÌİÎÏǏĬĪĨĮỊĲĴĶƘĹĻŁĽĿʼNŃN̈ŇÑŅŊÓÒÔÖǑŎŌÕŐỌØǾƠŒĥḥħıíìiîïǐĭīĩįịĳĵķƙĸĺļłľŀŉńn̈ňñņŋóòôöǒŏōõőọøǿơœŔŘŖŚŜŠŞȘṢẞŤŢṬŦÞÚÙÛÜǓŬŪŨŰŮŲỤƯẂẀŴẄǷÝỲŶŸȲỸƳŹŻŽẒŕřŗſśŝšşșṣßťţṭŧþúùûüǔŭūũűůųụưẃẁŵẅƿýỳŷÿȳỹƴźżžẓ"
    white_list = string.ascii_letters + string.digits + latin_similar + ' '
    white_list += "'"

    embeddings_chars = ''.join([c for c in tqdm(embeddings_index) if len(c) == 1]) # get all chars in embeddings_index with len==1
    embeddings_symbols = ''.join([c for c in embeddings_chars if not c in white_list]) # get all chars, which are no regular letters

    text_chars = build_vocab(list(text)) # returns a dict of char:char_count
    text_symbols = ''.join([c for c in text_chars if not c in white_list]) # all symbols that appear in text
    
    symbols_to_delete = ''.join([c for c in text_symbols if not c in embeddings_symbols]) # get all symbols from text, that have no embedding
    symbols_to_isolate = ''.join([c for c in text_symbols if c in embeddings_symbols]) # get all symbols from text, that have an embedding
    
    symbols = [s for s in embeddings_index if len(s)==1]
    known_punct = []
    unknown_punct = []

#    for p in punct:
#        try:
#            embeddings_index[p] # prüfe, ob Wort in Embedding vorhanden ist
#            known_punct.append(p)
#        except:
#            unknown_punct.append(p)
#        
#    return known_punct, unknown_punct
	

	

def get_punct_mapping(embeddings_index):
    """
	Checks which punctuation is actually known from embeddings_index
	If punctuation is known it creates a mapping from the punctuation mark to
	its replacement (which is basicaly just a separation of the punctuation by 
	whitespaces)
	Unknown punctuation marks will be replaced with whitespace
	
	
    :param 
        embeddings_index: dict with mapping word:embedding_vector
    :return: 
        punct_mapping: mapping from punctuation to its substitution string
    
    Note: 
        Here, special characters are NOT escaped. This might be lead to errors.
        Escaping speacial characters is handled in "multi_replace".
        Consider using re.escape(pattern) if you want change functions behaviour.
    """
    known_punct, unknown_punct = check_punct(embeddings_index=embeddings_index)
    punct_mapping = {}
    
    for p in known_punct:
        punct_mapping[p] = f' {p} '
    for p in unknown_punct:
        punct_mapping[p] = f' '
        
    return punct_mapping