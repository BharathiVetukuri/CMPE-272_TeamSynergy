import React, { useState, useEffect } from "react";
import axios from "axios";
import "./ChatbotPage.css";

const ChatbotPage = ({ user }) => {
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);

    // Fetch initial message
    useEffect(() => {
        setMessages([{ type: "bot", text: `Welcome ${user.name}! How can I assist you today?` }]);
    }, [user]);

    // Handle user input
    const handleUserMessage = async (userInput) => {
        if (!userInput.trim()) return;

        // Add user message to chat
        setMessages((prevMessages) => [...prevMessages, { type: "user", text: userInput }]);

        try {
            setLoading(true);

            // Call the API
            const response = await axios.post("http://127.0.0.1:8000/query/", {
                queries: [userInput],
            });

            const botResponse =
                response.data[0]?.result?.answer ||
                "I'm sorry, I couldn't find an answer to your question.";

            // Add bot response to chat
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
