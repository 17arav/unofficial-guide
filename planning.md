## Domain
This system makes unofficial ASU campus dining knowledge—such as hacky uses for M&G dollars, honest reviews of dining halls, and strategies to avoid overpriced or low-quality food—searchable for students. This knowledge is valuable but hard to find because the official ASU Dining websites only show promotional material, while the real experiences are buried in scattered Reddit threads and upperclassman lore.

## Documents
The source documents consist of 10 specific Reddit threads from r/ASU covering dining halls, M&G dollars, meal plans, and cheap off-campus food:
1. Making food as a freshman / dining hall alternatives (Reddit)
2. Cheap food spots near campus (Reddit)
3. Meal Exchange program changes (Reddit)
4. Barrett dining hall meal plan changes (Reddit)
5. The reality of M&G Bonus Dollars (Reddit)
6. Dining Hall Food Rant (Reddit)
7. Are Meal Plans a scam? (Reddit)
8. The secret behind the ASU Sugar Cookies (Reddit)
9. Tips for incoming freshmen / meal plans (Reddit)
10. Incoming student advice on dorm cooking (Reddit)

## Chunking Strategy
I will chunk the documents using a fixed character size of 500 characters with an overlap of 100 characters. 
* **Why this size:** Reddit threads consist of short, conversational opinions (comments) mixed with longer explanatory posts. 500 characters is roughly 2-4 sentences, which is perfect for capturing a complete thought or a specific review without diluting it with unrelated comments. 
* **Why this overlap:** A 100-character overlap ensures that if a user mentions a dining hall name at the end of one chunk and complains about it in the next, the context isn't lost across the boundary. If the chunks were too large (e.g., 2000 characters), specific questions about wait times or prices might get drowned out by unrelated complaints in the same thread.

## Retrieval Approach
* **Embedding Model:** `sentence-transformers` (`all-MiniLM-L6-v2`).
* **Top-k:** I will retrieve the top 4 chunks (`k=4`) per query. 4 chunks provide enough context for the LLM to synthesize an answer without overflowing the context window with irrelevant noise.
* **Production Tradeoffs:** If I were deploying this for real users without cost constraints, I would consider a model like OpenAI's `text-embedding-3-small` or Cohere's embeddings. While `all-MiniLM-L6-v2` is great for local, free, and fast execution, a paid API model typically offers better multilingual support and a much larger context length window for generating embeddings of highly technical or nuanced text.

## Evaluation Plan
Here are 5 test questions with expected "ground truth" answers based on ASU student consensus:
1. **Q: Which meal plan should incoming freshmen buy?** 
   *Expected Answer:* The smallest/cheapest one (like the Sparky plan). Students agree you get tired of dining hall food quickly and will want M&G or cash to eat elsewhere.
2. **Q: Is the Barrett dining hall worth the extra cost?** 
   *Expected Answer:* No. Most students say it's slightly better than Pitchforks or Hassy, but not worth the premium price tag.
3. **Q: What is the best way to use M&G dollars?** 
   *Expected Answer:* Use them at on-campus restaurants (like Chick-fil-A or Qdoba) or the POD markets, not to swipe into dining halls.
4. **Q: What changed with the Meal Exchange program?** 
   *Expected Answer:* Aramark changed/nerfed the options, restricting what students can actually get for a meal swipe at places like the MU, making it a worse deal than before.
5. **Q: What are the ASU dining hall sugar cookies?** 
   *Expected Answer:* They are highly praised, often jokingly (or seriously) called the best food item available on campus.

## Anticipated Challenges
1. **Reddit Noise:** Reddit threads have a lot of boilerplate text (usernames, upvote counts, "deleted" comments, and nested replies). If my cleaning step fails, chunks will be filled with useless metadata instead of actual opinions.
2. **Sarcasm and Slang:** College subreddits use heavy sarcasm (e.g., "Aramark provides 5-star Michelin dining"). The embedding model might struggle to match genuine questions to sarcastic answers, or the LLM might take sarcastic chunks literally.

## AI Tool Plan
I will use an AI tool (like ChatGPT or Claude) to help write the Python scripts. 
* **Ingestion:** I will prompt the AI with my "Documents" section and ask it to write a Python script using BeautifulSoup or the Reddit API (or just text file reading) to extract the raw text.
* **Chunking & Vector Store:** I will provide my "Chunking Strategy" and "Retrieval Approach" sections to the AI and ask it to write the ChromaDB and `sentence-transformers` implementation.
* **Grounded Generation:** I will give the AI my evaluation questions and ask it to help craft a strict system prompt for Groq (`llama-3.3-70b-versatile`) that forces the model to cite its sources and refuse to answer if the context is missing.

## Architecture
Document Ingestion (Raw Text) 
  ↓ 
Chunking (Python string slicing / Langchain text splitter) 
  ↓ 
Embedding + Vector Store (sentence-transformers: all-MiniLM-L6-v2 + ChromaDB) 
  ↓ 
Retrieval (Top-k = 4 semantic search) 
  ↓ 
Generation (Groq API / llama-3.3-70b-versatile)