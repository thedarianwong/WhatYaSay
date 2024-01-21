'use client';

import { useEffect, useRef, useState } from 'react';
import Link from 'next/link';

// const WebSocketURL = 'ws://localhost:8000/ws';

declare global {
    interface Window {
      SpeechRecognition: typeof SpeechRecognition;
      webkitSpeechRecognition: typeof SpeechRecognition;
    }
  }


const Home: React.FC = () => {
    const [isListening, setIsListening] = useState<boolean>(false);
    const [transcript, setTranscript] = useState<string>('');
    const recognitionRef = useRef<SpeechRecognition | null>(null);
    const [meetingAgenda, setMeetingAgenda] = useState<string>('');
    const [meetingGoals, setMeetingGoals] = useState<string>('');
    const [attendees, setAttendees] = useState<string>('');
    const [startTime, setStartTime] = useState<number>(0);
    const [elapsedTime, setElapsedTime] = useState<number>(0);
    const timerRef = useRef<NodeJS.Timeout | null>(null);
    const [interimTranscript, setInterimTranscript] = useState<string>('');
    const [summary, setSummary] = useState<string>('');


    useEffect(() => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            console.error('Your browser does not support Speech Recognition.');
            return;
        }
    
        // Initialize SpeechRecognition
        const recognition = new SpeechRecognition();
        recognition.continuous = true; // Capture continuous speech
        recognition.interimResults = true; // Show interim results
        recognition.lang = 'en-US'; // Set language
    
        recognition.onresult = (event: SpeechRecognitionEvent) => {
            let interimTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    setTranscript(prevTranscript => prevTranscript + ' ' + transcript);
                } else {
                    interimTranscript += transcript;
                }
            }
            // Update the component state with the interim transcript
            setInterimTranscript(interimTranscript);
        };
    
        recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
            console.error('Speech recognition error:', event.error);
        };
    
        recognitionRef.current = recognition;
    }, []);
    
    


  const handleToggleListening = () => {
    if (recognitionRef.current) {
      if (!isListening) {
        recognitionRef.current.start();
        const startTimestamp = new Date();
        setStartTime(startTimestamp.getTime());
        timerRef.current = setInterval(() => {
            const currentTime = new Date();
            setElapsedTime(currentTime.getTime() - startTimestamp.getTime());
        }, 1000);
      } else {
        recognitionRef.current.stop();
        if (timerRef.current) {
            clearInterval(timerRef.current);
        }
      }
      setIsListening(!isListening);
    }
  };


    const formatTime = (milliseconds: number): string => {
        const seconds = Math.floor(milliseconds / 1000) % 60;
        const minutes = Math.floor(milliseconds / 60000);
        return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    };

    const handleSubmit = async () => {
        try {
            // API endpoint
            const apiEndpoint = 'http://localhost:8000/summarize';
    
            // Prepare the request body
            const requestBody = {
                audio_content: transcript,
                context: meetingAgenda
            };
    
            // Make the API request
            const response = await fetch(apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                    // Include additional headers if necessary
                },
                body: JSON.stringify(requestBody)
            });
    
            if (!response.ok) {
                throw new Error('API request failed');
            }
    
            const responseData = await response.json();
            setTranscript(responseData); // Update the transcript with the summary
        } catch (error) {
            console.error('Error submitting data:', error);
        }
    };
    
    
	
    return (
        <div className="flex flex-col h-screen bg-gray-800 text-white overflow-hidden">
            <div className="flex flex-1 overflow-hidden">
                <div className="w-1/2 p-6 space-y-4 bg-gray-900 border-r border-gray-700">
                    <h2 className="text-2xl font-semibold text-blue-300 text-center">Meeting Details</h2>
                    <textarea
                        className="w-full p-2 bg-gray-800 border border-blue-500 rounded focus:border-blue-300"
                        placeholder="Meeting Agenda"
                        value={meetingAgenda}
                        onChange={(e) => setMeetingAgenda(e.target.value)}
                    />
                    <textarea
                        className="w-full p-2 bg-gray-800 border border-blue-500 rounded focus:border-blue-300"
                        placeholder="Goals of the Meeting"
                        value={meetingGoals}
                        onChange={(e) => setMeetingGoals(e.target.value)}
                    />
                    <textarea
                        className="w-full p-2 bg-gray-800 border border-blue-500 rounded focus:border-blue-300"
                        placeholder="Attendees"
                        value={attendees}
                        onChange={(e) => setAttendees(e.target.value)}
                    />
                    <div className="flex items-center justify-between">
                        <div>
                            <span>Meeting Time: {formatTime(elapsedTime)}</span>
                        </div>
                        {!isListening ? (
                            <button
                                className="px-4 py-2 font-bold rounded bg-green-500 hover:bg-green-600"
                                onClick={handleToggleListening}
                            >
                                Start Recording
                            </button>
                        ) : (
                            <button
                                className="px-4 py-2 font-bold rounded bg-red-500 hover:bg-red-600"
                                onClick={handleToggleListening}
                            >
                                Stop Recording
                            </button>
                        )}

                    </div>
                    <hr className="border-gray-700" />
                    <div className="flex justify-between">
                        <button className="px-4 py-2 font-bold rounded bg-purple-600 hover:bg-purple-700">
                            Save to Google Drive
                        </button>
                        <button className="px-4 py-2 font-bold rounded bg-blue-600 hover:bg-blue-700">
                            Download as PDF
                        </button>
                    </div>
                        <button onClick = {handleSubmit} className="w-full px-4 py-2 mt-4 font-bold rounded bg-green-600 hover:bg-green-700">
                            Submit Meeting
                        </button>
                </div>
                <div className="w-1/2 p-6 bg-gray-900 h-full flex flex-col">
                    <h2 className="text-2xl font-semibold text-blue-300 text-center mb-4">Transcript</h2>
                    {/* <div className=" flex-grow bg-gray-800 p-4 overflow-y-auto border border-blue-500 rounded">
                        transcript-display
                        {transcript ? <p>{transcript}</p> : <p className="text-white-500">Transcript will appear here...</p>}
                    </div> */}
                    <div className="transcript-display flex-grow bg-gray-800 p-4 overflow-y-auto border border-blue-500 rounded">
                    {transcript}
                    <span className="text-white-500 interim-transcript">{interimTranscript}</span>
                </div>
                </div>
            </div>
        </div>
    );
};

export default Home;
