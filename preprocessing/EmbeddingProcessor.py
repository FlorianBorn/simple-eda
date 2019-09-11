from tqdm import tqdm
import operator
import string

class EmbeddingProcessor():
    def __init__(self):
        # Attributes
        self.regular_characters = self.get_white_list()
        self.embeddings_index = None
        self.embeddings_chars = None
        self.embeddings_symbols = None
        self.text_chars = None
        self.text_symbols = None
        
        self.text_symbols = None
        self.known_symbols = None
        self.unknown_symbols = None
        self.known_symbols_dict = None
        self.unknown_symbols_dict = None
        
        #symbols_to_delete
        #symbols_to_isolate
        pass
    
    def load_pretrained(self, path, is_pkl=True):
        '''
        Loads embedding
        For now, embedding file must be a pickle file with format
        word:[d1,d2,...,dn]
        
        param:
            path: Path (String) to embedding (incl. filename)
        '''        
        # reset, if EmbeddingProcessor already had been fitted
        self.embeddings_chars = None
        self.embeddings_symbols = None
        
        with open(path,'rb') as f:
            emb_arr = pickle.load(f)
        self.embeddings_index = emb_arr
        
        # check embeddings dimension (look at multiple vectors in case 
        # of there are some erroneous vectors)
        lengths = []
        for i, v in enumerate(embp.embeddings_index.values()):
            lengths.append(len(v))
            if i==1000: break
        self.embeddings_dimension = max(lengths)
        
    
    def fit_on_text(self, text):
        '''
        Creates a Vocabulary (word:word_count) from text and stores it as class attribute
        
        param:
            text: Series containing text documents
        '''
        # reset, if EmbeddingProcessor already had been fitted
        self.text_chars = None
        self.text_symbols = None 
        self.text_symbols = None
        self.known_symbols = None
        self.unknown_symbols = None
        self.known_symbols_dict = None
        self.unknown_symbols_dict = None
        
        # create vocab
        token_lists = text.apply(lambda x: x.split())
        self.vocab = self.build_vocab(token_lists)
        

    def get_white_list(self):
        # definiere eine Liste von 'regulären' Buchstaben (keine Symbole, wie z.B. Smilies)
        latin_similar = "’'‘ÆÐƎƏƐƔĲŊŒẞÞǷȜæðǝəɛɣĳŋœĸſßþƿȝĄƁÇĐƊĘĦĮƘŁØƠŞȘŢȚŦŲƯY̨Ƴąɓçđɗęħįƙłøơşșţțŧųưy̨ƴÁÀÂÄǍĂĀÃÅǺĄÆǼǢƁĆĊĈČÇĎḌĐƊÐÉÈĖÊËĚĔĒĘẸƎƏƐĠĜǦĞĢƔáàâäǎăāãåǻąæǽǣɓćċĉčçďḍđɗðéèėêëěĕēęẹǝəɛġĝǧğģɣĤḤĦIÍÌİÎÏǏĬĪĨĮỊĲĴĶƘĹĻŁĽĿʼNŃN̈ŇÑŅŊÓÒÔÖǑŎŌÕŐỌØǾƠŒĥḥħıíìiîïǐĭīĩįịĳĵķƙĸĺļłľŀŉńn̈ňñņŋóòôöǒŏōõőọøǿơœŔŘŖŚŜŠŞȘṢẞŤŢṬŦÞÚÙÛÜǓŬŪŨŰŮŲỤƯẂẀŴẄǷÝỲŶŸȲỸƳŹŻŽẒŕřŗſśŝšşșṣßťţṭŧþúùûüǔŭūũűůųụưẃẁŵẅƿýỳŷÿȳỹƴźżžẓ"
        white_list = string.ascii_letters + string.digits + latin_similar + ' '
        white_list += "'"
        return white_list


    def build_vocab(self, token_lists, word_lvl=True, verbose =  True):
        """
        Creates a Dictionary of existing words and their word count from a list of tokens

        :param 
            token_lists: list of list of words
        :return: 
            dictionary of words and their count 
        """
        vocab = {}
        if word_lvl:
            token_lists_pbar = tqdm(token_lists, disable = (not verbose))
            token_lists_pbar.set_description("Build Vocab")
            for token_list in token_lists_pbar:  #tqdm(token_lists, disable = (not verbose)).set_description("Build Vocab")
                for word in token_list:
                    try: # wenn Wort bereits in Dict existiert, zähle es hoch
                        vocab[word] += 1
                    except KeyError: # wenn nicht, lege es an und setze Count auf 1
                        vocab[word] = 1
            #self.vocab = vocab
        else: # char level
            token_lists_pbar = tqdm(token_lists, disable = (not verbose))
            token_lists_pbar.set_description("Build CharLvL Vocab")
            for token_list in token_lists_pbar:  #tqdm(token_lists, disable = (not verbose)).set_description("Build Vocab")
                for word in token_list:
                    try: # wenn Wort bereits in Dict existiert, zähle es hoch
                        vocab[word] += 1
                    except KeyError: # wenn nicht, lege es an und setze Count auf 1
                        vocab[word] = 1
            #return vocab
            #self.vocab_chars = vocab
        return vocab


    def check_coverage(self, fit=True): #, embeddings_index
        """
        Checks if words from vocab exists in embeddings_index (this is the given (pre-trained) embedding)
        Returns a sorted dictionary of unknown words and their word count

        vocab is calculated by the 'build_vocab' function

        :return: dictionary of words not in embedding and their count (sorted from 
        """
        known_words = {}
        unknown_words = {}
        nb_known_words = 0
        nb_unknown_words = 0
        for word in self.vocab.keys():
            try:
                known_words[word] = self.embeddings_index[word]
                nb_known_words += self.vocab[word]
            except:
                unknown_words[word] = self.vocab[word]
                nb_unknown_words += self.vocab[word]
                pass

        print('Found embeddings for {:.3%} of vocab'.format(len(known_words) / len(self.vocab)))
        print('Found embeddings for  {:.3%} of all text'.format(nb_known_words / (nb_known_words + nb_unknown_words)))
        unknown_words = sorted(unknown_words.items(), key=operator.itemgetter(1))[::-1]

        return unknown_words[:40]

    
    def check_symbols(self, verbose=True):
        '''
        ToDo: Find a more suitable function name
        
        Calls __fit_symbols which finds known and unknown symbols from text in embeddings
        
        Creates:
            self.embeddings_chars: tokens in pre-trained embedding with len(token)==1
            self.embeddings_symbols: token in pre-trained emb, which are no regular chars
            self.vocab_chars: tokens in given text with len(token)==1
        
        '''
        # get embeddings chars and embeddings symbols
        embeddings_index_pbar = tqdm(self.embeddings_index)
        embeddings_index_pbar.set_description("Get embeddings_chars")
        self.embeddings_chars = ''.join([c for c in embeddings_index_pbar if len(c) == 1]) # get all chars in embeddings_index with len==1
        embeddings_index_pbar = tqdm(self.embeddings_index)
        embeddings_index_pbar.set_description("Get embeddings_symbols")
        self.embeddings_symbols = ''.join([c for c in embeddings_index_pbar if not c in self.regular_characters]) # get all chars, which are no regular letters
        
        #self.vocab_chars = build_vocab()
        text = ' '.join(self.vocab.keys())
        self.vocab_chars = self.build_vocab(text, word_lvl=False)
        self.__fit_symbols()
        if verbose:
            print(f"Known Symbols:\n{self.known_symbols}")
            print("")
            print(f"Unknown Symbols:\n{self.unknown_symbols}")

    def __fit_symbols(self): # , embeddings_index
        """
        Note: 
            this function don't seem to work as intended, e.g. the punctiation mark ' is not recognized
            as known punctuation
            As a workaround common punctuation marks are added to known symbols manually
        
        Checks if symbols from vocab are known in embeddings_index
        :creates attributes
            text_symbols: a list of 'regular' Text, that appear in the given text and the pre-trained embedding 
            known_symbols: a list of symbols (len==1 and not text symbols) that appear in both given text and embedding
            unknown_symbols: list of symbols that appear in embedding but not in the given text
            known_symbols_dict: mapping known_symbol:replacement
            unknown_symbols_dict mapping unknown_symbol:replacement

        :param 
            text: list of raw strings e.g. ['this is my house', 'the quick brown fox ;)']
            embeddings_index: dict with mapping word:embedding_vector
        :return: 
            known_punct: list of punctuations found in embeddings_index
            unkown_punct: list of punctuations not found in embeddings_index
        """
