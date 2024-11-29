
# def summarize(text):
#     import requests
#     # API_URL = "https://api-inference.huggingface.co/models/knkarthick/MEETING_SUMMARY"
#     API_URL = "https://api-inference.huggingface.co/models/openlm-research/open_llama_3b_v2"
#     headers = {"Authorization": "Bearer HUGGINGFACE_API"}
#     def query(payload):
#         response = requests.post(API_URL, headers=headers, json=payload)
#         return response.json()
        
#     output = query({
#         "inputs": f"{text}",
#         "options": {"wait_for_model": True}
#     })
#     return output


# a  =  """Tell me important event details from this conversation:
    
# Person A: Hey everyone, thanks for joining today's meeting. Let's dive right into our agenda. Person B, could you please update us on the progress of the marketing campaign?

# Person B: Absolutely, A. So far, we've successfully launched the social media ads, and engagement is looking promising. However, we did encounter a minor setback with the influencer collaboration. I'm working on resolving it and expect everything to be back on track by the end of the week.

# Person C: Thanks for the update, B. In the meantime, Person D, how are we doing on the development side? Any challenges or roadblocks we should be aware of?

# Person D: Good question, C. Overall, the development team is making steady progress. We're on schedule with the coding tasks, but we've identified a potential bottleneck in the testing phase. I've already discussed it with the QA team, and we're exploring ways to streamline the process without compromising quality.

# Person A: Great to know, D. Let's keep a close eye on that and ensure we maintain our timeline. Now, switching gears a bit, Person C, do you have updates on the budget and resource allocation?

# Person C: Certainly, A. Our finance team has reviewed the budget, and we're currently within our allocated limits. However, I recommend a slight reallocation of resources to address the unexpected influencer collaboration issue in the marketing campaign. I'll share the revised proposal with everyone after the meeting for feedback.

# Person B: Sounds like a plan, C. And just a heads up, I'll coordinate with the marketing team to ensure the revised plan aligns with their needs. Anything else on the agenda, A?

# Person A: No, I think we've covered the main points. Thanks, everyone, for your updates. Let's stay connected throughout the week to address any emerging issues. If there are no further questions, we can adjourn the meeting.

# Person D: No questions here. Thanks, everyone. Looking forward to a productive week.

# Person C: Agreed. Have a great day, everyone! We will have in a meeting on 16th December 2024. Make sure everybody joins the meet.

# Person B: Thanks, all. Until next time!
# """

# If and only if you find any event, include the following information:

# Date: [Insert date of the event]<br>
# Time: [Insert start and end time of the event]<br>
# Name of the event: [Insert name of the event]<br>
# Location: [Insert location of the event]<br>
def summarize(text):
    import replicate
    import os
    intro = """Find  events from the transcript and only and only if there are any dates mentioned in it get the events to create calendar cards for them otherwise just summarize the conversation.

Notes: [Insert any additional details or notes that might be useful]

"""
    text = intro+text
    os.environ["REPLICATE_API_TOKEN"] = "REPLICATE_API"
    output = replicate.run(
        "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        input={"prompt": text}
    )
    string = ""
    # The meta/llama-2-7b-chat model can stream output as it's running.
    # The predict method returns an iterator, and you can iterate over that output.
    for item in output:
        # https://replicate.com/meta/llama-2-7b-chat/api#output-schema
        string+=item
    return string



# sumup = summarize(a)
# print(sumup)

# """
#     Das : Hi and welcome to the a16z podcast. I'm Das, and in this episode, I talk SaaS go-to-market with David Ulevitch and our newest enterprise general partner Kristina Shen. The first half of the podcast looks at how remote work impacts the SaaS go-to-market and what the smartest founders are doing to survive the current crisis. The second half covers pricing approaches and strategy, including how to think about free versus paid trials and navigating the transition to larger accounts. But we start with why it's easier to move upmarket than down… and the advantage that gives a SaaS startup against incumbents.
#     David : If you have a cohort of customers that are paying you $10,000 a year for your product, you're going to find a customer that self-selects and is willing to pay $100,000 a year. Once you get one of those, your organization will figure out how you sell to, how you satisfy and support, customers at that price point and that size. But it's really hard for a company that sells up market to move down market, because they've already baked in all that expensive, heavy lifting sales motion. And so as you go down market with a lower price point, usually, you can't actually support it.
#     Das : Does that mean that it's easier for a company to do this go-to-market if they're a new startup as opposed to if they're a pre-existing SaaS?
#     Kristina : It's culturally very, very hard to give a product away for free that you're already charging for. It feels like you're eating away at your own potential revenue when you do it. So most people who try it end up pulling back very quickly.
    
