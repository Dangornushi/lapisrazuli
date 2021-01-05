import sys, os, re, glob


#TODO:Main / カーネル
class Main:
    def __init__(self):
        pass

    #TODO:data = すべてのデータ
    def run(self, dick, lis):
        valts = []
        i = 2
        case = 0
        arg = ""
        
        name = sys.argv[1]
        file = open(name, encoding="utf-8")
        conf = open(name.split(".")[0]+".las", "a", encoding="utf_8")
        data = file.readlines()
        file.close()

        valts.append(data)
        valts = [e for inner_list in valts for e in inner_list]
        for data in valts:
            data = data.replace("\n", "")
            
            if data.endswith(":") and data.startswith("    while") is False and data.startswith("put") is False:
                data1 = data.split(" ")[1].replace(")", "").split("(")[0]
                arg = data.split("(")[1].split(")")[0]
                
                if data1 == "main():":
                    pass
                
                else:
                    data = data1.replace(":", "") + "({}):".format(arg)
                
                conf.write("\n{}".format(data))
            
            elif data.startswith("    "):
                data = data.replace("    ", "").replace(";", "")

                if data.startswith("return"):
                    conf.write("\n    mov {}, {}".format("eax", data.split(" ")[1]))
                    conf.write("\n    ret\n")
                
                elif data.startswith("use"):
                    conf.write("\n    call {}".format(data.split(" ")[1]))
                
                elif "put" in data:
                    conf.write("\n    msg {}".format(data.split(":")[1]))

                elif data.startswith("int"):
                    if "," in data:
                        datav = data.split("=")[0].split("int ")[1].replace(" ", "").split(",")
                        datanum = data.split("=")[1].replace(" ", "").split(",")
                        dickl = dict(zip(datav, datanum))
                        for datav in datav:
                            conf.write("\n    mov {}, {}".format(datav, dickl[datav]))
                    else:
                        datav = data.split(" ")[1]
                        datanum = data.split(" ")[3]
                        conf.write("\n    mov {}, {}".format(datav, datanum))
                
                #x = 10 + 2
                # add x, 10, 2
                elif "+" in data:
                    data = data.replace(" ", "")
                    val = data.split("=")[0]
                    data2 = data.split("=")[1].split("+")[0]
                    data3 = data.split("=")[1].split("+")[1]
                    conf.write("\n    add {}, {}, {}".format(val, data2, data3))
                
                elif "-" in data:
                    data = data.replace(" ", "")
                    val = data.split("=")[0]
                    data2 = data.split("=")[1].split("-")[0]
                    data3 = data.split("=")[1].split("-")[1]
                    conf.write("\n    sub {}, {}, {}".format(val, data2, data3))
                
                elif "*" in data:
                    data = data.replace(" ", "")
                    val = data.split("=")[0]
                    data2 = data.split("=")[1].split("*")[0]
                    data3 = data.split("=")[1].split("*")[1]
                    conf.write("\n    mul {}, {}, {}".format(val, data2, data3))
                
                elif "/" in data:
                    data = data.replace(" ", "")
                    val = data.split("=")[0]
                    data2 = data.split("=")[1].split("/")[0]
                    data3 = data.split("=")[1].split("/")[1]
                    conf.write("\n    div {}, {}, {}".format(val, data2, data3))
                
                elif data.startswith("while"):
                    c = data.split(" ")[1].replace("{", "")
                    wc = 0
                    cou = 0
                    conf.write("\n    jmp _L{}".format(i))
                    conf.write("\n_L{}:".format(c))
                    if ">" in data or "<" in data:
                        conf.write("\n    cmp {}, {}".format(c, cou))
                        conf.write("\n    add {}, {}, 1".format("cou", "cou"))
                        wc += 1
                    i += 1
                
                elif data == "}":
                    if wc == 1:
                        conf.write("\n    jne _L{}".format(c))
                    else:
                        conf.write("\n    jmp _L{}".format(c))
                    conf.write("\nend")

        conf.write("\ncall main")
        conf.close()


if __name__ == '__main__':
    file_list = glob.glob("*las")
    for file in file_list:
        os.remove(file)
    f = open(sys.argv[1].split(".")[0]+".las", "x", encoding="utf_8")
    f.close()
    dick = {}
    lis = []
    omega = Main()
    omega.run(dick, lis)