#         embeddings_index_pbar = tqdm(self.embeddings_index)
#         embeddings_index_pbar.set_description("Get embeddings_chars")
#         self.embeddings_chars = ''.join([c for c in embeddings_index_pbar if len(c) == 1]) # get all chars in embeddings_index with len==1
#         embeddings_index_pbar.set_description("Get embeddings_symbols")
#         self.embeddings_symbols = ''.join([c for c in self.embeddings_chars if not c in self.regular_characters]) # get all chars, which are no regular letters

        #self.build_vocab(list(text), word_lvl=False) # returns a dict of char:char_count
        self.text_symbols = ''.join([c for c in self.vocab_chars if not c in self.regular_characters]) # all symbols that appear in text

        # add some common punctuation marks manually
        common_punctuation = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~“”’\''
        self.known_symbols = ''.join([c for c in self.text_symbols + common_punctuation if c in self.embeddings_symbols]) # all symbols from text, that have an embedding
        self.unknown_symbols = ''.join([c for c in self.text_symbols if not c in self.embeddings_symbols]) # all symbols from text, that have no embedding
        
        self.known_symbols_dict = {ord(c):f' {c} ' for c in self.known_symbols} # maps the ordinal value of a known symbol to it's replacement e.g. 85:' a '
        self.unknown_symbols_dict = {ord(c):f'' for c in self.unknown_symbols} # maps the ordinal value of a unknow symbol to it's replacement e.g. 85:''


    def replace_symbols(self, text, mapping):
        '''
        ToDo: Transfer it into a separate function, maybe
        
        param:
            text: the text, where symbols should be replaced
            mapping: a dictionary which maps the unicode code of a char to its replacement value (ord(c):replacement_string)
        '''
        #text = text.translate(self.unknown_symbols)
        #text = text.translate(self.known_dict)
        text = text.translate(mapping)
        return text
    
    
    def calculate_mean_vector(self):
        '''
        return:
            mean_vector: mean over all vectors from the pre-trained embedding
        '''
        mean_vector = np.zeros(shape=(1, self.embeddings_dimension))
        errors = 0
        for v in self.embeddings_index.values():
            try:
                mean_vector += v
            except:
                errors += 1
                pass
        mean_vector = mean_vector/len(self.embeddings_index)
        print(f"Calculated mean_vector. Ignored {(errors/len(self.embeddings_index))*100:.6f}% of all vectors while computing.")
        return mean_vector
    
    def transform(self):
        '''
        Creates an embedding matrix from the fitted text and the given pre-trained embeddings
        Each word from vocab, which is non present in the pre-trained embedding, is initialized with
        the mean vector computed over the pre-trained embedding
        
        return:
            embedding: new embeddings matrix
        '''
        embedding = np.zeros(shape=(len(self.vocab), self.embeddings_dimension))
        mean_vector = self.calculate_mean_vector()
        
        vocab_pbar = tqdm(enumerate(self.vocab))
        vocab_pbar.set_description('Create Embedding')
        for i, token in vocab_pbar:
            if token in self.embeddings_index:
                embedding[i] = self.embeddings_index[token]
            else:
                embedding[i] = mean_vector       
        return embedding