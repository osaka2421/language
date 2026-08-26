class NumberNode:
    def __init__(self,tok):
        self.token = tok

        self.pos_start =self.token.pos_start
        self.pos_end =self.token.pos_end

    def __repr__(self):
        return f'{self.token}'   
    
class VarAssignNode:
     def __init__(self,var_name_tok,value_node): 
          self.var_name_tok= var_name_tok
          self.value_node = value_node


          self.pos_start = self.var_name_tok.pos_start
          self.pos_end = self.var_name_tok.pos_end


class VarAccessNode:
     def __init__(self, var_name_tok,):
         self.var_name_tok =  var_name_tok

         self.pos_start = self.var_name_tok.pos_start
         self.pos_end =self.var_name_tok.pos_end 


class ListNode:
     def __init__(self, element_nodes ,pos_start,pos_end):
          self.element_nodes = element_nodes

          self.pos_start = pos_start
          self.pos_end = pos_end



class BinOpNode:
    def __init__(self,left_node,op_tok,right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end


    def __repr__(self):
        return f'{self.left_node},{self.op_tok},{self.right_node}'   
   
   
   
   
class WhenNode:
     def __init__(self,cases,otherwise_case):
          self.cases = cases
          self.otherwise_case = otherwise_case

          self.pos_start = self.cases[0][0].pos_start


          if self.otherwise_case:
               self.pos_end = self.otherwise_case.pos_end
          else:
               self.pos_end = self.cases[-1][1].pos_end

class WhileNode :
     def __init__(self,condition_node,body_node):

          self.condition_node = condition_node
          self.body_node = body_node

          self.pos_start = condition_node.pos_start
          self.pos_end = body_node.pos_end



class ForNode:
     def __init__(self,var_name_tok,start_value_node,end_value_node,step_value_node,body_node):
          self.var_name_tok = var_name_tok
          self.start_value_node = start_value_node
          self.end_value_node = end_value_node
          self.step_value_node = step_value_node
          self.body_node = body_node

          self.pos_start = self.var_name_tok.pos_start
          self.pos_end = self.body_node.pos_end


class ShowNode:
     def __init__(self,value_node):
          self.value_node = value_node


          self.pos_start = value_node.pos_start
          self.pos_end = value_node.pos_end

class InputNode:
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end

class FunNode:
     def __init__(self,var_name_tok,arg_name_toks,body_node):
          self.var_name_tok = var_name_tok
          self.arg_name_toks = arg_name_toks
          self.body_node = body_node

          self.pos_start = var_name_tok.pos_start
          self.pos_end = body_node.pos_end


class CallNode:
     def __init__(self,node_to_call,arg_nodes):
          self.node_to_call = node_to_call
          self.arg_nodes = arg_nodes


          self.pos_start = self.node_to_call.pos_start


          if len(self.arg_nodes) > 0 :
               self.pos_end = self.arg_nodes[-1].pos_end
          else:
               self.pos_end = self.node_to_call.pos_end


class ReturnNode:
     def __init__(self,node_to_return,pos_start,pos_end):
          self.node_to_return = node_to_return

          self.pos_start = pos_start
          self.pos_end = pos_end


class StringNode:
     def __init__(self,tok):
          self.tok = tok

          self.pos_start = tok.pos_start
          self.pos_end = tok.pos_end

class ListExprNode:
     def __init__(self,element_nodes,pos_start,pos_end):
          self.element_nodes = element_nodes
          self.pos_start = pos_start
          self.pos_end = pos_end


class IndexNode :
     def __init__(self, list_node, index_node):
          self.list_node = list_node
          self.index_node = index_node

          self.pos_start = list_node.pos_start 
          self.pos_end = index_node.pos_end

class IndexAssignNode:
     def __init__(self,index_node,value_node):
          self.index_node = index_node
          self.value_node = value_node

          self.pos_start = index_node.pos_start
          self.pos_end = value_node.pos_end 


class LenNode:
     def __init__(self,value_node):
          self.value_node = value_node

          self.pos_start = value_node.pos_start
          self.pos_end = value_node.pos_end
          
          
          
class UnaryOpNode:
     def __init__(self,op_tok,node):
          self.op_tok = op_tok
          self.node = node

          self.pos_start = self.op_tok.pos_start
          self.pos_end = node.pos_end

     def __repr__(self):
          return f'{self.op_tok},{self.node}'
     
