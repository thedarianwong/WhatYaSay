'use client';

import { useEffect, useRef, useState, MutableRefObject } from 'react';

const WebSocketURL = 'ws://localhost:8000/ws';

const Home: React.FC = () => {
    const [isRecording, setIsRecording] = useState<boolean>(false);
    const [transcript, setTranscript] = useState<string>('');
    const [meetingAgenda, setMeetingAgenda] = useState<string>('');
    const [meetingGoals, setMeetingGoals] = useState<string>('');
    const [attendees, setAttendees] = useState<string>('');
    const [startTime, setStartTime] = useState<number>(0);
    const [elapsedTime, setElapsedTime] = useState<number>(0);
    const socketRef = useRef<WebSocket | null>(null);
    const mediaRecorderRef = useRef<MediaRecorder | null>(null);
    const timerRef = useRef<NodeJS.Timeout | null>(null);


	useEffect(() => {
		socketRef.current = new WebSocket(WebSocketURL);

		socketRef.current.onopen = () => {
			console.log('WebSocket Connected');
		};

		socketRef.current.onmessage = (event: MessageEvent) => {
			console.log('Message received from server:', event.data);
			setTranscript(prev => prev + '\n' + event.data);
		};

		socketRef.current.onclose = () => {
			console.log('WebSocket Disconnected');
		};

		return () => {
			if (socketRef.current) {
				socketRef.current.close();
			}
		};
	}, []);

	const startRecording = async (): Promise<void> => {
		setIsRecording(true);
        setStartTime(Date.now());
        setElapsedTime(0); // Reset elapsed time to zero
        const startTimestamp = Date.now(); // Capture start timestamp
    
        timerRef.current = setInterval(() => {
            setElapsedTime(Date.now() - startTimestamp);
        }, 1000);
		console.log('Starting recording...');
		try {
			const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
			mediaRecorderRef.current = new MediaRecorder(stream);

			mediaRecorderRef.current.start(5000);

			mediaRecorderRef.current.ondataavailable = async (event: BlobEvent) => {
				if (
					socketRef.current &&
					socketRef.current.readyState === WebSocket.OPEN
				) {
					console.log('Sending audio data to server...');
					socketRef.current.send(event.data);
					console.log(event.data);
				} else {
					console.log('WebSocket not open. Unable to send data.');
				}
			};
		} catch (error) {
			console.error('Error starting recording:', error);
		}
	};

	const stopRecording = (): void => {
		setIsRecording(false);
        if (timerRef.current) {
            clearInterval(timerRef.current);
        }
		console.log('Stopping recording...');

		if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
			mediaRecorderRef.current.stop();
		}
	};

    const formatTime = (milliseconds: number): string => {
        const seconds = Math.floor(milliseconds / 1000) % 60;
        const minutes = Math.floor(milliseconds / 60000);
        return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
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
                        {!isRecording ? (
                            <button
                                className="px-4 py-2 font-bold rounded bg-green-500 hover:bg-green-600"
                                onClick={startRecording}
                            >
                                Start Recording
                            </button>
                        ) : (
                            <button
                                className="px-4 py-2 font-bold rounded bg-red-500 hover:bg-red-600"
                                onClick={stopRecording}
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
                    <button className="w-full px-4 py-2 mt-4 font-bold rounded bg-green-600 hover:bg-green-700">
                        Submit Meeting
                    </button>
                </div>
                <div className="w-1/2 p-6 bg-gray-900 h-full flex flex-col">
                    <h2 className="text-2xl font-semibold text-blue-300 text-center mb-4">Transcript</h2>
                    <div className="flex-grow bg-gray-800 p-4 overflow-y-auto border border-blue-500 rounded">
                        {transcript ? <p>{transcript}</p> : <p className="text-gray-500">Transcript will appear here...</p>}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Home;
