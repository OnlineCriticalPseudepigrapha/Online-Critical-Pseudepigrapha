#!/usr/bin/env python3
"""
Build Treatise of Shem (Tractatus Sem / CAVT 85)
Syriac text and English translation from:
Alphonse Mingana, Some Early Judæo-Christian Documents in the John Rylands Library
(Manchester: The University Press, 1917), pp. 24-29 (translation), 54-61 (Syriac text from MS Cod. Syr. 44).
Outputs:
  - static/docs/TracSem.xml (Grammateus DTD)
  - static/docs/tei/TracSem.xml (TEI P5 parallel segmentation)
"""

import os
import re

# 12 Zodiac signs:
# 1. Aries (Immera)
# 2. Taurus (Tawra)
# 3. Gemini (Tren Salme / Twins)
# 4. Cancer (Sartana)
# 5. Leo (Arya)
# 6. Virgo (Shebelta)
# 7. Libra (Massata)
# 8. Scorpio ('Eqarba)
# 9. Sagittarius (Qeshta)
# 10. Capricorn (Gadya)
# 11. Aquarius (Dawla)
# 12. Pisces (Nune)

CHAPTERS = [
    {
        "num": 1,
        "name": "Aries",
        "verses": [
            ("ܬܘܒ ܡܡܠܠܐ ܕܣܝܡ ܠܫܝܡ ܒܪ ܢܘܚ ܥܠ ܡܘܠܕܐ ܕܫܢ݇ܬܐ ܘܟܠܡܐ ܕܗܿܘܐ ܒܗ:", "Discourse written by Shem son of Noah about the beginning of the year and all that happens in it."),
            ("ܐܢ ܒܐܡܪܐ ܡܬܝܠܕܐ ܫܢܵ݇ܬܐ, ܫܢ݇ܬܐ ܩܛܝܢܬܐ ܬܗܘܐ.", "If the year begins in Aries: The year will be hard."),
            ("ܘܐܖ̇ܒܥܬ ܪ̈ܓܠܝܗܿ ܬܡܘܬ.", "The quadrupeds will die."),
            ("ܘܥܢ̈ܢܐ ܣܓܝ̈ܐܬܐ ܠܐ ܢܬܚ̈ܙܝܢ ܘܠܐ ܢܗ̈ܘܝܢ.", "There will not be many clouds."),
            ("ܘܙܪܥܐ ܩܘܡܬܐ ܠܐ ܗܘܿܝܐ ܠܗ: ܘܦܪ݇ܕܬܗ ܕܝܢ ܬܗܘܐ ܘܬܫܡܢ.", "The standing corn will not have good size, but it will have fat grains."),
            ("ܘܢܗܪܿܐ ܕܢܝܠܘܣ ܡܣܩܐ ܫܦܝܪ ܢܣܩ.", "The river Nile will overflow well."),
            ("ܘܡܠܟܐ ܕܪ̈ܗ݇ܘܡܝܐ ܠܐ ܢܩܘܐ ܒܚܕܐ ܕܘܟܬܐ.", "The king of the Romans will not remain in one place."),
            ("ܘܟܘܟ̈ܒܐ ܕܫܡܝܐ ܢܬܒܕܪܘܢ ܐܝܟ ܙܠܝ̈ܩܐ ܕܢܘܪܐ.", "The stars of heaven will be scattered like rays of fire."),
            ("ܘܣܗܪܐ ܢܚܫܟ.", "The moon will suffer eclipse."),
            ("ܘܙܪܥܐ ܩܕܡܝܐ ܢܐܒܕ: ܘܙܪܥܐ ܐ݇ܚܪܝܐ ܢܬܚܡܘܠ.", "The first crops will perish, and the second will be ingathered."),
            ("ܡܢ ܦܨܚܐ ܥܒܘܪܿܐ ܝܪܩܢܐ ܗܘܐ ܠܗ.", "From Passover corn will be mildewed."),
            ("ܘܫܢ݇ܬܐ ܒܝܫܬܐ ܐܝܬܝܗܿ ܕܩܖܒܐ ܪܒܐ ܘܫܚܩܐ ܒܟܠܗܿ ܐܪܥܐ: ܘܝܬܝܪܐܝܬ ܒܐܪܥܐ ܕܡܨܪܝܢ.", "The year will be bad, with severe war and distress over all the earth, especially over the land of Egypt."),
            ("ܘܢܬܬܒܪ̈ܢ ܐܠܦ̈ܐ ܣܓܝܐܬܐ ܡܐ ܕܸܒܚܿܫ ܝܡܐ.", "Many ships will break up when the sea is rough."),
            ("ܘܡܫܚܐ ܢܫܘܐ ܒܐܦܪܝܩܝ: ܘܚܛ̈ܐ ܢܙܥܪ̈ܢ: ܒܕܪܡܣܘܩ ܘܒܚܘܪܢ ܘܒܦܠܣܛܝܢܝ ܢܫܘ̈ܝܢ.", "Oil will be at a moderate price in Africa, and wheat will be at a low price; in Damascus, Hauran, and Palestine it will be at a moderate price."),
            ("ܘܟܘܪ̈ܗܢܐ ܡܫܚ̈ܠܦܐ ܘܡ̈ܚܘܬܐ ܘܙܘܥܐ ܢܗܘܐ ܒܗܿ: ܘܡܬܦܠܛܐ ܡܢܗܿ ܘܬܫܬܘܙܒ.", "(Palestine) will have different kinds of diseases, plagues, and earthquake, but it will be delivered from them and saved.")
        ]
    },
    {
        "num": 2,
        "name": "Taurus",
        "verses": [
            ("ܘܐܢ ܡܬܝܠܕܐ ܫܢ݇ܬܐ ܒܬܘܪܐ: ܟܠ ܕܐܝܬܘܗܝ ܫܡܗ ܒܝܬ ܐܘ ܝܘܕ ܐܘ ܟܦ ܢܬܟܪܗ: ܐܘ ܢܒܠܥ ܒܦܪܙܠܐ.", "If the year begins in Taurus: Anyone having in his name (the letters) Beith, Yodh, or Koph will be ill, or will be killed with iron weapons."),
            ("ܘܢܗܘܐ ܙܘܥܐ.", "There will be earthquake."),
            ("ܘܬܦܘܩ ܡ̣ܢ ܡܨܪܝܢ ܪܘܚܐ ܘܬܡܠܝܗ̇ ܠܟܠܗ̇ ܐܪܥܐ.", "A wind will start from Egypt and spread over all the earth."),
            ("ܘܢܗ̈ܘ̈ܝܢ ܒܗܿ ܚ̈ܛܐ ܘܡܛܪܐ ܪܽܘ̈ܪܒܐ: ܘܖܘܪ̈ܒܢܐ ܕܐܪܥܐ ܘܕܼܐܬܪ̈ܘܬܐ ܕܚܕܪ̈ܝܗܘܢ ܢܘܒܕܘܢ ܐܢܘܢ.", "The year will be rich in wheat and abundant rains, but the chiefs of the land and of the surrounding places will destroy that (wheat)."),
            ("ܘܡܛܪܿܐ ܕܫܢ݇ܬܐ ܢܬܚܣܟ ܬܠܬܐ ܝܪ̈ܚܝܢ: ܘܡ̣ܢ ܒܬܖܿܟܢ ܥܒܘܪܿܐ ܢܐܩܪ ܒܢܣܝܘܢܐ ܝܘ̈ܡܬܐ ܬܠܬܝܢ ܘܫܬܐ.", "The yearly rain will fail during three months, and then corn will be very dear during thirty-six days;"),
            ("ܘܢܡܘܬܘܢ ܐܢܫܐ ܣܓܝܐܐ ܡ̣ܢ ܟܘܪ̈ܗܢܐ ܕܓܪܓܪܬܐ: ܘܩܛܝܢܘܬܐ ܬܐܒܕܼ.", "many people will die from diseases of the throat, and then tribulation will cease."),
            ("ܘܙܪܥܐ ܩܕܡܝܐ ܢܐܒܕܼ ܗܟܢܐ: ܘܙܪܥܐ ܐ݇ܚܪܝܐ ܢܐܠ: ܘܣܥܪ̈ܐ ܘܕܼܩ̈ܐ ܢܐܠܘܢ.", "The first crops (of wheat) will perish, but as (above), the second crops will be ingathered, and barley with the watered cereals will be ingathered also."),
            ("ܘܕܼܝܘ̈ܐ ܥܠ ܒܢܝ̈ܢܫܐ ܢܦܠܘܢ: ܘܡܕܡ ܠܐ ܢܚܣܪܘܢ ܐܢܘܢ.", "The devils will attack the sons of men, but they will not harm them in anything."),
            ("ܘܡ̈ܠܟܐ ܬܪܶܝܢ ܢܩܘܡܘܢ ܥܠ ܚܕܕܵܐ.", "Two kings will rise against each other."),
            ("ܘܢܝܠܘܣ ܢܗܖܿܐ ܪܒܐ ܢܣܩ ܠܥܠ ܡ̣ܢ ܡܫܘܚܬܗ.", "The great river Nile will overflow above its normal rate."),
            ("ܗܠܝܢ ܕܐܝܬܝܗܘܢ ܒܐܠܦܐ ܒܓܘ ܝܡܐ ܘܐ݇ܢܫܐ ܕܼܐܝܬ ܒܝܡܐ ܢܗܘܘܢ ܒܫܚܩܐ ܩܫܝܐ: ܘܒܚܪܬܗ̇ ܕܫܢ݇ܬܐ ܒܘܪܟܬܐ ܣܓܝܐܬܐ ܬܗܘܐ.", "Those who are on board a ship in the sea, and those who are on the sea will be in great distress. At the end of the year there will be great blessing.")
        ]
    },
    {
        "num": 3,
        "name": "Gemini",
        "verses": [
            ("ܘܐܢ ܒܬܪܝܢ ܨܠܡ̈ܐ ܡܬܝܠܕܐ ܫܢܵܬܐ: ܢܗܘܐ ܣܗܪܶܐ ܫܦܝܪ.", "If the year begins in Gemini (the Two Figures): The moon will be good."),
            ("ܘܬܫܒ ܪܽܘܚܐ ܕܬܝܡܢܐ ܘܡܢܗ̇ܿ ܢܗܘܐ ܡܛܪܐ.", "A South wind will blow, from which rain will come."),
            ("ܘܟܠ ܕܐܝܬܘܗܝ ܫܡܗ ܬܘ ܐܘ ܚܝܬ ܐܘ ܡܝܡ ܢܗܘܐ ܒܦܪܨܘܦܗ ܓܪܳܒܐ ܐܘ ܫܘܚܢܐ.", "Anyone having in his name the letters Taw, Heth, or Mim will have tumours and boils in his face."),
            ("ܘܢܗܘܐ ܒܫܘܪܝܗܿ ܕܸܫܢ݇ܬܐ ܩܖܒܐ ܩܫܝܐ.", "At the beginning of the year there will be a severe war."),
            ("ܘܡܛܪ̈ܐ ܪܒܝܥܝܐ ܢܗܘܘܢ: ܘܙܪܥܐ ܢܫܦܖܿ: ܘܝܬܝܪܐܝܬ ܙܪܥܐ ܕܫܩܝܐ.", "There will be early rains, and the standing corn will be good, especially in the watered places."),
            ("ܘܥܘܩܒܪ̈ܬܐ ܢܣܓܝܢ ܒܐܪܥܐ.", "Mice will abound in the earth."),
            ("ܘ̈ܪܗ݇ܘܡܝܐ ܘܦܪ̈ܣܝܐ ܢܥܒܕܘܢ ܩܖܒܐ ܩܫܝܐ ܥܡ ܚܕ̈ܕܐ: ܘܢܦܩܘܢ ܪܗ݇ܘܡܝܐ ܒܐܠܦ̈ܐ ܒܝܡܐ: ܘܢܥܒܕܘܢ ܩܪܒܐ ܘܢܘܒܕܘܢ ܐܢܘܢ.", "The Romans and the Persians will wage a severe war against one another, and the Romans will come forth by ships on the sea, will fight and destroy them."),
            ("ܘܢܦܩܘܢ ܒܥܠܡܐ ܗܢܐ ܐܢܫܐ ܒܝ̈ܫܐ ܘܢܥܒܕܘܢ ܒܝܫܬܐ: ܘܢܗܘܐ ܪܢܝܐ ܘܫܚܩܐ ܩܫܝܐ.", "Malicious people will rise in the world, who will do mischief, and there will be great anxiety and distress."),
            ("ܘܒܫܘܠܡܗ̇ ܕܸܫܢ݇ܬܐ ܬܗܘܐ ܛܒܬܐ: ܘܢܝܠܘܣ ܢܗܪܐ ܢܣܩ ܫܦܝܪ.", "Good will come at the end of the year and the river Nile will overflow well.")
        ]
    },
    {
        "num": 4,
        "name": "Cancer",
        "verses": [
            ("ܘܐܢ ܒܣܪܛܢܐ ܡܬܝܠܕܐ ܫܢ݇ܬܐ: ܬܗܘܐ݀ ܒܫܘܪܝܗܿ ܕܫܢ݇ܬܐ ܫܘܝܘܬܐ ܕܥܒܘ̇ܪܿܐ: ܘܢܗܘܘܢ ܐ݇ܢܫܐ ܛܠܒܐܝܬ.", "If the year begins in Cancer: At the beginning of the year corn will be at a moderate price, and people will be comfortable."),
            ("ܘܢܝܠܘܣ ܢܣܩ ܦܠܓܗ ܕܡܣܩܗ.", "The Nile will overflow at half its normal rate."),
            ("ܘܐܠܟܣܢܕܪܝܐ ܬܬܐܠܨ ܘܢܗܘܐ ܒܗܿ ܫܚܩܐ ܡ̣ܢ ܡܘܬܢܐ.", "Alexandria will be besieged, and distress will be in it from pest."),
            ("ܘܢܨܡܚܘܢ ܟܘܟܒ̈ܐ ܪܽܘܪܒܐܝܬ: ܘܣܗܪܐ ܢܚܫܟ.", "Stars will shine very brightly, and the moon will suffer eclipse."),
            ("ܘܐܠܦ̈ܐ ܣܓܝ̈ܐܬܐ ܢܬܬܒܪ̈ܢ ܒܝܡܐ.", "Many ships will break up in the sea."),
            ("ܘܒܫܘܪܝܗܿ ܕܫܢ݇ܬܐ ܢܐܩܪ̈ܢ ܚܛܐ ܘܣܥܪ̈ܐ.", "At the beginning of the year wheat and barley will be dear."),
            ("ܘܪ̈ܘܚܐ ܢܣܓܝܢ: ܘܐܢܫܐ ܣܓܝ̈ܐܐ ܢܬܟܪܗܘܢ ܡ̣ܢ ܚܨܐ ܘܡܼ̣ܢ ܫܥܠܐ ܘܪ̈ܓܠܐ.", "Winds will abound, and many people will suffer from backaches, coughs, and soreness of the feet and eyes."),
            ("ܘܚܡܪܿܐ ܢܣܓܐ.", "Wine will be abundant."),
            ("ܘܬܘܪ̈ܐ ܘܥ̈ܢܐ ܘܩ̈ܛܝܢܬܐ ܢܐܒܕܘܢ: ܘܕܼܩ̈ܐ ܢܐܒܕܘܢ: ܘܡܫܚܐ ܢܫܘܐ ܐܢܘܢ.", "Oxen, sheep, and small cattle will perish; and cereals will also perish, but oil will make up for them."),
            ("ܘܒܫܘܠܡܗܿ ܕܸܫܢ݇ܬܐ ܬܐܩܪ ܝܥܠܬܐ ܬܫܥܐ ܝܘ̈ܡܬܐ: ܘܒܬܪ̇ܟܢ ܢܗܘܐ ܡܛܪܐ: ܘܬܗܘܐ ܒܗܿ ܒܘܪܟܬܐ ܣܓܝܐܬܐ.", "At the end of the year corn will be dear for nine days, and then there will be rain, and (the year) will have much blessing.")
        ]
    },
    {
        "num": 5,
        "name": "Leo",
        "verses": [
            ("ܘܐܢ ܒܐܪܝܐ ܡܬܝܠܕܐ ܫܢ݇ܬܐ: ܢܗܘܐ ܡܛܪܐ ܪܰܒܝܥܝܐ: ܘܐܖܿܥܐ ܬܐܒܕܼ ܡ̣ܢ ܪ̈ܘܚܐ ܕܓܖܶܒܝܐ.", "If the year begins in Leo: There will be early rains, but the soil will be scorched by North winds;"),
            ("ܘܙܪܥܐ ܢܬܪܚܡ: ܘܐܦ ܡܐܟܘܠܬܐ ܕܝܢ ܕܒܢܝ̈ܢܫܐ ܬܛܐܒ.", "corn will not be injured and the food of mankind will be good."),
            ("ܘܢܐܩܪ̈ܢ ܚܛ̈ܐ ܘܪܽܘܙܐ ܘܕܩܐ: ܘܢܫܩ̈ܝܢ ܚܛܐ.", "Wheat, rice, and cereals will be dear, and wheat will have to be watered."),
            ("ܘܡܫܚܬܐ ܘܬܡܪ̈ܐ ܢܐܩܪܘܢ.", "Oil and dates will be dear."),
            ("ܘܟܘܪ̈ܗܢܐ ܒܒܢܝ̈ܢܫܐ ܢܗܘܐ: ܘܒܛ̈ܢܬܐ ܘܩܛ̈ܝܢܬܐ ܢܐܒ̈ܘܢ.", "There will be diseases in sons of men and the pregnant animals will perish as well as small cattle."),
            ("ܘܡܠܟܐ ܢܬܟܬܫ ܥܡ ܡܠܟܐ.", "A king will fight against a king."),
            ("ܘܩܡܨܐ ܪܒܐ ܢܐܬܐ: ܘܠܐ ܢܒܨܪ ܐܠܐ ܩܠܝܠ ܡܕܡ.", "A considerable number of locusts will make their appearance and their number will decrease but slightly."),
            ("ܘܢܣܩ ܢܝܠܘܣ ܢܗܪܿܐ ܡܣܩܗ ܥܠܝܐ: ܘܢܗܘܐ ܟܐܒܐ ܕܪܫܐ ܠܐܢ݇ܫܐ: ܘܒܫܘܠܡܗ̇ ܕܫܢ݇ܬܐ ܢܗܘܐ ܡܛܪܐ ܣܓܝܐܐ.", "The river Nile will overflow to its highest rate. People will have headache. At the end of the year there will be much rain.")
        ]
    },
    {
        "num": 6,
        "name": "Virgo",
        "verses": [
            ("ܘܐܢ ܒܫܒܠܬܐ ܡܬܝܠܕܼܐ ܫܢܵ݇ܬܐ: ܟܠ ܡܢ ܕܐܝܬܘܗܝ ܫܡܗ ܝܘܕܼ ܐܘ ܣܡܟܬ ܘܒܝܬ ܘܢܘܢ ܢܗܘܐ ܟܪܝܗ: ܘܢܬܒܙܙ ܘܢܥܖ̇ܘܩ ܡ̣ܢ ܒܝܬܗ.", "If the year begins in Virgo: Anyone having in his name (the letters) Yodh, Semkath, Beith, or Nun will be ill, will be plundered, and will flee from his house."),
            ("ܘܢܗܘܐ ܒܫܘܪܶܝܗܿ ܕܸܫܢ݇ܬܐ ܚܣܝܪܘܬ ܡܝ̈ܐ ܒܕܘܟܐ ܕܘܟܐ: ܘܙܪܥܐ ܩܕܡܝܐ ܠܐ ܢܟܫܪ.", "At the beginning of the year there will be shortage of water in various places, and the first crops will not succeed."),
            ("ܘܐ݇ܢܫܐ ܫܚܝܩܐ ܢܗܘܘܢ: ܒܣܬܘܐ ܘܒܩܝܛܐ ܢܬܟܪܗܘܢ.", "People will be distressed: in winter and in summer they will be ill."),
            ("ܘܥܒܘܪܐ ܢܐܩܪ ܒܚܘܪܢ ܘܒܬܕܡܘܪ.", "Corn will be dear in Hauran and in Palmyra."),
            ("ܘܒܫܘܠܡܗ̇ ܕܫܢ݇ܬܐ ܢܫ̈ܘܝܢ ܩܠܝܠ: ܘܚܡܪܐ ܢܗܘܐ ܙܥܘܪ ܘܒܣܝܡ.", "At the end of the year prices will be slightly moderate, and wine will be scarce and sweet."),
            ("ܘܬܡܪ̈ܐ ܢܣܓܘܢ: ܘܡܫܚܐ ܢܐܩܪ: ܘܚܛ̈ܐ ܘܣܥܪ̈ܐ ܢܫ̈ܘܝܢ: ܘܕܩܐ ܢܙܥܪ.", "Dates will abound, oil will be dear, wheat and barley will be at a moderate price, and cereals will be scarce."),
            ("ܘܡܛܪܿܐ ܢܬܟܠܐ: ܘܠܐ ܢܚܘܬ ܥܠ ܐܪܥܐ ܬܠܬܝܢ ܝܘ̈ܡܝܢ ܥܕܡܐ ܠܦܨܚܐ.", "Rain will fail and will not fall upon the earth during thirty days down to the time of Passover."),
            ("ܘܡܠܟܐ ܢܬܟܬܫ ܥܡ ܡܠܟܐ ܘܢܩܛܠܝܘܗܝ.", "The king will fight against another king and will kill him."),
            ("ܘܐܠܟܣܢܕܪܝܐ ܬܐܒܕ: ܘܢܝܠܘܣ ܠܐ ܢܣܩ ܛܒܐܝܬ.", "Living in Alexandria will be dear. The Nile will not overflow well."),
            ("ܘܢܬܬܒܪ̈ܢ ܐܠܦ̈ܐ ܣܓܝ̈ܐܬܐ: ܘܒܫܘܠܡ ܫܢܬܐ ܗܘܿܝܐ ܫܘܝܘܬܐ ܕܟܠ ܡܕܡ.", "Many ships will break up. At the end of the year there will be moderation in everything.")
        ]
    },
    {
        "num": 7,
        "name": "Libra",
        "verses": [
            ("ܘܐܢ ܒܡܣܐܬܐ ܡܬܝܠܕܐ ܫܢܵ݇ܬܐ: ܡܛܪ̈ܐ ܪ̈ܒܝܥܝܐ ܢܗܘܘܢ: ܘܫܢ݇ܬܐ ܬܬܗܦܟ.", "If the year begins in Libra: There will be early rains, and the (order of the) year will be inverted."),
            ("ܘܢܚܘܢ ܐ݀ܢܫܐ ܡ̣ܢ ܪܘܚ ܕܡܕܢܚܐ.", "People will be secure from the East wind."),
            ("ܘܬܐܢ̈ܐ ܠܐ ܢܗܘܐ ܒܗܘܢ ܦܐܪ̈ܐ: ܘܬܡܖܪ̈ܐ ܘܡܫܚܐ ܢܣܓܘܢ.", "Fig-trees will not bear fruit. Dates and oil will abound."),
            ("ܘܚܡܪܐ ܢܐܩܪ: ܘܚܛ̈ܐ ܢܫܘ̈ܝܢ ܣܓܝ.", "Wine will be dear. Wheat will be at a very moderate price."),
            ("ܘܩܡܨܐ ܢܬܚܕܬ.", "Locusts will appear."),
            ("ܘܐܦܪܺܝܩܝ ܢܗܘܐ ܒܗܿ ܩܪܒܐ ܩܫܝܐ: ܘܟܘܪ̈ܗܢܐ ܩܫܝ̈ܐ ܒܒܢܝ̈ܢܫܐ ܢܗܘܘܢ.", "In Africa there will be a great and severe war. People will have acute diseases."),
            ("ܘܒܡܨܥܬܗܿ ܕܫܢܵܬܐ ܢܬܟܠܐ ܡܛܪܐ ܝܘܡܝ̈ܢ ܥܣܪܝܢ.", "In the middle of the year rain will fail during twenty days."),
            ("ܘܐܪ̈ܥܬܐ ܟܠܗܝܢ ܢܛ̈ܐܒܢ.", "All fields will be good."),
            ("ܘܟܠ ܕܐܝܬܘܗܝ ܫܡܗ ܝܘܕ ܐܘ ܒܝܬ ܢܬܟܪܗ: ܘܢܗܘܐ ܠܗ ܪܥܝܐ: ܘܢܐܙܠ ܒܓܠܘܬܐ ܡ̣ܢ ܐܪܥܗ.", "Anyone having in his name (the letters) Yodh or Beith will be ill, will have anxiety, and will emigrate from his country."),
            ("ܘܚܡܪܐ ܢܬܚܒܠ: ܘܓܘܪܐ ܢܣܓܐ.", "Wine will be spoiled, and adultery will increase with the increase of foul desires."),
            ("ܘܡܠܟܐ ܢܟܬܪ ܒܚܕܐ ܕܘܟܬܐ: ܘܢܐܙܠ ܫܘܠܛܢܐ ܡ̣ܢ ܐܪܥܐ.", "The king will remain in one place, and power will cease in the earth,"),
            ("ܘܖܽܘ̈ܪܒܢܐ ܢܥܪܩܘܢ ܒܝܡܐ: ܘܢܗܘܐ ܒܝܢܬܗܘܢ ܩܪܒܐ ܩܫܝܐ.", "and high officials will flee into the sea, and there will be between (them) a severe war."),
            ("ܘܢܗܘܐ ܒܓܠܝܠܐ ܙܘܥܐ ܩܫܝܐ.", "In Galilee there will be a violent earthquake."),
            ("ܘܠܣ̈ܛܝܐ ܢܦܩܘܢ ܒܚܘܪܢ ܘܒܕܪܡܣܘܩ.", "Marauders will appear in Hauran and in Damascus."),
            ("ܘܢܝܠܘܣ ܢܗܪܐ ܢܣܩ ܟܠܗ ܡܣܩܗ: ܘܢܗܘܐ ܒܡܨܪܝܢ ܫܪܥܘܛܐ ܩܫܝܐ: ܘܢܫܬܚܩܘܢ ܐ݇ܢܫܐ ܡܼܛܠ ܡܛܪܿܐ.", "The river Nile will overflow to its highest rate. In Egypt there will be a cruel pest. People will be in distress because of the shortage of rain.")
        ]
    },
    {
        "num": 8,
        "name": "Scorpio",
        "verses": [
            ("ܘܐܢ ܒܥܩܪܒܐ ܡܬܝܠܕܐ ܫܢ݇ܬܐ: ܬܫܒ ܪܽܘܚܐ ܕܓܪܒܝܐ ܒܫܘܪܝܗ̇ ܕܫܢ݇ܬܐ: ܘܢܗܘܘܢ ܡܛܪ̈ܐ ܣܓܝ̈ܐܐ ܪ̈ܒܝܥܝܐ.", "If the year begins in Scorpio: A North wind will blow at the beginning of the year, and there will be many early rains."),
            ("ܘܒܫܘܠܡܗܿ ܕܸܫܢ݇ܬܐ ܢܐܩܪ ܟܠ ܡܕܡ: ܘܡܛܪܐ ܢܙܥܪ: ܥܕܡܐ ܕܼܢܦܩܘܢ ܐ݇ܢܫܐ ܒܒܥܘܬܐ ܘܨܠܘܬܐ ܘܙܕܩ̈ܬܐ ܢܒܥܘܢ ܡ̣ܢ ܐܠܗܐ ܚܝܐ.", "At the end of the year everything will be dear, and rain will be so scarce that people will address prayers and supplications to the living God, for the sake of food."),
            ("ܘܟܘܪܗܢܐ ܢܗܘܐ ܒܢܫ̈ܐ ܕܒܛ̈ܢܢ.", "Pregnant women will have diseases."),
            ("ܘܣܓܝ̈ܐܐ ܡ̣ܢ ܒܢ̈ܝ̈ܢܫܐ ܢܫܢܘܢ ܡ̣ܢ ܐܬܪ̈ܘܬܗܘܢ ܡ̣ܢ ܐܘܠܨܢܐ.", "Many people will emigrate from their countries out of distress."),
            ("ܘܚܛ̈ܐ ܘܣܥܪ̈ܐ ܥ̈ܐܠܢ ܩܠܝܠ: ܘܕܩܐ ܢܐܠ.", "Wheat and barley will be ingathered, but only in small quantity; cereals will be ingathered."),
            ("ܘܚܡܪܐ ܘܡܫܚܐ ܢܗܘܐ.", "There will be wine and oil."),
            ("ܘܫܘܚ̈ܢܐ ܢܦܩܘܢ ܒܓܘܫ̈ܡܐ ܕܒܢܝ̈ܢܫܐ: ܘܠܐ ܢܚܣܪܘܢ ܐܢܘܢ.", "Boils will spring forth in the bodies of people but they will do no harm."),
            ("ܘܢܝܠܘܣ ܢܣܩ ܦܠܓܗ ܕܡܣܩܐ.", "The Nile will overflow half of its normal rate."),
            ("ܘܟܠ ܕܐܝܬܘܗܝ ܫܡܗ ܬܘ ܐܘ ܝܘܕ ܢܬܟܪܗ ܘܢܬܚܠܡ.", "Anyone having in his name (the letters) Taw, or Yodh, will be ill, but will recover."),
            ("ܘܟܠ ܕܡܬܝܠܕ ܒܥܩܪܒܐ ܚܝܿܐ: ܘܒܫܘܠܡܗܿ ܕܸܫܢ݇ܬܐ ܡܬܩܛܠ.", "Anyone born in Scorpio will live, but will be killed at the end of the year.")
        ]
    },
    {
        "num": 9,
        "name": "Sagittarius",
        "verses": [
            ("ܘܐܢ ܒܩܫܬܐ ܡܬܝܠܕܐ ܫܢ݇ܬܐ: ܟܠ ܕܐܝܬܘܗܝ ܫܡܗ ܒܝܬ ܐܘ ܦܐ ܢܗܘܐ ܠܗ ܫܚܩܐ ܘܟܘܪܗܢܐ ܩܫܝܐ.", "If the year begins in Sagittarius: Anyone having in his name (the letters) Beith, or Pe, will have severe illness and distress,"),
            ("ܘܒܫܘܪܝܗܿ ܕܸܫܢ݇ܬܐ ܢܬܩܫܐ: ܘܢܫܬܚܩܘܢ ܒܢܝ̈ܢܫܐ ܒܕܘܟ̈ܬܐ ܣܓܝ̈ܐܬܐ.", "which will be aggravated at the beginning of the year. People will be in distress in many places."),
            ("ܘܐܪܥܐ ܕܡܨܪܝܢ ܠܐ ܢܙܪܥܘܢ ܒܗܿ ܡܕܡ ܐܠܐ ܩܠܝܠ.", "Little will be sown in the land of Egypt."),
            ("ܘܒܡܨܥܬ ܫܢ݇ܬܐ ܢܗܘܐ ܡܛܪܿܐ ܣܿܓܝܐܐ.", "In the middle of the year there will be much rain."),
            ("ܘܢܚܡܠܘܢ ܒܢܝ̈ܢܫܐ ܥܒܘܪܐ ܒܒܝܬ ܐܘܨܪ̈ܐ ܡܸܛܠ ܙܥܘܪܘܬ ܡܛܪܐ.", "People will store corn in the barns because of the shortage of rain."),
            ("ܘܙܪܥܐ ܠܐ ܢܗܘܐ ܫܦܝܪ: ܘܫܘܠܡܗܿ̇ ܕܸܫܢ݇ܬܐ ܠܐ ܢܛܐܒ.", "Crops will not be good, so also will be the case at the end of the year."),
            ("ܘܚܡܪܐ ܘܡܫܚܐ ܢܫܘܘܢ ܣܓܝ.", "Wine and oil will be at a very moderate price."),
            ("ܘܓܘܪܐ ܢܣܓܐ: ܘܩܛܝܢܬܐ ܬܐܒܕܼ.", "Adultery will increase, and small cattle will perish.")
        ]
    },
    {
        "num": 10,
        "name": "Capricorn",
        "verses": [
            ("ܘܐܢ ܒܓܕܝܐ ܡܬܝܠܕܐ ܫܢܵ݇ܬܐ: ܟܠ ܕܐܝܬܘܗܝ ܫܡܗ ܩܘܦ ܢܬܟܪܗ ܘܢܬܒܙܙ ܘܢܒܠܥ ܒܣܝܦܐ.", "If the year begins in Capricornus: Anyone having in his name (the letters) Koph will be ill, will be plundered, and will be struck with sword."),
            ("ܘܪܘܚܐ ܡܕܢܚܝܬܐ ܡܕܼܒܪܐ ܠܗܿ ܠܫܢ݇ܬܐ.", "An East wind will dominate the year."),
            ("ܘܟܠ ܕܩܕܸܡ ܙܪܿܥ ܢܟܫܪ: ܐ݇ܚܪܝܐ ܠܐ ܢܟܫܪ.", "Everyone should sow earlier; the last in sowing will not succeed."),
            ("ܘܒܫܘܪܝܐ ܕܸܫܢ݇ܬܐ ܢܐܩܪ ܥܒܘܪܐ: ܘܢܣܓܘܢ ܓܠ̈ܠܐ ܘܡܚ̈ܫܘܠܐ: ܘܐܠܦܐ ܢܐܒܕܘܢ.", "At the beginning of the year corn will be dear. Waves and billows will increase. Ships will perish."),
            ("ܘܒܡܨܥܬܗܿ ܕܫܢ݇ܬܐ ܢܐܩܪ ܥܒܘܪܿܐ.", "In the middle of the year corn will be dear."),
            ("ܘܢܣܓܘܢ ܓܢܒ̈ܐ: ܘܦܠܚ̈ܘܗܝ ܕܫܘܠܛܢܐ ܒܝܫܝܢ ܢܗܘܘܢ.", "Thieves will increase. The officials of the state will be bad."),
            ("ܘܕܒܘܪ̈ܐ ܘܫܪܨܗܿ ܕܐܪܥܐ ܢܣܓܘܢ: ܘܢܒܐܫܘܢ ܐ݀ܢܫܐ ܣܓܝ̈ܐܐ.", "Wasps and reptiles of the earth will multiply and injure many people."),
            ("ܘܐ݇ܢܫܐ ܣܓܝ̈ܐܐ ܢܫܢܘܢ ܡ̣ܢ ܕܘܟܐ ܠܕܘܟܐ ܡܢ ܩܪܒܐ ܕܗܿܘܐ: ܘܢܣܓܘܢ ܩܪ̈ܒܐ ܒܐܪܥܐ.", "Many people will move from one place to another because of the war which will take place. Wars will increase in the earth."),
            ("ܘܒܫܘܠܡܗܿ ܕܫܢܵܬܐ ܢܙܥܪ ܡܛܪܐ.", "At the end of the year rain will be scarce."),
            ("ܘܒܕܘܟܝ̈ܬܐ ܢܐܠ ܙܪܥܐ: ܘܒܕܘܟ̈ܬܐ ܢܐܒܕܼ ܙܪܥܐ.", "In some places the standing corn will yield something, and in others it will perish."),
            ("ܘܟܘܪܗܢܐ ܒܕܪܡܣܘܩ ܢܗܘܐ ܘܒܚܘܪܢ: ܘܟܦܢܐ ܒܣܦܪ ܝܡܐ.", "There will be pest in Damascus and in Hauran, and famine in the littoral of the sea."),
            ("ܘܓܘܪܐ ܢܣܓܐ.", "Adultery will increase."),
            ("ܘܐ݇ܢܫܐ ܢܣܩܘܢ ܒܥܘܬܐ ܘܨ̈ܠܘܬܐ ܘܨܘܡܐ ܘܙܕܩ̈ܬܐ ܡܸܛܠ ܡܛܪܐ: ܘܙܪܥܐ ܕܫܩܝܐ ܛܒ ܢܗܘܐ.", "People will offer prayers and supplications, will fast and give alms for the sake of rain. The watered cereals will be normal.")
        ]
    },
    {
        "num": 11,
        "name": "Aquarius",
        "verses": [
            ("ܐܡܬܝ ܕܡܬܝܠܕܐ ܫܢ݇ܬܐ ܒܕܘܠܐ: ܟܠ ܕܐܝܬܘܗܝ ܫܡܗ ܠܡܕ ܐܘ ܦܐ ܢܬܟܪܗ: ܐܘ ܢܥܩܪ ܡ̣ܢ ܒܙܘܙܝܐ.", "When the year begins in Aquarius: Anyone having in his name (the letters) Lamadh or Pe will be ill, or will be uprooted through pillage."),
            ("ܘܒܫܘܪܿܝܗܿ ܕܸܫܢ݇ܬܐ ܢܕܥܪ ܡܛܪܐ: ܘܢܝܠܘܣ ܢܣܩ ܟܠܗ ܡܣܩܗ.", "At the beginning of the year rain will be scarce, and the Nile will overflow to its highest rate."),
            ("ܘܡܨܪܿܝܢ ܥܠ ܦܠܣܛܝܢܝ ܬܥܠ.", "Egypt will invade Palestine."),
            ("ܘܐܡܪ̈ܐ ܘܥܙ̈ܐ ܢܟܫܪܘܢ.", "Lambs and goats will prosper."),
            ("ܘܪܽܘܚܐ ܡܥܪܒܝܬܐ ܗܝِ ܡܕܒܪܐ ܠܫܢ݇ܬܐ ܗܝܿ.", "A West wind will dominate that year."),
            ("ܘܡܠܟܐ ܢܩܪܒ ܥܡ ܡܠܟܐ.", "A king will fight against a king."),
            ("ܘܙܪܥܐ ܩܕܝܡ ܢܟܫܪ: ܘܕܩܐ ܠܐ ܢܫܘܚ ܣܓܝ ܐܠܐ ܥܿܐܠ.", "Early crops will succeed, and cereals will not be plentiful, but normal."),
            ("ܘܬܓܪ̈ܐ ܢܒܥܘܢ ܡܥܕܪܢܘܬܐ ܡ̣ܢ ܐܠܗܐ ܚܝܐ: ܘܟܘܪ̈ܗܢܐ ܢܣܓܘܢ.", "Merchants will seek help from the living God, and illnesses will multiply.")
        ]
    },
    {
        "num": 12,
        "name": "Pisces",
        "verses": [
            ("ܘܐܢ ܒܢܘܢ̈ܐ ܡܬܝܠܕܐ ܫܢ݇ܬܐ: ܟܠ ܕܐܝܬܘܗܝ ܫܡܗ ܟܦ ܐܘ ܡܝܡ ܢܬܟܪܗ ܘܢܬܒܙܙ.", "If the year begins in Pisces: Anyone having in his name (the letters) Koph or Mim will be ill, and will be plundered."),
            ("ܫܢ݇ܬܐ ܛܒܬܐ ܬܗܘܐ: ܘܙܪܥܐ ܛܒ ܘܫܦܝܪ: ܘܡܛܪ̈ܐ ܪ̈ܒܝܥܝܐ ܢܗܘܘܢ.", "The year will be good, crops will be very good, and there will be early rains."),
            ("ܘܝܡܐ ܢܣܓܐ ܨܝܕܗ: ܘܡܐ ܕܒܚܳܫ ܐܠܦܐ ܢܬܬܒܪ̈ܢ.", "The sea will yield abundant fishing, but when it is rough ships will break up."),
            ("ܘܚܡܪܐ ܘܡܫܚܐ ܘܚܛ̈ܐ ܟܠܗܘܢ ܢܫܦܪܘܢ: ܘܙܪ̈ܥܐ ܛܒ ܢܣܓܘܢ.", "Wine, oil, and wheat will all be good, and standing crops will be very plentiful."),
            ("ܘܡܕ̈ܝ̈ܢܬܐ ܢܗܘܐ ܒܗܘܢ ܩܪ̈ܒܐ ܘܚܪܒܐ ܩܛܝܢܐ: ܘܩܘܪ̈ܝܐ ܬܐܒܕܢ: ܘܢܫܢܘܢ ܡ̣ܢ ܕܘܟܐ ܠܕܘܟܐ.", "In the cities there will be wars and cruel devastation; villages will be destroyed, and people will move from place to place."),
            ("ܘܢܦܩܘܢ ܠܣ̈ܛܝܐ ܡܼܢ ܦܠܣܛܝܢܐ: ܘܢܡܚܘܢ ܩܪܒܐ ܪܒܐ ܥܡ ܬܠܬ ܡܕܼܝ̈ܢܬܐ.", "Brigands will go forth from Palestine, and will wage a great battle against three cities."),
            ("ܘܪ̈ܗ݇ܘܡܝܐ ܙܟܝܢ ܘܡܙܕܟܝܢ: ܘܟܘܪܗܢܐ ܪܒܐ ܢܗܘܐ ܒܒܢܝ̈ܢܫܐ.", "The Romans will conquer and be conquered, and there will be great illness among the sons of men."),
            ("ܘܢܦܘܩ ܓܒܪܿܐ ܐܘܟܡܐ ܕܒܥܐ ܡܠܟܘܬܐ: ܘܒܝܬܐ ܕܡܠܟܘܬܐ ܢܐܒܕ.", "A dark-complexioned man will come forth seeking the kingdom, and the royal house will perish."),
            ("ܘܡܠܟܐ ܒܝܫܐ ܢܫܡܥ ܡܢܘ ܐܡܪܿܝܢ ܒܢ̈ܝܢܫܐ: ܘܡܚܪܒ ܡܕܝ̈ܢܬܐ ܣܓܝ̈ܐܬܐ.", "A wicked king will listen to gossip, and will lay waste many cities."),
            ("ܘܠܝܬ ܐܢܫ ܕܡܫܟܚ ܕܢܟܠܝܘܗܝ: ܘܕܚܠܬܐ ܕܐܠܗܐ ܘܪ̈ܚܡܘܗܝ ܦܪܝܩܝܢ ܡܢܗ.", "There will be no one able to stop him, and the fear of God and His mercy will be far from him."),
            ("ܘܒܫܘܠܡܗܿ ܕܫܢ݇ܬܐ ܢܗܘܐ ܫܝܢܐ ܘܫܠܡܐ ܒܒܢܝ̈ܢܫܐ: ܘܚܘܒܐ ܘܐܘܝܘܬܐ ܬܗܘܐ ܒܝܢܬ ܟܠܗܘܢ ܡܠܟ̈ܐ ܕܐܝܬ ܒܟܠܗ̇ ܐܪܥܐ.", "At the end of the year there will be peace and tranquillity among men, and love and harmony will prevail among all the kings of the whole earth.")
        ]
    }
]

