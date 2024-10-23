// src/Components/CryptoTable.js
import React, { useEffect, useState } from 'react';

function CryptoTable() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('/api/data')
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.error('Error fetching data:', error));
  }, []);

  return (
    <div>
      <h1>Crypto Dashboard</h1>
      <table border="1" cellPadding="5" cellSpacing="0">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Image</th>
            <th>Name</th>
            <th>Symbol</th>
            <th>Price</th>
            <th>Market Cap</th>
            <th>FDV</th>
            <th>CEX</th>
            <th>M Rank</th>
          </tr>
        </thead>
        <tbody>
          {data.map((coin) => (
            <tr key={coin.Rank}>
              <td>{coin.Rank}</td>
              <td>
                <img src={coin.Image} alt={coin.Name} width="25" height="25" />
              </td>
              <td>{coin.Name}</td>
              <td>{coin.Symbol}</td>
              <td>{coin.Price}</td>
              <td>{coin.MarketCap}</td>
              <td>{coin.FDV}</td>
              <td>{coin.CEX}</td>
              <td>{coin['M Rank']}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default CryptoTable;
