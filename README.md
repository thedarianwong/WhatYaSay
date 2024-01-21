# What DYa’ Say? 🎙️

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
