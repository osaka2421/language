
from errors. Error import RTError
class RTResult:
     def __init__(self):
          self.value = None
          self.error = None
          self.func_return_value = None
     
     def register(self,res) :
          if res.error : 
               self.error = res.error
          self.func_return_value = res.func_return_value
          return res.value
     
     def success(self,value):
          self.value = value
          self.error = None
          self.func_return_value = None
          return self
     
     def failure(self,error):
          self.value = None
          self.error = error
          self.func_return_value = None
          return self

     def success_return(self,value):
          self.func_return_value = value
          return self

         

     
     
################
#####values######


class Number:
     def __init__(self,value):
        self.value = value
        self.set_pos ()
        self.set_context()


     def set_pos(self,pos_start=None,pos_end=None):
          self.pos_start =pos_start
          self.pos_end = pos_end
          return self   
     

     def set_context(self,context=None):
          self.context = context
          return self
     
     def added_to(self,other):
          if isinstance(other,Number):
               return Number(self.value + other.value).set_context(self.context), None

     def subbed_by(self,other):
          if isinstance(other,Number):
               return Number(self.value - other.value).set_context(self.context), None

     def multed_by(self,other):
             if isinstance(other,Number):
               return Number(self.value * other.value).set_context(self.context) , None  

     def dived_by(self , other):
          if isinstance(other,Number):
                if other.value == 0:
                     return None , RTError(
                     other.pos_start,other.pos_end,
                        'Division by zero',self.context
                      )
                

                return Number(self.value / other.value).set_context(self.context), None 
          
     def powerd_by(self ,other):
          if isinstance(other,Number):
               return Number(self.value ** other.value).set_context(self.context),None

     def get_comparison_eq(self, other):
          if isinstance(other, Number):
              return Number(bool(self.value == other.value)).set_context(self.context), None

     def get_comparison_ne(self, other):
	     if isinstance(other, Number):
               return Number(bool(self.value != other.value)).set_context(self.context), None

     def get_comparison_lt(self, other):
          if isinstance(other, Number):
               return Number(bool(self.value < other.value)).set_context(self.context), None

     def get_comparison_gt(self, other):
          if isinstance(other, Number):
               return Number(bool(self.value > other.value)).set_context(self.context), None

     def get_comparison_lte(self, other):
          if isinstance(other, Number):
               return Number(bool(self.value <= other.value)).set_context(self.context), None

     def get_comparison_gte(self, other):
          if isinstance(other, Number):
               return Number(bool(self.value >= other.value)).set_context(self.context), None

     def anded_by(self, other):
          if isinstance(other, Number):
               return Number(bool(self.value and other.value)).set_context(self.context), None
          
     def ored_by(self, other):
          if isinstance(other, Number):
               return Number(bool(self.value or other.value)).set_context(self.context), None

     def notted(self):
          return Number(1 if self.value == 0 else 0).set_context(self.context), None       
     

     def copy(self):
          copy = Number(self.value)
          copy.set_pos(self.pos_start,self.pos_end)
          copy.set_context(self.context)
          return copy  


     def __repr__(self):
            return str(self.value)
     

class string:
     def __init__(self,value):
          self.value = value
          self.set_pos()
          self.set_context()

     def set_pos(self,pos_start = None, pos_end = None):
          self.pos_start = pos_start
          self.pos_end = pos_end
          return self
     

     def set_context(self,context = None):
          self.context = context
          return self
     
     def copy(self):
          copy = string(self.value)
          copy.set_pos(self.pos_start,self.pos_end)
          copy.set_context(self.context)
          return copy
     
     def __repr__(self):
          return str(self.value)
     

class Function:
     def __init__(self,name,body_node,arg_names):
          self.name = name
          self.body_node = body_node
          self.arg_names = arg_names
          self.context = None
          self.pos_start = None
          self.pos_end = None

     def set_pos(self,pos_start = None, pos_end = None):
          self.pos_start = pos_start
          self.pos_end = pos_end
          return self

     def set_context(self, context):
        self.context = context
        return self

     def copy(self):
          copy = Function(self.name,self.body_node,self.arg_names)
          copy.set_context(self.context)
          copy.set_pos(self.pos_start,self.pos_end)
          return copy
     

     def execute(self,args):
          from runtime.context import Context
          from runtime.SymbolTable import SymbolTable
          from runtime.interpreter import Interpreter

          res = RTResult()

          new_context = Context(self.name, self.context)
          new_context.symbol_table = SymbolTable()
          new_context.symbol_table.parent = self.context.symbol_table


          if len(args) != len(self.arg_names):
               return res.failure(RTError(
                    self.body_node.pos_start, self.body_node.pos_end,
                    f"Expected {len(self.arg_names)} arguments , got {len(args)}",
                    self.context
               ))
          

          for name,value in zip(self.arg_names,args):
               value.set_context(new_context)
               new_context.symbol_table.set(name,value)

          interpreter = Interpreter()
          
          value = res.register(interpreter.visit(self.body_node,new_context))


          if res.error : return res

          if res.func_return_value is not None :
               return res.success(res.func_return_value)

          return res.success(value)


class List:
     def __init__(self,elements):
          self.elements = elements
          self.set_pos()
          self.set_context()


     def set_pos(self,pos_start=None,pos_end=None):
          self.pos_start_start = pos_start
          self.pos_end= pos_end
          return self

     def set_context(self,context=None):
          self.context = context
          return self

     def copy(self):
          copy = List(self.elements)
          copy.set_pos(self.pos_start, self.pos_end)
          copy.set_context(self.context)
          return copy

     def __repr__(self):
          return "[" + ",".join(map(str,self.elements))+"]"
          