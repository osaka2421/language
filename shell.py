import main
import sys

def run_repl():
   while True:
      text = input("basic >>")

      if text.lower() == "exit":
        break
     
      if text == "":
        continue


      result , error = main.run("<stdin>",text)
    
      if error:
          print(error.as_string())
      if result is not None :
        if isinstance(result ,list) and len(result) == 1:
           print(result[0])
        else:
         print(result) 


def run_file(filename) :
   try:
      with open (filename , "r") as f :
         text = f.read()
      result , error = main.run(filename, text)   

      if error:
          print(error.as_string())
      if result is not None:
        print(result)
   except FileNotFoundError :
      print(f"filename {filename} is not found")

if __name__ =="__main__":
   if len(sys.argv) > 1 :
      run_file(sys.argv[1])
   else :
      run_repl()   
