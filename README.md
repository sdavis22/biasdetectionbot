# NLP Arrest Project for CSCI499- Computing for Social Good

## Dependencies

Flask: https://flask.palletsprojects.com/en/1.1.x/installation/#installation

NPM: https://www.npmjs.com/get-npm

Yarn: https://yarnpkg.com/getting-started/install

Install the above in the above order (I didn't mess with virtual environments, but you can).

## Running

Open up two terminal windows. In both of them `cd static`

In the first one, run `yarn start`, this will start the front end and load the React page in your browser

In the second one, run `yarn start-api`, this will start the backend, and get the submit button to actually function.

Once they're both run, you should be able to submit the form, and the web page should run coinflip.py and display the result.

## Twitterbot Dependencies

`python -m textblob.download_corpora`