def build_grammateus_xml():
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE document SYSTEM "document.dtd">',
        '<document id="TracSem">',
        '    <header>',
        '        <title>Treatise of Shem</title>',
        '        <author>Shem son of Noah (Pseudepigraphon)</author>',
        '        <editor>Alphonse Mingana (1917)</editor>',
        '        <description>Syriac text and English translation from Some Early Judæo-Christian Documents in the John Rylands Library (Manchester: The University Press, 1917), pp. 24-29, 54-61 (MS Cod. Syr. 44). Astrological/calendrical work in 12 chapters corresponding to the signs of the Zodiac (CAVT 85).</description>',
        '    </header>',
        '    <body>'
    ]
    for ch in CHAPTERS:
        c_num = ch["num"]
        for v_num, (syr, en) in enumerate(ch["verses"], 1):
            lines.append(f'        <div c="{c_num}" v="{v_num}">')
            lines.append(f'            <line lang="syr">{syr}</line>')
            lines.append(f'            <line lang="en">{en}</line>')
            lines.append('        </div>')
    lines.append('    </body>')
    lines.append('</document>\n')
    
    out_path = 'static/docs/TracSem.xml'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Wrote Grammateus XML: {out_path}')

def build_tei_p5_xml():
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<TEI xmlns="http://www.tei-c.org/ns/1.0">',
        '  <teiHeader>',
        '    <fileDesc>',
        '      <titleStmt>',
        '        <title>Treatise of Shem</title>',
        '        <author>Shem son of Noah (Pseudepigraphon)</author>',
        '        <editor>Alphonse Mingana</editor>',
        '        <respStmt>',
        '          <resp>TEI P5 Parallel Segmentation edition for Online Critical Pseudepigrapha</resp>',
        '          <name>Ken M. Penner</name>',
        '        </respStmt>',
        '      </titleStmt>',
        '      <publicationStmt>',
        '        <publisher>Online Critical Pseudepigrapha</publisher>',
        '        <pubPlace>St. Francis Xavier University, Antigonish, NS</pubPlace>',
        '        <availability>',
        '          <licence target="https://creativecommons.org/licenses/by/4.0/">CC-BY 4.0</licence>',
        '        </availability>',
        '      </publicationStmt>',
        '      <sourceDesc>',
        '        <biblStruct type="book">',
        '          <monogr>',
        '            <title level="m">Some Early Judæo-Christian Documents in the John Rylands Library</title>',
        '            <editor>Alphonse Mingana</editor>',
        '            <imprint>',
        '              <publisher>The University Press</publisher>',
        '              <pubPlace>Manchester</pubPlace>',
        '              <date when="1917">1917</date>',
        '              <biblScope unit="page">24-29, 54-61</biblScope>',
        '            </imprint>',
        '          </monogr>',
        '        </biblStruct>',
        '      </sourceDesc>',
        '    </fileDesc>',
        '  </teiHeader>',
        '  <text>',
        '    <body>'
    ]
    for ch in CHAPTERS:
        c_num = ch["num"]
        c_name = ch["name"]
        lines.append(f'      <div type="chapter" n="{c_num}">')
        for v_num, (syr, en) in enumerate(ch["verses"], 1):
            lines.append(f'        <p n="{v_num}">')
            lines.append(f'          <app>')
            lines.append(f'            <rdg wit="#Mingana1917" xml:lang="syr">{syr}</rdg>')
            lines.append(f'            <rdg type="translation" xml:lang="en">{en}</rdg>')
            lines.append(f'          </app>')
            lines.append(f'        </p>')
        lines.append('      </div>')
    lines.append('    </body>')
    lines.append('  </text>')
    lines.append('</TEI>\n')
    
    out_path = 'static/docs/tei/TracSem.xml'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Wrote TEI P5 XML: {out_path}')

if __name__ == '__main__':
    build_grammateus_xml()
    build_tei_p5_xml()
