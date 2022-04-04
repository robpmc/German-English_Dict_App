# German-English_Dict_App
 This project is intended for personal use only
 
 Background
 - I am currently in the process of learning German using the Pimsleur app aong with some other resources. While the app is fantastic for grammar and pronunciation, it is lacking when it comes to volume of vocabulary. The goal of this app is to use frequency dictionary of the 10,000 most used words in the German language combined with spaced repetition to increase vocabulary.



Part 1:
- COMPLETE - Obtain a ranked frequency list of the 10,000 mot commonly used words
- COMPLETE - Develop web scraper to gather data on german terms from Leo.org for definition, conjugation, examples, etc.
- COMPLETE - Cache word data in json file to be referenced later without requring realtime requests
- COMPLETE - Scrape first 500 words in order to test app
- Pending - Scrape the remaining 11,500 words with adequate delays to avoid pestering the leo.org servers

Part 2 IN WORK:
- Develop flashcard app for iOS using spaced repetition
- Test app with first 500 words
- Send to others for beta testing and feedback
- Implement changes/updates

App features:
- Spaced repetition learning
- Change the range of words practiced dynamically. As earlier words get practiced more and space between repetitions increases, move along the unlearned list
- Link to google translate or Leo.org for pronunciations
- Flash card shows the likely part of speech based on the order of the leo.org tables. Shows main definition, as well as 1-2 examples
- Expandable to show more definitions and examples
- Selectable options to show the other parts of speech related to the term
- Selectable to show conjugation tables if available/relevant
- Track list of words that have been practiced as well as the number of times practiced
- Ability to remove words if 100% confidence in them (Simple words like "the" "i" and others used every day don't necessarily need to be practiced)
- Ability to review list of "removed" words and return them to learning in case of accidental removal or wanting more repetitions
- When returning words, rank confidence to determine spacing/repetition


Stretch goals:
Include audio for pronunciations
- Scrape for audio for the current range as well as extending a little further
- Cache the audio
