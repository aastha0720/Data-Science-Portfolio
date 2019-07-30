#!/usr/bin/env python
# coding: utf-8

# # Profitable App Profiles for the App Store and Google Play Markets
# Our aim in this project is to find mobile app profiles that are profitable for the App Store and Google Play markets. We're working as data analysts for a company that builds Android and iOS mobile apps, and our job is to enable our team of developers to make data-driven decisions with respect to the kind of apps they build.
# 
# At our company, we only build apps that are free to download and install, and our main source of revenue consists of in-app ads. This means that our revenue for any given app is mostly influenced by the number of users that use our app. Our goal for this project is to analyze data to help our developers understand what kinds of apps are likely to attract more users.

# # 1. Exploring the Data

# Let's start by opening the two data sets and then continue with exploring the data.
# Find the documentation for the apps data collected here, [iOS](https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps/home), [Android](https://www.kaggle.com/lava18/google-play-store-apps/home)

# In[1]:


file1=open('AppleStore.csv')
from csv import reader
read_file1=reader(file1)
ios_apps=list(read_file1)
ios_header=ios_apps[0]
ios=ios_apps[1:]

opened_file = open('googleplaystore.csv')
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android = android[1:]


# In[2]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n')

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# In[3]:


#ios header and first few rows of the data set.
print('iOS Apps \n')
print(ios_header,'\n')
explore_data(ios,0,5,True)
print('\n Android Apps \n')
print(android_header)
print('\n')
explore_data(android, 0, 3, True)


# # 2. Data Cleaning
# In this step we are going to clean the data, ie, 
# 
# **Part 1. Remove inaccurate data.**
# 
# Android data has a row with inaccurate data, whereas, the iOS data seems to be correct.
# 

# In[4]:


print(android_header)
print(android[10472])
print(android[0])


# We see that row 10472 has an incorrect value in the Rating column. Hence, we delete the value.

# In[5]:


print(len(android))
del android[10472]
print(len(android))


# **Part 2. Remove duplicate data.**
# 
# On exploring the android data set we find that there are certain rows that have been repeated and would lead to incorrect analysis. Let's look at an  examples.

# In[6]:


for app in android:
    name=app[0]
    if name=='Instagram':
        print(app)


# These are not the only duplicate rows. We will look at all the duplicate rows present in the data set.

# In[7]:


duplicate_list=[]
unique_list=[]
for app in android:
    name=app[0]
    if name in unique_list:
        duplicate_list.append(name)
    else:
        unique_list.append(name)
        
print('Number of unique apps: ',len(unique_list))
print('Number of duplicate apps: ',len(duplicate_list),'and some examples are:\n', duplicate_list[:15])


# In[8]:


print(android_header)
for app in android:
    name=app[0]
    if name=='Instagram':
        print(app)


# In the above output we can see that the all rows have the same column values except the reviews column which has different values and we deduce that the row with the maximum value of reviews will be the lastest updated row. 

# To get rid of  the duplicate data we will create a dictionary of app names and the maximum value of the reviews column. After that we will create two list android_clean and already_added.
# For each app in android list we will add the app row in the android_clean list only if the app review value equal to the max review value taken from the dictionary review_map and if the app name in not present in the already_added app list.
# The app name is check in already_added list because for certain apps the value in reviews column is also same. to avoid adding the same again we will check the already_added list.

# In[9]:


reviews_max={}
for app in android:
    name=app[0]
    n_reviews=float(app[3])
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name]=n_reviews
    if name not in reviews_max:
        reviews_max[name]=n_reviews


# In[10]:


android_clean=[]
already_added=[]
for app in android:
    name=app[0]
    n_reviews=float(app[3])
    if (reviews_max[name]==n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)
        
explore_data(android_clean,0,3,True)


# **Part 3: Removing Non-English Apps**
# 
# We will be developing apps in English, hence we need to analyse the data for english apps only.

# In[11]:


print(ios[813][1])
print(ios[6731][1])
print(android_clean[4412][0])
print(android_clean[7940][0])


# ASCII range of the characters used in english language is 0-127. Hence we will keep only those names whose that fall within this range.
# 

# In[12]:


def is_english(string):
    for character in string:
        if ord(character) > 127:
            return False
    return True

print(is_english('Instagram'))
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))


# For 'Instachat 😜' and 'Docs To Go™ Free Office is the name of the file Suite, eventhough the names are in English but because they have used 😜 and ™, the function has returned False. To solve this issue we will make a change in in the function. The function returns False only if name app name has more than 3 characters that are not in english. This is not a completely correct way but will still give a decent result.

# In[13]:


# def is_english(string):
#     count=0
#     for character in string:
#         if ord(character) > 127:
#             count+=1
#     if count>3:
#         return False
#     else:
#         return True


# print(is_english('Instagram'))
# print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))
# print(is_english('Docs To Go™ Free Office Suite'))
# print(is_english('Instachat 😜'))




# Implementing the above function for android_clean list anf the ios list.

# In[14]:


english_android=[]
for app in android_clean:
    name=app[0]
    if is_english(name):
        english_android.append(app)

