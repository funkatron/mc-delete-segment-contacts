# MailChimp Delete Segment Contacts Script

This is a python script I wrote to delete the thousands of spam signups we had on a MailChimp mailing list.

To clean a list of spam addresses, MailChimp suggests you [create a multi-part segment](https://mailchimp.com/help/create-and-send-to-a-segment/)
to quarantine the contacts, and then delete them by hand in the UI. The UI only allows you to select 100 list members
at a time, though, and we had about 60 times that number.

Because I am a programmer, I can't stand doing repetitive tasks, even when it would take more time to write a script. So
I wrote a script.

This has not been tested extensively. It Works For Me. YMMV. 

***THIS DELETES THINGS PERMANENTLY FROM YOUR LISTS. BE SURE YOUR HAVE THE RIGHT CONTACTS IN YOUR SEGMENT***

## Setup and Execution

This assumes you are running at least **Python 3.5**. I'd also suggest using a virtual environment. Assuming you agree,
do this:

1. Clone this repo
2. `cd` into the cloned repo directory
3. `python -m venv venv` to make the virtual environment
4. `python venv/bin/activate` to activate the virtual environment
5. `pip install -r requirements.txt` to get the required packages
6. `cp .env.sample .env` to copy the sample .env file
7. Fill out the values in the `.env` file:

    - `MC_API_KEY` - see [this doc here](https://mailchimp.com/help/about-api-keys/)
    - `MC_LIST_ID` - the ID for the list you'll be cleaning up. Get this via [the API Playground](https://us6.api.mailchimp.com/playground/)
    - `MC_SEGMENT_ID` - the ID for the _segment_ of the list you'll be cleaning up. Get this via [the API Playground](https://us6.api.mailchimp.com/playground/), in the **subresources** for the list
    - `MC_DC` - The Data Center code for your account. This should be [the suffix of your API key](https://developer.mailchimp.com/documentation/mailchimp/guides/get-started-with-mailchimp-api-3/#resources).

8. Run the script with `python mc-delete-segment-contacts.py`. ***THIS WILL PERMANENTLY DELETE ALL THE CONTACTS IN THE SEGMENT***. Also, this could take a while, so you might want to get a cup of coffee.

Have fun, and be careful out there.

-Ed
