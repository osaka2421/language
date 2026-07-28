from core.tokens import *
from core.nodes import *
from errors. Error import InvalidSyntaxError 
class ParseResult:
     def __init__(self):
          self.error = None
          self.node = None
          self.advance_count = 0


     def register_advancement(self):
          self.advance_count += 1
          
          
     def register(self, res):
           self.advance_count += res.advance_count
           if res.error :self.error = res.error
           return res.node
   

     def success(self , node):
          self.node = node
          return self
          
     
     def failure(self ,error):
          if not self.error or self.advance_count == 0:

           self.error = error
          return self
          
    

###############
##### parser ##### 

class Parser:
    def __init__(self ,tokens):
        self.tokens =tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
            self.tok_idx+=1
            if self .tok_idx< len(self.tokens):
                self.current_tok = self.tokens[self.tok_idx]
                return self.current_tok
            
##################################################
    def parse (self):
            res = self.statements()

            if not res.error and self.current_tok.type_!=TT_EQF:
                 return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end, "Expected '+', '-', '*', '/' or '^'" ))
            return res
    
    def atom(self):
            res = ParseResult()
            tok = self.current_tok

            if tok.type_ in (TT_INT, TT_FLOAT):
                res.register_advancement()
                self.advance()
                return res.success(NumberNode(tok))
            
            elif tok.type_  == TT_IDENTIFIER:
                 res.register_advancement()
                 self.advance()

                 var_access = VarAccessNode(tok)

                 if self.current_tok.type_ == TT_LPAREN:
                      res.register_advancement()
                      self.advance()

                      arg_nodes = []

                      while self.current_tok.type_ != TT_RPAREN:
                           arg = res.register(self.expr())
                           if res.error:
                                return res 
                           
                           arg_nodes.append(arg)

                      res.register_advancement()
                      self.advance()

                      return res.success(CallNode(var_access,arg_nodes))
                 
                 return res.success(var_access)


            elif tok.type_ == TT_LPAREN:
                res.register_advancement()
                self.advance()
                expr = res.register(self.expr())
                if res.error: return res
                if self.current_tok.type_ == TT_RPAREN:
                    res.register_advancement()
                    self.advance()
                    return res.success(expr)
               
                else:
                    return res.failure(InvalidSyntaxError(
                         self.current_tok.pos_start,
                         self.current_tok.pos_end,
                         "Expected ')"))
                    
            elif tok.matches(TT_KEYWORD,'WHEN'):
                 when_expr = res.register(self.when_expr())  
                 
                 if res.error:
                      return res 
                 
                 return res.success(when_expr)
            
            elif tok.matches(TT_KEYWORD, 'WHILE'):
                 while_expr = res.register(self.while_expr())
                 if res.error:
                      return res
                 return res.success(while_expr)
            
            elif tok.matches(TT_KEYWORD ,'FOR'):
                 for_expr = res.register(self.for_expr())
                 if res.error:
                      return res
                 return res.success(for_expr)
            
            elif tok.matches(TT_KEYWORD,'FUN'):
                 fun_expr = res.register(self.fun_expr())
                 if res.error:
                      return res
                 return res.success(fun_expr)
            
            elif tok.type_ == TT_STRING:
                 res.register_advancement()
                 self.advance()
                 return res.success(StringNode(tok))
                        
            if tok.matches(TT_KEYWORD , "INPUT"):
                 res.register_advancement()
                 self.advance()
                 return res.success(InputNode(tok.pos_start, tok.pos_end))

            return res.failure(InvalidSyntaxError(
                 tok.pos_start, tok.pos_end,
                 "Expected int,float,identifier,When,'+ ' , '-' , or '('") )
             
    def power(self):
         return self.bin_op(self.atom,(TT_POWER, ),self.factor)
                                    
    
    def factor(self):
            res = ParseResult()
            tok = self.current_tok
            
            
            if tok.type_ in (TT_PLUS, TT_MINUS):
                 res.register_advancement()
                 self.advance()
                 factor = res.register(self.factor())
                 if res.error : return res
                 return res.success(UnaryOpNode(tok,factor))
            
            return self.power()
             
           
    def term(self):
         return self.bin_op(self.factor,(TT_MUL, TT_DIV))
    
    def arith_expr(self):
         return self.bin_op(self.term,(TT_PLUS,TT_MINUS))
    

    def comp_expr(self):
         res = ParseResult()

         if self.current_tok.matches(TT_KEYWORD , 'NOT'):
              op_tok = self.current_tok
              res.register_advancement()
              self.advance()

              node = res.register(self.comp_expr())
              if res.error: return res
              return res.success(UnaryOpNode(op_tok,node)) 
         
         
         
         node = res.register(self.bin_op(self.arith_expr,(TT_EE ,TT_NE, TT_LT, TT_LTE, TT_GT, TT_GTE)))

         if res.error:
              return res.failure(InvalidSyntaxError(
                   self.current_tok.pos_start ,self.current_tok.pos_end,
                    "Expected int ,float,identifier'+ ' , '-' , ' (' , 'NOT'"
               ))
         

         return res.success(node)
    
    def statements(self):
          res =ParseResult()
          statements = []

          while self.current_tok.type_ == TT_NEWLINE:   
                res.register_advancement()
                self.advance()

          statement = res.register(self.expr())
          if res.error :
                return res

          statements.append(statement)


          while True :
            while self.current_tok.type_ == TT_NEWLINE:
                 res.register_advancement()
                 self.advance()

            if (
                 self.current_tok.type_ == TT_EQF
                 or  self.current_tok.matches(TT_KEYWORD,'END')
            ):
                 break
                 
            statement = res.register(self.expr())
            if res.error:
                      return res
     
          
            statements.append(statement)

                
          return res.success(
               ListNode(
               statements,
               statements[0].pos_start,
               statements[-1].pos_end 
               )
          )
                
                
    def expr(self):
            res = ParseResult()


            if self.current_tok.matches(TT_KEYWORD,"SHOW"):
                 res.register_advancement()
                 self.advance()

                 value = res.register(self.expr())

                 if res.error:
                      return res
                 
                 return res.success(ShowNode(value))
                 

            
            if self.current_tok.matches(TT_KEYWORD, "HENSU"):
                 res.register_advancement()
                 self.advance()



                 if self.current_tok.type_ != TT_IDENTIFIER:     
                     return res.failure(InvalidSyntaxError(
                      self.current_tok.pos_start,self.current_tok.pos_end,
                      "expected identifier"
                    ))
                 
            
                 var_name = self.current_tok
                 res.register_advancement()
                 self.advance()

                 if self.current_tok.type_ != TT_EQ:
                     return res.failure(InvalidSyntaxError(
                       self.current_tok.pos_start,self.current_tok.pos_end,
                       "Expected '=' "
                      
                    ))

            
                 res.register_advancement()
                 self.advance()
                 expr = res.register(self.expr())
                 if res.error : return res 
                 return res.success(VarAssignNode(var_name, expr))


            if self.current_tok.matches(TT_KEYWORD, "RETURN"):
                 return_tok = self.current_tok
                 res.register_advancement()
                 self.advance()

                 expr = res.register(self.expr())
                 if res.error:
                      return res

                 return res.success(
                     ReturnNode(
                          expr,
                           return_tok.pos_start,
                          expr.pos_end
                     )
                      
                 )
                 
             

            node = res.register(self.bin_op(self.comp_expr,((TT_KEYWORD ,'AND'),(TT_KEYWORD ,'OR'))))

            if res.error: 
                 return res.failure(InvalidSyntaxError(
                      self.current_tok.pos_start,self.current_tok.pos_end ,
                     "Expected 'HENSU', int ,float,identifier'+ ' , '-' , or '('"
                ))
            return res.success(node)
       
    def when_expr(self):
         res = ParseResult()
         
         if not self.current_tok.matches(TT_KEYWORD, 'WHEN'):
              return res.failure(
                   InvalidSyntaxError(
                   self.current_tok.pos_start,
                   self.current_tok.pos_end,
                   "Expected 'WHEN'"
              ))
                   
         res.register_advancement()
         self.advance()      
         
         condition = res.register(self.expr())
         if res.error:
              return res
       
         if not self.current_tok.matches(TT_KEYWORD, 'DO'):
              return res.failure(InvalidSyntaxError(
                   self.current_tok.pos_start,self.current_tok.pos_end,
                   "Expected 'DO'"
              ))
          
         res.register_advancement()
         self.advance()    
         
         while self.current_tok.type_ == TT_NEWLINE:
              res.register_advancement()
              self.advance()
              
              
         body = res.register(self.expr())

         if res.error:
              return res
         
         cases = [(condition, body)]
         
         
            
         while self.current_tok.type_ == TT_NEWLINE:
              res.register_advancement()
              self.advance()  

         while self.current_tok.matches(TT_KEYWORD, 'ORWHEN'):
              res.register_advancement()
              self.advance()

              condition = res.register(self.expr())

              if res.error:
                   return res
              
              if not self.current_tok.matches(TT_KEYWORD, 'DO'):
                   return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start,self.current_tok.pos_end,
                        "Expected 'DO'"
                   ))
              
              if res.error:
                   return res
              
              res.register_advancement()
              self.advance()

              while self.current_tok.type_ == TT_NEWLINE:
                   res.register_advancement()
                   self.advance()

              body = res.register(self.expr())

              if res.error:
                   return res
              
              cases.append((condition,body))

              while self.current_tok.type_ == TT_NEWLINE:
                   res.register_advancement()
                   self.advance()

              
              
         otherwise_case = None
         
         if self.current_tok.matches(TT_KEYWORD, 'OTHERWISE'):
              res.register_advancement()
              self.advance()
              
              while self.current_tok.type_ == TT_NEWLINE:
                   res.register_advancement()
                   self.advance()
                   
              otherwise_case = res.register(self.expr())    
              
              
              if res.error:
                   return res
              
              
              while self.current_tok.type_ == TT_NEWLINE:
                       res.register_advancement()
                       self.advance()
                       
                       
         if not self.current_tok.matches(TT_KEYWORD, 'END'):
              return res.failure(InvalidSyntaxError(
                   self.current_tok.pos_start,self.current_tok.pos_end,
                   "Expected 'END'"
              ))
              
         res.register_advancement()     
         self.advance()
         
     
         return res.success(WhenNode(cases,otherwise_case))
    
    def while_expr(self):
         res = ParseResult()

         if not self.current_tok.matches(TT_KEYWORD, 'WHILE'):
              
              return res.failure(InvalidSyntaxError(
                   self.current_tok.pos_start,self.current_tok.pos_end,
                   "Expected 'WHILE'"
              ))
         
         res.register_advancement()
         self.advance()

         condition = res.register(self.expr())
         if  res.error:
              return res
         
         if not self.current_tok.matches(TT_KEYWORD,'DO'):
              return res.failure(InvalidSyntaxError(
                   self.current_tok.pos_start,self.current_tok.pos_end,
                   "Expected 'DO'"
              ))
         
         res.register_advancement()
         self.advance()

         while self.current_tok.type_ == TT_NEWLINE:
              res.register_advancement()
              self.advance()

         body = res.register(self.statements())
         if res.error:
              return res
         
         while self.current_tok.type_ == TT_NEWLINE:
              res.register_advancement()
              self.advance()

         if not self.current_tok.matches(TT_KEYWORD, 'END'):
              return res.failure(InvalidSyntaxError(
                   self.current_tok.pos_start,self.current_tok.pos_end,
                   "Expected 'END'"
              ))
         
         res.register_advancement()
         self.advance()

         return res.success(WhileNode(condition,body))
    

    def fun_expr(self):
         res = ParseResult()


         if not self.current_tok.matches(TT_KEYWORD,"FUN"):
              return res.failure(InvalidSyntaxError(
                   self.current_tok.pos_start , self.current_tok.pos_end,
                   "Expected 'FUN'"
              ))
         
         res.register_advancement()
         self.advance()


         if self.current_tok.type_ != TT_IDENTIFIER:
              return res.failure(InvalidSyntaxError(
                   self.current_tok.pos_start , self.current_tok.pos_end,
                   "Expected IDENTIFIER"
              ))
         
         var_name_tok = self.current_tok

         res.register_advancement()
         self.advance()

         if self.current_tok.type_ != TT_LPAREN :
              return res.failure(InvalidSyntaxError(
                   self.current_tok.pos_start , self.current_tok.pos_end ,
                   "Expected '('"
              ))
         

         res.register_advancement()
         self.advance()

         arg_name_toks = []

         while self.current_tok.type_ == TT_IDENTIFIER:
              arg_name_toks.append(self.current_tok)

              res.register_advancement()
              self.advance()

         if self.current_tok.type_ != TT_RPAREN:
              return  res.failure(InvalidSyntaxError(
                   self.current_tok.pos_start , self.current_tok.pos_end ,
                   "Expected ')'"
              ))
         
         res.register_advancement()
         self.advance()

         if not self.current_tok.matches(TT_KEYWORD, "DO"):
              return res.failure(InvalidSyntaxError(
                   self.current_tok.pos_start , self.current_tok.pos_end ,
                   "Expected 'DO '"
              ))
         

         res.register_advancement()
         self.advance()

         body_node = res.register(self.statements())

         if res.error:
              return res
         

         if not self.current_tok.matches(TT_KEYWORD,"END"):
              return res.failure(InvalidSyntaxError(
                   self.current_tok.pos_start,self.current_tok.pos_end,
                   "Expected 'END'"
              ))
         

         res.register_advancement()
         self.advance()


         return res.success(
              FunNode(
               var_name_tok,
              arg_name_toks,
              body_node
              ))

    def for_expr(self):
         res = ParseResult()


         if not self.current_tok.matches(TT_KEYWORD,"FOR"):
              return res.failure(InvalidSyntaxError(
                   self.current_tok.pos_start,self.current_tok.pos_end,
                   "Expected 'FOR'"
              ))
         
         res.register_advancement()
         self.advance()

         if self.current_tok.type_ != TT_IDENTIFIER:
              return res.failure(InvalidSyntaxError(
                   self.current_tok.pos_start,self.current_tok.pos_end,
                   "Expected Identifier"
              ))
         

         var_name = self.current_tok

         res.register_advancement()
         self.advance()


         if self.current_tok.type_ != TT_EQ:
              print("current token",self.current_tok)
              return res.failure(InvalidSyntaxError(
                   self.current_tok.pos_start,self.current_tok.pos_end,
                   "Expected  '='"
              ))
         


         res.register_advancement()
         self.advance()


         start_value = res.register(self.expr())



         if res.error:
              return res
         

         if not self.current_tok.matches(TT_KEYWORD,"TO"):
              return res.failure(InvalidSyntaxError(
                   self.current_tok.pos_start,self.current_tok.pos_end,
                   "Expected 'TO'"
              ))
         

         res.register_advancement()
         self.advance()

         end_value = res.register(self.expr())
         if res.error:
              return res
         

         step_value = None
         

         if self.current_tok.matches(TT_KEYWORD,"STEP"):
              res.register_advancement()
              self.advance()

              step_value = res.register(self.expr())
              if res.error:
                   return res


         if not self.current_tok.matches(TT_KEYWORD,"DO"):
              return res.failure(InvalidSyntaxError(
                   self.current_tok.pos_start,self.current_tok.pos_end,
                   "Expected 'DO'"
              ))
         

         res.register_advancement()
         self.advance()

         body = res.register(self.statements())
          
         if not self.current_tok.matches(TT_KEYWORD,"END"):
              return res.failure(InvalidSyntaxError(
                   self.current_tok.pos_start,self.current_tok.pos_end,
                   "Expected 'END'"
              ))
         
         res.register_advancement()
         self.advance()


         return res.success(ForNode(
              var_name,
              start_value,
              end_value,
              step_value,
              body
         ))

      
    def bin_op(self,func_a, op,func_b = None):
      if func_b == None:
          func_b = func_a
      res = ParseResult() 
      left = res.register(func_a())
      if res.error : return res 

      while self.current_tok.type_ in op or (self.current_tok.type_ , self.current_tok.value) in op:
          op_tok = self.current_tok
          res.register_advancement()
          self.advance()
          right = res.register(func_b())
          if res.error :return res
          left = BinOpNode(left,op_tok,right)

                    
      return res.success(left)
    


