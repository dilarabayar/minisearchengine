from os import path  # used for to check if input directory is exist
import os  # used for to take path and join path name with filenames.
import string  # used for prevent case sensitivity


class TrieNode:

    def __init__(self, word):
        self.word = word  # words that are added in trie
        self.index = []  # positions of node in a text.
        self.children = {}  # trie itself.
        self.isEndOfWord = False  # if node is end of word this will be true.


class Trie:

    def __init__(self, filename):
        self.root = TrieNode(None)  # root of trie.
        self.filename = filename  # which file this trie belongs.

    def add(self, key, position, filename):
        node = self.root
        ind = 0
        self.filename = filename
        for ch in key:
            position = position + 1
            if ch not in node.children:
                node.children[ch] = TrieNode(None)
                if ch == key[0]:  # If first character of word is not in trie.
                    ind = position
            elif ch in node.children and (ch == key[0]):  # If first character of word is already in trie.
                ind = position
            node = node.children[ch]  # move in trie.
            node.index.append(ind)  # append position of first node to all nodes in that word.

        node.word = key  # adding word to last node.
        node.isEndOfWord = True  # making true since this is last node.
        return position

    def commonWordSearch(self, listOfFiles, listName):
        # Used bfs search algorithm to find all keys in a first given file and then used normal trie key search in other ones.
        queue = [self.root]  # add root to queue.
        matched = 0
        matchedWords = []  # keeping common words in array.

        # finding words in trie with using bfs search.
        while queue:
            trieNode = queue.pop(0)
            if trieNode.word is not None:
                for j in range(0, len(listOfFiles)):
                    if listName.filename == listOfFiles[j].filename:
                        continue
                    elif listOfFiles[j].search(trieNode.word):
                        matched = matched + 1  # matching word found.
                if matched == len(listOfFiles) - 1:  # word must be in all of the tries.
                    matchedWords.append(trieNode.word)
                matched = 0
            queue.extend(list(trieNode.children.values()))

        print("Common words in a given files are: ")
        for i in range(0, len(matchedWords)):
            print(matchedWords[i])
        print("\n")

    def search(self, word):  # finding word in trie.
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]

        # Checking if we are in the last node in trie.This assures that word is not prefix.
        if node.isEndOfWord:
            return True
        else:
            return False

    def prefixSearch(self, key):
        node = self.root
        for ch in key:
            if ch not in node.children:  # if character is not in trie don't search anymore.
                print("Sorry, Couldn't find the prefix ", key, "in ", self.filename, "\n")
                return False
            node = node.children[ch]

        print(key, "prefix has been found in text and positions in the text are: ", end=' ')
        for k in range(len(node.index)):
            print(node.index[k], end=' ')
        print("\n")

    def printFileName(self):
        print(self.filename)


def readInputFiles():
    files = []
    check = True

    filePath = input("Enter the path of your file: ")
    while not path.isdir(filePath):  # checks if given input is path
        filePath = input("Directory is not exist! Please try again!: ")
    file_names = os.listdir(filePath)

    # this part takes files get rid of all end of line, punctuations and lowers all characters which ensures that search
    # is not case sensitive.Finally puts all of them in array. Returns both array and filenames.
    for file in os.listdir(filePath):
        if file.endswith('.txt'):
            check = False
            file_dir = os.path.join(filePath, file)
            if os.path.isfile(file_dir):
                with open(file_dir, "r") as file_name:
                    file_string = file_name.read().replace('\n', '')
                    file_string = ''.join([i for i in file_string if (not i.isdigit() or not i.isalpha())])
                    file_string = file_string.translate(str.maketrans('', '', string.punctuation)).lower()
                    files.append(file_string)

    if check:
        print("Sorry, in a given directory there is no text file. Please try again!")
    return check,files, file_names


def main():
    loop = True
    position = 0  # used for not losing positions.
    duplicate_check = 0
    entry = None
    valid_check = 0
    txt_check = True

    while txt_check:
        txt_check,file, names = readInputFiles()

    listOfTrie = [Trie(names[i]) for i in range(len(names))]
    listOfFiles = []

    for i in range(0, len(names)):
        word = file[i].split()
        for j in range(0, len(word)):
            position = (listOfTrie[i].add(word[j], position, names[i]))  # takes last position and gives to method again.this way we will not lose position.
        position = 0  # position was reset because file is over.

    while loop:
        print("1 for Prefix\n2 for Common Words\n3 for Exit")
        option = input("Please enter your choice [1-3]:")

        if option == '1':
            prefix = input("Enter the prefix:").lower()  # lowers word and make sures that it's not case sensitive.
            for i in range(0, len(names)):
                listOfTrie[i].prefixSearch(prefix)  # searching prefix in all of the files in a given path.
        elif option == '2':

            while entry != "end":  # takes input from user until he enters end word.
                entry = input("Please enter the files like [filename].txt and if you want to quit type end : ")
                # checks filenames in all ot the trie and if match found puts them in array.
                if not entry.endswith('.txt'):
                    if entry != "end":
                        print("Please make sure that you have entered valid text name! ")
                else:
                    for i in range(0, len(listOfTrie)):
                        if entry == listOfTrie[i].filename:
                            valid_check = 1
                            for j in range(0, len(listOfFiles)):
                                if listOfTrie[i].filename != listOfFiles[j].filename:
                                    duplicate_check = duplicate_check + 1
                            if duplicate_check == len(listOfFiles):  # check duplicates.
                                listOfFiles.append(listOfTrie[i])
                            duplicate_check = 0  # removes duplicate.
                    if valid_check != 1:
                        print("You have entered file name that does not exist in a given directory!")
                    valid_check = 0

            if not listOfFiles:
                print("Sorry, You did not enter any valid filename!")
                valid_check = 0

            else:
                print("All valid filenames are : ", end='')
                for i in range(0, len(listOfFiles)):
                    print(listOfFiles[i].filename, end=' ')
                print("\n")

                listOfFiles[0].commonWordSearch(listOfFiles, listOfFiles[0])
                valid_check = 0
                listOfFiles.clear()
            entry = None

        elif option == '3':
            print("End of the program...Bye...")
            loop = False
        else:
            print("Wrong selection of menu!Please try again.")


if __name__ == "__main__":
    main()
