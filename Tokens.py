class Token:
    def __init__(self):
        self.USED = 'USED'
        self.INT = 'INT'
        self.ID = 'ID'
        self.TOKEN_ARRAY = [
            (r'#[^\n]*', None),
            (r'[ \n\t]+', None),
            (r'if', self.USED),
            (r'else', self.USED),
            (r'for', self.USED),
            (r'while', self.USED),
            (r'do', self.USED),
            (r'end', self.USED),
            (r'and', self.USED),
            (r'not', self.USED),
            (r'or', self.USED),
            (r'!=', self.USED),
            (r':=', self.USED),
            (r'>=', self.USED),
            (r'>', self.USED),
            (r'<=', self.USED),
            (r'<', self.USED),
            (r'/', self.USED),
            (r'\*', self.USED),
            (r'-', self.USED),
            (r'\+', self.USED),
            (r';', self.USED),
            (r'\(', self.USED),
            (r'\)', self.USED),
            (r'==', self.USED),
            (r'[0-9]+', self.INT),
            (r'[A-Za-z][A-Za-z0-9_]*', self.ID),
        ]
