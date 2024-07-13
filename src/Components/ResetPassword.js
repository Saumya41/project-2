import React, { useState } from 'react';
import axios from 'axios';

const ResetPassword = () => {
    const [resetToken, setResetToken] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/reset-password', {
                reset_token: resetToken,
                new_password: newPassword
            });
            setMessage(response.data.msg);
        } catch (error) {
            setMessage('Error: ' + error.response.data.detail);
        }
    };

    return (
        <div>
            <h2>Reset Password</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Reset Token</label>
                    <input 
                        type="text" 
                        value={resetToken} 
                        onChange={(e) => setResetToken(e.target.value)} 
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
                <button type="submit">Reset Password</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default ResetPassword;
