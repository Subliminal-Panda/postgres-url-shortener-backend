
INTRODUCTION: BACKEND/API
------------

* This program's backend is built with Python.

* To generate random short URL's, a variable called saved_link is defined as: "".join([random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10)])

- This algorithm takes advantage of Python's native random and string libraries.

* To prevent duplicate links, the backend performs a database search for duplicate links. If a duplicate exists, it enters a while loop, re-rolling random links, until a unique link is generated. Though the odds of this happening are 62^10, it's always better to verify.

* To clone this repository and have a look at the code:

 1. Navigate in your preferred terminal (Windows: Command Prompt, PowerShell Linux: Bash Mac: Terminal) to the directory you would like to clone my repository to. You'll be downloading a set of files.

 2. When you're at the proper directory, run the following command:

  $ gh repo clone Subliminal-Panda/postgres-url-shortener-backend

INTRODUCTION: USING THE APP
------------

* This program is reasonably user-friendly, so it shouldn't be too tough to dive right in!

* I recommend running it inside codesandbox for the sake of simplicity. To get to it (if you're not in codesandbox already) navigate to the following URL:

https://codesandbox.io/s/beautiful-noyce-j499o?

*If you'd like to try this application outside codesandbox, skip down to CLONING THE FRONTEND REPOSITORY.

* To enter a URL, click the input field titled "Enter a new URL:" and enter your desired destination URL.

* It doesn't matter if it starts with a prefix of http://, https://, www., or even no prefix whatsoever! just make sure the URL is spelled correctly.

* If you would like to create your own custom short link, enter your desired link name in the "Custom short link (optional): input field. You can use spaces and special characters. Just keep in mind, if you write a short link that isn't short, it will overflow the display area. (It will still work, it just won't look very pretty.)

* Click the green "Submit Url" button. The backend will automatically recognize whether you've created a custom short link. If not, it will generate a random 10 character link instead.

* It might take just a moment to update the list with your new URL and Short Link (free databases are prioritized last... sad.)

* Once your link appears, you can click either the URL itself (to the left) or the short link (on the right) to visit the URL you entered! It's magical!

* To delete a URL and its corresponding Short Link, just click the pink/red "Delete Link" button to the right, on the same row.

REQUIREMENTS: CODE SANDBOX
------------

* This module (in codesandbox) requires the following dependencies, which should be pre-loaded:

 - react
 - react-dom
 - react-scripts

CLONING THE FRONTEND REPOSITORY
------------

* If you'd like to try this application outside codesandbox:

 1. Navigate in your preferred terminal (Windows: Command Prompt, PowerShell Linux: Bash Mac: Terminal) to the directory you would like to clone my repository to. You'll be downloading a set of files.

 2. When you're at the proper directory, run the following command:

  $ gh repo clone Subliminal-Panda/postgres-url-shortener-frontend

 3. If you don't have npm already, install it at the following link:

 https://github.com/npm/npm/archive/refs/tags/v5.2.0.zip

 4. You'll also need to install scss and sass via npm. Once you've got npm, run the following commands in your terminal:

  $ npm install sass
  $ npm install compile-sass

 5. Then run it:

  $ npm start

That should do it! The backend is always running, so you don't need to do anything special for that.
