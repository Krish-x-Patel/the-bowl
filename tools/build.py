#!/usr/bin/env python3
"""Builds index.html for The Bowl from one menu list, so prices only live in one place.

Prices and "liked" numbers are from the Uber Eats menu (checked Nov 22, 2026).
Delivery-app prices are often higher than in-store prices. Update them after the visit.
"""
import html

UBER = "https://www.ubereats.com/store/the-bowl/mhZMz5KuTgmDhU29NgQJkg"
MAPS = "https://www.google.com/maps/dir/?api=1&destination=The+Bowl+369+Cobb+Pkwy+S+Marietta+GA"
EMBED = "https://www.google.com/maps?q=The+Bowl,+369+Cobb+Pkwy+S,+Marietta,+GA&output=embed"
TEL = "tel:+17707021129"

# group id, group title, items: (name, price, description, image or None, liked or None)
MENU = [
 ("bowls", "Bowls", [
  ("Ramen", "15.99", "Japanese-style noodles in a rich meat broth", "ramen", "91% liked it (191)"),
  ("Bibimbap", "15.99", "Korean rice dish with chili paste and sauteed vegetables", "bibimbap", "88% liked it (70)"),
  ("Original Bowl", "14.99", "A savory rice bowl filled with flavorful toppings", "original-bowl", "95% liked it (24)"),
 ]),
 ("specials", "Featured specials", [
  ("Bulgogi hot stone bowl", "19.99", "Marinated beef served sizzling in a hot stone bowl", None, "80% liked it (46)"),
  ("Poke bowl", "17.95", "Fresh fish salad with vegetables and rice", None, "85% liked it (34)"),
 ]),
 ("bundles", "Bowl and drink bundles", [
  ("Ramen bundle", "18.95", "Our ramen with your choice of Coca-Cola drink", None, "100% liked it (7)"),
  ("Stir fry ramen bundle", "18.95", "Japanese-style noodles stir fried with vegetables, with your choice of Coca-Cola drink", "stir-fry-ramen", "92% liked it (13)"),
  ("Bibimbap bundle", "18.95", "Our bibimbap with your choice of Coca-Cola drink", None, "85% liked it (7)"),
 ]),
 ("sides", "Sides", [
  ("Chicken pot stickers (8)", "8.99", "Chicken dumplings with our house-made ginger soy sauce, fermented for 3 months", None, "97% liked it (528)"),
  ("Shrimp egg rolls (2)", "5.99", "Crisp rolls filled with shrimp and egg", None, "97% liked it (47)"),
  ("Spring rolls (2)", "4.49", "Vegetable spring rolls", None, "93% liked it (91)"),
  ("Jumbo shrimp tempura", "8.99", "Breaded and fried jumbo shrimp with yum yum sauce", None, "90% liked it (140)"),
  ("Crab cream croquettes (4)", "9.99", "Crab and vegetables, breaded and fried, with two sauces", None, "86% liked it (43)"),
  ("Takoyaki", "8.99", "Crispy balls filled with tender octopus", None, "80% liked it (15)"),
  ("Seaweed salad", "4.99", "", None, "94% liked it (56)"),
  ("Steamed veggies", "4.99", "Broccoli, carrots, cabbage, zucchini and onions", None, "83% liked it (18)"),
  ("Steamed rice", "3.50", "Freshly cooked white rice", None, "92% liked it (120)"),
 ]),
 ("extras", "Add to your bowl", [
  ("Galbi", "13.99", "Grilled ribs marinated in Korean BBQ sauce", None, "98% liked it (60)"),
  ("Bulgogi", "12.99", "Stir-fried Black Angus ribeye", None, "80% liked it (110)"),
  ("Spicy pork", "8.99", "Grilled pork belly in our signature spicy sauce (about 1 or 2 out of 10)", None, "94% liked it (19)"),
  ("Herb grilled chicken", "7.99", "Chicken marinated with chopped fresh herbs", None, None),
  ("Extra noodles", "4.99", "For ramen or stir fry ramen", None, "100% liked it (11)"),
  ("Extra vegetables", "3.99", "", None, "83% liked it (6)"),
  ("Egg", "3.00", "", None, "91% liked it (35)"),
  ("Extra sauce", "1.00", "Tell us which sauce you'd like", None, "83% liked it (48)"),
 ]),
 ("drinks", "Drinks", [
  ("Canned soda", "3.99", "Coke, Diet Coke, Coke Zero, Cherry Coke, Cherry Coke Zero, Sprite, Orange Fanta or ginger ale", None, None),
  ("Jarritos", "3.99", "Pineapple, mango, grapefruit or mandarin", None, None),
  ("Ramune", "3.99", "Japanese marble soda", None, "100% liked it (7)"),
  ("Gold Peak sweet tea", "3.99", "", None, None),
  ("Canned coffee", "3.99", "", None, None),
  ("Oolong, jasmine or green tea", "4.50", "", None, None),
  ("Organic juice or lemonade", "4.99", "Lemonade, cranberry, peach, orange mango or black currant", None, None),
  ("Bruce Cost ginger ale", "4.99", "", None, None),
 ]),
]
# Bowl cards (big photos): Uber Eats "most liked" order, then the best-rated photo dish
POPULAR = [("Ramen", "#1 most liked"), ("Bibimbap", "#2 most liked"), ("Original Bowl", "#3 most liked"),
           ("Stir fry ramen bundle", "")]

