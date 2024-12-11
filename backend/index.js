const express = require("express")
const app = express()
const cors = require("cors")
const PORT = 3000;
const path = require("path")
const mongoose = require("mongoose")
const {checkForAuthenticationCookie} = require("./middleware/auth.js")
const cookieParser = require("cookie-parser");


const mongouri = "mongodb+srv://singhmaneshwar08:singh@cluster0.kzv3s.mongodb.net"
const dbname = "planteasycare"
mongoose.connect(`${mongouri}/${dbname}`)
.then((e)=>{
    console.log("mongodb connected")
})
.catch((e)=>{
    console.log("error while connecting mongodb")
})

const userRoute = require("./routes/userroute.js")

app.use(cors())
app.use(cookieParser())

app.use(express.static(path.join(__dirname, '..', 'templates')));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(checkForAuthenticationCookie('token'))
// app.get('/api',(req,res)=>{
//     res.json({message : " testing the api"})
// })
app.use('/user', userRoute)

// app.get('/test',(req,res)=>{
//     res.send("hey")
// })

app.get("/api/login-status", (req, res) => {
    if (req.user) {
        return res.json({ isLoggedIn: true, email: req.user.email });
    }
    res.json({ isLoggedIn: false });
});


app.listen(PORT,()=>{
    console.log(`APP listening on ${PORT}`)
})
