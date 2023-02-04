const mongoose = require("mongoose")


const compSchema = new mongoose.Schema({
    
    description: String,
    marka: String,
    model: String,
    ekran: String,
    ram: Number,
    ekran_karti: String,
    islemci: String,
    fiyat: Number,
    puan: String,
    yorum_sayisi: String,
    url: String,
    img_url: String
},
{collection:'hepsiburada'});

module.exports = mongoose.model("hepsiburada",compSchema)