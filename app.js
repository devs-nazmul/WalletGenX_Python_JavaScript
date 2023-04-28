const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('wallet.db');
const fs = require('fs');

async function checkBalances() {
  db.all('SELECT xpub, words FROM wallet', async function(err, rows) {

    if (err) {
      console.log(err);
      return;
    }
    let i = 0
    for (const row of rows) {
      let xpub = row.xpub
      let words = row.words

      let url = `https://api.blockchain.info/haskoin-store/btc/xpub/${xpub}`
      try {
        const response = await fetch(url);
        const data = await response.json()
        i+=1
        const balance = await data.balance.utxo
        console.log(`${await balance}  -  ${i} `)

        if (balance > 0){
          const fileName = '----winwin.txt'
          const filePath = '../' + fileName
          let content = `${words}\n${xpub} \n\n`
          

          fs.appendFile(filePath, content, (err) => {
          if (err) throw err;
          console.log('The file has been saved!')}
          )
        }


      } catch (err){
        console.log(`API Error ${err.message} - ${xpub}`)
        await new Promise(resolve => setTimeout(resolve, 2000));

      }
    }
  });
}

checkBalances()
