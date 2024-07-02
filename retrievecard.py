import re
import os
from playwright.sync_api import sync_playwright, expect
from time import sleep

AUTH_FILE = 'auth.json'

def importcards(deck, email, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = navigate_to_cards(browser, email, password)
        card_number = navigatetodeck(page, deck)
        cards=[]
        # instead retrieve the number of cards in the deck
        while len(cards) < card_number:
            card = retrievecard(page)
            if card in cards:
                pass
            cards.append(retrievecard(page))
            print(f'{len(cards)} out of {card_number} cards retrieved!')
        browser.close()
    #print(cards)
    print(f"Total cards collected: {len(cards)} / {card_number}")
    return cards

def check_if_card(page):
    title = page.title()
    return "card" in title.lower()

def save_auth_file(page):
    page.context.storage_state(path=AUTH_FILE)

def load_auth_file(browser):
    if os.path.exists(AUTH_FILE):
        context = browser.new_context(storage_state=AUTH_FILE)
        return context
    return browser.new_context()

def is_authenticated(page):
    page.goto("https://cards.ucalgary.ca/collection")
    return page.title() == "Cards - Collection"


def login(page, email, password):
    page.goto("https://cards.ucalgary.ca/collection")
    print(f"Navigating to {page.title()}")
    page.get_by_placeholder("email").fill(email)
    page.get_by_placeholder("password").fill(password)
    page.get_by_role('button', name='Login').click()

    if page.title() == "Cards - Login":
        print("Check your username or password")
        exit()

    print(page.title())
    expect(page).to_have_title(re.compile("Collection"))
    save_auth_file(page)


def navigate_to_cards(browser, email, password):
    context = load_auth_file(browser)
    page = context.new_page()
    if is_authenticated(page):
        print("Already authenticated. Skipping login.")
    else:
        print("Authentication required. Logging in.")
        login(page, email, password)
    return page


def navigatetodeck(page, heading):
    deckurl = get_deck_url(page, heading)
    card_number = get_card_number(page, deckurl)
    deck = "https://cards.ucalgary.ca" + deckurl + "?timer-enabled=1&amp;mode=sequential"
    print(deck)
    page.goto(deck)
    page.wait_for_url('**/card/**')
    page.wait_for_selector('div.solution.container')
    print(page.title())
    return card_number

def get_deck_url(page, heading):
    # Wait for the deck link to be visible
    deck_link = page.query_selector(f'a:has-text("{heading}")')
    if deck_link:
        deck_url = deck_link.get_attribute('href')
        print(f"Deck URL: {deck_url}")
        return deck_url
    else:
        print(f"Deck named '{heading}' not found")
        return None

def get_card_number(page, deckurl):
    details_url = deckurl.replace("deck", "details")
    details = "https://cards.ucalgary.ca" + details_url
    page.goto(details)
    confirmdeck = input(f"Please confirm the deck is correct: {details} \n(Y/N): ")
    if confirmdeck != "Y":
        print("Exiting. . .")
        quit()
    cardcountjs = page.query_selector_all('div.container div.details div span.label')
    labels = []
    for label in cardcountjs:
        labels.append(str(label.text_content()))
    cardcountxt = "".join(labels).strip()
    cardcountlist = cardcountxt.split(" ")
    cardcount = int(cardcountlist[-1])
    print(f"Number of cards: {cardcount}")
    return cardcount

def retrievecard(page):
    # Wait for the h3 element to be present
    try:
        page.wait_for_selector('div.solution.container h3', timeout=60000)
    except Exception as e:
        print(f"Error waiting for h3 element: {e}")

    # Locate the <img> element and get its src attribute
    img_element = page.query_selector('div.solution.container .photo-question img')
    if img_element:
        img_src = img_element.get_attribute('src')
        photo = "<img src=\"https://cards.ucalgary.ca" + img_src + "\">"
        #print(f"Image src: {photo}")
    else:
        print("Image element not found")

    # Locate the first <h3> element within the specified container and get its text content
    h3_element = page.query_selector('div.solution.container h3')
    if h3_element:
        question = h3_element.text_content()
        #print(f"Question: {question}")
    else:
        print("Question element not found")

    # Locate all option labels and concatenate their text content
    option_elements = page.query_selector_all('div.solution.container .image.question .options label')
    options = [option.text_content() for option in option_elements]
    hint = "<br>".join(options)
    #print(f"Hint: {hint}")

    # Get the "message" in the results container
    message_element = page.query_selector('div.results.container .message')
    if message_element:
        answer = message_element.text_content()
        #print(f"Answer: {answer}")
    else:
        print("Message element not found")

    # Get the paragraph in the td element
    feedback_element = page.query_selector('div.results.container td')
    if feedback_element:
        feedback = feedback_element.text_content()
        #print(f"Feedback: {feedback}")
    else:
        print("Feedback element not found")

    selectanswer(page, answer)

    return([question, photo, hint, answer, feedback])

def selectanswer(page, answer):
    # Select the correct option based on the "answer" message
    option_to_select = page.query_selector(f'div.solution.container .image.question .options label:has-text("{answer}")')
    if option_to_select:
        option_to_select.click()
        #print(f"Selected option: {answer}")
    else:
        print(f"Option '{answer}' not found")

    # Submit the form
    submit_button = page.query_selector('div.solution.container .submit button')
    if submit_button:
        submit_button.click()
        #print("Form submitted")
    else:
        print("Submit button not found")

    # Click the "Next Card" button
    next_card_button = page.query_selector('div.actions #next')
    if next_card_button:
        next_card_button.click()
        #print("Navigated to next card")
    else:
        print("Next Card button not found")



