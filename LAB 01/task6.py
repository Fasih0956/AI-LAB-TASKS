def check_anagram(word1 , word2):
    anagram = True
    sorted1= "".join(sorted(word1, key=str.lower))  # to avoid cas sensitivity
    sorted2= "".join(sorted(word2, key=str.lower))

    for i in range ( 0 , len(word1) , 1):  # both word1 = word2 in len if anagram
          if sorted1[i] == sorted2[i]:
               continue
          else:
               anagram = False
               break
    return anagram

word1 = "listen"
word2 = "silent"
result = check_anagram(word1 , word2)
if result:
     print("YES")
else:
     print("NO")
          


    

