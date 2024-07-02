#Library

import genanki
import random
def deckgen(cards, deckname):
    my_model = genanki.Model(
      1112570210,
      'Cards',
      fields=[
        {'name': 'Question'},
        {'name': 'Photo'},
        {'name': 'Options'},
        {'name': 'Answer'},
        {'name': 'More Information'}
      ],
      templates=[
        {
          'name': 'Basic',
          'qfmt': '<div class="bar"> <div class="subdeck">{{#Subdeck}}{{Subdeck}}{{/Subdeck}}</div> <div class="tag">{{#Tags}}{{Tags}}{{/Tags}}</div> </div> <div class=background> {{#Question}}{{Question}}{{/Question}}<br>{{#Photo}}{{Photo}}{{/Photo}} <div class=hint>{{#Options}}<br>{{hint:Options}}{{/Options}}</div> </div>',
          'afmt': '<div class="bar"> <div class="subdeck">{{#Subdeck}}{{Subdeck}}{{/Subdeck}}</div> <div class="tag">{{#Tags}}{{Tags}}{{/Tags}}</div> </div> <div class=background> {{#Question}}{{Question}}{{/Question}}<br>{{#Photo}}{{Photo}}{{/Photo}} <hr id=answer> {{#Answer}}{{Answer}}{{/Answer}} <p></p> {{#More Information}} <input type="checkbox" id="box"><label for="box">Additional Information</label><br> <div class="hidden"> <div class=extra>{{More Information}}</div> </div> <br> {{/More Information}} </div>',
        },
      ],
        css=".card{padding:15px 20px;font:20px arial;color:#fff;text-align:center}.hint{font-size:16px;font-style:italic}.background{border-radius:9px;padding:20px;background:#1e1e1e}.background img{width:auto;height:auto;display:block;margin-left:auto;margin-right:auto}.background.night_mode{border-radius:9px;padding:20px;background:#1e1e1e}.cloze{font-weight:700;color:orange}.bar{margin-bottom:-25px;background:#121212;border-top-right-radius:9px;border-top-left-radius:9px;padding-top:10px;padding-bottom:30px;z-index:-1}.subdeck{color:rgba(255,255,255,0.60);font-size:14px}.tag{color:rgba(255,255,255,0.87);font-size:13px;font-style:italic}input[type=checkbox]{position:absolute;top:-9999px;left:-9999px}.hidden{display:none}#box:checked~.hidden{display:block}label{border-radius:4px;padding:8px;font:bold 12px arial;color:#fff;background:#363636}.extra{border-radius:9px;padding-top:20px;background:#1e1e1e;font-size:15px;color:#fff}.images{max-width:800px;display:flex;flex-flow:row wrap;margin:auto;justify-content:center}.images>div{width:50%}img{display:block;width:100%;height:100%;object-fit:cover;max-width:100%}"
    )

    my_deck = genanki.Deck(
        random.randrange(1 << 30, 1 << 31),
        deckname,
    )

    for card in cards:
        my_note = genanki.Note(
            model=my_model,
            fields=card
        )
        my_deck.add_note(my_note)

    genanki.Package(my_deck).write_to_file(deckname+'.apkg')