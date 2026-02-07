# D&D 5E Character Sheet Generator

Given a JSON character description

Create an HTML page that is a D&D 5E character sheet. In the style of homebrewery.

NPC generator

PC generator

## ComfyUI

I should make a ComfyUI node to generate the NPC card

My thinking is it takes an image

## Aspect Ratio

I am thinking MTG aspect ratio because of the sleeves I have that are compatible

Monsters can have a landscape or portrait configuration depending on the creature? Like alligators are landscape, while humanoids are portrait?

But perhaps I can do square aspect ratio, it's easier to generate?

I'm leaning toward MTG

2.5 x 3.5 in
63.5 x 88.9 mm


## OpenVTT

I should make a tool to import sheets into OpenVTT and to print those sheets

I copied the VTT html page using F12 and element picker

# STATS

What information makes it into the card?

CORE STATS
- HP
- AC
- PROF
- CR
- Initiative
- Passive Perception WIS+PROF
- Speed

ATTRIBUTES, SAVE
- STR
- DEX
- CON
- INT
- WIS
- CHA

PROFICIENCISES

Strength

Athletics

Dexterity

Acrobatics
Sleight of Hand
Stealth

Intelligence

Arcana
History
Investigation
Nature
Religion

Wisdom

Animal Handling
Insight
Medicine
Perception
Survival

Charisma

Deception
Intimidation
Performance
Persuasion

RESISTENCE, IMMUNITY, WEAKNESS
- DAMAGE TYPE

DESCRIPTION

I would like to have a description of the creature and habit

I can do small and wall of text to fit all in the back?


# LAYOUT

## Card MTG Landscaper

![](/NPC-sheet-idea/NPC%201.jpg)

I use a mtg card landscape format

NPC name on top

three columns

on right column

- NPC illustration
- stat block

on center column

- abilities with roll
- proficiency is a different text like bold italic? or color

on left column

- skills

Not enough space for everything. I want it to be artistic

## Card MTG portrait double sided

I use the front for illustration and stat block

I use the rear for abilities and skills

How many cards I need?

The front I think of name, race, class, and four core numbers
HP AC Initiative and Passive perceptin
Perhaps with their glyps like shield, heart, eye, foot
I should have the speed, in there, I don't really need passive perception here
I am thinking of speed in various mediums walk, swim, fly, float

Creature size, weight and dimensions

The back should have abilities, attributes, resistencies, 

I do use a separate card for the active abilities? Most creatures should fit a single card I think. I flip it and have both

## Active and Passives

I'm thinking the active and passive abilities can be another card where I have one card for each attack and passive with its own back

But NPC usually have 

## Material

I should 2D print on some hard smooth paper and get some premium finish I think

# PYTHON

Perhaps I should do a json image, that will create all the outputs using python PIL

I can use an LLM to generate the json base, and tweak it

I should have full image, with opacity

The back could be manual image, or better just no background? It's there for info using clear sleeves

# DISTRIBUTION

I am thinking of doing a patreon, and release NPCs individuallty with also their statue and base

Linktree

I want to package my one shots so that other people can make use of them

# UV

uv venv .venv --python 3.13

.venv\Scripts\activate

I do have PIL in the system python



