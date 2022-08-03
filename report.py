def remove_none_values(dict):
    ans = {}
    for key in dict.keys():
        if dict[key] != None:
            ans[key] = dict[key]
    return ans

def myFunc(e):
    a,b = e
    return b 

def sort_pages(dict):
    ans = []
    for key in dict.keys():
        ans.append((key,dict[key]))
    ans.sort(reverse = True, key = myFunc)
    return ans

def print_report(pages):
    ans = remove_none_values(pages)
    ans = sort_pages(ans)
    for x in ans:
        print("Found "+str(x[1])+" internal links to "+x[0])