ITEMS = {i[0]: i for g in MENU for i in g[2]}
e = html.escape

def slug(s): return "".join(c if c.isalnum() else "-" for c in s.lower()).strip("-")

def bowls_html():
    out = []
    for name, badge in POPULAR:
        n, price, desc, img, liked = ITEMS[name]
        b = f'<span class="tag">{e(badge)}</span>' if badge else ''
        lk = f'<p class="lk">{e(liked.replace("(", "· ").replace(")", " ratings"))}</p>' if liked else ''
        out.append(f'''        <a class="bowl" href="#item-{slug(n)}">
          <span class="ph">{b}<img src="images/{img}.jpg" alt="{e(n)}" width="825" height="660" loading="lazy"></span>
          <span class="meta"><h3>{e(n)}</h3><span class="pr">${price}</span></span>
          <p>{e(desc)}</p>
          {lk}
        </a>''')
    return "\n".join(out)

def tabs_html():
    return "\n".join(f'        <a class="tab" role="tab" href="#{gid}" id="tab-{gid}" aria-controls="{gid}" aria-selected="false">{e(t)}</a>' for gid, t, _ in MENU)

def panels_html():
    out = []
    for gid, title, items in MENU:
        out.append(f'      <div class="panel" id="{gid}" role="tabpanel" aria-labelledby="tab-{gid}">\n        <h3>{e(title)}</h3>\n        <ul>')
        for n, price, desc, img, liked in items:
            d = f'<span class="ds">{e(desc)}</span>' if desc else ''
            lk = f'<span class="lk">{e(liked)}</span>' if liked else ''
            out.append(f'          <li id="item-{slug(n)}"><span class="nm">{e(n)}</span><span class="pr">${price}</span>{d}{lk}</li>')
        out.append('        </ul>\n      </div>')
    return "\n".join(out)

TEMPLATE = open('tools/template.html').read()
page = (TEMPLATE.replace('{{BOWLS}}', bowls_html()).replace('{{TABS}}', tabs_html()).replace('{{PANELS}}', panels_html())
        .replace('{{UBER}}', UBER).replace('{{MAPS}}', MAPS).replace('{{EMBED}}', EMBED).replace('{{TEL}}', TEL))
assert '{{' not in page
open('index.html', 'w').write(page)
print('built', len(page), 'bytes;', sum(len(g[2]) for g in MENU), 'menu items')
