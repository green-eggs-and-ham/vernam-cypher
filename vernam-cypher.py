import random
class Vernam:
    def __init__(self):
        print("Begin Setup...")
        self.key=""
        self.edit_definition(definition_type="i",check_override=True)
        self.edit_definition(definition_type="k")
        self.output_text=""
        self.functions={"cach":self.cach,"translate":self.translate,"redefine":self.prompt_edit,"output":self.output,"help":self.get_help,"exit":self.prompt_exit,"generate":self.get_key}
        print("Setup Complete.")
        self.terminal_loop()
    

    def cach(self):
        self.definition=input("Available definitions:\n'i' - INPUT ("+str(len(self.input_text))+")\n'k' - KEY ("+str(len(self.key))+")\nLeave blank for none:")
        if self.definition=="i"or self.definition=="k":self.confirmation=input("Confirmation Required to overwrite OUTPUT ('y'/'n'):").lower()
        if self.definition=="i" and self.confirmation=="y":self.output_text=self.input_text
        elif self.definition=="k" and self.confirmation=="y":self.output_text=self.key
        else:print("No changes made.")


    def text_format(self,inp="",inverse=False):
        if inverse:return [chr(int(i2,2)) for i2 in [''.join(i1) for i1 in[i0 for i0 in inp]]]
        else:
            out=[list(b) for b in [bin(ord(c)) for c in inp]]
            print("Adding Buffer...")
            for i in range(0,len(out)):
                while len(out[i])<9:out[i].insert(2,'0')
            return out


    def translate(self):
        if len(self.input_text)>0:
            print("Beginning Translation.")
            self.format_input=self.text_format(self.input_text)
            self.format_key=self.text_format(self.key)
            self.format_output=[]
            for i,j in enumerate(self.format_input):
                self.sub_out=[]
                for k in range(0,len(j)):
                    if self.format_input[i][k] == "b": self.sub_out.append("b")
                    else:self.sub_out.append(str(int(self.format_input[i][k]!=self.format_key[i][k])))
                self.format_output.append(self.sub_out) 
            self.output_text=self.text_format(inp=self.format_output,inverse=True)
            print("Translation Complete, OUTPUT Cached.")
        else:print("INPUT is empty.\nRecomendation:call 'redefine'.")


    def prompt_edit(self):
        if input("Specify definition ('i' for INPUT, 'k' for KEY):").lower()=="k":
            if input("Confirmation Required for KEY ('y'/'n'):").lower()=='y':self.edit_definition(definition_type="k")
            else: print("KEY Preserved.")
        else: 
            if input("Confirmation Required for INPUT ('y'/'n'):").lower()=='y':self.edit_definition(definition_type="i")
            else: print("INPUT Preserved.")
        if len(self.input_text)!=len(self.key):
            print("KEY is not the same length as INPUT.\nINPUT length:",len(self.input_text),"\nKEY length:",len(self.key),"\nRedefinition required:")
            self.prompt_edit()


    def edit_definition(self,definition_type="i",check_override=False):
        if definition_type=="i":print("Resetting INPUT...")
        else:print("Resetting KEY...")
        self.input_type=input("Input Type ('s' for string, 'l' for list):")
        self.input_source=input("Input Source ('t' for text, 'f' for file):")
        if definition_type=="k":self.key_wrap=input("Wrap KEY to INPUT length? ('y'/'n')")
        if self.input_source.lower()=='f':
            try:
                with open(input("Specify Text File:"),"r") as f:
                    if definition_type=="i":self.input_text=f.read()
                    else:self.key=f.read()
                print("Read Successful.")
            except:print("An ERROR occurred loading desired file.\nRecomendation:check file naming, extension, and state.")
        else:
            if definition_type=="i":self.input_text=input("Input:")
            else:self.key=input("Key:")
        if self.input_type.lower()=='l':
            if definition_type=="i":
                try:self.input_text=eval(self.input_text)
                except:print("Can not convert INPUT to a list")
            else:
                try:self.input_text=eval(self.key)
                except:print("Can not convert KEY to a list")
        if definition_type=="k":
            if self.key_wrap.lower()=="y":
                if type(self.key)==str:self.key=list(self.key)
                counter=0
                while len(self.key)<len(self.input_text):
                    self.key.append(self.key[counter])
                    counter+=1
                if input("OUTPUT new KEY? ('y'/'n')").lower()=="y":print(self.key)
        if len(self.input_text)==len(self.key):print("New definition accepted.")
        elif not check_override:
            print("KEY is not the same length as INPUT.\nINPUT length:",len(self.input_text),"\nKEY length:",len(self.key),"\nRedefinition required:")
            self.prompt_edit()
        

    def output(self):
        self.output_val=""
        if self.output_text:
            if input("Output Format ('l' for default list, 's' for string):").lower()=="s":
                for i in self.output_text:self.output_val+=i
            else:self.output_val=self.output_text
            if input("Output Type ('t' for text, 'f' for file):").lower()=="f":
                print("WARNING: Any contents in selected file will be overwritten.")
                self.file_name=input("File Name (leave blank for default):")
                if not self.file_name:self.file_name="vernam-output.txt"
                print("Saving...")
                try:
                    with open (self.file_name,"w") as f:f.write(str(self.output_val))
                except:print("An ERROR occurred loading desired file.\nRecomendation:check file naming, extension, and state.")
                print("File Saved.")
            else:print(self.output_val)
        else:print("OUTPUT is empty.\nAn OUTPUT is required to function.")


    def prompt_exit(self):
        print("Exiting the program will result in cached data being lost.")
        if input("Confirmation Required ('y'/'n'):").lower()=='y':exit()
        else: print("Resuming...")


    def get_key(self):
        try:
            self.key_type=input("Key Strength (0=Weak,1=Medium,2=Strong):")
            if self.key_type>1:print("Warning: Strong Key Strength is currently unsuitable for the translator.\nRecomendation:Manually remove obscure unicode characters.")
            self.key_charas=""
            for i in range(0,int(input("Key Length:"))):
                self.charatype=random.randint(0,int(self.key_type))            
                if self.charatype == 1: self.key_charas += str(chr(random.randint(97, 122)))
                elif self.charatype == 0: self.key_charas += str(random.randint(0,9))
                else: 
                    self.uniplane=random.randint(0,18)
                    if not self.uniplane: self.key_charas += str(chr(random.randint(0,55295)))
                    else: self.key_charas += str(chr(random.randint(63744,1114111)))
            print("Generation Complete. Key:\n"+str(self.key_charas))
        except:
            print("An ERROR occurred during generation.\nRecomendation:attempt a different generation configuration.")


    def get_help(self):
        print("\nAvailable Commands:\n'translate' - encodes or decodes your INPUT and caches the result.\n'redefine' - allows you to change your INPUT and KEY definitions.\n'output' - takes any cached result and outputs it as the user desires it.\n'generate' - creates a string of random characters with custom strength and length.\n'cach' - allows you to cach your INPUT or KEY to OUTPUT.\n'help' - displays this message.\n'exit' - terminates the program.\n")


    def terminal_loop(self):
        while True:
            self.command=input("Specify new operation, or type 'help':")
            if self.command in self.functions:
                caller=self.functions[self.command]
                caller()
            else:print("Unknown command, enter a valid operation.")


if __name__=='__main__':
    print("Vernam Cypher V3\nCreated by Oscar Bullen\n")
    v=Vernam()