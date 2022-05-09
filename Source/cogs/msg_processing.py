import json

from .other_methods import load_config

config = load_config(
    r'C:\Users\Misiek\Desktop\Python\raceday\Source\config.json')


class MessagePreparator:
    """
    A bunch of functions that process messages for a deep learning 
    model.

    Available methods:
    drop_special_characters
    lower_letters
    prepare_sequence
    overwrite_json_file
    """

    path_to_vocabulary = config['pathToVocab']

    with open(path_to_vocabulary, encoding='utf8') as json_file:
        data = json.load(json_file)

    @staticmethod
    def drop_special_characters(msg: str) -> str:
        """
        Function drop_special_characters removes all characters from
        message that are not: letters, numbers or spaces.

        Parameters
        ----------
        msg : str
            A message from which special characters will be removed.

        Returns
        -------
        str
        """
        msg = [character for character in msg
               if (character in list('abcdefghijklmnoprstuwyzxvq0123456789 '))]
        msg = "".join(msg)
        return msg

    @staticmethod
    def lower_letters(msg: str) -> str:
        """
        Function lower_letters replaces all uppercase letters with 
        lowercase letters.

        Parameters
        ----------
        msg : str
            A message which all letters will be replaced with lowercase 
            letters.

        Returns
        -------
        str
        """
        return msg.lower()

    @classmethod
    def prepare_sequence(cls, msg: str) -> list:
        """
        Function prepare_sequence replaces all words with numbers from 
        model_vocab.json file. If a word is missed, then it is added 
        with assigned a unique value.  

        Parameters
        ----------
        msg : str
            A message where words are replaced with tokens. List that 
            contains such values can feed a DL model.

        Returns
        -------
        list
        """
        word_index = []
        for word in msg.split(' '):
            if (word not in cls.data.keys()):
                cls.data[word] = len(cls.data) + 1
                cls.overwrite_json_file()

            word_index.append(cls.data[word])
        return word_index

    @classmethod
    def overwrite_json_file(cls) -> None:
        """
        Function overwrite_json_file overwrites the vocabulary set if a 
        new word was used. This method is used in the function 
        MessagePreparator.prepare_sequence.
        """
        with open(cls.path_to_vocabulary, "w", encoding='utf8') as outfile:
            json.dump(cls.data, outfile, ensure_ascii=False)
