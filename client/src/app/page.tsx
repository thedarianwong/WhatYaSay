'use client';

import { useEffect, useRef, useState, MutableRefObject } from 'react';

const WebSocketURL = 'ws://localhost:8000/ws';

const Home: React.FC = () => {
	const [isRecording, setIsRecording] = useState<boolean>(false);
	const [transcript, setTranscript] = useState<string>('');
	const socketRef: MutableRefObject<WebSocket | null> =
		useRef<WebSocket | null>(null);

	useEffect(() => {
		socketRef.current = new WebSocket(WebSocketURL);

		socketRef.current.onopen = () => {
			console.log('WebSocket Connected');
		};

		socketRef.current.onmessage = (event: MessageEvent) => {
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
		try {
			const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
			const mediaRecorder = new MediaRecorder(stream);

			mediaRecorder.ondataavailable = async (event: BlobEvent) => {
				if (
					socketRef.current &&
					socketRef.current.readyState === WebSocket.OPEN
				) {
					socketRef.current.send(event.data);
				}
			};
			mediaRecorder.start(250);
		} catch (error) {
			console.error('Error starting recording:', error);
		}
	};

	const stopRecording = (): void => {
		setIsRecording(false);
		if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
			socketRef.current.close();
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
