// const mongoose = require("mongoose");

// const formSchema = new mongoose.Schema({
//     Firstname :{
//         type:String,
//         required:true,
      
//     },
//     Lastname :{
//         type:String,
//         required:true,
      
//     },
//     EmailID:{
//         type: String,
//         required: true,
//         unique: true,
      
//     },
//     Gender:{
//         type: String,
//         required: true,
      
        
//     },
//     MobileNumber:{
//         type: Number,
//         required: true,
//         unique: true,
      
//     },
    
   
//     Birthday:{
//         type: Date,
//         required: true,
      
//     },
//     Address:{
//         type: String,
//         required: true,
      
//     },
//     City:{
//         type: String,
//         required: true,
      
//     },
//     Pincode:{
//         type: Number,
//         required: true,
      
//     },
//     State:{
//         type: String,
//         required: true,
      
//     },
//     Qualification:{
//         type: String,
//         required: true,
      
//     },
//     Course:{
//         type: String,
//         required: true,
      
//     }
// })

// const Register = new mongoose.model("registers", formSchema);
// module.exports = Register;

const mongoose = require("mongoose");

const userSchema = new mongoose.Schema({
   
    Firstname : {
        type:String,
        required:true,
        
    },
    Lastname : {
        type:String,
        required:true,
       
    },
    Username : {
        type:String,
        required:true,
       
    },
    DOB : {
        type:Date,
        required:true,
        
    },
    Adhar : {
        type:Number,
        required:true,
        unique:true
        
    },
    Phone:{
        type:Number,
        required:true,
    },
    // password :{
    //   type:String,
    //   required:true

    // },
    // confirmpassword :{
    //     type:String,
    //   required:true
    // }
})

const Register = new mongoose.model("registers", userSchema);

module.exports = Register;












