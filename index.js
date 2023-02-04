const express = require("express")
const app = express()
const mongoose = require("mongoose")
const userRoute = require("./routes/user")
const amazon = require("./amazon")
const hepsiburada = require("./hepsiburada")
app.set("view engine","ejs");
app.use(express.static('node_modules'));
//const { run } = require("node:test")

 mongoose.connect('mongodb://localhost:27017/yazlab'
).then(()=>console.log("success")).catch((err)=>{console.log(err);});

 run()
async function run(){
    try{
        
        const amazon_data = await amazon.find()
        const hepsi_data = await hepsiburada.find()
        var same_model1 = [];
        amazon_data.forEach(function(obj1){
            hepsi_data.forEach(function(obj2){
                if(obj1.model === obj2.model){
                    if(obj1.model != null){
                        same_model1.push(obj1.model);
                    }
                    
                }
            });
        })
        
        //same_model =  same_model.filter((item, index) => same_model.indexOf(item) !== index);
        same_model1 = same_model1.filter((item,index) => same_model1.indexOf(item) === index);
        console.log(same_model1)
        function model_each(item){
            if(same_model1 == item){
                console.log("suc");
                return true
                
            }
           return true
        }
        app.use("/:id",function(req,res){
            var urun = amazon_data.find(u => u.model == req.params.id);
            if(!urun){
                urun = hepsi_data.find(u => u.model == req.params.id);
                
            }
            var control = false;
                hepsi_data.forEach(function(obj2){
                    if(urun.model === obj2.model){
                        if(obj2.model != null){
                            control = true 
                    }

                    
                }
               
                });
                if(control){
                    const hepsi = hepsi_data.find(u => u.model === urun.model)
                    res.render("sam_model",{data: {amzn: urun,hpsi: hepsi}});
                }
                else{
                    res.render("product-details",urun);
                }
                
                            
          
            
        });
        
        app.use("/",function(req,res){
            res.render("main",{data: {amzn: amazon_data,hpsi: hepsi_data}});
        });
       
    } catch (e){
        console.log(e.message)
    }
}


 
app.use(express.json());



app.listen(5000, ()=>{
    //console.log("server running")
}); 
  

