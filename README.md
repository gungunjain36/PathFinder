
# PathFinder AI 
![WhatsApp Image 2024-12-21 at 3 29 29 PM](https://github.com/user-attachments/assets/c0891279-e986-4588-b933-8e304e8cc63d)

## 1. Project Overview
PathFinder AI is an intelligent tech event discovery platform designed to automate the process of finding, processing, and delivering relevant tech events to users. By leveraging web crawling, AI processing, and social media integration, it provides a seamless, user-friendly event discovery experience.

---
![WhatsApp Image 2024-12-21 at 3 30 01 PM](https://github.com/user-attachments/assets/1628d053-e293-4212-b7a7-bbec0dd7a82a)
![WhatsApp Image 2024-12-21 at 3 30 30 PM](https://github.com/user-attachments/assets/d7771b66-df38-4358-a6d8-8e2539bdc5bb)

## 2. Problem Statement
Discovering relevant tech events is often:
- **Time-consuming:** Manually searching for events across multiple platforms is inefficient.
- **Scattered Information:** Event details are distributed across various websites and social media channels.
- **Irrelevant Results:** Generic search engines often fail to filter results based on specific user needs.
- **Missed Opportunities:** Many events go unnoticed due to lack of a centralized discovery platform.

**PathFinder AI aims to solve these issues** by:
- Automating event discovery.
- Filtering and personalizing results.
- Providing structured, actionable information in real-time.
- Integrating with social media and calendar tools for better engagement.

---
![WhatsApp Image 2024-12-21 at 3 30 40 PM](https://github.com/user-attachments/assets/619f13f4-62ae-4970-baf3-fa5baa30ff07)

## 3. System Components

### A. Frontend Implementation (`/frontend`)
- **Tech Stack:** React, Tailwind CSS.
- **Key Features:**
  - **Dynamic Animations:** Interactive landing page with event stats.
  - **Event Filtering:** Users can filter events based on date, category, and location.
  - **Responsive Design:** Optimized for all device sizes.
  - **Documentation Page:** Includes an architecture diagram for better understanding.
  


### B. Backend Services (`/backend/app/services`)
- **Tech Stack:** FastAPI, LLaMA AI, Playwright.
- **Key Services:**
  1. **Processor Service (`processor.py`)**
     - Handles text chunking for efficient processing.
     - Implements advanced deduplication using LLM.
     - Extracts structured data from raw event details.
  2. **Crawler Service (`crawler.py`)**
     - Uses Playwright for rendering JavaScript-heavy pages.
     - Implements smart query generation for relevant results.
     - Validates and filters content to ensure accuracy.
  3. **Social Integration Service (`create_tweet.py`)**
     - Automates X (Twitter) posting with engagement tracking.
     - Formats content smartly for higher reach and visibility.

---

## 4. Tech Stack
| Layer        | Technologies Used       |
|--------------|--------------------------|
| **Frontend** | React, Tailwind CSS      |
| **Backend**  | FastAPI, Python          |
| **AI**       | LLaMA 3.1 (70B model)    |
| **Crawling** | Playwright, BeautifulSoup|
| **Database** | JSON Storage                  |
| **Hosting**  | Local Deployment|

---

## 5. Challenges Faced
1. **Crawling JavaScript-Heavy Pages:**  
   - Many event pages heavily rely on JavaScript rendering.
   - **Solution:** Integrated Playwright to handle JS-based dynamic content.

2. **Token Limitation in AI Models:**  
   - LLaMA's 4K token limit required intelligent chunking of large HTML content.
   - **Solution:** Developed a smart chunking algorithm with relevance scoring.

3. **Duplicate Event Handling:**  
   - Duplicate entries from multiple sources were common.
   - **Solution:** Used AI-based deduplication and content comparison.

4. **Rate Limiting and Bot Detection:**  
   - Crawling multiple websites triggered rate-limiting.
   - **Solution:** Implemented rate limiting, error handling, and retries.

5. **Social Media Formatting:**  
   - Automating Twitter posts with engaging content required customization.
   - **Solution:** Created a formatting pipeline to generate concise, high-quality posts.

---

## 6. Key Features
- **Real-Time Discovery:** Automatically fetches live events.
- **Google Calendar Integration:** Allows users to add events to their calendars directly.
- **Smart Filters:** Filter events based on parameters like category, location, and date.
- **Social Media Bot:** Automatically shares updates on X (Twitter).
- **Responsive Design:** Accessible on mobile, tablet, and desktop devices.
- **Interactive Documentation:** System architecture is visually documented for better understanding.

---

## 7. Data Flow
1. **Crawling:** The crawler fetches event pages from websites.
2. **Chunking:** Content is cleaned and divided into smaller chunks.
3. **AI Processing:** LLaMA processes chunks, extracting structured data.
4. **Deduplication:** Extracted data is filtered for uniqueness.
5. **Storage:** Final event details are stored in the database.
6. **Frontend Display:** Events are displayed to users in a clean UI.
7. **Social Media Posting:** Processed events are shared on social media platforms.

---

## 8. File Structure
```
/frontend
  ├── src/
  │   ├── components/
  │   │   ├── App.jsx
  │   │   ├── Hero.jsx
  │   │   ├── Documentation.jsx
  │   │   ├── EventCard.jsx
  │   │   └── Filter.jsx
  │   └── utils/
  │       └── calendar.js
  └── public/
      └── icons/

/backend
  └── app/
      ├── services/
      │   ├── processor.py
      │   ├── crawler.py
      │   └── create_tweet.py
      └── config.py
```

---

## 9. Setup Instructions

### A. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### B. Backend Setup
```bash
cd backend

python3 -m venv venv && source venv/bin/activate (on Mac)

python -m venv venv && ./venv/Scripts/activate (on Windows)

pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 10. Environment Variables

### Frontend (`.env`):
- `VITE_API_URL=http://localhost:8000`

### Backend (`.env`):
- `AI_API_KEY=your_api_key`
- `X_API_KEY=your_twitter_api_key`
- `X_API_KEY_SECRET=your_twitter_secret`
- `X_ACCESS_TOKEN=your_access_token`
- `X_ACCESS_TOKEN_SECRET=your_access_token_secret`

---

## 11. API Endpoints
- **GET `/results`**: Fetch processed events.
- **POST `/process`**: Trigger event processing.
- **GET `/health`**: API health check.

---

## 12. Future Improvements
- Enhanced event categorization with ML.
- Real-time user notifications.
- Integration with more social media platforms.
- Advanced search capabilities based on user preferences.
- Recommendation system for personalized event suggestions.

---

## 13. Contact & Support
- **Twitter:** [@Gungun__23](https://twitter.com/Gungun__23)
