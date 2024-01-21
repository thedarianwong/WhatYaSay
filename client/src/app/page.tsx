'use client';

import { useEffect, useRef, useState, MutableRefObject } from 'react';

const WebSocketURL = 'ws://localhost:8000/ws';

const Home: React.FC = () => {
	const [isRecording, setIsRecording] = useState<boolean>(false);
	const [transcript, setTranscript] = useState<string>('');
	const socketRef: MutableRefObject<WebSocket | null> = useRef<WebSocket | null>(null);
	const mediaRecorderRef: MutableRefObject<MediaRecorder | null> = useRef<MediaRecorder | null>(null);


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
		console.log('Stopping recording...');

		if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
			mediaRecorderRef.current.stop();
		}
	};
	
	return (
		<div className="flex h-screen">
			<div className="flex flex-col items-center justify-center w-1/2 bg-gray-200">
				{!isRecording ? (
					<button
						className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
						onClick={startRecording}
					>
						Start Recording
					</button>
				) : (
					<button
						className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
						onClick={stopRecording}
					>
						Stop Recording
					</button>
				)}
			</div>
			<div className="w-1/2 p-4 overflow-auto bg-white">
				<p>{transcript}</p>
			</div>
		</div>
	);
};

export default Home;
