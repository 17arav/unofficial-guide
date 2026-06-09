import os

data_dir = "data"
os.makedirs(data_dir, exist_ok=True)

documents = {
    "source_1.txt": "Freshman year tip: don't rely entirely on the dining halls. Pitchforks gets old fast, and Hassy is hit or miss. Get a mini-fridge and microwave if you can. Making your own quick meals saves so much time when you're cramming for engineering midterms.",
    "source_2.txt": "Looking for cheap lunch spots near campus? Honestly, getting off campus is better. If you have an electric scooter like a Hiboy, just zip over to University Drive or Mill Ave. There are plenty of local spots that are cheaper and way better quality than the MU.",
    "source_3.txt": "The recent changes to the Meal Exchange program are brutal. It used to be a great deal, but the new Aramark policies nerfed the options at the MU. You get way less food for a swipe now. It's almost always better to just use M&G dollars instead of trying to force a meal exchange.",
    "source_4.txt": "Is the Barrett dining hall worth the extra cost? Most students say no. It's slightly better than Pitchforks, and they have a gelato bar, but the premium price tag isn't justified unless you eat a massive amount of food every single day.",
    "source_5.txt": "M&G Bonus Dollars are confusing. Basically, they are promotional funds that expire at the end of the year, unlike regular M&G which rolls over (sometimes). Always use your bonus dollars first! The best use for M&G is at on-campus chains like Chick-fil-A or Qdoba.",
    "source_6.txt": "Dining hall rant: The chicken is always dry and the lines during lunch rush are insane. If you have a tight schedule between classes, don't even try going to the MU dining halls at noon. Just grab something from the POD market.",
    "source_7.txt": "Are meal plans a scam? Kind of. The all-access plan forces you to eat on campus constantly to get your money's worth. Get the smallest plan possible (like the Sparky plan) and use the money you saved to buy real groceries or eat off campus.",
    "source_8.txt": "The ASU sugar cookies are legitimately the best food item on campus. You can find them at the dining halls and sometimes the POD markets. They are baked fresh, super soft, and completely addictive. Always grab two if you see them.",
    "source_9.txt": "Advice for incoming freshmen: Don't buy the biggest meal plan. You will get tired of the food by October. Instead, load up on M&G dollars. M&G gives you flexibility to eat at the fast food places in the MU or grab coffee at Starbucks when you're pulling an all-nighter.",
    "source_10.txt": "Dorm cooking is totally doable. You can make pasta, rice, and even eggs in a microwave if you buy the right containers. It's much healthier than eating pizza at the dining hall every night, and you avoid the constant crowds."
}

for filename, content in documents.items():
    filepath = os.path.join(data_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("All 10 text files successfully populated!")