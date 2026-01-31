def check_palindrome(word):
    palindrome = True
    for i in range(len(word)//2):
        if word[i] != word[-i-1]:
          palindrome = False
        break
    return palindrome

word = "civic"
result = check_palindrome(word)
if result:
   print("YES")
else:
   print("NO")

