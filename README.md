# What DYa’ Say? 🎙️
![WhatDyaSay](https://github.com/thedarianwong/WhatYaSay/assets/93755359/5c6bb2ce-bbdf-4ae6-a02a-a508bcab535f)

## 🌟 Project Overview
"What DYa’ Say?" is a cutting-edge web-based application designed to offer real-time transcription services with enhanced features for summarizing and structuring transcribed content into an easily accessible note format. Ideal for students, professionals, or anyone in need of documenting and organizing spoken information efficiently.

### 🎯 Objectives
- 📝 Provide real-time transcription of lectures, meetings, or conversations.
- 📊 Offer options for transforming transcriptions into summarized and structured notes.
- 💾 Enable users to save these notes in various formats for future reference.

### ✨ Features
- **User Authentication:** Optional login for a personalized experience and additional features.
- **Real-Time Transcription:** Using speech-to-text API to transcribe spoken words in real-time.
- **Speaker Identification:** Implement speaker diarization to differentiate speakers during transcription.
- **Summarization and Structuring:** Post-recording option to convert raw transcripts into summarized, note-like formats.
- **Storage and Export Options:** Ability to save notes directly to Google Drive, Email, or download as PDF.
- **Latex Document Formatting:** Convert notes into a well-structured LaTeX format.

## 🔧 Technical Specifications
- **Front-End:** Next.js
- **Back-End:** Python with FastApi.
- **APIs:** Speech-to-Text (e.g., Google Cloud Speech-to-Text), Speaker Diarization, LaTeX rendering (Coming Soon).
- **Authentication:** OAuth for Google Drive/Email integration; JWT for user session management (Coming Soon).
- **Storage:** Cloud storage integration for logged-in users; local storage for session persistence.

## 📚 User Stories
1. **The Note-Taking Student:** 🎓 Focus entirely on your lecture, without the hassle of jotting down notes. Our app transcribes lectures in real time, allowing you to review and study the material at your own pace post-session.
2. **The Efficient Professional:** 💼 Engage fully in meetings, knowing every detail is captured and ready to be converted into organized notes for later reference.
3. **Hackathon Participants:** 👥 Brainstorm with your team, while our app documents and organizes your innovative ideas into a structured format, enhancing productivity and creativity.

## 🚀 Development Plan
### Phase 1 - Setup and Basic Functionality
- 🛠 Set up the development environment and project skeleton.
- 🗣 Integrate the speech-to-text API for basic real-time transcription.

### Phase 2 - Advanced Features and UI
- 🎨 Develop the UI for recording, displaying transcription, and post-processing options.
- 🔊 Implement speaker diarization and transcription summarization logic.

### Phase 3 - User Authentication and Storage
- 🔒 Add a user authentication system.
- ☁️ Integrate Google Drive and Email APIs for storage options.

### Phase 4 - Testing and Refinement
- 🧪 Conduct thorough testing, including user acceptance testing.
- 🔄 Refine features based on feedback.

### Phase 5 - Deployment and Launch
- 🌐 Deploy the application to a web server.
- 🚀 Officially launch the app for public use.

## Difficulties
It was our first time building an application that utilizes mostly Google's API and Authentication so we were spending lots of time setting it up. We also had trouble establishing the websocket to ensure the smooth audio data delivery from the client side to the server side. It was not receiving properly, we tried sending in bytes, buffer and all sorts of methods but we just did not find a way to ensure that it is smooth and happening in real time. This is something we would like to fix after the hackathon since this is the most important aspect of the project. For now, we will just be submitting the version where we are utilizing just web speech built-in API in Chrome. We will also link the Authentication afterwards, we just got the token. 

## Build
```bash
# Navigate to the client directory and run the start-dev script
cd client
./start-dev.sh

# Navigate to the server directory and run the start-dev script
cd server
./start-dev.sh
