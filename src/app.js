// const express = require("express");
// const path = require("path");
// const app = express();
// const mongoose = require('mongoose');


// const Register = require("./models/registers");

// const port = process.env.PORT || 3000;w
// mongoose.connect("mongodb://localhost:27017/governmentReg",{
//     useNewUrlParser: true,
//     useUnifiedTopology: true,
    
// })
// const db = mongoose.connection
// db.on('error',(err)=>{
//     console.log(err)
// })
// db.once('open',()=>{
//     console.log('Database Connection established!');
// })

// const static_path = path.join(__dirname, "../public");
// const template_path =  path.join(__dirname, "../src/views"); 

// app.use(express.json());
// app.use(express.urlencoded({extended:false}))

// app.use(express.static(static_path))
// app.use(express.static(template_path))
// app.set("views",template_path);

// app.get("/",(req,res)=>{
//     res.render("index");
// });
// app.get("/register",(req,res)=>{
//     res.render("register");
// });
// app.post("/register",async(req,res)=>{
//     try{
//        const governmentReg = new Register({
//         Firstname: req.body.Firstname,
//         LastName: req.body.LastName,
//         EmailID: req.body.EmailID,
//         MobileNumber: req.body.MobileNumber,
//         Gender: req.body.Gender,
//         BirthDay: req.body.BirthDay,
//         Address: req.body.Address,
//         City: req.body.City,
//         PinCode: req.body.PinCode,
//         State: req.body.State,
//         Qualification: req.body.Qualification,
//         Course: req.body.Course,



//        })
//        const registered = await governmentReg.save();
//        res.status(200).send("Registration successful");
       
//     }catch(error){
//         res.status(400).send(error);
//     }
// })
// app.listen(port,()=>{
//     console.log('Server is running at port no ${port}');
// })




const express = require("express");
   const path = require("path");
 const mongoose = require('mongoose')
const app = express();
// var http = require('http');
// var fs = require('fs');
// http.createServer(function(req,res){
//     fs.readFile("./mernbackend/public/index.html", "utf-8", function(err,html){
//         res.writeHead(200,{"Content-Type":"text/html"});
//         res.end(html);
//     });
    
// });
const register = require("./models/register")
const PORT = process.env.PORT || 3000
 mongoose.connect('mongodb://localhost:27017/governmentReg', {useNewUrlParser: true, useUnifiedTopology: true})
 const db = mongoose.connection
 
 db.on('error', (err)=>{
     console.log(err)
 })

 db.once('open', ()=>{
     console.log('Database Connection Established!')
 })

//  app.use('/htmlFiles',express.static(__dirname+'/public'))
//   console.log(path.join(__dirname,"../public"))
     const staticPath = path.join(__dirname,"../public/css");
     app.use(express.static(staticPath));
// app.get("/",(req,res)=> {
//     res.send("hello from the thapatechnical")
// });
 app.use(express.json());
  app.use(express.urlencoded({extended:false}));
  app.get("/index",(req,res)=>{
      res.render("index")
  });
 


app.post("/register", async (req,res) =>{
    try{
       
 
         const registerUser = new register ({
           
             Firstname : req.body.firstname,
             Lastname : req.body.lastname,
             Username : req.body.username,
             DOB : req.body.dob,
             Adhar : req.body.adhaar,
             Phone : req.body.phone,
            
         })
        const registered = await registerUser.save();
        res.status(201).render("index");
        
     } catch(error){
         res.status(400).send(error);
     }
 })
 





app.listen(PORT, () => {
    console.log('server is running at port no',{PORT});
})
















































