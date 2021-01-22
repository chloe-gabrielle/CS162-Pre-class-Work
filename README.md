# Session 2.2

### 1. Get started
To set up a suitable environment for this session's code:
```bash
$ PYTHONENCODING=utf-8 python3 blackjack.py
```
And you should be able to play a simplified form of blackjack.

### 2. Read `blackjack.py` and identify its structure

The exercise for today's seminar is to refactor this program into a well-designed, object-oriented program. Labeling a program as object-oriented does not make it inherently good, and what follows is a short justification of why we should care about good design and object-orientation.

For this course, we will define a program to be well designed if:
>There are many potential features that could be added to the program, and each feature only requires a small number of locations to edited.

This is arguably *the* key aspect of good design.  It is the only requirement that allows a project to grow in scale and complexity.  If you have a project of millions of lines of code (e.g. the linux kernel, a modern web-browser) then good design is essential.  Consider a large project that is badly designed (ie. adding a single feature usually affects the entire codebase) then progress will necessarily be very slow.  Not only will an engineer need to understand millions of lines of code, but they will also need to synchronously make changes in many locations (to avoid introducing bugs).  This bad project also has the side effect that whenever one new feature is rolled out by another team then it will most likely affect the progress of all other teams ("stepping on each other's toes").

The thing that can save us is the notion of abstraction.  We can break down a large project into many small subsystems.  Each subsystem can hide the complexity of the implementation from other subsystems. This decouples what a subsystem does from how it does it.  

This notion of good design doesn't necessarily lead us into object-oriented principles, and there have been other interesting approaches (eg. google functional programming techniques).  However historically object-orientation has been the most successful and scaled to the largest projects.

Phew! That was quite a long aside.  Let's get back to today's task of getting a better codebase for our little Blackjack project.  This is a poorly designed project because all sorts of things are done all over the place.

### 3. Add support for another language

Run the following code in bash:
```bash
$ LANG=zh_CN PYTHONENCODING=utf-8 python3 blackjack.py
```
And the blackjack program is in Chinese.

Minerva is a very multicultural institution with many different languages being spoken.  While we use English in the classroom, we certainly should accommodate non-native speakers if they want to play blackjack in their leisure time and in their native language. The best way to do this is to abstract way how a particular point in the game is presented to the user.

A bad implementation will require a single global variable called language and have code littered with if statements like (please excuse my google translate):

```python
if LANGUAGE == 'en':
    print('You have gone bust!')
elif LANGUAGE == 'de':
    print('Du bist Pleite gegangen!')
elif LANGUAGE == 'es':
    print('¡Te has vuelto loco!')
```

External Web resources could be found [here](https://inventwithpython.com/blog/2014/12/20/translate-your-python-3-program-with-the-gettext-module/).

Complete the following steps to add support for your language:
1. Locate the position for pygettext.py and msgfmt.py. For Mac, they are located in your Python3 folder, in examples/Tools/i18n/; For Windows, they are in \Tools\i18n.

A quick way to findout the python3 folder you are using (Mac)
```bash
which python3
```

2. Run the following command: (Assuming pygettext.py is in the same folder)
```bash
$ python3 pygettext.py -o gettext.po blackjack.py
```

3. Open gettext.pot. Translate each sentence after msgid and fill the empty string after mgsstr. If you don't know the language well, use google translate to help you.

4. Run the following command: (Assuming msgfmt.py is in the same folder)
```bash
$ python3 msgfmt.py -o blackjack.mo gettext.po
```

5. Move blackjack.mo into /locale/Your_Language_Code/LC_MESSAGES/. Run:
```bash
$ LANG=Your_Language_Code PYTHONENCODING=utf-8 python3 blackjack.py
```
Replace Your_Language_Code above with your language code.

6. Enjoy!

Think about the following question:
1. Did you write any code?
2. Did the translation process require any knowledge about programming?
3. Why this is a good implementation of abstraction?

### 4. Refactor a better random number generator

Before walking into this session, look through both class Card & CardDeck. Here's the original version of card representation:

```python
def get_deck():
    '''Return a list of the all 52 playing cards.
    This list is sorted and always in the same order.
    '''
    suits = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
    rank = ('Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
    cards = list(itertools.product(rank, ['of'], suits))
    return [" ".join(l) for l in cards]
```

Think about the following question:
1. Which of them suit abstraction better?
2. If we want to support a new poker game, e.g. 24 points, which one provides a better basic structure for additional features?

In a real project, we would (and should) use the facilities provided by python in the `random` module. However, this will give you the opportunity to design a simple class and see how the refactored code is (hopefully) simpler and better separated.

The current implementation of random function within blackjack is badly designed. Think about whether there are any leaks in the current version of implementation, and whether it satisfies the concept of abstraction.

Also, it turns out that [RANDU](https://en.wikipedia.org/wiki/RANDU) is actually a bad random number generator (and RANDU was used by many real scientific computing centers for over a decade).  A better choice is to use a lagged fibonacci generator (which is what is actually used in the `random` module).

There is some example code for you to use in the file `mersenne.py` (this python code is adapted from [here](http://code.activestate.com/recipes/578056-mersenne-twister/)).

Identify the following:
1. The current implementation refers to the data for the random number generator in many lines. Identify each line of code where this happens.
2. If we are using a random number generator, what functionality do we actually care about?

Program the following:
1. Build a random number based on the RANDU implementation code that hides as much implementation detail as possible and only exposes the needed functionality.
2. Build a random number generator based on the Mersenne twister code that hides as much implementation detail as possible and only exposes the needed functionality.
3. Refactor your blackjack code so that it uses one of the new random number generator classes and it is easy to swap between either class.

### 5. (Optional) Implement more Blackjack rules

Find out what the full set of rules are for blackjack.  There are many subtleties that have been left out of the current implementation.  Find one such subtlety and implement it in the refactored codebase.  If you have done a good job of design then adding a new rule should affect a small number of locations in the codebase.  Think about how it would have been implemented in the old design, and whether this is an improvement or not.
# CS162-Pre-class-Work
