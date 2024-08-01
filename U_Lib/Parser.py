class Parser:
    def __init__(self, filePath, commentDelim: str = "#") -> None:
        self.commentDelim = commentDelim
        self.origLines = None
        self.comments = []
        self.words = []
        self.collapsedList = []

        with open(filePath) as f:
            self.origLines = f.readlines()

        for line in self.origLines:
            match line[0]:
                case "[":
                    pass
                case self.commentDelim:
                    self.comments.append(line)
                    pass
                case _:
                    self.words.append(line)
                    pass

    def breakDownAllStrings(self, delim: str = " "):
        self.collapsedList = []

        for word in self.words:
            if delim in word:
                for sub in word.split(delim):
                    self.collapsedList.append(sub)

                continue

            self.collapsedList.append(word)

        return self.collapsedList
