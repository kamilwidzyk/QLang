import os

data = open("data.txt").read()

lines = data.split("\n")

parsed = {}

name = ""
letters = ""
number = ""
description = ""
test_path = ""
test_content = ""

def store():
    global name
    global letters
    global number
    global description
    global test_path
    global parsed

    if(name == ""):
        return

    if letters not in parsed:
        parsed[letters] = [name, letters, {
                "number": number,
                "description": description,
                "path": test_path,
                "test": test_content

            }
        ]
    else:
        parsed[letters].append({
            "number": number,
            "description": description,
            "path": test_path,
            "test": test_content
        })

    number = ""
    description = ""
    test_path = ""

for line in lines:
    if(line == ""):
        continue
    if "->" in line:
        name = line.split("->")[0][:-1].replace("Exception", "")
        letters = line.split("->")[1][1:]
        continue
    if number == "":
        number = line.split(":")[0].replace(" ", "").replace("\t", "")
        continue
    else:
        if "TEST:" in line:
            test_path = "..\\..\\tests\\" + line.split("TEST: ")[1].replace(" ", "").replace("\t", "").replace("/", "\\")
            if(not test_path.endswith("no")):
                test_content = open(test_path).read()
            store()
        else:
            description += line.replace("\t", "")[8:] + "\n"


print(parsed)

for letters in parsed.keys():
    entry = parsed[letters]
    name = entry[0]
    entries = entry[2:]
    for e in entries:
        number_dir = letters.lower() + "\\" + e["number"]
        if not os.path.exists(number_dir):
            os.mkdir(number_dir)

        test_file_path = number_dir + "\\test.ql"
        if not os.path.exists(test_file_path):
            f = open(test_file_path,'w')
            f.write(e["test"])
            f.close()

        tex_path = number_dir + "\\error.tex"
        input_path = "chapter-E-error-codes/" + letters.lower() + "/" + e["number"] + "/" + "test.tex"
        if not os.path.exists(tex_path):
            f = open(tex_path, 'w')
            f.write("\\subsubsection{" + letters.upper() + "-" + e["number"] +"}\\label{sec:error_code_" + letters.lower() + "_" + e["number"] + "}\n\n" + e["description"] + "\n\\input{" + input_path + "}\n")
            f.close()

        main_tex = letters.lower() + "\\" + name + ".tex"
        error_input = "chapter-E-error-codes/" + letters.lower() + "/" + e["number"] + "/" + "error.tex"
        if os.path.exists(main_tex):
            f = open(main_tex, 'a')
            f.write("\n\\input{" + error_input +"}")
            f.close()
        print("-----")
        print(letters)
        print(e["number"])
        print(number_dir)