#     """
# import requests

# API_URL = "https://api-inference.huggingface.co/models/knkarthick/MEETING-SUMMARY-BART-LARGE-XSUM-SAMSUM-DIALOGSUM-AMI"
# headers = {"Authorization": "Bearer HUGGINGFACE_API"}

# def query(payload):
# 	response = requests.post(API_URL, headers=headers, json=payload)
# 	return response.json()

# output = query({
# 	"inputs": """Tell me important event details from this conversation:
    
# Person A: Hey everyone, thanks for joining today's meeting. Let's dive right into our agenda. Person B, could you please update us on the progress of the marketing campaign?

# Person B: Absolutely, A. So far, we've successfully launched the social media ads, and engagement is looking promising. However, we did encounter a minor setback with the influencer collaboration. I'm working on resolving it and expect everything to be back on track by the end of the week.

# Person C: Thanks for the update, B. In the meantime, Person D, how are we doing on the development side? Any challenges or roadblocks we should be aware of?

# Person D: Good question, C. Overall, the development team is making steady progress. We're on schedule with the coding tasks, but we've identified a potential bottleneck in the testing phase. I've already discussed it with the QA team, and we're exploring ways to streamline the process without compromising quality.

# Person A: Great to know, D. Let's keep a close eye on that and ensure we maintain our timeline. Now, switching gears a bit, Person C, do you have updates on the budget and resource allocation?

# Person C: Certainly, A. Our finance team has reviewed the budget, and we're currently within our allocated limits. However, I recommend a slight reallocation of resources to address the unexpected influencer collaboration issue in the marketing campaign. I'll share the revised proposal with everyone after the meeting for feedback.

# Person B: Sounds like a plan, C. And just a heads up, I'll coordinate with the marketing team to ensure the revised plan aligns with their needs. Anything else on the agenda, A?

# Person A: No, I think we've covered the main points. Thanks, everyone, for your updates. Let's stay connected throughout the week to address any emerging issues. If there are no further questions, we can adjourn the meeting.

# Person D: No questions here. Thanks, everyone. Looking forward to a productive week.

# Person C: Agreed. Have a great day, everyone! We will have in a meeting on 16th December 2024. Make sure everybody joins the meet.

# Person B: Thanks, all. Until next time!
# """
# })

# print(output)
# output


# from summa import summarizer

# # Meeting transcript
# meeting_transcript ="""
# Give me event details in this conversation:
# Das : Hi and welcome to the a16z podcast. I'm Das, and in this episode, I talk SaaS go-to-market with David Ulevitch and our newest enterprise general partner Kristina Shen. The first half of the podcast looks at how remote work impacts the SaaS go-to-market and what the smartest founders are doing to survive the current crisis. The second half covers pricing approaches and strategy, including how to think about free versus paid trials and navigating the transition to larger accounts. But we start with why it's easier to move upmarket than down… and the advantage that gives a SaaS startup against incumbents.
#     David : If you have a cohort of customers that are paying you $10,000 a year for your product, you're going to find a customer that self-selects and is willing to pay $100,000 a year. Once you get one of those, your organization will figure out how you sell to, how you satisfy and support, customers at that price point and that size. But it's really hard for a company that sells up market to move down market, because they've already baked in all that expensive, heavy lifting sales motion. And so as you go down market with a lower price point, usually, you can't actually support it.
#     Das : Does that mean that it's easier for a company to do this go-to-market if they're a new startup as opposed to if they're a pre-existing SaaS?
#     David: Let's meet at our Bombay Office on 21st December at
#     Kristina : It's culturally very, very hard to give a product away for free that you're already charging for. It feels like you're eating away at your own potential revenue when you do it. So most people who try it end up pulling back very quickly.
#  """

# def extract_key_points_and_summary(text):
#     # Use Summa's summarizer function for automatic summarization
#     summary = summarizer.summarize(text)

#     # Extract key points by splitting the text into lines
#     key_points = text.split('\n')

#     return key_points, summary

# # Call the function with the meeting transcript
# key_points, summary = extract_key_points_and_summary(meeting_transcript)

# # Display results
# print("Key Points:")
# for point in key_points:
#     print("-", point)

# print("\nSummary:")
# print(summary)

