const {Router} = require('express');
const path = require("path")
const User = require('../models/user.model.js')
const {checkForAuthenticationCookie} = require("../middleware/auth.js")

const router = Router()

router.post("/logout", checkForAuthenticationCookie("token"), (req, res) => {
    // Clear the token from the user's cookies
    res.clearCookie("token");
    
    // Send a response confirming the logout
    res.json({ message: "Successfully logged out." });
});

router.get("/register", (req, res) => {
    res.sendFile(path.join(__dirname, '..', '..', 'frontend', 'register.html'));
});

router.get("/login", (req, res) => {
    res.sendFile(path.join(__dirname, '..', '..', 'frontend', 'login.html'));
});

router.post("/register", async (req, res) => {
    const { username, email, password } = req.body;
    
    try {
        
        
        // Create a new user
        const newUser = new User({ username, email, password:password });
        
        await newUser.save();
        
        res.redirect('/');
    } catch (error) {
        console.error(error);
        res.status(500).send("Error registering user.");
    }
});

router.post('/login',async (req,res)=>{
    const {email,password} = req.body;
    
     try {
        const token =await User.matchPasswordAndGenerateToken(email,password)
    //    console.log(token)
       res.cookie('token',token).redirect('/')
     } catch (error) {
        console.log(error)
        res.status(401).json({ error: "Incorrect email or password" });
        
     }
})

module.exports = router