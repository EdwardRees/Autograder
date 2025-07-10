import platform
import os

compileCode = "find . -name \"*.java\" ! -name \"Tests.java\" -exec javac {} \\;"
compileTest=""
if platform.system() == "Windows":
    compileTest = "javac -cp '.;lib/junit-platform-console-standalone-1.9.2.jar' Tests.java;"
else:
    compileTest = "javac -cp '.:lib/junit-platform-console-standalone-1.9.2.jar' Tests.java;"

runTest = "java -jar lib/junit-platform-console-standalone-1.9.2.jar --class-path . --scan-class-path"


os.system(compileCode)
os.system(compileTest)

os.system(f"{runTest} &> java-results.txt")

total = 0
successful = 0
failed = 0
started = 0

resultText = []
try:
    with open("java-results.txt", "r") as f:
        count = 0
        for line in f:
            line = line.strip() 
            count+=1
            if("Thanks for using" in line):
                continue
            if(len(line) == 0):
                continue
            if("JUnit" in line):
                continue
            if("containers" in line or "skipped" in line):
                continue
            if(f"[36m" in line):
                continue
            resultText.append(line)
    resultText.append("") 
except FileNotFoundError:
    resultText = ["No java-results.txt found!"]

for line in resultText:
    line = line.strip("[]").strip()
    section = line.split(" ")[0]
    count = int(section) if section.isdigit() else 0
    if "found" in line:
        total = count
    if "started" in line:
        started = count
    if "successful" in line:
        successful = count
    if "failed" in line:
        failed = count

passRate = total * 0.6
passed = False
if successful / total > 0.6:
    passed = True

resultText.append("Passed 🎉!" if passed else "Failed 😢!")
resultText = "\n".join(resultText)
with open("test-results.txt", "w") as f:
    f.write(resultText)

os.remove("java-results.txt")
