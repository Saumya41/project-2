import React from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
import CreatePassword from './Components/CreatePassword';
import ForgotPassword from './components/ForgotPassword';
import ResetPassword from './components/ResetPassword';


function App() {
    return (
        <Router>
            <div>
                <nav>
                    <ul>
                        <li>
                            <Link to="/create-password">Create Password</Link>
                        </li>
                        <li>
                            <Link to="/forgot-password">Forgot Password</Link>
                        </li>
                        <li>
                            <Link to="/reset-password">Reset Password</Link>
                        </li>
                    </ul>
                </nav>
                <Switch>
                    <Route path="/create-password">
                        <CreatePassword />
                    </Route>
                    <Route path="/forgot-password">
                        <ForgotPassword />
                    </Route>
                    <Route path="/reset-password">
                        <ResetPassword />
                    </Route>
                </Switch>
            </div>
        </Router>
    );
}

export default App;