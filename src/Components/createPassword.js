import React, { useState } from 'react';
import axios from 'axios';

const CreatePassword = () => {
    const [email, setEmail] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/create-password', {
                email,
                new_password: newPassword
            });
            setMessage(response.data.msg);
        } catch (error) {
            setMessage('Error: ' + error.response.data.detail);
        }
    };

    return (
        <div>
            <h2>Create Password</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Email</label>
                    <input 
                        type="email" 
                        value={email} 
                        onChange={(e) => setEmail(e.target.value)} 
                        required 
                    />
                </div>
                <div>
                    <label>New Password</label>
                    <input 
                        type="password" 
                        value={newPassword} 
                        onChange={(e) => setNewPassword(e.target.value)} 
                        required 
                    />
                </div>
                <button type="submit">Create Password</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default CreatePassword;
