# QULTURE AND ART  
# Overview 

Qulture and Art is a platform for people to share stories about their culture. Content is user-generated. Key features are listed below.  

# Live demo 
Access a deployed version of the platform here: https://web-production-0082.up.railway.app/

Options to login to access full range of features:

First option: Click on 'Login" on the navigation bar and login via:
1. Your personal Google account using Google OAuth, or 
2. The following login details: 
- username: maxfullerton
- password: Max789$$$
  
Second option: Click on "Signup" on the navigation bar and create a new account
 
# Technologies used 

Full-stack:
- Flask (Python and HTML) 

Database: 
- Postgres 
- Peewee 
- Hosted on Amazon Web Services RDS 

# Key features 

**Sign-up for new users**

- New users can create an account using Google OAuth or by filling up the form. 
- Checks are included to ensure passwords contain an uppercase, a lowercase and a special character.  

<img src="https://user-images.githubusercontent.com/85789376/192550183-97d426f6-a44d-481e-a224-4ea77d832486.png" height="300"> 

**Login for existing users**

- Existing users can input their information to login or login via Google OAuth. 
- An error appears if the login details are not matching with details in the database. 

<img src="https://user-images.githubusercontent.com/85789376/192550188-5147e4ff-0889-425d-b0e6-8765c4f2e7f7.png" height="300"> 


**Main post feed**
- Users can view all posts of other public users or private, authorised users that they follow.
- Each post consists of the profile picture of the person posting, a title, a caption and a picture. 
- Each post also has a like button and a donation button. 
- Posts are arranged with the most recent post at the top 
- There is a "Back to top" button on screen to enable quick access to the top of the page 

<img src="https://user-images.githubusercontent.com/85789376/192550190-75b8defd-79ad-49ab-a7b3-baf6dda4e5f8.png" height="300"> 

**User feed**
- Displays a profile picture and a caption. 
- Displays all posts posted by user. 
- Shows a list of all the accounts that the user is following.
- Contains buttons to allow user to approve/reject folower requests, update profile picture, edit personal details and post a new story. 

<img src="https://user-images.githubusercontent.com/85789376/192550181-3f829943-872e-4361-b906-d3e886703e55.png" height="300"> 

**New post upload page**
- Users can upload a picture, fill in a title, and add a description. 

<img src="https://user-images.githubusercontent.com/85789376/192550174-4d3254f7-67c2-450e-be80-7feba14ddd87.png" height="300"> 


**Visit the user feed of other users**
- Users can visit the user feed of other public users.
- If the user's account is set to public, all users can see their posts.  
<img src="https://user-images.githubusercontent.com/85789376/192556232-5a853124-18b1-45b3-9783-b980d132a9e9.png" height="300"> 
<img src="https://user-images.githubusercontent.com/85789376/192556238-c4d10089-8f79-4423-a6a2-3b2f7ddf222d.png" height="300"> 

- If the user's account is set to private, only existing approved followers can see their posts. 

<img src="https://user-images.githubusercontent.com/85789376/192560982-b25232a0-4b08-4358-bd89-8d0a3e525425.png" height="300"> 
<img src="https://user-images.githubusercontent.com/85789376/192560988-206bb704-d280-4a90-bc0c-72a990039314.png" height="300"> 
<img src="https://user-images.githubusercontent.com/85789376/192560998-5cbf6a61-3151-444f-85bf-a691205acc90.png" height="300"> 

**Approve/reject follower requests page**
- Users can check on new follower requests (applicable only to users who set their account to private)
- Users can check their list of followers and accounts that they are following 

<img src="https://user-images.githubusercontent.com/85789376/192550169-61566fa8-cded-42df-a48c-560ef8e368c0.png" height="300"> 

**Update profile picture page**
- Users can upload a new profile picture.
- Users will receive a message when the profile picture has been successfully uploaded.

<img src="https://user-images.githubusercontent.com/85789376/192550163-5a1aa21b-d91a-404f-b1c0-bb1b9b29895f.png" height="300"> 

**Edit personal information page**
- Users can make changes to their username, password, personal description, name, and email.
- Users can also update their privacy options to either private or public. 
<img src="https://user-images.githubusercontent.com/85789376/192550162-4e5aa706-81ca-488d-b661-7a8070984d7d.png" height="300">
<img src="https://user-images.githubusercontent.com/85789376/192556085-54e4b5d2-d296-41fb-9503-1a5c8d1f524d.png" height="300">

**Donation page**
- Users can make donations to other users using a Braintree payment gateway. 
<img src="https://user-images.githubusercontent.com/85789376/192550159-79b8d7f9-9e28-4a16-a732-14519db1d4c4.png" height="300"> 
