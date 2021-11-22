#!/usr/bin/env python
# coding: utf-8

# In[6]:


# Remove empty lists from nested set of lists
def removeEmptyLists(myList):
    newList = []
    
    for index, lst in enumerate(myList):
        if len(lst)!=0: newList.append(myList[index])
            
    return newList


# In[ ]:




