const express = require('express')
const bodyParser = require('body-parser');
const cors = require('cors');
const mysql = require('mysql');

const conn = mysql.createConnection({
    host: 'db4free.net',
    user: 'secret',
    password: 'secret',
    database: 'pokemondb',
    port: 3306
});

const PORT = process.env.PORT || 5000

var app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded());
app.use(cors());

app.get('/', (req,res) => {
  res.send('<h1>Selamat Datang di API Pokemon</h1>')
})

app.get('/pokemon', (req,res) => {
  if(!req.query.name) {
    req.query.name = ''
  }

  var sql = `SELECT * from pokemon WHERE Name Like '%${req.query.name}%'`;

  if(req.query.generation) {
    sql += ` AND Generation = ${req.query.generation}`
  }
  if(req.query.legendary) {
    sql += ` AND Legendary = '${req.query.legendary}'`
  }
  if(req.query.type1) {
    sql += " AND `Type 1` = '" + req.query.type1 + "'"
  }
  if(req.query.type2) {
    sql += " AND `Type 2` = '" + req.query.type2 + "'"
  }
  if(req.query.mintotal && req.query.maxtotal) {
    sql += ` AND (Total >= ${req.query.mintotal} and Total <= ${req.query.maxtotal})`
  }

  conn.query(sql, (err,results) => {
    if(err) throw err;

    res.send(results)
  })
})

app.get('/pokemon/:id', (req,res) => {
  var sql = `SELECT * FROM pokemon WHERE Id = ${req.params.id}`;

  conn.query(sql, (err, results) => {
    if(err) throw err;
    
    res.send(results)
  })
})

app.post('/saveprediction', (req,res) => {
  var sql = `INSERT into historypredict SET ? `;

  var data = req.body;
  data.createddate = new Date();

  conn.query(sql, data, (err,results) => {
      if(err) res.send({ status: 'Error', message: err, saveddata:data});

      res.send({ status: 'Success', message: 'Add Success!'})
  })
})

app.get('/getlistprediction', (req,res) => {
  var sql = `SELECT * from historypredict;`;

  conn.query(sql, (err,results) => {
    if(err) throw err;

    res.send(results)
  })
})

app.get('/pesenburger', (req,res) => {
  console.log(req.query)
  res.send(`<h1>
  Ga ada burger mas disini sorry, 
  pokemon haram untuk dimakan</h1>`)
})

app.listen(PORT, () => console.log('API aktif di port ' + PORT))