english_ios=[]
for app in ios:
    name=app[1]
    if is_english(name):
        english_ios.append(app)
        
print('\n\nAndroid Apps')
explore_data(english_android, 0, 3, True)
print('\n\nios Apps')
explore_data(english_ios, 0, 3, True)


# **Part 4. Removing Non-Free Apps**
# 
# Our company makes only free apps, so we need to remove apps that are not free from both the android apps and ios apps

# In[15]:


def free_apps(app_list, index):
    free_apps=[]
    for app in app_list:
        price=(app[index])
        if price=='0' or price=='0.0' :
            free_apps.append(app)
            
    return free_apps

android_final=free_apps(english_android,7)
ios_final=free_apps(english_ios,4)
print(len(ios_final))
print(len(android_final))


# # Most Common Apps by Genre
# 
# **Part One**
# 
# As we mentioned in the introduction, our aim is to determine the kinds of apps that are likely to attract more users because our revenue is highly influenced by the number of people using our apps.
# 
# To minimize risks and overhead, our validation strategy for an app idea is comprised of three steps:
# 
# Build a minimal Android version of the app, and add it to Google Play.
# If the app has a good response from users, we then develop it further.
# If the app is profitable after six months, we also build an iOS version of the app and add it to the App Store.
# Because our end goal is to add the app on both the App Store and Google Play, we need to find app profiles that are successful on both markets. For instance, a profile that might work well for both markets might be a productivity app that makes use of gamification.
# 
# Let's begin the analysis by getting a sense of the most common genres for each market. For this, we'll build a frequency table for the prime_genre column of the App Store data set, and the Genres and Category columns of the Google Play data set.
# 
# **Part Two**
# 
# We'll build two functions we can use to analyze the frequency tables:
# 
# One function to generate frequency tables that show percentages. 
# Another function that we can use to display the percentages in a descending order

# # Analysis of the Data
# 
# We will start be analyzing the frequency table data for iOS apps.

# In[16]:


def freq_table(dataset,index):
    table={}
    for app in dataset:
        if app[index] in table:
            table[app[index]]+=1
        else:
            table[app[index]]=1
    length=len(dataset)
    for app in table:
        table[app]=(table[app]/length)*100
    return table

def display_table(dataset,index):
    table=freq_table(dataset,index)
    table_list=[]
    for row in table:
        tuple_key=(table[row],row)
        table_list.append(tuple_key)
    sorted_table=sorted(table_list, reverse=True)
    for row in sorted_table:
        print(row[1],' : ',row[0])
print('\n iOS Apps Genre Frequency Table ')
display_table(ios_final, -5)


# The most common English apps in the App Store are Games at 58% and then Entertainment apps at 7.8%. This is followed by Photo & Video apps at 4% and then Education apps at 3.6%. 
# 
# We can see that more apps are being made for Fun and Entertainment purposes like games, photo and video, social networking, sports, music and apps for practical purposes like education, shopping, utilities, productivity, lifestyle are rare.
# 
# Also, the above data only gives us an insight on the genres of apps that are available in the App Store. This does not tell us what apps are being preferred more by the users. 

# In[17]:


print('\n Android Apps Category Frequency Table ')
display_table(android_final, 1)
print('\n Android Apps Genre Frequency Table ')
display_table(android_final, 9)


# 
# The landscape seems significantly different on Google Play: there are not that many apps designed for fun, and it seems that a good number of apps are designed for practical purposes (family, tools, business, lifestyle, productivity, etc.). However, if we investigate this further, we can see that the family category (which accounts for almost 19% of the apps) means mostly games for kids.
# 
# The difference between the Genres and the Category columns is not crystal clear, but one thing we can notice is that the Genres column is much more granular (it has more categories). We're only looking for the bigger picture at the moment, so we'll only work with the Category column moving forward.
# 
# Up to this point, we found that the App Store is dominated by apps designed for fun, while Google Play shows a more balanced landscape of both practical and for-fun apps. Now we'd like to get an idea about the kind of apps that have most users.
# 

# # Most Popular Apps by Genre on the App Store
# One way to find out what genres are the most popular (have the most users) is to calculate the average number of installs for each app genre. For the Google Play data set, we can find this information in the Installs column, but for the App Store data set this information is missing. As a workaround, we'll take the total number of user ratings as a proxy, which we can find in the rating_count_tot app.
# 
# Below, we calculate the average number of user ratings per app genre on the App Store:

# In[18]:


genre_list=freq_table(ios_final,-5)
for genre in genre_list:
    total=0
    len_genre=0
    for app in ios_final:
        app_genre=app[-5]
        if app_genre==genre:
            n_rating=float(app[5])
            total+=n_rating
            len_genre+=1
    avg_rating=total/len_genre
    print(genre,':',avg_rating)
        


# We see that genres like Navigation, Reference, Social Network and music have the maximum number of users. Let us look deeper into it.

# In[19]:


for app in ios_final:
    if app[-5]=='Navigation':
        print(app[1],':',app[5])


# In[20]:


for app in ios_final:
    if app[-5]=='Reference':
        print(app[1],':',app[5])


