import React, { useState, useEffect } from 'react';
import { jwtDecode } from "jwt-decode"; // Ensure correct import
import { useNavigate } from 'react-router-dom';


const LoginPage = ({ setUser }) => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const navigate = useNavigate();

    // Predefined username/password pairs
    const predefinedUsers = {
        "Rutuja@123": "Password@123",
        "Bharthi@123": "Password@123",
        "Shubham@123": "Password@123",
        "Mann@123": "Password@123"
    };

    // Handle Google Sign-In response
    useEffect(() => {
        const handleCallbackResponse = (response) => {
            const userObject = jwtDecode(response.credential);
            console.log("Google User: ", userObject);
            setUser(userObject);
            navigate('/chatbot');
        };

        // Initialize Google OAuth
        window.google.accounts.id.initialize({
            client_id: "535687600192-m0cpf8rp531ecqv9varbnhntk2uhi6f2.apps.googleusercontent.com", // Replace with your Client ID
            callback: handleCallbackResponse,
        });

        // Render the Google Sign-In button
        window.google.accounts.id.renderButton(
            document.getElementById('googleSignInButton'),
            { theme: 'outline', size: 'large' }
        );
    }, [navigate, setUser]);

    // Handle username/password login
    const handleLogin = () => {
        if (predefinedUsers[username] === password) {
            const userObject = { name: username }; // Simple user object
            setUser(userObject);
            navigate('/chatbot'); // Redirect to chatbot
        } else {
            setErrorMessage("Invalid username or password");
        }
    };

    return (
        <div className="login-page">
            <h1>University Chatbot Login</h1>

            <div className="login-options">
                {/* Username and Password Login */}
                <div className="manual-login">
                   
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <button onClick={handleLogin}>Login</button>
                    {errorMessage && <p className="error">{errorMessage}</p>}
                </div>

                <div className="divider">OR</div>

                {/* Google Sign-In */}
                <div className="google-login">
                    <h2>Sign in with Google</h2>
                    <div id="googleSignInButton"></div> {/* Google Sign-In Button */}
                </div>
            </div>
        </div>
    );
};

export default LoginPage;
