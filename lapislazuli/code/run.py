import sys

class Run:
    def __init__(self):
        self.wc = 0

    def run(self):
        file = open(sys.argv[1], encoding="utf-8")
        data2 = file.readlines()

        dick = {}
        lis = []
        lisf = []
        lisw = []
        i = 0
        wc = 0

        for data in data2:
            data = data.replace("\n", "")

            if data.startswith("    "):
                if wc == 1:
                    lisw.append(data.replace("    ", "") + ";")
                else:
                    lis.append("{};".format(data.replace("    ", "")))
            
            elif data.endswith(":") and data.startswith("_") is False:
                func = data.replace(":", "")
                lisf.append(func)
            
            elif data.startswith("_"):
                c = data.split("L")[1].replace(":", "")
                wc += 1

            elif data == "end":
                dick["L{}".format(c)] = "".join(lisw)
                self.test(dick, "L{}".format(c), int(c))
                wc = 0

            elif data.startswith("call"):
                dick = dict(zip(lisf, "".join(lis).split("ret;")))
                self.test(dick, func, i)
            

        
        file.close()

    def test(self, dick, f, i):
        lis = dick[f].split(";")
        lisf = f
        for data in lis:
            data = data.split(";")
            data = [a for a in data if a != '']

            for data in data:
                if data.endswith(")"):
                    val = data.split("msg ")[1].split("(")[0]+"("+data.split("(")[1]
                    self.test(dick, val, i)
                    val = dick[val]
                    if '"' in val:
                        print(val.replace('"', ""))
                    
                    else:
                        try:
                            print(dick[val])

                        except KeyError:
                            print(val)
                
                else:
                    if data.startswith("mov"):
                        data1 = data.split(", ")
                        datas = data1[0].split(" ")[1]

                        if datas == "eax":
                            dick[lisf] = "".join(data1[1:])
                        
                        else:
                            dick[datas] = data1[1]
                    
                    elif data.startswith("call"):
                        func = data.split(" ")[1]
                        self.test(dick, func, i)

                    elif data.startswith("msg"):
                        if ' "' in data.split("msg")[1]:
                            print(data.split("msg")[1].replace(' "', "").replace('"', ""))
                        else:
                            print(dick[data.split("msg ")[1]])
                    
                    elif data.startswith("add"):
                        formula = data.split(",")[1].replace(" ", "")
                        formula2 = data.split(",")[2].replace(" ", "")
                        val = data.split(",")[0].split(" ")[1]
                        try:
                            dick[val] = int(dick[formula]) + int(dick[formula2])
                        
                        except KeyError:
                            
                            try:
                                dick[val] = int(formula) + int(dick[formula2])

                            except KeyError:
                                dick[val] = int(formula) + int(formula2)

                    elif data.startswith("sub"):
                        formula = data.split(",")[1].replace(" ", "")
                        formula2 = data.split(",")[2].replace(" ", "")
                        val = data.split(",")[0].split(" ")[1]
                        dick[val] = int(dick[formula]) - int(dick[formula2])
                    
                    elif data.startswith("mul"):
                        formula = data.split(",")[1].replace(" ", "")
                        formula2 = data.split(",")[2].replace(" ", "")
                        val = data.split(",")[0].split(" ")[1]
                        dick[val] = int(dick[formula]) * int(dick[formula2])
                    
                    elif data.startswith("div"):
                        formula = data.split(",")[1].replace(" ", "")
                        formula2 = data.split(",")[2].replace(" ", "")
                        val = data.split(",")[0].split(" ")[1]
                        dick[val] = int(dick[formula]) / int(dick[formula2])
                    
                    elif data.startswith("jmp"):
                        jmp = data.split(" ")[1].replace("_", "")
                        try:
                            if i > 1:
                                dick[jmp] = dick[jmp]
                                i -= 1
                                self.test(dick, jmp, i)
                        except KeyError:
                            pass
                    

if __name__ == '__main__':
    Run().run()
