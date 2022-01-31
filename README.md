# Woodworking Mastery - Milestone 3 Project by Mikael Lindberg
Final resubmit january 31st 2022.

## Special Disclosure!
My project is completely and utterly in shambles!!!  Somehow, somewhere I have coded on the wrong repo and as that is not enough of a mistake, the last resubmission was of the wrong repo!

In the final days of january, I set out to update, test and finish my MS3 project. I knew I had some mugs to fix with a userpage form and I needed to add some templates as well as add som user articles (to make the page more "alive")..

During bugfixing of the user page, I read the assessment one more time, and something about 1.3 and 1.4 struck me as odd. I had made a full CRUD functionality for logged in users to add articles, update and delete them..

After several hours of total anguish while trying to sort out the mess I have concluded the following:

The first repo for the original submission, was this one, that I have decided to continue on...
After submitting, I decided to start another repo for the testing of new snippets of code, for new features and to follow along videos from YouTube, that repo was named Flask-app-turorials (notice the typo..?). 

When it was time to begin resubmission, I started a repository called MS3-wood-mastery, but somehow I continued on the flask-app-tutorials repo, in part.. But also on the MS3-wood-mastery repo..

After last resubmission I made a clone of my repository and named it MS3-wood-mastery-clone. I thought I was making the final adjustments in that repo but noticed that the functionality was not what I expected.. I started to search my repos for my "latest" work and disovered to my disbelief that i had continued to use Flask-app-turorial for my project..  

I then discovered to my horror that the repository that was logged for resumission was in fact Flask-app-turorial, which I have continued to used, since it was my "play-around-repo"

That repo, while most advanced has a lot of broken/commented out code not intended to be used... 

My MS3-wood-mastery (and clone) have some of the later CRUD functionality while it still misses some parts of the templates I had written in the other repo.. and later have rewritten or even deleted... 

OUCH!!!

I have therefore decided to restart my journey on MS3 where I first began, in this repo and will try to copy in the code one after another and test it along the way...

![snapshots](/static/pics/somerandompic.JPG "Snapshots of webpage")

## Table of Contents
1. [Introduction](#Introduction)
2. [Ux](#ux)
- [User Stories](#user&nbsp;stories)
3. [Features](#features)
- [Upcoming Features](#upcoming&nbsp;features)
4. [Technologies Used](#Technologies&nbsp;Used)
5. [Testing](#testing)
- [Expected Outcome](#expected&nbsp;outcome)
- [Bugs](#bugs)
- [Manual Testing](#manual&nbsp;testing)
- [Conclusion](#conclusion)
6. [Deployment](#deployment)
7. [Credits](#credits)
8. [WireFrames](#wireframes)
9. [Media](#media)
10. [Acknowledgements](#Acknowledgements)

# Introduction
The inspiration for this project comes from my interests of woodworking and trying to build jigs for easier builds. 
I love watching walkthrough videos on Youtube by experienced woodworkers. The annoying part is that its difficult and time consuming to find good content.
As the developer I aim to create a webpage / forum for avid woodworkers that wish to share their skill with others.

# UX
 The site should be easy and intuitive to navigate. It should have a distinct design that is present on all content pages. Easy to use on both mobile and larger devices.

The forums should have a clear and easy to understand category system as well as easy and intuitive features to ask questions as well as to publish content. Forums should be seperate from sections where walkthroughs are published.

## User&nbsp;Stories
- The problem with most forums and youtube content is the difficulty to find quality. Most times I watch videos for minutes only to find that its garbage, either by the quality of content or that its impossible to hear what the woodworker is saying. I would appreciate a site that is easy to navigate and "easy" to find content that other viewers have given high ratings, for quality. Also I would like a feature that gives me as a consumer advice on equipment or the workshop. Not only premium but simply tools that are of good quality and a good buy.

# Features
- Registered users can upload content and post articles / questions.
- Guest users only have viewing rights.
- Content from experienced users seperated from forums that are about questions
- Users must register with valid credentials so as to be transparent and promote "good behaviour"
- Easy to upload files/pictures and videos. As well as linking to urls (youtube)
- A rating service so that good content is distinguished from mediocre.
- Easy to search for quality content, walkthroughs and specific keywords in

## Upcoming&nbsp;Features

- Ratings function that sorts search queries.

# Technologies&nbsp;Used

CSS styling was used by utilizing Bootstrap framework. The code snippets have been implemented from [Bootstrap](getbootstrap.com).
Javascript was used for writing the logic behind the interactivity. (only for CKEditor)
CKEditor was implemented for textarea funcionality.
Flask WTFORMS for forms, authentication, validation.
Google Icons CDN for all site icons. (no icons used)

# Testing
NOT YET TESTED...
JS Hint
HTML Validator
CSS Validator

## Expected&nbsp;Outcome
All site pages should load as expected. guest users should have the ability to view the site. Only registered and logged in users should be allowed to post content. Admin account to moderate content and suspend users. An 404 custom page for missing or invalid page requests.

## Bugs

### Initial report before submitting
I have not got it working as planned... I have most flask/python functionality written but not all. Have spent to much time trying to figure out specific features, like the ratings. But have not got it working. I used MaterializeCSS in the beginning, as this evolved from the walktrough project. I have however switched to Bootstrap due to difficulties getting the desired effects.. I spent way too much time trying to get the navbar and sidenav (which I have scrapped) to work as I intended.

I have deployed it to Heroku earlier in development and got it working. However, as of 11.30 I find out I have an error when viewing site through Heroku...

### Updated january 2022, manual trouble shooting
1.   During the last weeks of coding I noticed another issue. When I make a new requirements.txt it has started to include all installed packages, not sure why... Update, found the issue about the bloated requirements.txt on Slack and have tried the fix recommended. Not sure if it worked or not...
2.  Function decorator not workin properly when signed in - Bug was a typo in the session name for @wraps decorator.
3.  Retested the add_article function, works, adding to db. Needs to be completed with author (session user) and date_posted. completed.
4.  Have tested full CRUD functionality. Had trouble populating form fields for edit. Solved - Edit article populates form on entry.
5.  Continued testing on form validation. made some changes to validators.
6. Add article does not work. All of a sudden.. Edit articles works..  Seems to be related to extension CKeditor for TextAreaField formatting.. Have tried another to solve this issue, after a few hours sleep. still no effect.. Finally decided to remove CKEditor functionality on add_article form. Now it works..




# Deployment
Debugger is turned off.

It is published using Github: https://github.com/d99mli/woodworking_mastery
Deployed using Heroku: https://woodworking-mastery-d99mli.herokuapp.com/


# Credits
I have used Stackoverflow extensively during the Javascript parts of the course.
Flask docs and WTForms docs have been used extensibly.
The Code Institute walkthrough with Tim Nelson was the foundation to this course
Corey Schafer and his Tutorial series on Flask was a great help https://www.youtube.com/c/Coreyms/videos


## Media
-To be continued..
No media added...


## Acknowledgements
Big thanks as always to Code Institute Tutors for the patience in helping me and to all students on Slack for help in troubleshooting!