# In[21]:


for app in ios_final:
    if app[-5]=='Social Networking':
        print(app[1],':',app[5])


# Looking at the above data we see that Navigation genre is dominated by Google Maps and Waze, whereas, the Social Networking genre is dominated by Facebook, Pinterest and skype. <br>
# When a certain genre is dominated by a only a few apps, it is probably not wise to make another app that will compete with them. <br>
# Reference apps have a Bible app and several dictionary apps. So we can make an app by digitalizing a popular book.<br>
# Other apps that have good number of user reviews are :<br>
# Weather 
# <br>
# Finance 
# <br>
# Food & Drink 

# # Most Popular Apps by Genre on Google Play
# For the Google Play market, we actually have data about the number of installs, so we should be able to get a clearer picture about genre popularity. However, the install numbers don't seem precise enough — we can see that most values are open-ended (100+, 1,000+, 5,000+, etc.):

# In[22]:


category_freq=freq_table(android_final,1)
for category in category_freq:
    total=0
    len_=0
    for app in android_final:
        category_app=app[1]
        if category==category_app:
            n_installs=app[5]
            n_installs=n_installs.replace('+','')
            n_installs=n_installs.replace(',','')
            total+=float(n_installs)
            len_+=1
    avg_installs=total/len_
    print(category,':',avg_installs)
    
            


# 
# On average, communication apps have the most installs: 38,456,119. This number is heavily skewed up by a few apps that have over one billion installs (WhatsApp, Facebook Messenger, Skype, Google Chrome, Gmail, and Hangouts), and a few others with over 100 and 500 million installs:

# In[23]:


for app in android_final:
    if app[1] == 'COMMUNICATION' and (app[5] == '1,000,000,000+'
                                      or app[5] == '500,000,000+'
                                      or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# If we removed all the communication apps that have over 100 million installs, the average would be reduced roughly ten times:

# In[24]:


under_100_m = []

for app in android_final:
    n_installs = app[5]
    n_installs = n_installs.replace(',', '')
    n_installs = n_installs.replace('+', '')
    if (app[1] == 'COMMUNICATION') and (float(n_installs) < 100000000):
        under_100_m.append(float(n_installs))
        
sum(under_100_m) / len(under_100_m)


# We see the same pattern for the video players category, which is the runner-up with 24,727,872 installs. The market is dominated by apps like Youtube, Google Play Movies & TV, or MX Player. The pattern is repeated for social apps (where we have giants like Facebook, Instagram, Google+, etc.), photography apps (Google Photos and other popular photo editors), or productivity apps (Microsoft Word, Dropbox, Google Calendar, Evernote, etc.).
# 
# Again, the main concern is that these app genres might seem more popular than they really are. Moreover, these niches seem to be dominated by a few giants who are hard to compete against.
# 
# The game genre seems pretty popular, but previously we found out this part of the market seems a bit saturated, so we'd like to come up with a different app recommendation if possible.
# 
# The books and reference genre looks fairly popular as well, with an average number of installs of 8,767,811. It's interesting to explore this in more depth, since we found this genre has some potential to work well on the App Store, and our aim is to recommend an app genre that shows potential for being profitable on both the App Store and Google Play.

# In[25]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0], ':', app[5])


# The book and reference genre includes a variety of apps: software for processing and reading ebooks, various collections of libraries, dictionaries, tutorials on programming or languages, etc. It seems there's still a small number of extremely popular apps that skew the average:

# In[26]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000,000+'
                                            or app[5] == '500,000,000+'
                                            or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# Google Play Books : 1,000,000,000+
# Bible : 100,000,000+
# Amazon Kindle : 100,000,000+
# Wattpad 📖 Free Books : 100,000,000+
# Audiobooks from Audible : 100,000,000+
# However, it looks like there are only a few very popular apps, so this market still shows potential. Let's try to get some app ideas based on the kind of apps that are somewhere in the middle in terms of popularity (between 1,000,000 and 100,000,000 downloads):

# In[27]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000+'
                                            or app[5] == '5,000,000+'
                                            or app[5] == '10,000,000+'
                                            or app[5] == '50,000,000+'):
        print(app[0], ':', app[5])


# This niche seems to be dominated by software for processing and reading ebooks, as well as various collections of libraries and dictionaries, so it's probably not a good idea to build similar apps since there'll be some significant competition.
# 
# We also notice there are quite a few apps built around the book Quran, which suggests that building an app around a popular book can be profitable. It seems that taking a popular book (perhaps a more recent book) and turning it into an app could be profitable for both the Google Play and the App Store markets.
# 
# However, it looks like the market is already full of libraries, so we need to add some special features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes on the book, a forum where people can discuss the book, etc.
# 
# # Conclusions
# In this project, we analyzed data about the App Store and Google Play mobile apps with the goal of recommending an app profile that can be profitable for both markets.
# 
# We concluded that taking a popular book (perhaps a more recent book) and turning it into an app could be profitable for both the Google Play and the App Store markets. The markets are already full of libraries, so we need to add some special features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes on the book, a forum where people can discuss the book, etc.

# In[ ]:




