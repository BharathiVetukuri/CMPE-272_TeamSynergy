import React, { useState, useEffect } from "react";
import axios from "axios";
import "./ChatbotPage.css";

const ChatbotPage = () => {
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);

    // Fetch initial message from API
    useEffect(() => {
        const fetchInitialMessage = async () => {
            try {
                const response = await axios.get("https://py-fast-api-theshubh007s-projects.vercel.app/");
                const message = response.data.message || "Welcome to InsightBot!";
                setMessages([{ type: "bot", text: message }]);
            } catch (error) {
                console.error("Error fetching initial message:", error);
                setMessages([{ type: "bot", text: "Unable to load the initial message. Please try again later." }]);
            }
        };

        fetchInitialMessage();
    }, []);

    // Function to handle user input
    const handleUserMessage = async (userInput) => {
        // Add user message to chat
        setMessages((prevMessages) => [...prevMessages, { type: "user", text: userInput }]);

        try {
            setLoading(true);
            const response = await axios.post("https://py-fast-api-theshubh007s-projects.vercel.app/query", {
                query: userInput,
            });
            const botResponse = response.data.message || "I'm sorry, I couldn't understand that.";
            setMessages((prevMessages) => [...prevMessages, { type: "bot", text: botResponse }]);
        } catch (error) {
            console.error("Error fetching bot response:", error);
            setMessages((prevMessages) => [
                ...prevMessages,
                { type: "bot", text: "Sorry, something went wrong. Please try again later." },
            ]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="chatbot-container">
            <div className="chat-header">
                <h1>InsightBot</h1>
                <p>How can I assist you today?</p>
            </div>
            <div className="chat-window">
                {messages.map((message, index) => (
                    <div
                        key={index}
                        className={`message ${message.type === "bot" ? "bot-message" : "user-message"}`}
                    >
                        {message.text}
                    </div>
                ))}
                {loading && <div className="message bot-message">Typing...</div>}
            </div>
            <div className="chat-input-container">
                <input
                    type="text"
                    placeholder="Ask me anything..."
                    onKeyDown={(e) => {
                        if (e.key === "Enter" && e.target.value.trim() !== "") {
                            handleUserMessage(e.target.value);
                            e.target.value = ""; // Clear input
                        }
                    }}
                />
                <button
                    onClick={() => {
                        const input = document.querySelector(".chat-input-container input");
                        if (input.value.trim() !== "") {
                            handleUserMessage(input.value);
                            input.value = ""; // Clear input
                        }
                    }}
                >
                    Send
                </button>
            </div>
        </div>
    );
};

export default ChatbotPage;
