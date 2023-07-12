import codecs

data = []
with open('codes/context.enc', mode='rb') as file:
    data = [line.strip() for line in file.readlines()]

ans = []
decode_list = ["utf-8","utf-16","euc-kr","utf-32"]
not_decoded = 0
not_included =[]

for line in data:
    flag = False

    for act in decode_list:
        try:
            ans_line = codecs.decode(line,encoding=act)
            ans.append(ans_line)
            flag=True
            break
        except:
            continue

    if(not flag):
        not_decoded+=1
        not_included.append(line)
        line = b'\00' + line 
        for act in decode_list:
            try:
                ans_line = codecs.decode(line,encoding=act)
                ans.append(ans_line)
                not_decoded -= 1
                not_included.pop()
                break
            except:
                continue

final_ans = ""
for i in ans:
    final_ans += i+"\n"

print(final_ans)
print("skipped:"+str(not_decoded))
print(not_included)



