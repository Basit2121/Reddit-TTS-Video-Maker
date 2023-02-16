import praw
import pyttsx3
from playwright.sync_api import playwright, sync_playwright
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip

# Connect to the Reddit API
reddit = praw.Reddit(client_id='XJauAx6ojQ442IOs9tlyFg',
                     client_secret='YWJHr2B3SJTr1MF9ljElwLLSAx0hjA',
                     user_agent='basitcarry')

# Get the top post from the AskMe subreddit for today
subreddit = reddit.subreddit("offmychest")
for submission in subreddit.top(time_filter='day', limit=1):
    post_title = submission.title
    post_url = submission.url
    post = submission.title + "\n" + submission.selftext

    # Define the list of words to be censored
    words_to_censor = ['rape', 'sex', 'fuck', 'murder', 'porn']

    # Replace each word in the list with asterisks
    post = submission.title + "\n" + submission.selftext
    for word in words_to_censor:
        post = post.replace(word, '*' * len(word))

    # Narrate the post using pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', 'english-uk')
    engine.setProperty('rate', 150) 
    engine.setProperty('gender', 'male')
    engine.save_to_file(post, 'test.mp3')
    engine.runAndWait()

    # Take screenshot of the post
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome")
        context = browser.new_context()
        page = context.new_page()
        page.goto(post_url)
        # Wait for the div to be loaded
        page.wait_for_selector(".uI_hDmU5GSiudtABRz_37")
        # Get the bounding box of the div
        element_handle = page.query_selector(".uI_hDmU5GSiudtABRz_37")
        bounding_box = element_handle.bounding_box()
        # Take a screenshot of the div
        page.screenshot(path="post.png", clip=bounding_box)
        browser.close()
        print("The full screenshot has been saved as full_post.png")

    # Load the video and audio files
    video = VideoFileClip("bgvideo.mp4")
    audio = AudioFileClip("test.mp3")

    # Calculate the total duration of the audio
    audio_duration = audio.duration

    # Cut the video to be 3 seconds longer than the audio
    video_duration = audio_duration + 3
    video = video.subclip(1, video_duration)

    # Overlay the custom image on the video
    image = ImageClip("post.png").set_pos(("center","center"))
    image = image.set_duration(audio_duration)

    # Combine the audio and video
    final_video = CompositeVideoClip([video, image])
    final_video = final_video.set_audio(audio)

    # Save the final video
    final_video.write_videofile("final_video.mp4")
    print("The final video has been saved as final_video.mp4")