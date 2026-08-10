TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD='KEYWORD'
TT_EQ = 'EQ'
TT_PLUS ='PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_COMMA = 'COMMA'
TT_POWER = "POWER"
TT_RPAREN = 'RPAREN'
TT_LPAREN ='LPAREN'
TT_LSQUARE = "LSQUARE"
TT_RSQUARE = "RSQUARE"
TT_EE = 'EE'
TT_NE = 'NE'
TT_LT = 'LT'
TT_GT = 'GT'
TT_LTE = 'LTE'
TT_GTE = 'GTE'
TT_STRING = "STRING"
TT_NEWLINE = 'NEWLINE'
TT_EQF    =  'EOF'


KEYWORDS = ["HENSU","AND","OR","NOT","WHEN","DO","ORWHEN","END","OTHERWISE","SHOW","INPUT"
            ,"WHILE","FOR","STEP","TO","FUN","RETURN"]


class Token:
    def __init__(self,type_,value=None,pos_start=None,pos_end=None):
        self.type_ = type_
        self.value = value

        if pos_start:
             self.pos_start = pos_start.copy()
             self.pos_end = pos_start.copy()
             self.pos_end.advance() 

        if pos_end:
             self.pos_end = pos_end.copy()


    def matches (self,type_ ,value):
         return self.type_ == type_ and self.value== value
               
   

    def __repr__(self):
        if self.value: return f'{self.type_}:{self.value}'
        return f'{ self.type_}'
    



