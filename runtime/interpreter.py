from core.tokens import *
from runtime.values import *
class Interpreter :
       def visit(self,node ,context):      
          method_name = f'visit_{type(node).__name__}'
          method = getattr(self,method_name,self.no_visit_method)
          return method(node ,context)
     

       def no_visit_method(self,node, context):
          raise Exception(f'No visit_{type(node).__name__} method defined')

###########################################################################3     
      
       def visit_NumberNode(self,node, context):
            return RTResult().success(
             Number(node.token.value)
             .set_context(context).set_pos(node.pos_start,node.pos_end)
           )#
       

       def visit_VarAccessNode(self,node, context):
            res = RTResult()
            var_name = node.var_name_tok.value
            value = context.symbol_table.get(var_name)



            if not value:
               return res.failure(RTError(
                    node.pos_start,node.pos_end,
                    f"'{var_name}'is not defined",
                    context
               ))
            
            value = value.copy().set_pos(node.pos_start,node.pos_end)
            return res.success(value)
       

       def visit_VarAssignNode(self,node,context):
            res = RTResult()
            var_name = node.var_name_tok.value 
            value = res.register(self.visit(node.value_node, context))
            if res.error : return res

            context.symbol_table.set(var_name,value)
            return res.success(None)
       
       def visit_ListNode(self,node,context):
            res = RTResult()
            results =[]

            for element_nodes in node.element_nodes:
                 value = res.register(self.visit(element_nodes,context))

                 if res.error:
                      return res

                 if res.func_return_value is not None:
          
                      return res
                 
                 if value is not None:
                      results.append(value)

            return res.success(None)

           
       

       def visit_ForNode(self,node,context):
            res = RTResult()

            start_value = res.register(
                 self.visit(node.start_value_node,context)
            )


            end_value = res.register(
                 self.visit(node.end_value_node,context)
            )


            if node.step_value_node:
                 step_value = res.register(
                      self.visit(node.step_value_node,context)

                 )

            else :
                 step_value = Number(1)


            i = start_value.value

            while i <= end_value.value:
                 context.symbol_table.set(
                      node.var_name_tok.value, 
                      Number(i)
                 )
                 
                 res.register (self.visit(node.body_node,context)
                 )

                 if res.error:
                      return res
                 

                 i += step_value.value


            return res.success(None)
       
       
       def visit_WhenNode(self,node,context):
            res = RTResult()


            for condition,body in node.cases:
                 condition_value = res.register(self.visit(condition,context))
                 

                 if res.error:
                      return res
                 
                 if condition_value.value:
                      value = res.register(self.visit(body,context))
                         
                      
                      if res.error:
                           return res
                      

                      return res.success(value)
                 
            if node.otherwise_case:
               value = res.register(self.visit(node.otherwise_case,context))
               if res.error:
                    return res
               
               return res.success(value)
            
            return res.success(Number(0))
       
       
       def visit_WhileNode(self,node,context):
            res = RTResult()
            loop_count = 0 
            max_loop = 10000
            while True:
                 loop_count += 1
                 if loop_count > max_loop:
                      return res.failure(RTError(
                           node.pos_start,node.pos_end,
                           "Infinite loop detect",context
                      ))
                      
     
                 condition = res.register(self.visit(node.condition_node,context))
                 if  res.error:
                      return res
                 
                 if not condition.value:
                      break
                 
                 res.register(self.visit(node.body_node,context))
                 if res.error:
                      return res
                 
            return res.success(None)
       
       def visit_FunNode(self,node,context):
            res = RTResult()


            func_name = node.var_name_tok.value
            body_node = node.body_node
            arg_names = [arg.value for arg in node.arg_name_toks]


            func_value = Function(
                 func_name,
                 body_node,
                 arg_names
            ).set_context(context)


            context.symbol_table.set(func_name,func_value)


            return res.success(None)
       

       def visit_CallNode(self,node,context):
            res = RTResult()

            value_to_call = res.register(
                 self.visit(node.node_to_call,context)
            )

            if res.error:
                 return res
            

            args = []

            for arg_node in node.arg_nodes:
                 args.append(
                      res.register(
                           self.visit(arg_node,context)
                      )
                 )

                 if res.error:
                      return res
            return_value = res.register(
                 value_to_call.execute(args)
            )
           
            if res.error:
                 return res
            
            return res.success(return_value)

       def visit_ReturnNode(self,node,context):
            res= RTResult()

            value = res.register(self.visit(
                 node.node_to_return,context
            ))

            if res.error:
                 return res

            return res.success_return(value)
            
       def visit_ShowNode(self,node,context):
            res = RTResult()

            value = res.register(
                 self.visit(node.value_node,context))
            
            if res.error:
                 return res
            
            print(value)

            return res.success(None)

       def  visit_ListExprNode(self,node,context):
            res = RTResult()

            elements = []

            for element_node in node.element_nodes:
                 elements.append(res.register(self.visit(element_node,context)))

                 if res.error:
                      return res

            return res.success(
                 List(elements)
                 .set_context(context)
                 .set_pos(node.pos_start,node.pos_end)
            )
                 
       
       
       def visit_InputNode(self,node,context):
            res =RTResult()
         

            text = input()

            try :
                 value = int(text)
            except:
                 try:
                      value = float(text)
                 except:
                      return res.failure(RTError(
                           node.pos_start,
                           node.pos_end,
                           "Expected a Number",context
                      ))
                 
            return res.success(Number(value))
       
       def visit_StringNode(self,node,context):      
            return RTResult().success(
                 string(node.tok.value)
                 .set_context(context).set_pos(node.pos_start,node.pos_end)
                 
            )

       def visit_IndexNode(self, node, context):
            res = RTResult()

            list_value = res.register(self.visit(node.list_node, context))
            if res.error:
                 return res

            index = res.register(self.visit(node.index_node,context))
            if res.error:
                 return res

            if not isinstance(list_value, List):
                 return res.failure(
                      RTError(
                           node.pos_start,
                           node.pos_end,
                           "Expected a list",
                           context
                      )
                 )

            if not isinstance(index,Number):
                 return res.failure(
                      RTError(
                           node.pos_start,
                           node.pos_end,
                           "List index must be a number",
                           context
                      )
                 )

            try :
                 return res.success(
                      list_value.elements[int(index.value)].copy()
                 )
            except IndexError:
                 return res.failure(
                      RTError(
                           node.pos_start,
                           node.pos_end,
                           "List index out of range",
                           context
                      )
                      
                 )

       def visit_IndexAssignNode(self, node, context):
            res = RTResult()

            list_value = res.register(self.visit(node.index_node.list_node, context))
            if res.error:
                     return res

            index = res.register(self.visit(node.index_node.index_node, context))
            if res.error:
                     return res

            value = res.register(self.visit(node.value_node, context))
            if res.error:
                    return res

            if not isinstance(list_value, List):
                return res.failure(
                     RTError(
                          node.pos_start,
                          node.pos_end,
                          "value is not a list",
                          context
                     )
                )
            if not isinstance(index, Number):
                 return res.failure(
                      RTError(
                           node.pos_start,
                           node.pos_end,
                           "List index must be a number",
                            context
                            
                      )
                 )

            try:
                 list_value.elements[int(index.value)] = value

            except IndexError:
                 return res.failure(
                      RTError(
                           node.pos_start,
                           node.pos_end,
                           "List index out of range"
                      )
                 )

            return res.success(list_value)
       

            
          
       def visit_BinOpNode(self,node,context):
         res = RTResult()
         left = res.register(self.visit(node.left_node,context))
         if res.error : return res
         right = res.register(self.visit(node.right_node,context))
         if res.error : return res 

         if node.op_tok.type_ == TT_PLUS:
              result,error = left.added_to(right)

         elif node.op_tok.type_ == TT_MINUS:
              result,error = left.subbed_by(right)

         elif node.op_tok.type_ == TT_MUL:
              result,error = left.multed_by(right)

         elif node.op_tok.type_ == TT_DIV:  
              result,error = left.dived_by(right)

         elif node.op_tok.type_ == TT_POWER:
              result,error = left.powerd_by(right)   

         elif node.op_tok.type_ == TT_EE:
               result, error = left.get_comparison_eq(right)
     
         elif node.op_tok.type_ == TT_NE:
               result, error = left.get_comparison_ne(right)

         elif node.op_tok.type_  == TT_LT:
               result, error = left.get_comparison_lt(right)

         elif node.op_tok.type_ == TT_GT:
               result, error = left.get_comparison_gt(right)

         elif node.op_tok.type_ == TT_LTE:
               result, error = left.get_comparison_lte(right)

         elif node.op_tok.type_ == TT_GTE:
               result, error = left.get_comparison_gte(right)
               
         elif node.op_tok.matches(TT_KEYWORD, 'AND'):
               result, error = left.anded_by(right)

         elif node.op_tok.matches(TT_KEYWORD, 'OR'):
              result, error = left.ored_by(right)            

         if error:
              return res.failure(error)

         return res.success(result.set_pos(node.pos_start,node.pos_end))

       def visit_UnaryOpNode(self,node,context): 
        res = RTResult()
        number = res.register(self.visit(node.node,context))
        if res.error : return res   

        error = None

        if node.op_tok.type_ == TT_MINUS:
             number,error = number.multed_by(Number(-1))
        elif node.op_tok.matches(TT_KEYWORD, 'NOT'):
             number, error = number.notted()
        

        if error : return res.failure(error)

        else:
           return res.success(number.set_pos(node.pos_start,node.pos_end))
        